#!/usr/bin/env python3
"""
从本地文稿文件中提取元数据和链接
"""
import re
import json
import openpyxl
from pathlib import Path
from datetime import datetime

# 配置
MD_DIR = Path("/Users/apple/Documents/mycc/2-Projects/P003-YITANG-Study/004-正式课程")
EXCEL_PATH = "/Users/apple/Documents/mycc/2-Projects/P003-YITANG-Downloader/下载追踪表.xlsx"

def extract_from_markdown(file_path):
    """从 Markdown 文件中提取元数据和链接"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取元数据（frontmatter）
    metadata = {
        'title': '',
        'teacher': '',
        'category': '',
        'lesson_url': '',
        'doc_urls': [],
        'download_time': '',
        'image_count': 0
    }

    lines = content.split('\n')
    in_frontmatter = False

    for line in lines:
        # 检查 frontmatter 开始
        if line.strip() == '> 课程链接：':
            in_frontmatter = True
        elif line.strip() == '>' and in_frontmatter:
            break

        if in_frontmatter:
            # 提取课程链接
            if '课程链接：' in line:
                metadata['lesson_url'] = line.split('课程链接：')[1].strip()
            # 提取文稿链接
            elif '文稿链接：' in line and line.strip():
                doc_url = line.split('文稿链接：')[1].strip()
                if doc_url and doc_url.startswith('http'):
                    metadata['doc_urls'].append(doc_url)
            # 提取讲师
            elif '讲师：' in line:
                metadata['teacher'] = line.split('讲师：')[1].strip()
            # 提取分类
            elif '分类：' in line:
                metadata['category'] = line.split('分类：')[1].strip()
            # 提取下载时间
            elif '下载时间：' in line:
                metadata['download_time'] = line.split('下载时间：')[1].strip()
        else:
            # 提取标题（第一个 # 后的内容）
            if line.strip().startswith('# ') and not metadata['title']:
                metadata['title'] = line.replace('#', '').strip()
                # 如果是第一个标题，作为课程名称
                if '全员必修' in metadata['title'] or '必修' in metadata['title'] or '实操' in metadata['title']:
                    metadata['title'] = metadata['title'].replace('*', '').strip()
                break

    # 统计图片数量
    metadata['image_count'] = content.count('![[')

    return metadata

def scan_all_markdowns():
    """扫描所有文稿文件"""
    md_files = list(MD_DIR.rglob("*文稿.md"))
    print(f"找到 {len(md_files)} 个文稿文件")

    results = []

    for md_file in md_files:
        try:
            metadata = extract_from_markdown(md_file)
            metadata['file_path'] = str(md_file)
            results.append(metadata)
            print(f"✓ {md_file.name}: {metadata['title'][:30]}")
        except Exception as e:
            print(f"✗ {md_file.name}: {e}")

    return results

def save_to_excel(results):
    """保存到 Excel"""
    wb = openpyxl.load_workbook(EXCEL_PATH)
    ws = wb.active

    # 获取表头
    headers = ['序号', '日期', '分类', '来源', '内容名称', '讲师',
               '选课链接', '回放链接', '文稿链接', '作业链接', '作业飞书',
               'Candy1标题', 'Candy1链接', 'Candy2标题', 'Candy2链接',
               'Candy3标题', 'Candy3链接', 'Candy4标题', 'Candy4链接',
               '其他链接',
               '视频下载', '音频提取', '文稿下载', '整体状态',
               '文件路径', '失败原因', '备注']

    # 填入数据
    for i, data in enumerate(results, start=1):
        if not data['title']:
            continue

        row_data = [
            i,  # 序号
            '',  # 日期
            '',  # 分类
            '',  # 来源
            data['title'],  # 内容名称
            data['teacher'],  # 讲师
            data['lesson_url'],  # 选课链接
            '',  # 回放链接（待提取）
            '',  # 文稿链接
            '',  # 作业链接
            '',  # 作业飞书
        ] + [''] * 8 + [  # Candy 1-4（标题+链接）
            '',  # 其他链接
            '',  # 视频下载
            '',  # 音频提取
            '本地已有',  # 文稿下载
            '已完成',  # 整体状态
            data['file_path'],  # 文件路径
            '',  # 失败原因
            f'图片数: {data[\"image_count\"]}, 下载时间: {data[\"download_time\"]}'  # 备注
        ]

        ws.append(row_data)

    # 保存
    wb.save(EXCEL_PATH)
    print(f"\n数据已保存到 {EXCEL_PATH}")

if __name__ == '__main__':
    print("扫描本地文稿文件...")
    results = scan_all_markdowns()

    print(f"\n提取到 {len(results)} 门课程的数据")
    print("正在保存到 Excel...")
    save_to_excel(results)

    print("\n完成！")
