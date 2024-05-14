import re
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def convert_to_24h(time_str):
    """ Convert 12-hour time format to 24-hour time format. """
    return re.sub(r'(\d{1,2}):(\d{2}) (AM|PM)', lambda match: "{:02d}:{:02d}".format(
        (int(match.group(1)) % 12) + (12 if match.group(3) == 'PM' else 0),
        int(match.group(2))), time_str)

def create_pdf_with_text(text, filename):
    """ Create a new PDF file with given text. """
    c = canvas.Canvas(filename, pagesize=letter)
    text_object = c.beginText(40, 750)
    text_object.setFont("Helvetica", 12)
    # Insert modified text into new PDF
    for line in text.split('\n'):
        text_object.textLine(line)
    c.drawText(text_object)
    c.save()

def modify_pdf_times(input_file, output_file):
    reader = PdfReader(input_file)
    all_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            modified_text = convert_to_24h(text)
            all_text += modified_text + "\n\n"

    create_pdf_with_text(all_text, output_file)
    print("Modified PDF saved as:", output_file)

# Define file paths
input_file = 'schedule.pdf'
output_file = 'new-schedule.pdf'

# Modify the PDF and save it to new file
modify_pdf_times(input_file, output_file)

