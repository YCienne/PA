import pyttsx4
import pypdf
book = open('Stu.pdf', 'rb')
pdf_reader = pypdf.PdfReader(book)
pages = len(pdf_reader.pages)
print(pages)
speaker = pyttsx4.init()
for num in range(pages):
    page = pdf_reader.pages
    text = page.extract_text(pages[num])
    speaker.say(text)
    speaker.runAndWait()
