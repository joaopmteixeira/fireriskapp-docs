import json
from pathlib import Path
import pypdfium2 as p
import pypdfium2.raw as raw

OUT = Path(__file__).resolve().parent.parent
res = {}
for label, name in [
    ("dre", "Portaria-1532_2008.pdf"),
    ("orig", "Portaria-1532_2008_original.pdf"),
]:
    path = OUT.parent / name
    info = {"exists": path.exists()}
    if path.exists():
        info["size_bytes"] = path.stat().st_size
        d = p.PdfDocument(str(path))
        n = len(d)
        per = [len(d[i].get_textpage().get_text_range()) for i in range(n)]
        info["pages"] = n
        info["total_text_chars"] = sum(per)
        info["pages_with_text"] = sum(1 for x in per if x > 20)
        imgcounts = []
        for i in range(n):
            cnt = 0
            try:
                for obj in d[i].get_objects():
                    if obj.type == raw.FPDF_PAGEOBJ_IMAGE:
                        cnt += 1
            except Exception as e:
                cnt = -1
            imgcounts.append(cnt)
        info["total_image_objects"] = sum(c for c in imgcounts if c > 0)
        info["img_per_page"] = imgcounts
        info["page1_text_head"] = d[0].get_textpage().get_text_range()[:300]
        # check for the DRE placeholder marker
        full = "".join(d[i].get_textpage().get_text_range() for i in range(n))
        info["count_ver_documento_original"] = full.count("ver documento original")
        info["count_TEXTO_INTEGRANTE"] = full.count("TEXTO INTEGRANTE DO ATO ORIGINAL")
    res[label] = info

(OUT / "_build" / "probe.json").write_text(
    json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8"
)
print("done")
