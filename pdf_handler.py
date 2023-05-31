import pytesseract
from pdf2image import convert_from_path
import PyPDF2
from dotenv import load_dotenv
import io
import os
import fitz

load_dotenv()
poppler_path = os.getenv('POPPLER_PATH')

def pdf_convert():
    images = convert_from_path('./.cache/temp.pdf', poppler_path=poppler_path)
    pdf_writer = PyPDF2.PdfFileWriter()
    for image in images:
        page = pytesseract.image_to_pdf_or_hocr(image, extension='pdf')
        pdf = PyPDF2.PdfFileReader(io.BytesIO(page))
        pdf_writer.addPage(pdf.getPage(0))
    # export the searchable PDF to searchable.pdf
    with open("./.cache/temp.pdf", "wb") as f:
        pdf_writer.write(f)

def pdf_classifier(pdf_file):
    with open(pdf_file, "rb") as f:
        pdf = fitz.open(f)
        res = []
        label = 0
        for page in pdf:
            image_area = 0.0
            text_area = 0.0
            for b in page.get_text("blocks"):
                if '<image:' in b[4]:
                    r = fitz.Rect(b[:4])
                    image_area = image_area + abs(r)
                else:
                    r = fitz.Rect(b[:4])
                    text_area = text_area + abs(r)
            # page is all text
            if image_area == 0.0 and text_area != 0.0:
                res.append(1)
            # page is all image
            if text_area == 0.0 and image_area != 0.0:
                res.append(0)
        if 0 in res:
          print('Pdf is image-based')
        else:
          label = 1
          print('Pdf is text-based')
        return label

# if __name__ == '__main__':
#     pdf_classifier('/Users/sonali/Desktop/deep-learning.pdf')
#     pdf_classifier('/Users/sonali/Downloads/F&Q Booklet _Hypertension.pdf')