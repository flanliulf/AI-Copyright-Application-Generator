#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前端页面完整性验证脚本
检查页面清单中定义的所有页面是否都已生成，并验证页面代码的完整性

注意：验证时会考虑CSS处理策略
- 原始HTML文件应包含完整的CSS样式
- 拼接后的文档会移除CSS，只保留HTML结构和JavaScript
- 验证会检查CSS省略标记的存在
"""

import os
import json
import re
from pathlib import Path

class Colors:
    """终端颜色定义"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color

def print_colored(color, message):
    """打印带颜色的消息"""
    print(f"{color}{message}{Colors.NC}")

def print_success(message):
    print_colored(Colors.GREEN, f"✅ {message}")

def print_warning(message):
    print_colored(Colors.YELLOW, f"⚠️  {message}")

def print_error(message):
    print_colored(Colors.RED, f"❌ {message}")

def print_info(message):
    print_colored(Colors.BLUE, f"ℹ️  {message}")

def extract_pages_from_page_list(page_list_file):
    """从页面清单文档中提取页面列表"""
    if not os.path.exists(page_list_file):
        print_error(f"页面清单文件不存在: {page_list_file}")
        return []
    
    try:
        with open(page_list_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取页面信息的正则表达式模式
        patterns = [
            r'(\d+)\.\s*(.+?)\.html',  # 匹配 "1. login.html"
            r'`(.+?)\.html`',          # 匹配 "`login.html`"
            r'(\w+)\.html',            # 匹配 "login.html"
        ]
        
        pages = set()
        for pattern in patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            for match in matches:
                if isinstance(match, tuple):
                    page_name = match[-1] if len(match) > 1 else match[0]
                else:
                    page_name = match
                
                if page_name and not page_name.isdigit():
                    pages.add(f"{page_name}.html")
        
        return sorted(list(pages))
        
    except Exception as e:
        print_error(f"读取页面清单文件失败: {e}")
        return []

def check_html_completeness(html_file):
    """检查HTML文件的完整性"""
    issues = []
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查基本HTML结构
        if not re.search(r'<!DOCTYPE\s+html>', content, re.IGNORECASE):
            issues.append("缺少 DOCTYPE 声明")
        
        if not re.search(r'<html[^>]*>', content, re.IGNORECASE):
            issues.append("缺少 <html> 标签")
        
        if not re.search(r'<head[^>]*>.*</head>', content, re.IGNORECASE | re.DOTALL):
            issues.append("缺少完整的 <head> 部分")
        
        if not re.search(r'<body[^>]*>.*</body>', content, re.IGNORECASE | re.DOTALL):
            issues.append("缺少完整的 <body> 部分")
        
        # 检查CSS样式（原始HTML文件应该包含CSS，拼接后的文档会移除CSS）
        has_css = (
            re.search(r'<style[^>]*>.*</style>', content, re.IGNORECASE | re.DOTALL) or
            re.search(r'<link[^>]*stylesheet[^>]*>', content, re.IGNORECASE) or
            re.search(r'<!-- CSS.*已省略', content, re.IGNORECASE)  # 检查CSS省略标记
        )
        if not has_css:
            issues.append("缺少CSS样式或CSS省略标记")
        
        # 检查文件大小（过小可能不完整）
        file_size = os.path.getsize(html_file)
        if file_size < 1024:  # 小于1KB
            issues.append(f"文件过小 ({file_size} bytes)，可能不完整")
        
        # 检查是否包含省略标记
        omission_patterns = [
            r'此处省略',
            r'代码较长.*省略',
            r'其余.*类似',
            r'\[注：.*省略.*\]',
            r'<!-- 省略 -->',
            r'省略其余',
        ]
        
        for pattern in omission_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append(f"发现省略标记: {pattern}")
        
        return issues
        
    except Exception as e:
        return [f"无法读取文件: {e}"]

def validate_frontend_pages():
    """验证前端页面完整性"""
    print_colored(Colors.PURPLE, "🔍 前端页面完整性验证")
    print_colored(Colors.BLUE, "=" * 60)
    
    # 获取项目路径
    base_dir = Path(__file__).parent
    page_list_file = base_dir / "process_docs" / "页面清单.md"
    front_dir = base_dir / "output_sourcecode" / "front"
    output_file = base_dir / "output_docs" / "前端源代码.txt"
    
    print_info(f"检查目录: {base_dir}")
    print_info(f"页面清单: {page_list_file}")
    print_info(f"前端目录: {front_dir}")
    print()
    
    # 步骤1: 提取页面清单
    print_colored(Colors.CYAN, "📋 步骤1: 分析页面清单")
    expected_pages = extract_pages_from_page_list(page_list_file)
    
    if not expected_pages:
        print_warning("无法从页面清单中提取页面信息，尝试扫描前端目录...")
        if front_dir.exists():
            expected_pages = [f.name for f in front_dir.glob("*.html")]
        else:
            print_error("前端目录不存在且无法提取页面清单")
            return
    
    print_info(f"预期页面数量: {len(expected_pages)}")
    for page in expected_pages:
        print(f"  - {page}")
    print()
    
    # 步骤2: 检查文件存在性
    print_colored(Colors.CYAN, "📁 步骤2: 检查文件存在性")
    missing_pages = []
    existing_pages = []
    
    if not front_dir.exists():
        print_error(f"前端目录不存在: {front_dir}")
        return
    
    for page in expected_pages:
        page_file = front_dir / page
        if page_file.exists():
            existing_pages.append(page)
            print_success(f"文件存在: {page}")
        else:
            missing_pages.append(page)
            print_error(f"文件缺失: {page}")
    
    print()
    
    # 步骤3: 检查文件完整性
    print_colored(Colors.CYAN, "🔍 步骤3: 检查文件完整性")
    incomplete_pages = []
    
    for page in existing_pages:
        page_file = front_dir / page
        issues = check_html_completeness(page_file)
        
        if issues:
            incomplete_pages.append((page, issues))
            print_warning(f"文件不完整: {page}")
            for issue in issues:
                print(f"    - {issue}")
        else:
            print_success(f"文件完整: {page}")
    
    print()
    
    # 步骤4: 检查汇总文档
    print_colored(Colors.CYAN, "📄 步骤4: 检查汇总文档")
    
    if output_file.exists():
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                doc_content = f.read()
            
            file_size = os.path.getsize(output_file)
            if file_size > 1024 * 1024:
                size_str = f"{file_size / (1024 * 1024):.2f} MB"
            elif file_size > 1024:
                size_str = f"{file_size / 1024:.2f} KB"
            else:
                size_str = f"{file_size} bytes"
            
            print_success(f"汇总文档存在: {output_file}")
            print_info(f"文档大小: {size_str}")
            
            # 检查汇总文档中的页面数量
            page_separators = re.findall(r'=== (.+?\.html) ===', doc_content)
            print_info(f"汇总文档包含页面: {len(page_separators)}")
            
            # 检查是否有省略标记
            omission_found = re.search(r'此处省略|代码较长.*省略|其余.*类似|\[注：.*省略.*\]', doc_content, re.IGNORECASE)
            if omission_found:
                print_error(f"汇总文档包含省略标记: {omission_found.group()}")
            else:
                print_success("汇总文档无省略标记")
                
        except Exception as e:
            print_error(f"读取汇总文档失败: {e}")
    else:
        print_warning(f"汇总文档不存在: {output_file}")
        print_info("可以运行 python3 generate_frontend_sourcecode.py 生成")
    
    print()
    
    # 生成验证报告
    print_colored(Colors.CYAN, "📊 验证报告汇总")
    print("=" * 60)
    
    total_pages = len(expected_pages)
    existing_count = len(existing_pages)
    complete_count = existing_count - len(incomplete_pages)
    
    print(f"📋 预期页面数量: {total_pages}")
    print(f"📁 已生成页面数量: {existing_count}")
    print(f"✅ 完整页面数量: {complete_count}")
    print(f"❌ 缺失页面数量: {len(missing_pages)}")
    print(f"⚠️  不完整页面数量: {len(incomplete_pages)}")
    
    if total_pages > 0:
        completion_rate = (complete_count / total_pages) * 100
        print(f"💯 完成率: {completion_rate:.1f}%")
    
    print()
    
    # 问题总结
    if missing_pages or incomplete_pages:
        print_colored(Colors.RED, "🔧 需要修复的问题:")
        
        if missing_pages:
            print_error("缺失的页面:")
            for page in missing_pages:
                print(f"  - {page}")
        
        if incomplete_pages:
            print_warning("不完整的页面:")
            for page, issues in incomplete_pages:
                print(f"  - {page}:")
                for issue in issues:
                    print(f"    * {issue}")
        
        print()
        print_info("建议操作:")
        print("1. 检查页面清单是否正确定义了所有页面")
        print("2. 重新使用AI生成缺失或不完整的页面")
        print("3. 确保AI生成时遵循完整性要求")
        print("4. 运行 python3 generate_frontend_sourcecode.py 重新生成汇总文档")
    else:
        print_colored(Colors.GREEN, "🎉 所有页面验证通过！前端代码生成完整。")
    
    return len(missing_pages) + len(incomplete_pages)

def main():
    """主函数"""
    try:
        issues_count = validate_frontend_pages()
        return 0 if issues_count == 0 else 1
    except Exception as e:
        print_error(f"验证过程中发生错误: {e}")
        return 2

if __name__ == "__main__":
    exit(main())