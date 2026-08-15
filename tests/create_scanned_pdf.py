from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image, ImageDraw, ImageFont


# --------------------------------------------------
# 1. Create a fake medical report as an image
# --------------------------------------------------

image_path = "data/raw/scanned_report_page.png"

image = Image.new("RGB", (1275, 1650), "white")
draw = ImageDraw.Draw(image)

try:
    font = ImageFont.truetype("arial.ttf", 32)
    small_font = ImageFont.truetype("arial.ttf", 24)
except OSError:
    font = ImageFont.load_default()
    small_font = ImageFont.load_default()


lines = [
    "MEDICAL LABORATORY REPORT",
    "",
    "Patient Name: Sample Patient",
    "Age: 25",
    "",
    "COMPLETE BLOOD COUNT",
    "",
    "Hemoglobin: 11.2 g/dL",
    "Reference Range: 12.0 - 16.0 g/dL",
    "",
    "WBC Count: 8,500 /uL",
    "Reference Range: 4,000 - 11,000 /uL",
    "",
    "Platelet Count: 250,000 /uL",
    "Reference Range: 150,000 - 450,000 /uL",
    "",
    "Vitamin D: 18 ng/mL",
    "Reference Range: 30 - 100 ng/mL",
]


y = 100

for i, line in enumerate(lines):
    current_font = font if i == 0 else small_font
    draw.text((100, y), line, fill="black", font=current_font)
    y += 60


image.save(image_path)


# --------------------------------------------------
# 2. Put that image inside a PDF
# --------------------------------------------------

pdf_path = "data/raw/scanned_medical_report.pdf"

pdf = canvas.Canvas(pdf_path, pagesize=letter)

pdf.drawImage(
    image_path,
    0,
    0,
    width=letter[0],
    height=letter[1],
)

pdf.save()

print(f"Scanned PDF created at: {pdf_path}")