"""Render report/report.md -> report/report.pdf (minimal Markdown: #, ##, ###,
paragraphs, '- ' bullets, pipe tables, ![caption](path) images, **bold**,
*italic*, `code`, [text](url)). Usage: python -m whoiswho.report"""
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (Image, KeepTogether, ListFlowable, ListItem, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

SRC = Path("report/report.md")
OUT = Path("report/report.pdf")
INK = colors.HexColor("#0b0b0b")
MUTED = colors.HexColor("#52514e")
RULE = colors.HexColor("#d9d8d3")
ACCENT = colors.HexColor("#2a78d6")

ss = getSampleStyleSheet()
BODY = ParagraphStyle("body", parent=ss["BodyText"], fontName="Times-Roman", fontSize=10.5, leading=14,
                      textColor=INK, spaceAfter=6)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=8.5, leading=10.5)
CAP = ParagraphStyle("cap", parent=BODY, fontSize=9, leading=11.5, textColor=MUTED, spaceAfter=10)
TITLE = ParagraphStyle("title", parent=BODY, fontName="Helvetica-Bold", fontSize=17, leading=21,
                       alignment=TA_CENTER, spaceAfter=6)
SUB = ParagraphStyle("sub", parent=BODY, alignment=TA_CENTER, textColor=MUTED, fontSize=10)
H1 = ParagraphStyle("h1", parent=BODY, fontName="Helvetica-Bold", fontSize=12.5, leading=16,
                    spaceBefore=10, spaceAfter=4, textColor=INK, keepWithNext=1)
H2 = ParagraphStyle("h2", parent=BODY, fontName="Helvetica-Bold", fontSize=10.5, leading=13,
                    spaceBefore=6, spaceAfter=3, keepWithNext=1)


def inline(t):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<link href="\2" color="#2a78d6">\1</link>', t)
    t = re.sub(r"`([^`]+)`", r'<font face="Courier" size="9">\1</font>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*([^*]+)\*(?![\w*])", r"<i>\1</i>", t)
    return t


def table(rows):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    cells = [r for r in cells if not all(re.fullmatch(r":?-{2,}:?", c) for c in r)]
    data = [[Paragraph(("<b>%s</b>" if i == 0 else "%s") % inline(c), SMALL) for c in r] for i, r in enumerate(cells)]
    ncol = len(cells[0])
    first = 0.30 if ncol > 2 else 0.4
    widths = [17 * cm * first] + [17 * cm * (1 - first) / (ncol - 1)] * (ncol - 1)
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (-1, 0), 0.8, INK), ("LINEBELOW", (0, 0), (-1, 0), 0.5, INK),
        ("LINEBELOW", (0, -1), (-1, -1), 0.8, INK), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


def build():
    lines = SRC.read_text().splitlines()
    story, para, bullets, trows = [], [], [], []

    def flush():
        nonlocal para, bullets, trows
        if para:
            story.append(Paragraph(inline(" ".join(para)), BODY))
        if bullets:
            story.append(ListFlowable([ListItem(Paragraph(inline(b), BODY), leftIndent=12) for b in bullets],
                                      bulletType="bullet", start="•", leftIndent=12, bulletFontSize=8))
        if trows:
            story.extend([table(trows), Spacer(1, 6)])
        para, bullets, trows = [], [], []

    for ln in lines:
        s = ln.rstrip()
        if s.startswith("<!--"):
            continue
        if s.startswith("|"):
            if para or bullets:
                flush()
            trows.append(s)
            continue
        if trows:
            flush()
        if s.startswith("# "):
            flush(); story.append(Paragraph(inline(s[2:]), TITLE))
        elif s.startswith("::sub "):
            flush(); story.append(Paragraph(inline(s[6:]), SUB))
        elif s.startswith("## "):
            flush(); story.append(Paragraph(inline(s[3:]), H1))
        elif s.startswith("### "):
            flush(); story.append(Paragraph(inline(s[4:]), H2))
        elif s.strip() == "::pagebreak":
            flush(); story.append(PageBreak())
        elif m := re.match(r"!\[(.*)\]\((.*?)\)(?:\{w=([\d.]+)\})?", s):
            flush()
            img = Image(m.group(2))
            w = float(m.group(3) or 16) * cm
            img.drawHeight = img.drawHeight * w / img.drawWidth
            img.drawWidth = w
            story.append(KeepTogether([img, Paragraph(inline(m.group(1)), CAP)]))
        elif s.startswith("- "):
            if para:
                story.append(Paragraph(inline(" ".join(para)), BODY)); para = []
            bullets.append(s[2:])
        elif not s.strip():
            flush()
        elif bullets and ln.startswith("  "):
            bullets[-1] += " " + s.strip()
        else:
            para.append(s.strip())
    flush()

    def deco(c, d):
        c.saveState()
        c.setFont("Helvetica", 8)
        c.setFillColor(MUTED)
        c.drawRightString(A4[0] - 2 * cm, 1.2 * cm, str(d.page))
        c.drawString(2 * cm, 1.2 * cm, "Name Tags Lie · Apart Swarm Alignment Sprint 2026")
        c.restoreState()

    OUT.parent.mkdir(exist_ok=True)
    SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm,
                      bottomMargin=2 * cm, title="Name Tags Lie: Who Is Who in an AI Agent Swarm").build(story, onFirstPage=deco,
                                                                                  onLaterPages=deco)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    build()
