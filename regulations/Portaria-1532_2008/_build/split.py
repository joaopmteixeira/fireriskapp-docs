"""Split full_document.md (from the original DR PDF) into one markdown file per Artigo,
optimised for Obsidian: YAML frontmatter, wikilink navigation, an index.md and a
metadata.md.

Pipeline:
  1. Clean DR page furniture (running headers, page numbers).
  2. Drop the leading content from the previous diploma (before the SCIE "ANEXO").
  3. Walk the document tracking Título / Capítulo / Secção state.
  4. Emit articles/art_NNN_<slug>.md with frontmatter + nav footer.
  5. Emit index.md (tree with wikilinks) and metadata.md.

Run:
    python docs/regulations/Portaria-1532_2008/_build/split.py
"""

from __future__ import annotations

import re
import unicodedata
from datetime import date
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent
FULL_MD = OUT / "full_document.md"
ARTICLES = OUT / "articles"
INDEX_MD = OUT / "index.md"
META_MD = OUT / "metadata.md"

REGULAMENTO = "RT-SCIE (Portaria n.º 1532/2008)"
SOURCE_PDF = "Portaria-1532_2008_original.pdf"

# ---- regexes ---------------------------------------------------------------
# DR running header on each page, e.g.
# "9050 Diário da República, 1.ª série — N.º 250 — 29 de Dezembro de 2008"
RE_DR_HEADER = re.compile(
    r"^\s*#*\s*\d{0,5}\s*Diário da República.*?\d{4}\s*$", re.IGNORECASE
)
# Standalone page-number-ish lines
RE_PAGENUM = re.compile(r"^\s*#*\s*\d{1,4}\s*$")

# Heading lines (docling emits "## ..." for headings)
RE_TITULO = re.compile(r"^#+\s*T[ÍI]TULO\s+([IVXLCDM\d]+)\b\s*(.*)$", re.IGNORECASE)
RE_CAPITULO = re.compile(r"^#+\s*CAP[ÍI]TULO\s+([IVXLCDM\d]+)\b\s*(.*)$", re.IGNORECASE)
RE_SECCAO = re.compile(r"^#+\s*SEC[ÇC][ÃA]O\s+([IVXLCDM\d]+)\b\s*(.*)$", re.IGNORECASE)
RE_ARTIGO = re.compile(r"^#+\s*Artigo\s+(\d+)\.?\s*[º°ªo]?\s*(.*)$", re.IGNORECASE)

# Marker where the SCIE regulation really begins (skip previous diploma on page 1)
RE_ANEXO_START = re.compile(r"^#*\s*ANEXO\b", re.IGNORECASE)
# ANEXO I (definitions) — end of the article series
RE_ANEXO_I = re.compile(r"^#*\s*ANEXO\s+I\b", re.IGNORECASE)


def strip_accents(s: str) -> str:
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def slugify(text: str, maxlen: int = 40) -> str:
    text = strip_accents(text).lower()
    text = re.sub(r"[«»\"'()]+", "", text)
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    if len(text) > maxlen:
        text = text[:maxlen].rsplit("_", 1)[0]
    return text or "sem_titulo"


def clean_lines(raw: str) -> list[str]:
    out = []
    for line in raw.splitlines():
        if RE_DR_HEADER.match(line):
            continue
        out.append(line.rstrip())
    return out


def find_start(lines: list[str]) -> int:
    """Index of the first SCIE 'ANEXO' heading (start of regulation)."""
    for i, line in enumerate(lines):
        if RE_ANEXO_START.match(line) and "I" not in line.split()[1:2]:
            # plain 'ANEXO' (regulation), not 'ANEXO I'
            if not RE_ANEXO_I.match(line):
                return i
    return 0


def is_heading_caption(line: str) -> bool:
    """A '##'-style heading line that is likely an epígrafe/caption (not a marker)."""
    return line.lstrip().startswith("#")


def main() -> None:
    raw = FULL_MD.read_text(encoding="utf-8")
    lines = clean_lines(raw)

    start = find_start(lines)
    lines = lines[start:]

    titulo = capitulo = seccao = ""
    titulo_num = capitulo_num = seccao_num = ""

    # Collected articles: list of dicts
    articles: list[dict] = []
    current: dict | None = None
    body: list[str] = []

    def flush():
        nonlocal current, body
        if current is not None:
            current["body"] = "\n".join(body).strip()
            articles.append(current)
        body = []

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]

        # Stop the article series at ANEXO I (definitions) and beyond.
        if RE_ANEXO_I.match(line):
            flush()
            current = None
            break

        m_t = RE_TITULO.match(line)
        m_c = RE_CAPITULO.match(line)
        m_s = RE_SECCAO.match(line)
        m_a = RE_ARTIGO.match(line)

        if m_t:
            titulo_num = m_t.group(1)
            cap = (m_t.group(2) or "").strip()
            if not cap:
                cap = next_caption(lines, i)
            titulo = f"Título {titulo_num} — {cap}".strip(" —")
            capitulo = seccao = ""
            capitulo_num = seccao_num = ""
            i += 1
            continue
        if m_c:
            capitulo_num = m_c.group(1)
            cap = (m_c.group(2) or "").strip()
            if not cap:
                cap = next_caption(lines, i)
            capitulo = f"Capítulo {capitulo_num} — {cap}".strip(" —")
            seccao = ""
            seccao_num = ""
            i += 1
            continue
        if m_s:
            seccao_num = m_s.group(1)
            cap = (m_s.group(2) or "").strip()
            if not cap:
                cap = next_caption(lines, i)
            seccao = f"Secção {seccao_num} — {cap}".strip(" —")
            i += 1
            continue
        if m_a:
            flush()
            num = int(m_a.group(1))
            epi = (m_a.group(2) or "").strip()
            if not epi:
                epi = next_caption(lines, i)
            current = {
                "numero": num,
                "epigrafe": epi,
                "titulo": titulo,
                "capitulo": capitulo,
                "seccao": seccao,
            }
            # skip the caption line if it was consumed
            i += 1
            # if next line is the caption heading we just used, skip it
            if epi and i < n and is_heading_caption(lines[i]):
                cap_text = re.sub(r"^#+\s*", "", lines[i]).strip()
                if cap_text == epi:
                    i += 1
            continue

        if current is not None:
            body.append(line)
        i += 1

    flush()

    write_articles(articles)
    write_index(articles)
    write_metadata(articles)
    print(f"Wrote {len(articles)} articles + index.md + metadata.md")


def next_caption(lines: list[str], i: int) -> str:
    """The first non-empty heading/text line after index i, used as epígrafe."""
    j = i + 1
    while j < len(lines):
        s = lines[j].strip()
        if s:
            return re.sub(r"^#+\s*", "", s).strip()
        j += 1
    return ""


def file_stem(num: int, epi: str) -> str:
    return f"art_{num:03d}_{slugify(epi)}"


def write_articles(articles: list[dict]) -> None:
    ARTICLES.mkdir(parents=True, exist_ok=True)
    for f in ARTICLES.glob("art_*.md"):
        f.unlink()

    stems = {a["numero"]: file_stem(a["numero"], a["epigrafe"]) for a in articles}

    for idx, a in enumerate(articles):
        num = a["numero"]
        stem = stems[num]
        prev_stem = stems.get(articles[idx - 1]["numero"]) if idx > 0 else None
        next_stem = stems.get(articles[idx + 1]["numero"]) if idx + 1 < len(articles) else None

        fm = ["---"]
        fm.append(f"numero: {num}")
        fm.append(f'epigrafe: "{a["epigrafe"]}"')
        fm.append(f'titulo: "{a["titulo"]}"')
        fm.append(f'capitulo: "{a["capitulo"]}"')
        fm.append(f'seccao: "{a["seccao"]}"')
        fm.append(f'regulamento: "{REGULAMENTO}"')
        fm.append(f'source: "{SOURCE_PDF}"')
        fm.append("tags: [scie, regulamento, artigo]")
        fm.append("---")

        head = f"# Artigo {num}.º — {a['epigrafe']}".rstrip(" —")

        nav = []
        nav.append(f"[[{prev_stem}|◀ Anterior]]" if prev_stem else "◀")
        nav.append("[[index|Índice]]")
        nav.append(f"[[{next_stem}|Seguinte ▶]]" if next_stem else "▶")
        nav_line = " · ".join(nav)

        content = "\n".join(fm) + "\n\n" + head + "\n\n" + a["body"].strip() + "\n\n---\n" + nav_line + "\n"
        (ARTICLES / f"{stem}.md").write_text(content, encoding="utf-8")


def write_index(articles: list[dict]) -> None:
    lines = ["# Índice — Regulamento Técnico SCIE", "",
             f"Portaria n.º 1532/2008, de 29 de dezembro · {len(articles)} artigos.", ""]
    last_t = last_c = last_s = None
    for a in articles:
        if a["titulo"] != last_t:
            last_t = a["titulo"]; last_c = last_s = None
            if last_t:
                lines.append(f"\n## {last_t}")
        if a["capitulo"] != last_c:
            last_c = a["capitulo"]; last_s = None
            if last_c:
                lines.append(f"\n### {last_c}")
        if a["seccao"] != last_s:
            last_s = a["seccao"]
            if last_s:
                lines.append(f"\n#### {last_s}")
        stem = file_stem(a["numero"], a["epigrafe"])
        label = f"Artigo {a['numero']}.º — {a['epigrafe']}".rstrip(" —")
        lines.append(f"- [[{stem}|{label}]]")
    INDEX_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_metadata(articles: list[dict]) -> None:
    nums = [a["numero"] for a in articles]
    fm = [
        "---",
        'titulo: "Regulamento Técnico de Segurança contra Incêndio em Edifícios (RT-SCIE)"',
        'diploma: "Portaria n.º 1532/2008"',
        "data: 2008-12-29",
        "entrada_vigor: 2009-01-01",
        f'source: "{SOURCE_PDF}"',
        f"n_artigos: {len(articles)}",
        f"artigo_min: {min(nums) if nums else 0}",
        f"artigo_max: {max(nums) if nums else 0}",
        'metodo_conversao: "docling 2.55.1 (sem OCR, tabelas estruturadas)"',
        f"data_conversao: {date.today().isoformat()}",
        "tags: [scie, regulamento, metadata]",
        "---",
        "",
        "# Regulamento Técnico de Segurança contra Incêndio em Edifícios (RT-SCIE)",
        "",
        "Aprovado pela **Portaria n.º 1532/2008, de 29 de dezembro**, ao abrigo do "
        "artigo 15.º do Decreto-Lei n.º 220/2008, de 12 de Novembro. Entrada em vigor: "
        "1 de Janeiro de 2009.",
        "",
        "Ver o [[index|Índice]] para navegar pelos artigos.",
        "",
        "> [!note] Conversão",
        "> Conteúdo convertido a partir do PDF original do Diário da República "
        f"(`{SOURCE_PDF}`) com docling, sem OCR. As tabelas (Quadros I a LI) foram "
        "extraídas como tabelas markdown. Pode conter pequenas imperfeições de layout; "
        "em caso de dúvida, confirmar no diploma oficial.",
        "",
    ]
    META_MD.write_text("\n".join(fm), encoding="utf-8")


if __name__ == "__main__":
    main()
