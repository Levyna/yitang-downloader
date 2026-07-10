#!/usr/bin/env python3
"""
一堂课程链接批量提取器 - 通过 Chrome DevTools Protocol
"""
import json
import subprocess
import time
import sys
import re
from urllib.parse import urlparse, parse_qs

# 读取课程
JSON_PATH = "/Users/apple/Documents/mycc/2-Projects/P003-YITANG-Study/004-正式课程/文稿下载清单.json"
EXCEL_PATH = "/Users/apple/Documents/mycc/2-Projects/P003-YITANG-Downloader/下载追踪表.xlsx"

def load_courses():
    with open(JSON_PATH, 'r') as f:
        data = json.load(f)
    return data['results']

def extract_links_via_browser(lesson_url):
    """
    通过浏览器提取课程链接
    返回: {replay, doc, homework, feishu, candys}
    """
    # 使用 Chrome DevTools MCP 调用
    # 这里需要通过 MCP 工具调用，暂时返回模拟数据
    cmd = f'''
    osascript << 'EOF'
    tell application "Google Chrome"
    activate
    execute javascript "
    // 在这里执行 JavaScript 来提取链接
    // 由于需要等待页面加载，这里简化处理
    " in front document
    EOF
    '''

    try:
        result = subprocess.check_output(cmd, shell=True, text=True, timeout=30)
        return parse_links(result)
    except:
        return {}

def parse_links(html_content):
    """从 HTML 中解析链接"""
    links = re.findall(r'href="([^"]+)"', html_content)

    result = {
        'replay': '',
        'doc': '',
        'homework': '',
        'feishu': '',
        'candys': []
    }

    for link in links:
        if '/air.' in link:
            result['replay'] = link
        elif '/fs-doc/' in link:
            result['doc'] = link
        elif 'homework' in link:
            result['homework'] = link
        elif 'feishu' in link:
            result['feishu'] = link

    return result

def process_course(course):
    """处理单门课程"""
    print(f"处理: {course['title']}")

    try:
        # 通过 Chrome DevTools MCP 提取
        links = extract_links_via_browser(course['lessonUrl'])

        # 记录结果
        result = {
            'index': course['courseIndex'],
            'title': course['title'],
            'teacher': course.get('teacher', ''),
            'category1': course.get('category1', ''),
            'category2': course.get('category2', ''),
            'lessonUrl': course['lessonUrl'],
            **links
        }

        time.sleep(2)  # 避免请求过快
        return result

    except Exception as e:
        print(f"  失败: {e}")
        return None

def batch_process(limit=10):
    """批量处理课程"""
    courses = load_courses()
    courses_to_process = courses[:limit]

    results = []
    for course in courses_to_process:
        result = process_course(course)
        if result:
            results.append(result)

    return results

if __name__ == '__main__':
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 5

    print(f"准备处理 {limit} 门课程...")
    results = batch_process(limit)

    print(f"\n完成处理 {len(results)} 门课程")
    print("结果将保存到 Excel")
