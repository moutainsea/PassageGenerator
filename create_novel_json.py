import zipfile
import xml.etree.ElementTree as ET
import os
import glob
import json
import re

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
    match = re.search(r'第([一二三四五六七八九十百]+)章', filename)
    if match:
        chinese_num = match.group(1)
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
            # Get title from first line
            title = content.split('\n')[0] if content else ''
            chapters.append({
                "index": chapter_num,
                "title": title,
                "content": content,
                "small_event_id": "E" + str(chapter_num)
            })
    
    # Sort by chapter number
    chapters.sort(key=lambda x: x["index"])
    
    # Read third volume txt file
    third_volume_path = os.path.join(folder_path, '第三卷.txt')
    if os.path.exists(third_volume_path):
        with open(third_volume_path, 'r', encoding='utf-8') as f:
            third_volume_content = f.read()
        
        # Parse third volume chapters
        # The format is: 第三卷 第一章 正面硬扛
        third_chapters = re.findall(r'第三卷 第([一二三四五六七八九十]+)章 (.+?)\n(.+?)(?=第三卷 第|$)', third_volume_content, re.DOTALL)
        for match in third_chapters:
            chinese_num = match[0]
            title = match[1]
            content = match[2]
            chinese_to_int = {
                '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
                '六': 6, '七': 7, '八': 8, '九': 9, '十': 10
            }
            chapter_num = 37 + chinese_to_int.get(chinese_num, 0)  # Third volume starts at chapter 38
            chapters.append({
                "index": chapter_num,
                "title": title,
                "content": content,
                "small_event_id": "E" + str(chapter_num)
            })
    
    # Sort again
    chapters.sort(key=lambda x: x["index"])
    
    # Create novel json structure
    novel = {
        "name": "海贼王之百亿贝利海贼猎人",
        "outline": {
            "event_library": {
                "big_events": [
                    {
                        "summary": "海贼猎人之路",
                        "middle_events": [
                            {
                                "summary": "第一卷 海贼猎人",
                                "small_events": []
                            },
                            {
                                "summary": "第二卷 七武海",
                                "small_events": []
                            },
                            {
                                "summary": "第三卷 顶上战争",
                                "small_events": []
                            }
                        ]
                    }
                ]
            },
            "subplots": [
                {
                    "id": "subplot_1",
                    "name": "海贼猎人之路",
                    "description": "主角夏里亚成为海贼猎人的历程",
                    "chapter_indices": [1, 37],
                    "stages": []
                },
                {
                    "id": "subplot_2",
                    "name": "七武海之路",
                    "description": "主角夏里亚成为七武海的历程",
                    "chapter_indices": [20, 37],
                    "stages": []
                },
                {
                    "id": "subplot_3",
                    "name": "顶上战争",
                    "description": "主角夏里亚参与顶上战争",
                    "chapter_indices": [38, 41],
                    "stages": []
                }
            ]
        },
        "chapters": chapters,
        "tags": ["海贼王", "同人", "爽文", "穿越"],
        "description": "在海贼王的世界里，有着各种各样的恶魔果实，有着十分先进的未来科技，有着各有特色的不同种族。夏落作为一名刚毕业的大学生，他穿越到了海贼王的世界，而他的愿望则是想成为一名世界第一的赏金猎人。",
        "author": "未知",
        "platform": "fanqie"
    }
    
    # Save to json file
    output_path = 'd:\\PassageGenerator\\output\\novels\\海贼王之百亿贝利海贼猎人.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(novel, f, ensure_ascii=False, indent=2)
    
    print("已生成json文件: " + output_path)
    print("总章节数: " + str(len(chapters)))

if __name__ == '__main__':
    main()