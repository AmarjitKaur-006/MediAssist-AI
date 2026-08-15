from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


output_path = "data/raw/sample_medical_report.pdf"

pdf = canvas.Canvas(output_path, pagesize=letter)

pdf.setFont("Helvetica", 14)
pdf.drawString(72, 750, "MEDICAL LABORATORY REPORT")

pdf.setFont("Helvetica", 11)
pdf.drawString(72, 720, "Patient Name: Sample Patient")
pdf.drawString(72, 700, "Age: 25")

pdf.drawString(72, 660, "COMPLETE BLOOD COUNT")

pdf.drawString(72, 630, "Hemoglobin: 11.2 g/dL")
pdf.drawString(72, 610, "Reference Range: 12.0 - 16.0 g/dL")

pdf.drawString(72, 580, "WBC Count: 8,500 /uL")
pdf.drawString(72, 560, "Reference Range: 4,000 - 11,000 /uL")

pdf.drawString(72, 530, "Platelet Count: 250,000 /uL")
pdf.drawString(72, 510, "Reference Range: 150,000 - 450,000 /uL")

pdf.drawString(72, 480, "Vitamin D: 18 ng/mL")
pdf.drawString(72, 460, "Reference Range: 30 - 100 ng/mL")

pdf.save()

print(f"Sample PDF created at: {output_path}")