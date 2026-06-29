from fpdf import FPDF
from datetime import datetime


def generate_pdf(pcode, data_map):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", "B", 16)

    pdf.cell(
        0,
        10,
        "AI EV Diagnostic Report",
        ln=True
    )

    pdf.set_font("Arial", "", 12)

    pdf.cell(
        0,
        10,
        f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
        ln=True
    )

    pdf.cell(
        0,
        10,
        f"P-Code: {pcode}",
        ln=True
    )

    pdf.ln(5)

    for title, content in data_map.items():

        pdf.set_font(
            "Arial",
            "B",
            12
        )

        pdf.cell(
            0,
            8,
            str(title),
            ln=True
        )

        pdf.set_font(
            "Arial",
            "",
            11
        )

        pdf.multi_cell(
            180,
            8,
            str(content)
        )

        pdf.ln(2)

    filename = f"{pcode}_report.pdf"

    pdf.output(filename)

    return filename