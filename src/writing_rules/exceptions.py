"""Keep explained, term-specific exceptions; reject native blanket suppressions."""
import re

ALLOW = re.compile(r'text-rules-allow:[ \t]*((?:[\w-]+\.)?R\d+)[ \t]+(\S+)[ \t]+([^\s][^\r\n]*)')
NATIVE = re.compile(r'\bvale\s+(?:off\b|on\b|[\w.-]+\s*=)', re.I)


def declarations(source, suffix):
    result, errors = {}, []
    fence = None
    visible = []
    for line, text in enumerate(source.splitlines(), 1):
        stripped = text.strip()
        if suffix in ('.md', '.txt') and re.match(r'(`{3,}|~{3,})', stripped):
            marker = stripped[0]
            fence = None if fence == marker else marker
            visible.append('')
            continue
        if fence:
            visible.append('')
            continue
        visible.append(text)
    cleaned = '\n'.join(visible)
    pattern = r'<!--.*?-->|(?m:^[ \t]*\.\. [^\n]*|^[ \t]*//[^\n]*|^[ \t]*\#[^\n]*)|/\*.*?\*/'
    for comment in re.finditer(pattern, cleaned, re.S):
        text = comment[0]
        line = cleaned[:comment.start()].count('\n') + 1
        if NATIVE.search(text):
            errors.append(f'{line}: Native Vale suppression is disabled. Use an explained text-rules-allow comment.')
        if 'text-rules-allow:' not in text:
            continue
        body = re.sub(r'(?:-->|\*/)\s*$', '', text).strip()
        match = ALLOW.search(body)
        if not match:
            errors.append(f'{line}: Exception requires a rule, a term and a reason.')
        else:
            result[line] = (match[1].split('.')[-1], match[2], match[3])
    return result, errors


def permitted(alert, allowances):
    for line in (alert['Line'] - 1, alert['Line']):
        item = allowances.get(line)
        if item and item[0] == alert['Check'].split('.')[-1]:
            term = item[1]
            left = r'(?<![\w-])' if re.match(r'[\w-]', term) else ''
            right = r'(?![\w-])' if re.search(r'[\w-]$', term) else ''
            if re.search(left + re.escape(term) + right, alert.get('Match', ''), re.I):
                return True
    return False
