"""Generate PDF CV from markdown files using fpdf2."""

import re
from pathlib import Path

from fpdf import FPDF

from app.config import settings

_pdf_cache: dict[str, bytes] = {}

CV_FILES = {
    "en": "cv/CV_Narymane_Chabane.md",
    "fr": "cv/CV_Narymane_Chabane.md",
}

FONT_FAMILY = "DejaVu"


class CvPDF(FPDF):
    """Custom PDF renderer for the CV with Unicode support."""

    def __init__(self):
        super().__init__()
        font_dir = Path(__file__).resolve().parent / "fonts"
        self.add_font(FONT_FAMILY, "", str(font_dir / "DejaVuSans.ttf"), uni=True)
        self.add_font(FONT_FAMILY, "B", str(font_dir / "DejaVuSans-Bold.ttf"), uni=True)
        self.add_font(FONT_FAMILY, "I", str(font_dir / "DejaVuSans-Oblique.ttf"), uni=True)

    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font(FONT_FAMILY, "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def _parse_table(lines: list[str]) -> list[list[str]]:
    """Parse markdown table lines into rows of cells."""
    rows = []
    for line in lines:
        line = line.strip()
        if not line.startswith("|"):
            continue
        if re.match(r"^\|[\s\-:|]+\|$", line):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        rows.append(cells)
    return rows


def _render_table(pdf: CvPDF, rows: list[list[str]]):
    """Render a table in the PDF."""
    if not rows:
        return
    col_count = len(rows[0])
    page_width = pdf.w - pdf.l_margin - pdf.r_margin
    col_widths = [page_width / col_count] * col_count
    if col_count == 2:
        col_widths = [page_width * 0.3, page_width * 0.7]

    for i, row in enumerate(rows):
        is_header = i == 0
        if is_header:
            pdf.set_font(FONT_FAMILY, "B", 8)
            pdf.set_fill_color(240, 240, 240)
        else:
            pdf.set_font(FONT_FAMILY, "", 8)

        max_h = 6
        for j, cell in enumerate(row):
            lines_needed = max(1, len(pdf.multi_cell(col_widths[j], 5, cell, dry_run=True, output="LINES")))
            max_h = max(max_h, lines_needed * 5)

        y_start = pdf.get_y()
        for j, cell in enumerate(row):
            x = pdf.l_margin + sum(col_widths[:j])
            pdf.set_xy(x, y_start)
            pdf.multi_cell(
                col_widths[j], 5, cell,
                border=1, fill=is_header,
                new_x="RIGHT", new_y="TOP",
            )
        pdf.set_y(y_start + max_h)


def _clean_bold(text: str) -> list[tuple[str, bool]]:
    """Split text into segments with bold markers."""
    parts = []
    segments = re.split(r"\*\*(.+?)\*\*", text)
    for i, seg in enumerate(segments):
        if seg:
            parts.append((seg, i % 2 == 1))
    return parts


def _parse_rich_segments(text: str) -> list[dict]:
    """Parse text into segments: plain, bold, or link."""
    segments = []
    # Convert bare URLs to markdown links (but not those already in []() format)
    text = re.sub(r"(?<!\()(https?://[^\s\)]+)", lambda m: f"[{m.group(1)}]({m.group(1)})" if f"]({m.group(1)})" not in text else m.group(0), text)
    # Extract links [text](url)
    parts = re.split(r"\[(.+?)\]\((.+?)\)", text)
    for i, part in enumerate(parts):
        if i % 3 == 0:
            # Plain/bold text
            for content, is_bold in _clean_bold(part):
                segments.append({"text": content, "bold": is_bold, "url": None})
        elif i % 3 == 1:
            # Link text (next part is URL)
            segments.append({"text": part, "bold": False, "url": parts[i + 1]})
        # i % 3 == 2 is the URL, already consumed
    return segments


def _write_rich_line(pdf: CvPDF, text: str, size: int = 10):
    """Write a line with bold segments and clickable links."""
    segments = _parse_rich_segments(text)
    for seg in segments:
        if seg["url"]:
            pdf.set_font(FONT_FAMILY, "", size)
            pdf.set_text_color(40, 80, 180)
            pdf.write(6, seg["text"], seg["url"])
            pdf.set_text_color(0, 0, 0)
        else:
            pdf.set_font(FONT_FAMILY, "B" if seg["bold"] else "", size)
            pdf.write(6, seg["text"])
    pdf.ln(6)


def generate_cv_pdf(lang: str) -> bytes:
    """Generate a PDF from the markdown CV and cache it."""
    if lang == "fr":
        md_path = Path(settings.documents_fr_dir) / CV_FILES["fr"]
    else:
        md_path = Path(settings.documents_dir) / CV_FILES["en"]

    content = md_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    pdf = CvPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    i = 0
    table_buffer: list[str] = []
    in_table = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Detect table
        if stripped.startswith("|") and not in_table:
            in_table = True
            table_buffer = [stripped]
            i += 1
            continue
        elif in_table and stripped.startswith("|"):
            table_buffer.append(stripped)
            i += 1
            continue
        elif in_table and not stripped.startswith("|"):
            in_table = False
            rows = _parse_table(table_buffer)
            _render_table(pdf, rows)
            table_buffer = []
            pdf.ln(3)

        # H1
        if stripped.startswith("# "):
            text = stripped[2:]
            pdf.set_font(FONT_FAMILY, "B", 20)
            pdf.set_text_color(30, 30, 30)
            pdf.cell(0, 12, text, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
            i += 1
            continue

        # H2
        if stripped.startswith("## "):
            text = stripped[3:]
            pdf.ln(4)
            pdf.set_font(FONT_FAMILY, "B", 13)
            pdf.set_text_color(50, 80, 140)
            pdf.cell(0, 8, text, new_x="LMARGIN", new_y="NEXT")
            pdf.set_draw_color(50, 80, 140)
            pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
            pdf.ln(4)
            i += 1
            continue

        # H3
        if stripped.startswith("### "):
            text = stripped[4:]
            pdf.ln(2)
            pdf.set_font(FONT_FAMILY, "B", 11)
            pdf.set_text_color(60, 60, 60)
            pdf.cell(0, 7, text, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
            i += 1
            continue

        # Horizontal rule
        if stripped == "---":
            pdf.ln(2)
            i += 1
            continue

        # Bullet points
        if stripped.startswith("- "):
            text = stripped[2:]
            pdf.set_text_color(0, 0, 0)
            pdf.set_font(FONT_FAMILY, "", 9)
            x = pdf.get_x()
            pdf.cell(5, 6, "\u2022 ")
            pdf.set_x(x + 6)
            _write_rich_line(pdf, text, 9)
            i += 1
            continue

        # Sub-bullet points
        if stripped.startswith("+ ") or (stripped.startswith("- ") and line.startswith("  ")):
            text = re.sub(r"^[+\-]\s*", "", stripped)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font(FONT_FAMILY, "", 8)
            x = pdf.get_x()
            pdf.cell(12, 5, "  \u25e6 ")
            pdf.set_x(x + 14)
            _write_rich_line(pdf, text, 8)
            i += 1
            continue

        # Empty line
        if not stripped:
            pdf.ln(2)
            i += 1
            continue

        # Regular text
        pdf.set_font(FONT_FAMILY, "", 10)
        pdf.set_text_color(0, 0, 0)
        _write_rich_line(pdf, stripped, 10)
        i += 1

    # Flush remaining table
    if table_buffer:
        rows = _parse_table(table_buffer)
        _render_table(pdf, rows)

    pdf_bytes = bytes(pdf.output())
    _pdf_cache[lang] = pdf_bytes
    return pdf_bytes


def get_cv_pdf(lang: str) -> bytes:
    """Return cached PDF or generate it."""
    if lang in _pdf_cache:
        return _pdf_cache[lang]
    return generate_cv_pdf(lang)
