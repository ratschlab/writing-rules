"""Per-file error counts. Updating can only record reductions."""
from collections import Counter


def counts(alerts):
    result = {}
    for file, items in alerts.items():
        count = Counter(a['Check'] for a in items if a['Severity'] == 'error')
        if count:
            result[file] = dict(sorted(count.items()))
    return result


def compare(now, base):
    increases, reductions = [], []
    for file in sorted(set(now) | set(base)):
        for rule in sorted(set(now.get(file, {})) | set(base.get(file, {}))):
            n, b = now.get(file, {}).get(rule, 0), base.get(file, {}).get(rule, 0)
            if n > b:
                increases.append((file, rule, b, n))
            elif n < b:
                reductions.append((file, rule, b, n))
    return increases, reductions
