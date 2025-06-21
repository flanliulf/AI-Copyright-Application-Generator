#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前端源代码拼接脚本
将 output_sourcecode/front/ 目录下所有HTML文件内容拼接生成统一的前端源代码文档
省略CSS内容以减少文档长度，保留核心HTML结构和JavaScript逻辑
"""

import os
import re
from datetime import datetime

def remove_css_content(html_content):
    """
    移除HTML中的CSS样式内容，保留其他部分
    """
    # 移除 <style> 标签及其内容
    html_content = re.sub(r'<style[^>]*>.*?</style>', '    <!-- CSS样式已省略 -->', html_content, flags=re.DOTALL)
    
    # 移除内联样式属性（可选，保留一些简单的样式）
    # html_content = re.sub(r'\s+style="[^"]*"', '', html_content)
    
    return html_content

def extract_html_files(front_dir):
    """
    提取前端目录中的所有HTML文件
    """
    html_files = []
    if os.path.exists(front_dir):
        for file in os.listdir(front_dir):
            if file.endswith('.html'):
                html_files.append(file)
    
    # 按文件名排序
    html_files.sort()
    return html_files

def generate_frontend_sourcecode():
    """
    生成前端源代码文档
    """
    # 定义路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    front_dir = os.path.join(base_dir, 'output_sourcecode', 'front')
    output_dir = os.path.join(base_dir, 'output_docs')
    output_file = os.path.join(output_dir, '前端源代码.txt')
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取所有HTML文件
    html_files = extract_html_files(front_dir)
    
    if not html_files:
        print(f"错误：在 {front_dir} 目录下没有找到HTML文件")
        return
    
    print(f"找到 {len(html_files)} 个HTML文件:")
    for file in html_files:
        print(f"  - {file}")
    
    # 页面映射（用于生成更友好的标题）
    page_mapping = {
        'login.html': '登录页面',
        'dashboard.html': '仪表盘页面',
        'materials.html': '素材库管理页面',
        'ai-assistant.html': 'AI智能助手页面',
        'users.html': '用户权限管理页面',
        'analytics.html': '数据统计分析页面',
        'wechat-config.html': '企业微信集成配置页面',
        'settings.html': '系统设置页面'
    }
    
    # 开始生成文档
    print("开始生成前端源代码文档...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        
        # 处理每个HTML文件
        for i, html_file in enumerate(html_files, 1):
            file_path = os.path.join(front_dir, html_file)
            page_title = page_mapping.get(html_file, html_file.replace('.html', '页面'))
            
            print(f"处理文件 {i}/{len(html_files)}: {html_file}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as html_f:
                    html_content = html_f.read()
                
                # 移除CSS内容
                html_content = remove_css_content(html_content)
                
                # 写入文件分隔标识和源代码
                f.write(f"=== {html_file} ===\n")
                f.write(html_content)
                f.write("\n\n")
                
            except Exception as e:
                print(f"处理文件 {html_file} 时出错: {e}")
                f.write(f"=== {html_file} ===\n")
                f.write(f"错误：无法读取文件内容 - {e}\n\n")
    
    print(f"✅ 前端源代码文档生成完成！")
    print(f"📁 输出文件: {output_file}")
    
    # 显示文件大小
    try:
        file_size = os.path.getsize(output_file)
        if file_size > 1024 * 1024:
            size_str = f"{file_size / (1024 * 1024):.2f} MB"
        elif file_size > 1024:
            size_str = f"{file_size / 1024:.2f} KB"
        else:
            size_str = f"{file_size} bytes"
        print(f"📊 文件大小: {size_str}")
    except:
        pass

def main():
    """
    主函数
    """
    print("=" * 60)
    print("前端源代码拼接脚本")
    print("=" * 60)
    
    try:
        generate_frontend_sourcecode()
    except Exception as e:
        print(f"❌ 脚本执行失败: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())