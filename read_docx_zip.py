import zipfile
import xml.etree.ElementTree as ET
import sys

def read_docx(file_path):
    with zipfile.ZipFile(file_path, 'r') as z:
        xml_content = z.read('word/document.xml')
        tree = ET.fromstring(xml_content)
        
        paragraphs = []
        for paragraph in tree.findall('.//w:p', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
            texts = []
            for text in paragraph.findall('.//w:t', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
                if text.text:
                    texts.append(text.text)
            paragraphs.append(''.join(texts))
        
        return '\n'.join(paragraphs)

if __name__ == '__main__':
    file_path = sys.argv[1]
    print(read_docx(file_path))