from fpdf import FPDF

def generate_certificate(name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.cell(200, 20, txt="MindMate AI Certificate", ln=1, align="C")
    pdf.set_font("Arial", "", 16)
    pdf.cell(200, 10, txt=f"Congrats, {name}!", ln=2, align="C")
    pdf.cell(200, 10, txt="You’ve journaled for 7 days 🎉", ln=3, align="C")
    pdf.output("MindMate_Certificate.pdf")
