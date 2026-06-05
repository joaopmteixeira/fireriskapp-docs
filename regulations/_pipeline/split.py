"""Generic regulation article splitter — reads config.json, splits full_document.md.

Parameterised port of Portaria-1532_2008/_build/split.py. All regulation-specific
values (name, PDF source, skip/stop sections, tags) come from config.json so
the same script works for any Portuguese legal regulation in Diário da República.

Usage:
    python docs/regulations/_pipeline/split.py docs/regulations/<regulation-dir>/

config.json keys used:
    regulamento       — display name, written into frontmatter
    pdf_original      — source PDF filename (basename only, for frontmatter)
    skip_to_section   — (optional) skip document content until this heading pattern
                        (e.g. "ANEXO" when the regulation is preceded by other diplomas)
    stop_at_section   — (optional) stop collecting articles at this heading pattern
                        (e.g. "ANEXO I" for the definitions annex)
    tags              — (optional, default ["regulamento","artigo"]) frontmatter tags
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path


# ── Generic DR page furniture (applies to all Diário da República documents) ──
RE_DR_HEADER = re.compile(
    r"^\s*#*\s*\d{0,5}\s*Diário da República.*?\d{4}\s*$", re.IGNORECASE
)
RE_PAGENUM = re.compile(r"^\s*#*\s*\d{1,4}\s*$")

# ── Structure headings (generic Portuguese legal structure) ──
RE_TITULO   = re.compile(r"^#+\s*T[ÍI]TULO\s+([IVXLCDM\d]+)\b\s*(.*)$",    re.IGNORECASE)
RE_CAPITULO = re.compile(r"^#+\s*CAP[ÍI]TULO\s+([IVXLCDM\d]+)\b\s*(.*)$",  re.IGNORECASE)
RE_SECCAO   = re.compile(r"^#+\s*SEC[ÇC][ÃA]O\s+([IVXLCDM\d]+)\b\s*(.*)$", re.IGNORECASE)
RE_ARTIGO   = re.compile(r"^#+\s*Artigo\s+(\d+)\.?\s*[º°ªo]?\s*(.*)$",      re.IGNORECASE)


def _section_re(pattern: str) -> re.Pattern | None:
    if not pattern:
        return None
    escaped = re.escape(pattern.strip())
    escaped = escaped.replace(r"\ ", r"\s+")
    return re.compile(rf"^#*\s*{escaped}\b", re.IGNORECASE)


def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def slugify(text: str, maxlen: int = 40) -> str:
    text = strip_accents(text).lower()
    text = re.sub(r"[«»\"'()]+", "", text)
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    if len(text) > maxlen:
        text = text[:maxlen].rsplit("_", 1)[0]
    return text or "sem_titulo"


def clean_lines(raw: str) -> list[str]:
    return [line.rstrip() for line in raw.splitlines() if not RE_DR_HEADER.match(line)]


def find_start(lines: list[str], skip_re: re.Pattern | None, stop_re: re.Pattern | None) -> int:
    if skip_re is None:
        return 0
    for i, line in enumerate(lines):
        if skip_re.match(line):
            if stop_re is None or not stop_re.match(line):
                return i
    return 0


def is_heading_caption(line: str) -> bool:
    return line.lstrip().startswith("#")


def next_caption(lines: list[str], i: int) -> str:
    j = i + 1
    while j < len(lines):
        s = lines[j].strip()
        if s:
            return re.sub(r"^#+\s*", "", s).strip()
        j += 1
    return ""


def file_stem(num: int, epi: str) -> str:
    return f"art_{num:03d}_{slugify(epi)}"


def parse_articles(
    lines: list[str],
    skip_re: re.Pattern | None,
    stop_re: re.Pattern | None,
) -> list[dict]:
    start_idx = find_start(lines, skip_re, stop_re)
    lines = lines[start_idx:]

    titulo = capitulo = seccao = ""
    articles: list[dict] = []
    current: dict | None = None
    body: list[str] = []

    def flush() -> None:
        nonlocal current, body
        if current is not None:
            current["body"] = "\n".join(body).strip()
            articles.append(current)
        body.clear()

    i, n = 0, len(lines)
    while i < n:
        line = lines[i]

        if stop_re and stop_re.match(line):
            flush()
            break

        m_t = RE_TITULO.match(line)
        m_c = RE_CAPITULO.match(line)
        m_s = RE_SECCAO.match(line)
        m_a = RE_ARTIGO.match(line)

        if m_t:
            cap = (m_t.group(2) or "").strip() or next_caption(lines, i)
            titulo = f"Título {m_t.group(1)} — {cap}".strip(" —")
            capitulo = seccao = ""
            i += 1; continue
        if m_c:
            cap = (m_c.group(2) or "").strip() or next_caption(lines, i)
            capitulo = f"Capítulo {m_c.group(1)} — {cap}".strip(" —")
            seccao = ""
            i += 1; continue
        if m_s:
            cap = (m_s.group(2) or "").strip() or next_caption(lines, i)
            seccao = f"Secção {m_s.group(1)} — {cap}".strip(" —")
            i += 1; continue
        if m_a:
            flush()
            num = int(m_a.group(1))
            epi = (m_a.group(2) or "").strip() or next_caption(lines, i)
            current = {"numero": num, "epigrafe": epi, "titulo": titulo,
                       "capitulo": capitulo, "seccao": seccao}
            i += 1
            if epi and i < n and is_heading_caption(lines[i]):
                if re.sub(r"^#+\s*", "", lines[i]).strip() == epi:
                    i += 1
            continue

        if current is not None:
            body.append(line)
        i += 1

    flush()
    return articles


def write_articles(articles: list[dict], articles_dir: Path,
                   regulamento: str, source_pdf: str, tags_yaml: str) -> None:
    articles_dir.mkdir(parents=True, exist_ok=True)
    for f in articles_dir.glob("art_*.md"):
        f.unlink()

    stems = {a["numero"]: file_stem(a["numero"], a["epigrafe"]) for a in articles}

    for idx, a in enumerate(articles):
        num = a["numero"]
        stem = stems[num]
        prev_stem = stems.get(articles[idx - 1]["numero"]) if idx > 0 else None
        next_stem = stems.get(articles[idx + 1]["numero"]) if idx + 1 < len(articles) else None

        fm = [
            "---",
            f"numero: {num}",
            f'epigrafe: "{a["epigrafe"]}"',
            f'titulo: "{a["titulo"]}"',
            f'capitulo: "{a["capitulo"]}"',
            f'seccao: "{a["seccao"]}"',
            f'regulamento: "{regulamento}"',
            f'source: "{source_pdf}"',
            f"tags: {tags_yaml}",
            "---",
        ]
        head = f"# Artigo {num}.º — {a['epigrafe']}".rstrip(" —")
        nav_parts = [
            f"[[{prev_stem}|◀ Anterior]]" if prev_stem else "◀",
            "[[index|Índice]]",
            f"[[{next_stem}|Seguinte ▶]]" if next_stem else "▶",
        ]
        content = "\n".join(fm) + "\n\n" + head + "\n\n" + a["body"].strip() + "\n\n---\n" + " · ".join(nav_parts) + "\n"
        (articles_dir / f"{stem}.md").write_text(content, encoding="utf-8")


def write_index(articles: list[dict], index_md: Path, regulamento: str) -> None:
    lines = [f"# Índice — {regulamento}", "", f"{len(articles)} artigos.", ""]
    last_t = last_c = last_s = None
    for a in articles:
        if a["titulo"] != last_t:
            last_t = a["titulo"]; last_c = last_s = None
            if last_t: lines.append(f"\n## {last_t}")
        if a["capitulo"] != last_c:
            last_c = a["capitulo"]; last_s = None
            if last_c: lines.append(f"\n### {last_c}")
        if a["seccao"] != last_s:
            last_s = a["seccao"]
            if last_s: lines.append(f"\n#### {last_s}")
        stem = file_stem(a["numero"], a["epigrafe"])
        label = f"Artigo {a['numero']}.º — {a['epigrafe']}".rstrip(" —")
        lines.append(f"- [[{stem}|{label}]]")
    index_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_metadata(articles: list[dict], meta_md: Path,
                   config: dict, source_pdf: str, tags_yaml: str) -> None:
    nums = [a["numero"] for a in articles]
    diploma = config.get("diploma", config["regulamento"])
    fm = [
        "---",
        f'regulamento: "{config["regulamento"]}"',
        f'diploma: "{diploma}"',
        f'source: "{source_pdf}"',
        f"n_artigos: {len(articles)}",
        f"artigo_min: {min(nums) if nums else 0}",
        f"artigo_max: {max(nums) if nums else 0}",
        f'metodo_conversao: "docling (sem OCR, tabelas estruturadas)"',
        f"data_conversao: {date.today().isoformat()}",
        f"tags: {tags_yaml}",
        "---",
        "",
        f"# {config['regulamento']}",
        "",
        f"Ver o [[index|Índice]] para navegar pelos artigos.",
        "",
    ]
    meta_md.write_text("\n".join(fm), encoding="utf-8")


def main() -> None:
    reg_dir = Path(sys.argv[1]).resolve()
    config = json.loads((reg_dir / "config.json").read_text(encoding="utf-8"))

    regulamento = config["regulamento"]
    source_pdf = Path(config["pdf_original"]).name
    skip_re = _section_re(config.get("skip_to_section", ""))
    stop_re = _section_re(config.get("stop_at_section", ""))
    tags = config.get("tags", ["regulamento", "artigo"])
    tags_yaml = "[" + ", ".join(tags) + "]"

    full_md = reg_dir / "full_document.md"
    raw = full_md.read_text(encoding="utf-8")
    lines = clean_lines(raw)

    articles = parse_articles(lines, skip_re, stop_re)
    write_articles(articles, reg_dir / "articles", regulamento, source_pdf, tags_yaml)
    write_index(articles, reg_dir / "index.md", regulamento)
    write_metadata(articles, reg_dir / "metadata.md", config, source_pdf, tags_yaml)
    print(f"Wrote {len(articles)} articles + index.md + metadata.md")


if __name__ == "__main__":
    main()
