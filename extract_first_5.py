#!/usr/bin/env python3
import json
import openpyxl

# 读取课程
with open('/Users/apple/Documents/mycc/2-Projects/P003-YITANG-Study/004-正式课程/文稿下载清单.json', 'r') as f:
    data = json.load(f)

courses = data['results'][:5]  # 前 5 门

print(f"准备处理 {len(courses)} 门课程...")
for i, c in enumerate(courses):
    print(f"{i+1}. {c['title']}")
    print(f"   链接: {c['lessonUrl']}")
