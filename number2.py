from fpdf import FPDF
import pdfplumber
import re

def convert_to_24h(time_str):
    """ Convert 12-hour time format to 24-hour time format. """
    return re.sub(r'(\d{1,2}):(\d{2})\s*(AM|PM)', lambda match: "{:02d}:{:02d}".format(
        (int(match.group(1)) % 12) + (12 if match.group(3).strip() == 'PM' else 0),
        int(match.group(2))), time_str)

class PDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       # If the font file is in the same directory as the script
        self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf')

# If the font file is in another directory, use the absolute path
        self.add_font('DejaVu', '', 'C:/path/to/fonts/DejaVuSansCondensed.ttf')

    def add_page_with_text(self, text):
        self.add_page()
        self.multi_cell(200, 10, text)

def modify_pdf_times(input_file, output_file):
    with pdfplumber.open(input_file) as pdf:
        all_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                modified_text = convert_to_24h(text)
                all_text += modified_text + "\n\n"

        pdf_writer = PDF()
        pdf_writer.add_page_with_text(all_text)
        pdf_writer.output(output_file)
    print("Modified PDF saved as:", output_file)

# Define file paths
input_file = 'schedule.pdf'
output_file = 'new-schedule.pdf'

# Modify the PDF and save it to a new file
modify_pdf_times(input_file, output_file)
