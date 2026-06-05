import json, re
from pathlib import Path
import pypdfium2 as p
import pypdfium2.raw as raw

OUT = Path(__file__).resolve().parent.parent
orig = OUT.parent / "Portaria-1532_2008_original.pdf"
d = p.PdfDocument(str(orig))
n = len(d)
pages = [d[i].get_textpage().get_text_range() for i in range(n)]

res = {}

# 1) Locate SCIE regulation boundaries
def find_pages(needle):
    return [i + 1 for i, t in enumerate(pages) if needle.lower() in t.lower()]

res["pages_with_1532"] = find_pages("1532/2008")
res["pages_with_regulamento_tecnico_scie"] = find_pages(
    "Regulamento Técnico de Segurança contra Incêndio"
)
res["pages_with_titulo_I_objecto"] = find_pages("Objecto e definições")
res["pages_with_anexo_I_definicoes"] = find_pages("ANEXO I")

# 2) Count tables and figures markers across whole doc
full = "\n".join(pages)
res["count_QUADRO"] = len(re.findall(r"\bQUADRO\b", full))
res["count_Quadro_word"] = len(re.findall(r"\bQuadro\b", full))
res["count_FIGURA"] = len(re.findall(r"\bFIGURA\b", full, re.I))
res["count_Figura"] = len(re.findall(r"\bFig(?:ura)?\b", full))

# 3) Vector path objects per page (figures are likely drawn as paths)
path_counts = []
for i in range(n):
    cp = 0
    try:
        for obj in d[i].get_objects():
            if obj.type == raw.FPDF_PAGEOBJ_PATH:
                cp += 1
    except Exception:
        cp = -1
    path_counts.append(cp)
res["path_objs_per_page"] = path_counts
res["pages_with_many_paths"] = [i + 1 for i, c in enumerate(path_counts) if c and c > 50]

# 4) Show heads of pages to find where 1532 SCIE starts
heads = {}
for i in range(n):
    h = pages[i][:90].replace("\r", " ").replace("\n", " ")
    heads[i + 1] = h
res["page_heads"] = heads

(OUT / "_build" / "probe2.json").write_text(
    json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8"
)
print("done")
