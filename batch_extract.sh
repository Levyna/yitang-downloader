#!/bin/bash
# 一堂课程链接批量提取脚本

CHROME_PORT=9222
EXCEL_PATH="/Users/apple/Documents/mycc/2-Projects/P003-YITANG-Downloader/下载追踪表.xlsx"
JSON_PATH="/Users/apple/Documents/mycc/2-Projects/P003-YITANG-Study/004-正式课程/文稿下载清单.json"

echo "开始批量提取课程链接..."
echo "课程总数: 171"

# 使用 Python + Chrome DevTools MCP 批量处理
python3 << PYTHON_SCRIPT
import json
import subprocess
import time

# 读取课程列表
with open('$JSON_PATH', 'r') as f:
    data = json.load(f)
courses = data['results']

print(f"准备处理 {len(courses)} 门课程")

# 检查 Chrome 是否运行
try:
    result = subprocess.run(['lsof', '-i', ':$CHROME_PORT'], capture_output=True)
    if result.returncode != 0:
        print("错误: Chrome 未运行")
        exit(1)
except:
    print("错误: 无法检查 Chrome 状态")
    exit(1)

print("Chrome 已连接，开始处理..."

# TODO: 通过 MCP 批量处理每门课程
# 这里需要实现与 Chrome DevTools MCP 的交互

print("批量处理完成")
PYTHON_SCRIPT
