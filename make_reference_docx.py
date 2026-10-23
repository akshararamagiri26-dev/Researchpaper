"""Create a minimal double-spaced reference DOCX for the Pandoc manuscript build.

This is a formatting aid, not an official Elsevier template. Always inspect the
rendered file against the current Knowledge-Based Systems instructions.
"""
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_LINE_SPACING
from docx.enum.section import WD_SECTION

doc = Document()
section = doc.sections[0]
section.top_margin = Inches(1)
section.bottom_margin = Inches(1)
section.left_margin = Inches(1)
section.right_margin = Inches(1)

styles = doc.styles
normal = styles["Normal"]
normal.font.name = "Times New Roman"
normal.font.size = Pt(12)
normal.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
normal.paragraph_format.space_after = Pt(0)

for name, size in (("Title", 16), ("Heading 1", 14), ("Heading 2", 12), ("Heading 3", 12)):
    style = styles[name]
    style.font.name = "Times New Roman"
    style.font.size = Pt(size)
    style.font.bold = True
    style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(0)

for name in ("Caption",):
    if name in styles:
        styles[name].font.name = "Times New Roman"
        styles[name].font.size = Pt(10)
        styles[name].paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE

doc.core_properties.title = "Knowledge-Based Systems manuscript reference styles"
doc.core_properties.subject = "Double-spaced review copy; not an official journal template"
doc.save("manuscript_reference.docx")
