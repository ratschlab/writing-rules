"""Extract and decode user-facing source strings; Vale handles prose matching."""
import ast
import inspect
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Unit:
    line: int
    text: str


def walk(node):
    yield node
    for child in node.named_children:
        yield from walk(child)


def cpp_text(node, data):
    if node.type == 'concatenated_string':
        return ''.join(cpp_text(c, data) for c in node.named_children if c.type != 'comment')
    source = data[node.start_byte:node.end_byte].decode('utf8')
    raw = re.fullmatch(r'(?:u8|[uUL])?R"([^ ()\\\t\r\n]*)\((.*)\)\1"', source, re.S)
    if raw:
        return raw[2]
    source = re.sub(r'^(?:u8|[uUL])(?=")', '', source)
    try:
        return ast.literal_eval(source.replace('\\\n', ''))
    except (ValueError, SyntaxError) as exc:
        raise ValueError(f'Unsupported C++ literal on line {node.start_point.row + 1}') from exc


def cpp_units(source, options=None, diagnostics=None):
    import tree_sitter_cpp
    from tree_sitter import Language, Parser
    options = options or {}
    language = Language(tree_sitter_cpp.language())
    parser = Parser(language)
    data = source.encode('utf8')
    tree = parser.parse(data)
    if diagnostics is not None and tree.root_node.has_error:
        for node in walk(tree.root_node):
            if node.type == 'ERROR' or node.is_missing:
                diagnostics.append(node.start_point.row + 1)
                break
        else:
            diagnostics.append(tree.root_node.start_point.row + 1)
    result = []
    for node in walk(tree.root_node):
        if node.type not in ('string_literal', 'raw_string_literal', 'concatenated_string'):
            continue
        if node.parent and node.parent.type in ('concatenated_string', 'preproc_include'):
            continue
        parent = node.parent
        selected = options.get('all_strings', False)
        while parent and not selected:
            if parent.type == 'call_expression':
                fn = parent.child_by_field_name('function')
                name = data[fn.start_byte:fn.end_byte].decode('utf8') if fn else ''
                selected = bool(re.search(r'(?:->|\.)(?:error|warn|critical)$', name))
                if name in ('fprintf', 'std::fprintf'):
                    args = parent.child_by_field_name('arguments')
                    first = args.named_children[0] if args.named_children else None
                    selected = first is not None and data[first.start_byte:first.end_byte] == b'stderr'
                if parent.parent and parent.parent.type == 'throw_statement':
                    selected = True
                if selected or name not in ('fmt::format', 'std::format'):
                    break
            if parent.type == 'binary_expression':
                left = parent.child_by_field_name('left')
                if left and data[left.start_byte:left.end_byte].startswith(b'std::cerr'):
                    selected = True
                    break
            parent = parent.parent
        if selected:
            result.append(Unit(node.start_point.row + 1, cpp_text(node, data)))
    return result


def python_units(source, options=None):
    options = options or {}
    calls = set(options.get('calls', ['ValueError', 'RuntimeError', 'print']))
    keywords = set(options.get('keywords', ['detail', 'description', 'help']))
    tree = ast.parse(source)
    result = []

    def value(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        if isinstance(node, ast.JoinedStr):
            return ''.join(v.value if isinstance(v, ast.Constant) else 'X' for v in node.values)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            a, b = value(node.left), value(node.right)
            if a is not None and b is not None:
                return a + b
        return None

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = node.func.id if isinstance(node.func, ast.Name) else getattr(node.func, 'attr', '')
        candidates = list(node.args[:1]) if name in calls else []
        candidates += [kw.value for kw in node.keywords if kw.arg in keywords]
        for candidate in candidates:
            text = value(candidate)
            if text is not None:
                result.append(Unit(candidate.lineno, text))
    return result


def python_docstrings(source):
    """Return reStructuredText with the public docstrings at their source lines, or None."""
    tree = ast.parse(source)
    nodes = [tree]
    for node in tree.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith('_'):
            nodes.append(node)
            if isinstance(node, ast.ClassDef):
                nodes += [m for m in node.body if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))
                          and not m.name.startswith('_')]
    lines = [''] * len(source.splitlines())
    found = False
    for node in nodes:
        first = node.body[0] if node.body else None
        if not (isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)):
            continue
        raw = first.value.value.split('\n')
        offset = next((i for i, text in enumerate(raw) if text.strip()), len(raw))
        for i, text in enumerate(inspect.cleandoc(first.value.value).split('\n')):
            line = first.lineno - 1 + offset + i
            if line < len(lines):
                lines[line] = text
                found = True
    return '\n'.join(lines) + '\n' if found else None
