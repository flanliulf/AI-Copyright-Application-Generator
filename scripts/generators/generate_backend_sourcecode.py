#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
后端源代码拼接脚本
将 output_sourcecode/backend/ 目录下所有Java文件及配置文件内容拼接生成统一的后端源代码文档
输出纯源代码内容，不包含额外说明
"""

import os
import glob
from datetime import datetime

def get_file_type_priority(file_path):
    """
    获取文件类型优先级，用于排序
    """
    if file_path.endswith('pom.xml'):
        return 1
    elif file_path.endswith('.yml') or file_path.endswith('.yaml'):
        return 2
    elif file_path.endswith('.properties'):
        return 3
    elif file_path.endswith('Application.java'):
        return 4
    elif 'entity' in file_path.lower():
        return 5
    elif 'mapper' in file_path.lower():
        return 6
    elif 'service' in file_path.lower():
        return 7
    elif 'controller' in file_path.lower():
        return 8
    elif 'dto' in file_path.lower():
        return 9
    elif 'vo' in file_path.lower():
        return 10
    elif 'config' in file_path.lower():
        return 11
    elif 'util' in file_path.lower():
        return 12
    else:
        return 13

def extract_backend_files(backend_dir):
    """
    提取后端目录中的所有源代码文件
    """
    file_patterns = [
        '**/*.java',
        '**/*.xml',
        '**/*.yml',
        '**/*.yaml',
        '**/*.properties',
        '**/*.sql'
    ]
    
    all_files = []
    if os.path.exists(backend_dir):
        for pattern in file_patterns:
            files = glob.glob(os.path.join(backend_dir, pattern), recursive=True)
            all_files.extend(files)
    
    # 过滤掉一些不需要的文件
    excluded_patterns = [
        'target/',
        '.class',
        'test/',
        'Test.java',
        '.git/',
        'node_modules/'
    ]
    
    filtered_files = []
    for file_path in all_files:
        should_exclude = False
        for pattern in excluded_patterns:
            if pattern in file_path:
                should_exclude = True
                break
        if not should_exclude:
            filtered_files.append(file_path)
    
    # 按照文件类型和路径排序
    filtered_files.sort(key=lambda x: (get_file_type_priority(x), x))
    
    return filtered_files

def get_relative_path(file_path, backend_dir):
    """
    获取相对于backend目录的路径
    """
    return os.path.relpath(file_path, backend_dir)

def generate_backend_sourcecode():
    """
    生成后端源代码文档
    """
    # 定义路径
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 回到项目根目录
    backend_dir = os.path.join(base_dir, 'output_sourcecode', 'backend')
    output_dir = os.path.join(base_dir, 'output_docs')
    output_file = os.path.join(output_dir, '后端源代码.txt')
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取所有后端文件
    backend_files = extract_backend_files(backend_dir)
    
    if not backend_files:
        print(f"错误：在 {backend_dir} 目录下没有找到后端源代码文件")
        return
    
    print(f"找到 {len(backend_files)} 个后端源代码文件:")
    for file_path in backend_files:
        rel_path = get_relative_path(file_path, backend_dir)
        print(f"  - {rel_path}")
    
    # 开始生成文档
    print("开始生成后端源代码文档...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # 处理每个源代码文件
        for i, file_path in enumerate(backend_files, 1):
            rel_path = get_relative_path(file_path, backend_dir)
            
            print(f"处理文件 {i}/{len(backend_files)}: {rel_path}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as source_f:
                    file_content = source_f.read()
                
                # 写入文件分隔标识和源代码
                f.write(f"=== {rel_path} ===\n")
                f.write(file_content)
                f.write("\n\n")
                
            except Exception as e:
                print(f"处理文件 {rel_path} 时出错: {e}")
                f.write(f"=== {rel_path} ===\n")
                f.write(f"错误：无法读取文件内容 - {e}\n\n")
    
    print(f"✅ 后端源代码文档生成完成！")
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
    print("后端源代码拼接脚本")
    print("=" * 60)
    
    try:
        generate_backend_sourcecode()
    except Exception as e:
        print(f"❌ 脚本执行失败: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())