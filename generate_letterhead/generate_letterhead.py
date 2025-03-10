import argparse
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader

# Constants for image paths
LOGO_PATH = "src/logo.png"
SIGNATURE_PATH = "src/signature.png"
FONT_SEGOETV_REGULAR_PATH = "fonts/SegoeTVRegular.ttf"
FONT_SEGOETV_BOLD_PATH = "fonts/SegoeTVBold.ttf"

# Company Address
COMPANY_NAME = "Lambda Equity (Pty) Ltd"
REGISTRATION = "Reg: 2025/211083/07"
ADDRESS_LINES = [
    "92 Alltimers Street",
    "Everywhere",
    "San Franscisco",
    "1112"
]

def read_text_from_file(file_path):
    """Reads the content of the text file"""
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return file.read()
    else:
        print(f"Error: The file '{file_path}' does not exist.")
        return ""
    
# Register Segoe UI Font
if os.path.exists(FONT_SEGOETV_REGULAR_PATH):
    pdfmetrics.registerFont(TTFont("SegoeTV-Regular", FONT_SEGOETV_REGULAR_PATH))
else:
    print("Warning: Segoe UI font file not found. Falling back to default font.")

# Register Segoe UI Bold Font
if os.path.exists(FONT_SEGOETV_BOLD_PATH):
    pdfmetrics.registerFont(TTFont("SegoeTV-Bold", FONT_SEGOETV_BOLD_PATH))
else:
    print("Warning: Segoe UI Bold font file not found. Falling back to default font.")    

def create_letterhead(recipient, subject, text, output_filename="letterhead.pdf"):
    # Setup canvas
    c = canvas.Canvas(output_filename, pagesize=A4)
    width, height = A4

    # # Insert Logo
    # logo = ImageReader(LOGO_PATH)
    # logo_width, logo_height = 210, 150  # Adjust size as needed
    # c.drawImage(logo, 40, height - 140, width=logo_width, height=logo_height, mask='auto')


    # Insert Centered Logo
    logo = ImageReader(LOGO_PATH)
    logo_width, logo_height = 250, 150  # Adjust as needed
    logo_x = (width - logo_width) / 2  # Centering the logo
    c.drawImage(logo, logo_x, height - 160, width=logo_width, height=logo_height, mask='auto')


    # Add Company Name & Address with Extra Spacing
    address_start_y = height - 160  # Add space after the logo
    c.setFont("SegoeTV-Bold", 12)
    c.drawString(40, address_start_y, COMPANY_NAME)

    c.setFont("SegoeTV-Regular", 12)
    c.drawString(40, address_start_y - 15, REGISTRATION)

    address_y = address_start_y - 35  # Further push down the address to avoid overlap
    for line in ADDRESS_LINES:
        c.drawString(40, address_y, line)
        address_y -= 15

    # Add Confidential Label with more spacing
    c.setFont("SegoeTV-Bold", 12)
    c.drawString(40, address_y - 30, "Private & Confidential")

    # Addressing the recipient
    c.setFont("SegoeTV-Regular", 12)
    c.drawString(40, address_y - 60, f"Dear {recipient},")

    # Subject Line
    c.setFont("SegoeTV-Bold", 12)
    c.drawString(40, address_y - 90, f"Re: {subject}")

    # Letter Body
    text_start_y = address_y - 120
    c.setFont("SegoeTV-Regular", 12)
    text_lines = text.split("\n")
    for line in text_lines:
        c.drawString(40, text_start_y, line)
        text_start_y -= 20

    # Closing line
    c.drawString(40, text_start_y - 20, "Yours sincerely,")
    
    # Add "Jhon Doe"
    c.setFont("SegoeTV-Bold", 12)
    c.drawString(40, text_start_y - 40, "John Doe")

    # Draw a separator line
    c.line(40, text_start_y - 60, 200, text_start_y - 60)

    # Insert Signature
    signature = ImageReader(SIGNATURE_PATH)
    sig_width, sig_height = 120, 60  # Adjust size as needed
    c.drawImage(signature, 40, text_start_y - 120, width=sig_width, height=sig_height, mask='auto')
   
    # # Insert Signature at Fixed Position (Always ~100 pts from the bottom)
    # signature = ImageReader(SIGNATURE_PATH)
    # sig_width, sig_height = 120, 60  # Adjust size as needed
    # c.drawImage(signature, 40, 60, width=sig_width, height=sig_height, mask='auto')


    # Save the PDF
    c.save()
    print(f"Letterhead saved as {output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a letterhead PDF.")
    parser.add_argument("--recipient", required=True, help="Recipient's name")
    parser.add_argument("--subject", required=True, help="Subject of the letter")
    parser.add_argument("--text", required=True, help="Body text of the letter")

    args = parser.parse_args()

    # Read text from file
    body_text = read_text_from_file(args.text)

    create_letterhead(args.recipient, args.subject, body_text)
