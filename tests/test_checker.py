import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from unittest import mock
from types import SimpleNamespace

from writing_rules.cli import export_package, scan, main
from writing_rules.exceptions import declarations, permitted
from writing_rules.ratchet import compare
from writing_rules.sources import cpp_units, python_docstrings, python_units

PROJECT = Path(__file__).resolve().parents[1]
VALE = os.environ.get('VALE', 'vale')


class Sources(unittest.TestCase):
    def test_cpp_join_decode_and_raw(self):
        for source in ['"something " "went wrong"', '"something\\nwent wrong"', 'R"(something went wrong)"']:
            with self.subTest(source=source):
                got = cpp_units('void f() { logger->error('+source+'); }')
                self.assertEqual(' '.join(got[0].text.split()), 'something went wrong')

    def test_cpp_unicode_and_literal_prefix(self):
        self.assertEqual(cpp_units('logger->error(u8"Café");')[0].text, 'Café')

    def test_nested_format(self):
        self.assertEqual(cpp_units('throw std::invalid_argument(fmt::format("Oops {}", name));')[0].text,'Oops {}')

    def test_parse_recovery_is_reported(self):
        notes=[]
        cpp_units('void f() { logger->error("Oops");',diagnostics=notes)
        self.assertTrue(notes)

    def test_python_join_and_interpolation(self):
        self.assertEqual(python_units('raise ValueError("something " "went wrong")')[0].text, 'something went wrong')
        self.assertEqual(python_units('raise ValueError(f"Missing {name}")')[0].text, 'Missing X')

    def test_cpp_std_fprintf_stderr(self):
        source = 'void f() { std::fprintf(stderr, "Oops"); std::fprintf(out, "Fine"); }'
        self.assertEqual([u.text for u in cpp_units(source)], ['Oops'])

    def test_python_public_docstrings_keep_lines(self):
        source = ('"""Module text."""\n'
                  'class A:\n'
                  '    """\n'
                  '    Class text.\n'
                  '\n'
                  '        Indented.\n'
                  '    """\n'
                  '    def run(self):\n'
                  '        """Method text."""\n'
                  '    def _hidden(self):\n'
                  '        """Hidden text."""\n'
                  'def _private():\n'
                  '    """Private text."""\n')
        lines = python_docstrings(source).split('\n')
        self.assertEqual(len(lines), len(source.split('\n')))
        self.assertEqual({i + 1: t for i, t in enumerate(lines) if t},
                         {1: 'Module text.', 4: 'Class text.', 6: '    Indented.', 9: 'Method text.'})
        self.assertIsNone(python_docstrings('def _f():\n    """Private."""\n'))

    def test_cpp_scope(self):
        source = '#include "kmer/a.hpp"\n// Oops\nvoid f() { logger->debug("Oops"); logger->warn("Oops"); }'
        self.assertEqual([(u.line,u.text) for u in cpp_units(source)],[(3,'Oops')])


class Exceptions(unittest.TestCase):
    def test_missing_reason(self):
        for source in ['<!-- text-rules-allow: R8 kmer -->', '/* text-rules-allow: R8 kmer */',
                       '// text-rules-allow: R8 kmer\nreason on another line']:
            self.assertTrue(declarations(source,'.md')[1])

    def test_native_cannot_bypass(self):
        for source in ['<!-- vale off -->', 'Oops <!-- vale off -->', '<!--\nvale off\n-->', '.. vale Writing.R1 = NO']:
            self.assertTrue(declarations(source,'.md')[1])

    def test_documented_code_example_is_not_directive(self):
        self.assertFalse(declarations('```md\n<!-- vale off -->\n```\n','.md')[1])

    def test_term_applies_only_to_matched_word(self):
        allowances, errors=declarations('<!-- text-rules-allow: R8 kmer exact quoted spelling -->\nCount kmer and kmers.','.md')
        self.assertFalse(errors)
        alert={'Line':2,'Check':'MetaGraph.R8','Match':'kmer'}
        self.assertTrue(permitted(alert,allowances))
        self.assertFalse(permitted(dict(alert,Match='kmers'),allowances))


class Baseline(unittest.TestCase):
    def test_cli_update_refuses_increase_without_writing(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/'writing-rules.json').write_text('{"include":["*.md"]}')
            baseline=root/'writing-rules-baseline.json'
            baseline.write_text('{}\n')
            with mock.patch('writing_rules.cli.subprocess.run',return_value=SimpleNamespace(stdout='vale version 3.26.0\n')), \
                 mock.patch('writing_rules.cli.tracked_files',return_value=['a.md']), \
                 mock.patch('writing_rules.cli.scan',return_value=({'a.md':[{'Check':'Writing.R1','Severity':'error'}]},[])), \
                 mock.patch('builtins.print'):
                self.assertEqual(main(['check','--root',str(root),'--update-baseline']),1)
            self.assertEqual(baseline.read_text(),'{}\n')

    def test_six_baseline_transitions(self):
        cases=[({'a':{'R1':1}},{'a':{'R1':2}},False,True),
               ({'a':{'R1':2}},{'a':{'R1':1}},True,False),
               ({'b':{'R1':1}},{'a':{'R1':1}},True,True),
               ({'a':{'R1':1}},{},True,False),
               ({},{'a':{'R1':1}},False,True),
               ({},{},False,False)]
        for now,base,increase,reduction in cases:
            with self.subTest(now=now,base=base):
                inc,dec=compare(now,base)
                self.assertEqual((bool(inc),bool(dec)),(increase,reduction))


class Integration(unittest.TestCase):
    def test_default_preserves_uncertainty_and_punctuation(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            export_package(root/'WritingRules.zip')
            config = root/'.vale.ini'
            config.write_text('StylesPath = styles\nPackages = '+str(root/'WritingRules.zip')+'\n')
            run = subprocess.run([VALE, 'sync', '--no-global'], cwd=root, text=True, capture_output=True)
            self.assertEqual(run.returncode, 0, run.stdout+run.stderr)
            (root/'uncertainty.md').write_text('The operation may have completed; check its status.\n')
            alerts, _ = scan(root, ['uncertainty.md'], {}, VALE, config)
            self.assertFalse([a for a in alerts.get('uncertainty.md', []) if a['Severity']=='error'])

    def test_objective_cpp_messages_are_checked(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            export_package(root/'WritingRules.zip')
            config = root/'.vale.ini'
            config.write_text('StylesPath = styles\nPackages = '+str(root/'WritingRules.zip')+'\n'
                              '[*.{md,rst,txt}]\nWriting.R1 = YES\n')
            run = subprocess.run([VALE, 'sync', '--no-global'], cwd=root, text=True, capture_output=True)
            self.assertEqual(run.returncode, 0, run.stdout+run.stderr)
            (root/'m.mm').write_text('void f(id device) {\n    id queue = [device newCommandQueue];\n'
                                     '    if (queue == nil) throw std::runtime_error("No queue; stop");\n}\n')
            alerts, _ = scan(root, ['m.mm'], {}, VALE, config)
            self.assertEqual([a['Line'] for a in alerts['m.mm'] if a['Check'] == 'Writing.R1'], [3])

    def test_python_docstrings_are_checked_as_rst(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            export_package(root/'WritingRules.zip')
            config = root/'.vale.ini'
            config.write_text('StylesPath = styles\nPackages = '+str(root/'WritingRules.zip')+'\n'
                              '[*.{md,rst,txt}]\nWriting.R1 = YES\n')
            run = subprocess.run([VALE, 'sync', '--no-global'], cwd=root, text=True, capture_output=True)
            self.assertEqual(run.returncode, 0, run.stdout+run.stderr)
            (root/'m.py').write_text('def f():\n    """Run it; then stop.\n\n    Use ``a;b`` here.\n    """\n'
                                     '    raise ValueError("Bad; fix it")\n')
            options = {'source': {'python': {'calls': ['ValueError']}}}
            alerts, _ = scan(root, ['m.py'], options, VALE, config)
            self.assertEqual([a['Line'] for a in alerts['m.py']], [6])
            options['source']['python']['docstrings'] = 'public'
            alerts, _ = scan(root, ['m.py'], options, VALE, config)
            self.assertEqual(sorted(a['Line'] for a in alerts['m.py'] if a['Check'] == 'Writing.R1'), [2, 6])

    def test_fixture_suite_and_package_overrides(self):
        cases=json.loads((PROJECT/'tests/cases.json').read_text())
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            export_package(root/'WritingRules.zip')
            with zipfile.ZipFile(root/'WritingRules.zip') as archive:
                for notice in ('LICENSE', 'AUTHORS'):
                    self.assertEqual(archive.read('WritingRules/'+notice), (PROJECT/notice).read_bytes())
            shutil.copytree(PROJECT/'tests/fixtures/styles',root/'styles')
            config=root/'.vale.ini'
            config.write_text('StylesPath = styles\nPackages = '+str(root/'WritingRules.zip')+'\n'
                              '[*.{md,rst,txt}]\nBasedOnStyles = MetaGraph\n'
                              'Writing.R1 = YES\nWriting.R4 = YES\nWriting.R7 = YES\n'
                              '[*.ts]\nWriting.R1 = YES\nWriting.R4 = YES\nWriting.R7 = YES\n'
                              '[*.tsx]\nWriting.R1 = YES\nWriting.R4 = YES\nWriting.R7 = YES\n'
                              '[*jargon*.md]\nWriting.R5 = YES\n[*actor.md]\nWriting.R9 = YES\n')
            p=subprocess.run([VALE,'sync','--no-global'],cwd=root,text=True,capture_output=True)
            self.assertEqual(p.returncode,0,p.stdout+p.stderr)
            for name,source,expected in cases:
                with self.subTest(name=name):
                    (root/name).write_text(source)
                    # Deliberate policy changes: native directives are rejected,
                    # malformed exceptions fail explicitly, bare SQL must be marked as code.
                    if name.startswith('native_allow') or name=='bare_allow.md':
                        with self.assertRaises(ValueError):scan(root,[name],{},VALE,config)
                        continue
                    if name=='literal_sql.txt':expected=['R1']
                    alerts,_=scan(root,[name],{},VALE,config)
                    actual=sorted({a['Check'].split('.')[-1] for a in alerts.get(name,[]) if a['Severity']=='error'})
                    self.assertEqual(actual,expected)
            config.write_text(config.read_text()+'\n[*semicolon_spaced.md]\nWriting.R1 = NO\n')
            alerts,_=scan(root,['semicolon_spaced.md'],{},VALE,config)
            self.assertFalse([a for a in alerts.get('semicolon_spaced.md',[]) if a['Severity']=='error'])


if __name__=='__main__':
    unittest.main()
