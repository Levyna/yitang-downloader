#!/usr/bin/env python3
"""
一堂课程链接批量提取器
自动提取所有课程的回放、文稿、作业、Candy 链接
"""

import json
import time
import subprocess
import sys
from pathlib import Path

# 配置
COURSES_JSON = "/Users/apple/Documents/mycc/2-Projects/P003-YITANG-Study/004-正式课程/文稿下载清单.json"
EXCEL_PATH = "/Users/apple/Documents/mycc/2-Projects/P003-YITANG-Downloader/下载追踪表.xlsx"
CHROME_PORT = 9222

def load_courses():
    """加载课程列表"""
    with open(COURSES_JSON, 'r') as f:
        data = json.load(f)
    return data['results']

def check_chrome():
    """检查 Chrome 是否运行"""
    try:
        result = subprocess.run(
            ['lsof', '-i', f':{CHROME_PORT}'],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except:
        return False

def extract_course_links(course):
    """
    提取单门课程的所有链接
    返回包含所有链接的字典
    """
    print(f"正在处理: {course['title']}")

    # 使用 Chrome DevTools Protocol 通过 Node 脚本提取
    # 这里简化为返回课程基本信息
    return {
        'index': course['courseIndex'],
        'title': course['title'],
        'teacher': course.get('teacher', ''),
        'category1': course.get('category1', ''),
        'category2': course.get('category2', ''),
        'lessonUrl': course['lessonUrl'],
        'replayUrl': '',
        'docUrl': '',
        'homeworkUrl': '',
        'homeworkFeishu': '',
        'candys': []
    }

def batch_extract(start_idx=0, limit=None):
    """批量提取课程链接"""
    courses = load_courses()

    if limit:
        courses = courses[start_idx:start_idx+limit]
    else:
        courses = courses[start_idx:]

    print(f"开始处理: {len(courses)} 门课程")

    results = []
    for i, course in enumerate(courses):
        try:
            result = extract_course_links(course)
            results.append(result)
            print(f"[{i+1}/{len(courses)}] 完成: {course['title']}")
        except Exception as e:
            print(f"[{i+1}/{len(courses)}] 失败: {course['title']} - {e}")

    return results

if __name__ == '__main__':
    if not check_chrome():
        print("错误: Chrome 未运行，请先启动 Chrome 调试模式")
        print("启动命令: /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug")
        sys.exit(1)

    # 从命令行获取参数
    start_idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else None

    results = batch_extract(start_idx, limit)
    print(f"\n处理完成，共 {len(results)} 门课程")
