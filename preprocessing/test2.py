import pdfplumber
import PyPDF2
import docx


mydoc = docx.Document()
pdfFileObj = open('D:\\sem-7\\SGP\\Resume Ranking\\AI_ML_Learning-master\\AI_ML_Learning-master\\resume_rating\\static\\UPLOAD_FOLDER\\Prince Ajudiya resume.pdf', 'rb')  # pdffile loction
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
with pdfplumber.open(pdfFileObj) as pdf:
    for i in range(0, pdfReader.numPages):
        first_page = pdf.pages[i]
        pdfContent = first_page.extract_text()
        mydoc.add_paragraph(pdfContent)

        print("=================================================================")

mydoc.save("D:\\sem-7\\SGP\\Resume Ranking\\AI_ML_Learning-master\\AI_ML_Learning-master\\resume_rating\\static\\filename.docx")