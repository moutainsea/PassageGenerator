from docx import Document
import sys

def read_docx(file_path):
    doc = Document(file_path)
    content = []
    for para in doc.paragraphs:
        content.append(para.text)
    return '\n'.join(content)

if __name__ == '__main__':
    file_path = sys.argv[1]
    print(read_docx(file_path))