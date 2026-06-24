import zipfile
import xml.etree.ElementTree as ET
import os
import glob

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

def get_chapter_number(filename):
    # Extract chapter number from filename
    import re
    match = re.search(r'第([一二三四五六七八九十百]+)章', filename)
    if match:
        chinese_num = match.group(1)
        # Convert Chinese number to integer
        chinese_to_int = {
            '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
            '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
            '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15,
            '十六': 16, '十七': 17, '十八': 18, '十九': 19, '二十': 20,
            '二十一': 21, '二十二': 22, '二十三': 23, '二十四': 24, '二十五': 25,
            '二十六': 26, '二十七': 27, '二十八': 28, '二十九': 29, '三十': 30,
            '三十一': 31, '三十二': 32, '三十三': 33, '三十四': 34, '三十五': 35,
            '三十六': 36, '三十七': 37, '三十八': 38, '三十九': 39, '四十': 40,
            '四十一': 41, '四十二': 42, '四十三': 43, '四十四': 44, '四十五': 45,
            '四十六': 46, '四十七': 47, '四十八': 48, '四十九': 49, '五十': 50
        }
        return chinese_to_int.get(chinese_num, 0)
    return 0

def main():
    folder_path = 'D:\\网络文学作品\\海贼王之百亿贝利海贼猎人'
    docx_files = glob.glob(os.path.join(folder_path, '*.docx'))
    
    # Filter out temporary files
    docx_files = [f for f in docx_files if not os.path.basename(f).startswith('~')]
    
    # Sort files by chapter number
    chapters = []
    for file_path in docx_files:
        chapter_num = get_chapter_number(os.path.basename(file_path))
        if chapter_num > 0:
            content = read_docx(file_path)
            chapters.append((chapter_num, os.path.basename(file_path), content))
    
    # Sort by chapter number
    chapters.sort(key=lambda x: x[0])
    
    # Output all chapters
    for chapter_num, filename, content in chapters:
        print("\n=== 第" + str(chapter_num) + "章 ===")
        print("文件: " + filename)
        print("内容长度: " + str(len(content)) + " 字")
        print("内容前500字: " + content[:500] + "...")
        print("-" * 50)

if __name__ == '__main__':
    main()