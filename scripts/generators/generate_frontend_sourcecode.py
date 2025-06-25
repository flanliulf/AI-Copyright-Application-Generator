#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前端源代码拼接脚本
将 output_sourcecode/front/ 目录下所有HTML文件内容拼接生成统一的前端源代码文档

CSS处理策略：
- 彻底移除 <style> 标签及其内容
- 移除 CSS 外部链接 (rel="stylesheet")  
- 移除内联样式属性 (style="...")
- 保留HTML结构和JavaScript逻辑
- 保留class属性（可能对JavaScript功能重要）

这样可以显著减少文档长度，突出核心程序逻辑，更适合软著申请材料要求
"""

import os
import re
import math

def remove_css_content(html_content):
    """
    彻底移除HTML中的CSS样式内容，只保留HTML结构和JavaScript逻辑
    """
    # 移除 <style> 标签及其内容
    html_content = re.sub(r'<style[^>]*>.*?</style>', 
                         '\n    <!-- CSS样式已省略，完整CSS请查看原始HTML文件 -->\n', 
                         html_content, flags=re.DOTALL)
    
    # 移除CSS外部链接（保留JavaScript和字体链接）
    html_content = re.sub(r'<link[^>]*rel=["\']stylesheet["\'][^>]*>', 
                         '    <!-- CSS外部链接已省略 -->', 
                         html_content, flags=re.IGNORECASE)
    
    # 移除内联样式属性
    html_content = re.sub(r'\s+style=["\'][^"\']*["\']', '', html_content)
    
    # 移除CSS相关的class属性（可选，保留功能性class）
    # 这里我们保留class属性，因为它们可能对JavaScript功能重要
    
    return html_content

def estimate_tokens(text):
    """
    估算文本的token数量 (粗略估算：1 token ≈ 4 个字符)
    """
    return len(text) // 4

def split_content_by_token_limit(html_files, front_dir, max_tokens=30000):
    """
    根据token限制智能分批HTML文件
    """
    batches = []
    current_batch = []
    current_tokens = 0
    
    for html_file in html_files:
        file_path = os.path.join(front_dir, html_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 移除CSS后估算token数
            clean_content = remove_css_content(content)
            file_tokens = estimate_tokens(clean_content)
            
            # 如果单个文件就超过限制，需要进一步处理
            if file_tokens > max_tokens:
                # 如果当前批次不为空，先保存
                if current_batch:
                    batches.append(current_batch)
                    current_batch = []
                    current_tokens = 0
                
                # 将大文件单独作为一个批次（或进一步拆分）
                batches.append([html_file])
                print(f"⚠️  文件 {html_file} 较大 (~{file_tokens} tokens)，单独处理")
                continue
            
            # 检查加入当前文件后是否超限
            if current_tokens + file_tokens > max_tokens and current_batch:
                # 保存当前批次，开始新批次
                batches.append(current_batch)
                current_batch = [html_file]
                current_tokens = file_tokens
            else:
                # 加入当前批次
                current_batch.append(html_file)
                current_tokens += file_tokens
                
        except Exception as e:
            print(f"⚠️  读取文件 {html_file} 时出错: {e}")
            current_batch.append(html_file)  # 仍然加入批次，稍后处理
    
    # 保存最后一个批次
    if current_batch:
        batches.append(current_batch)
    
    return batches

def compress_html_content(html_content, compression_level=1):
    """
    进一步压缩HTML内容以减少token数量
    
    compression_level:
    1 - 轻度压缩：移除多余空白，保留结构
    2 - 中度压缩：移除注释，简化标签
    3 - 重度压缩：只保留核心结构和JavaScript
    """
    if compression_level >= 1:
        # 移除多余的空白和换行
        html_content = re.sub(r'\n\s*\n', '\n', html_content)  # 移除空行
        html_content = re.sub(r'^\s+', '', html_content, flags=re.MULTILINE)  # 移除行首空白
        
    if compression_level >= 2:
        # 移除HTML注释
        html_content = re.sub(r'<!--[^>]*-->', '', html_content, flags=re.DOTALL)
        # 移除多余的标签属性（保留重要的id, class, onclick等）
        # 这里可以根据需要进一步定制
        
    if compression_level >= 3:
        # 重度压缩：只保留核心结构
        # 移除大部分非功能性内容，只保留关键的DOM结构和JavaScript
        html_content = re.sub(r'<meta[^>]*>', '', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'<link[^>]*>', '', html_content, flags=re.IGNORECASE) 
        
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
    # 定义路径 (脚本移动到子目录后需要调整相对路径)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 回到项目根目录
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
    
    # 智能分批处理以避免token超限
    print("\n🔍 分析文件大小并智能分批...")
    batches = split_content_by_token_limit(html_files, front_dir, max_tokens=25000)
    
    print(f"📊 将生成 {len(batches)} 个文档文件:")
    for i, batch in enumerate(batches, 1):
        print(f"  批次 {i}: {len(batch)} 个文件")
    
    
    # 开始生成文档
    print("\n🚀 开始生成前端源代码文档...")
    
    generated_files = []
    
    for batch_idx, batch in enumerate(batches, 1):
        # 为每个批次生成单独的文件
        if len(batches) == 1:
            batch_output_file = output_file
        else:
            batch_output_file = output_file.replace('.txt', f'_part{batch_idx}.txt')
        
        generated_files.append(batch_output_file)
        
        print(f"\n📝 生成批次 {batch_idx}/{len(batches)} ({len(batch)} 个文件)")
        
        with open(batch_output_file, 'w', encoding='utf-8') as f:
            # 写入批次说明头部
            if len(batches) > 1:
                f.write(f"前端源代码文档 - 第 {batch_idx} 部分\n")
                f.write(f"包含文件: {', '.join(batch)}\n")
                f.write(f"生成时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'='*80}\n\n")
            
            total_tokens = 0
            
            # 处理当前批次的每个HTML文件
            for i, html_file in enumerate(batch, 1):
                file_path = os.path.join(front_dir, html_file)
                
                print(f"  处理文件 {i}/{len(batch)}: {html_file}")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as html_f:
                        html_content = html_f.read()
                    
                    # 移除CSS内容
                    html_content = remove_css_content(html_content)
                    
                    # 如果内容仍然过大，进行压缩
                    file_tokens = estimate_tokens(html_content)
                    if file_tokens > 15000:  # 单文件超过15K tokens时压缩
                        print(f"    ⚠️  文件较大，应用压缩 (~{file_tokens} tokens)")
                        html_content = compress_html_content(html_content, compression_level=2)
                        file_tokens = estimate_tokens(html_content)
                        print(f"    ✅ 压缩后 ~{file_tokens} tokens")
                    
                    total_tokens += file_tokens
                    
                    # 写入文件分隔标识和源代码
                    f.write(f"=== {html_file} ===\n")
                    f.write(html_content)
                    f.write("\n\n")
                    
                except Exception as e:
                    print(f"    ❌ 处理文件 {html_file} 时出错: {e}")
                    f.write(f"=== {html_file} ===\n")
                    f.write(f"错误：无法读取文件内容 - {e}\n\n")
            
            print(f"  📊 批次 {batch_idx} 预估token数: ~{total_tokens}")
    
    print(f"\n✅ 前端源代码文档生成完成！")
    if len(generated_files) == 1:
        print(f"📁 输出文件: {generated_files[0]}")
    else:
        print(f"📁 输出文件 ({len(generated_files)} 个):")
        for i, file_path in enumerate(generated_files, 1):
            print(f"  {i}. {file_path}")
    
    # 显示文件大小统计
    total_size = 0
    print(f"\n📊 文件大小统计:")
    try:
        for i, file_path in enumerate(generated_files, 1):
            file_size = os.path.getsize(file_path)
            total_size += file_size
            
            if file_size > 1024 * 1024:
                size_str = f"{file_size / (1024 * 1024):.2f} MB"
            elif file_size > 1024:
                size_str = f"{file_size / 1024:.2f} KB"
            else:
                size_str = f"{file_size} bytes"
            
            if len(generated_files) > 1:
                print(f"  Part {i}: {size_str}")
            else:
                print(f"  总大小: {size_str}")
        
        if len(generated_files) > 1:
            if total_size > 1024 * 1024:
                total_str = f"{total_size / (1024 * 1024):.2f} MB"
            elif total_size > 1024:
                total_str = f"{total_size / 1024:.2f} KB"
            else:
                total_str = f"{total_size} bytes"
            print(f"  📊 总计: {total_str}")
            
    except Exception as e:
        print(f"  ⚠️  无法获取文件大小: {e}")
    
    # 智能建议
    if len(generated_files) > 1:
        print(f"\n💡 建议:")
        print(f"  • 生成了 {len(generated_files)} 个分段文件以避免token超限")
        print(f"  • 在AI对话中可以分批次粘贴每个文件内容")
        print(f"  • 或者选择最重要的几个页面单独处理")

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