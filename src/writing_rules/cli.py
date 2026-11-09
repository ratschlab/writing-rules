"""Run Vale on a repository's selected prose and normalized diagnostics."""
import argparse
import fnmatch
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

from .exceptions import declarations, permitted
from .ratchet import compare, counts
from .sources import cpp_units, python_docstrings, python_units

VALE_VERSION = 'vale version 3.26.0'


def tracked_files(root, config):
    result = subprocess.run(['git', '-C', str(root), 'ls-files', '-z'], check=True, capture_output=True)
    files = result.stdout.decode().split('\0')
    selected = sorted({f for f in files if f and
                       any(fnmatch.fnmatch(f, p) for p in config['include']) and
                       not any(fnmatch.fnmatch(f, p) for p in config.get('exclude', []))})
    for file in selected:
        path = root / file
        if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError(f'Scoped file is missing, a symlink, or outside the repository: {file}')
    return selected


def scan(root, files, config, vale, vale_config):
    result, allowed, errors = {}, [], []
    with tempfile.TemporaryDirectory(prefix='writing-rules-') as scratch:
        scratch = Path(scratch)
        origins, exceptions = {}, {}
        for file in files:
            source = (root / file).read_text(encoding='utf8')
            suffix = Path(file).suffix
            exceptions[file], issues = declarations(source, suffix)
            errors.extend(f'{file}:{issue}' for issue in issues)
            positions = None
            options = config.get('source', {})
            if suffix in ('.cpp', '.hpp', '.cc', '.h', '.cu', '.cuh', '.mm'):
                opts = dict(options.get('cpp', {}))
                opts['all_strings'] = any(fnmatch.fnmatch(file, p) for p in opts.get('all_strings_in', []))
                recovered = []
                units = cpp_units(source, opts, recovered)
                for line in recovered:
                    result.setdefault(file, []).append({
                        'Line': line, 'Check': 'Writing.ParseRecovery', 'Severity': 'warning',
                        'Message': 'Tree-sitter recovered syntax here. Review source-string coverage.', 'Match': ''})
            elif suffix == '.py':
                units = python_units(source, options.get('python'))
                if options.get('python', {}).get('docstrings') == 'public':
                    docstrings = python_docstrings(source)
                    if docstrings is not None:
                        target = scratch / (file + '.rst')
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_text(docstrings, encoding='utf8')
                        origins[str(target)] = (file, None)
            else:
                units = None
            if units is not None:
                positions, lines = {}, []
                for unit in units:
                    positions[len(lines)+1] = unit.line
                    lines += [unit.text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' '), '']
                source = '\n'.join(lines)
            target = scratch / (file + '.txt' if positions is not None else file)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(source, encoding='utf8')
            origins[str(target)] = (file, positions)
        if errors:
            raise ValueError('\n'.join(errors))
        if not origins:
            return {}, []
        run = subprocess.run([vale, '--no-global', '--config='+str(vale_config), '--output=JSON', *origins],
                             text=True, capture_output=True, timeout=120)
        if run.returncode not in (0, 1):
            raise ValueError('Vale failed: '+run.stdout+run.stderr)
        try:
            output = json.loads(run.stdout)
        except ValueError as exc:
            raise ValueError('Invalid Vale output: '+run.stdout+run.stderr) from exc
        if not isinstance(output, dict) or any(k not in origins for k in output):
            raise ValueError('Unexpected Vale output: '+run.stdout)
        if run.stderr.strip():
            raise ValueError('Vale reported parser diagnostics: '+run.stderr)
        for path, alerts in output.items():
            file, positions = origins[path]
            for original in alerts:
                alert = dict(original)
                if positions is not None:
                    if alert['Line'] not in positions:
                        raise ValueError(f'Cannot map Vale finding to source: {file}:{alert["Line"]}')
                    alert['Line'] = positions[alert['Line']]
                    alert['Location'] = 'message-start'
                    alert.pop('Span', None)
                if permitted(alert, exceptions[file]):
                    allowed.append({'file': file, **alert})
                else:
                    result.setdefault(file, []).append(alert)
        return result, allowed


def export_package(destination):
    assets = Path(__file__).parent / 'assets'
    with zipfile.ZipFile(destination, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(assets.rglob('*')):
            if path.is_file():
                archive.write(path, 'WritingRules/'+str(path.relative_to(assets)))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    export = sub.add_parser('export-package')
    export.add_argument('destination', type=Path)
    check = sub.add_parser('check')
    check.add_argument('--root', type=Path, default=Path.cwd())
    check.add_argument('--config', type=Path, default=Path('writing-rules.json'))
    check.add_argument('--vale-config', type=Path, default=Path('.vale.ini'))
    check.add_argument('--vale', default='vale')
    check.add_argument('--baseline', type=Path, default=Path('writing-rules-baseline.json'))
    check.add_argument('--report', action='store_true')
    check.add_argument('--update-baseline', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.command == 'export-package':
            export_package(args.destination)
            return 0
        root = args.root.resolve()
        resolve = lambda p: p if p.is_absolute() else root / p
        version = subprocess.run([args.vale, '--version'], check=True, capture_output=True, text=True).stdout.strip()
        if version != VALE_VERSION:
            raise ValueError(f'Expected {VALE_VERSION}, got {version}')
        config = json.loads(resolve(args.config).read_text())
        files = tracked_files(root, config)
        print(f'Scope: {len(files)} files', file=sys.stderr)
        alerts, allowed = scan(root, files, config, args.vale, resolve(args.vale_config))
        baseline = resolve(args.baseline)
        base = json.loads(baseline.read_text()) if baseline.exists() else {}
        now = counts(alerts)
        increases, reductions = compare(now, base)
        if args.update_baseline and not increases:
            baseline.write_text(json.dumps(now, indent=2)+'\n')
        print(json.dumps({'files': files, 'alerts': alerts, 'allowed': allowed,
                          'counts': now, 'increases': increases, 'reductions': reductions}, indent=2))
        return 0 if args.report else int(bool(increases))
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
