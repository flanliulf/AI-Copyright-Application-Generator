#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一源代码文档生成脚本
一次性生成前端、后端和数据库的所有源代码文档
"""

import os
import subprocess
import sys
from datetime import datetime

def run_script(script_name, description):
    """
    运行指定的脚本
    """
    print(f"\n{'='*60}")
    print(f"正在执行: {description}")
    print(f"脚本: {script_name}")
    print(f"{'='*60}")
    
    try:
        # 检查脚本是否存在
        if not os.path.exists(script_name):
            print(f"❌ 错误：脚本文件不存在 {script_name}")
            return False
        
        # 运行脚本
        result = subprocess.run([sys.executable, script_name], 
                               capture_output=True, 
                               text=True, 
                               encoding='utf-8')
        
        if result.returncode == 0:
            print(result.stdout)
            print(f"✅ {description} 执行成功！")
            return True
        else:
            print(f"❌ {description} 执行失败！")
            print("错误信息:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 执行 {description} 时出错: {e}")
        return False

def main():
    """
    主函数
    """
    print("="*80)
    print("统一源代码文档生成脚本")
    print("="*80)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 定义要执行的脚本
    scripts = [
        ("generate_frontend_sourcecode.py", "前端源代码文档生成"),
        ("generate_backend_sourcecode.py", "后端源代码文档生成"),
    ]
    
    success_count = 0
    total_count = len(scripts)
    
    # 逐个执行脚本
    for script_name, description in scripts:
        if run_script(script_name, description):
            success_count += 1
    
    # 输出总结
    print(f"\n{'='*80}")
    print("执行总结")
    print(f"{'='*80}")
    print(f"总脚本数: {total_count}")
    print(f"成功执行: {success_count}")
    print(f"失败数量: {total_count - success_count}")
    print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if success_count == total_count:
        print("\n🎉 所有源代码文档生成完成！")
        print("\n📁 生成的文档:")
        print("  - output_docs/前端源代码.txt")
        print("  - output_docs/后端源代码.txt")
        print("\n💡 注意：数据库代码.txt 需要通过系统提示词在AI生成阶段直接创建")
        return 0
    else:
        print(f"\n⚠️  有 {total_count - success_count} 个脚本执行失败，请检查错误信息")
        return 1

if __name__ == "__main__":
    exit(main())