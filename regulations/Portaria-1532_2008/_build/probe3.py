import json, re
from pathlib import Path
import pypdfium2 as p

OUT = Path(__file__).resolve().parent.parent
dre = OUT.parent / "Portaria-1532_2008.pdf"
d = p.PdfDocument(str(dre))
full = "\n".join(d[i].get_textpage().get_text_range() for i in range(len(d)))

# Show the ~120 chars before each "ver documento original" to classify table vs figure
ctxs = []
for m in re.finditer(r"ver documento original", full):
    start = max(0, m.start() - 160)
    snippet = full[start:m.start()].replace("\r", " ").replace("\n", " ")
    ctxs.append(snippet[-160:])

res = {
    "n_placeholders": len(ctxs),
    "contexts": ctxs,
    "mentions_figura": sum(1 for c in ctxs if re.search(r"figura|esquema|gráfico|imagem", c, re.I)),
    "mentions_quadro": sum(1 for c in ctxs if re.search(r"quadro", c, re.I)),
}
(OUT / "_build" / "probe3.json").write_text(
    json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8"
)
print("placeholders:", len(ctxs), "| figura-ish:", res["mentions_figura"], "| quadro-ish:", res["mentions_quadro"])
