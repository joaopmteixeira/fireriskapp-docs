import re
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent
lines = (OUT / "full_document.md").read_text(encoding="utf-8").splitlines()

RE_ART = re.compile(r"^#+\s*Artigo\s+(\d+)\.?\s*[º°ªo]?\s*(.*)$", re.IGNORECASE)
RE_REG = re.compile(r"Regulamento t[ée]cnico de seguran", re.IGNORECASE)
RE_ANEXO = re.compile(r"^#*\s*ANEXO\b", re.IGNORECASE)

print("=== lines matching 'Regulamento tecnico...' / ANEXO ===")
for i, l in enumerate(lines):
    if RE_REG.search(l) or RE_ANEXO.match(l):
        print(i, repr(l[:80]))

print("\n=== all Artigo headings (idx | num | caption) ===")
seq = []
for i, l in enumerate(lines):
    m = RE_ART.match(l)
    if m:
        seq.append((i, int(m.group(1))))
        cap = m.group(2).strip()
        if not cap:
            # look ahead
            for j in range(i + 1, min(i + 4, len(lines))):
                s = lines[j].strip()
                if s:
                    cap = re.sub(r"^#+\s*", "", s)[:50]
                    break
        print(f"{i:5d} | {m.group(1):>4} | {cap[:55]}")

print("\n=== numbers present ===")
nums = [n for _, n in seq]
print(sorted(set(nums)))
from collections import Counter
dups = {k: v for k, v in Counter(nums).items() if v > 1}
print("dups:", dups)
print("missing 1..309:", [n for n in range(1, 310) if n not in set(nums)])
