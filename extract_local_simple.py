#!/usr/bin/env python3
import re
import json
import openpyxl
from pathlib import Path

MD_DIR = Path("/Users/apple/Documents/mycc/2-Projects/P003-YITANG-Study/004-正式课程")
EXCEL_PATH = "/Users/apple/Documents/mycc/2-Projects/P003-YITANG-Downloader/下载追踪表.xlsx"

def extract_from_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    metadata = {
        'title': '',
        'teacher': '',
        'category': '',
        'lesson_url': '',
        'doc_urls': [],
        'download_time': '',
        'file_path': str(file_path)
    }

    # 简单正则提取
    for line in content.split('\n'):
        if '课程链接：' in line:
            metadata['lesson_url'] = line.split('课程链接：')[1].strip()
        elif '讲师：' in line:
            metadata['teacher'] = line.split('讲师：')[1].strip()
        elif '分类：' in line:
            metadata['category'] = line.split('分类：')[1].strip()
        elif '文稿链接：' in line and 'http' in line:
            url = re.search(r'https://[^\s]+', line)
            if url:
                metadata['doc_urls'].append(url.group(0))
        elif '下载时间：' in line:
            metadata['download_time'] = line.split('下载时间：')[1].strip()
        elif line.strip().startswith('# ') and not metadata['title']:
            metadata['title'] = line.replace('#', '').strip()

    return metadata

def main():
    md_files = list(MD_DIR.rglob("*文稿.md"))
    print(f"找到 {len(md_files)} 个文稿文件")

    wb = openpyxl.load_workbook(EXCEL_PATH)
    ws = wb.active

    idx = 2  # 从第2行开始（第1行是表头）

    for md_file in md_files:
        try:
            data = extract_from_markdown(md_file)
            if data['title']:
                # 简化的行数据（只填关键字段）
                row = [idx, '', '', '', data['title'], data['teacher'], 
                       data['lesson_url'], '', '', '', '', '',
                       '', '', '', '', '', '', '', '', '', '',
                       '', '', '', '本地已有', data['file_path'], '', 
                       f"图片数: {data['doc_urls'].__len__()}"
                       ]
                ws.append(row)
                idx += 1
                print(f"{idx-1}. {data['title'][:40]}")
        except Exception as e:
            print(f"跳过: {md_file.name} - {e}")

    wb.save(EXCEL_PATH)
    print(f"\n完成！已处理 {idx-1} 门课程")
    print(f"数据已保存到: {EXCEL_PATH}")

if __name__ == '__main__':
    main()
