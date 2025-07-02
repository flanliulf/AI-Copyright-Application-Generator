#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI驱动的企业级软件开发工作流程 - 项目初始化脚本 (安全版本)
版本: 1.1
描述: 自动创建新项目的目录结构和固定文档，修复编码问题
"""

import os
import sys
import json
import shutil
import argparse
import locale
from datetime import datetime
from pathlib import Path

# 设置系统编码环境
def setup_encoding():
    """设置系统编码环境"""
    try:
        # 设置locale为UTF-8
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'C.UTF-8')
        except locale.Error:
            pass  # 忽略locale设置错误
    
    # 确保环境变量支持UTF-8
    os.environ['LANG'] = 'en_US.UTF-8'
    os.environ['LC_ALL'] = 'en_US.UTF-8'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # Windows特殊处理
    if sys.platform.startswith('win'):
        import codecs
        if hasattr(sys.stdout, 'buffer'):
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
        if hasattr(sys.stderr, 'buffer'):
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)

# 初始化编码设置
setup_encoding()

class Colors:
    """终端颜色定义"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def print_message(color, message):
    """打印带颜色的消息"""
    print(f"{color}{message}{Colors.RESET}")

def print_success(message):
    print_message(Colors.GREEN, f"✓ {message}")

def print_info(message):
    print_message(Colors.BLUE, f"ℹ {message}")

def print_warning(message):
    print_message(Colors.YELLOW, f"⚠ {message}")

def print_error(message):
    print_message(Colors.RED, f"✗ {message}")

def safe_input(prompt, default=""):
    """安全的用户输入函数，处理编码问题"""
    try:
        if default:
            full_prompt = f"{prompt} (默认: {default}): "
        else:
            full_prompt = f"{prompt}: "
        
        # 使用bytes处理输入以避免编码问题
        print(full_prompt, end='', flush=True)
        
        # 直接从stdin读取bytes并解码
        if hasattr(sys.stdin, 'buffer'):
            line = sys.stdin.buffer.readline()
            user_input = line.decode('utf-8', errors='replace').strip()
        else:
            user_input = input().strip()
        
        return user_input if user_input else default
        
    except (UnicodeDecodeError, UnicodeError) as e:
        print_error(f"输入编码错误: {e}")
        print_warning("请确保终端支持UTF-8编码")
        return default
    except KeyboardInterrupt:
        print_error("\n用户中断操作")
        sys.exit(1)
    except EOFError:
        print_error("\n输入结束")
        return default
    except Exception as e:
        print_error(f"输入错误: {e}")
        return default

def safe_yes_no_input(prompt, default_no=True):
    """安全的是/否输入函数"""
    try:
        suffix = "(y/N)" if default_no else "(Y/n)"
        response = safe_input(f"{prompt} {suffix}", "").lower()
        
        if default_no:
            return response in ['y', 'yes', '是', '1', 'true']
        else:
            return response not in ['n', 'no', '否', '0', 'false']
    except Exception as e:
        print_error(f"输入处理错误: {e}")
        return not default_no

def get_ui_design_style():
    """获取UI设计风格选择"""
    print_info("请选择UI设计风格 (12种专业设计风格):")
    print_info("专业商务类型:")
    print("  1. 企业商务风格 (Corporate) - 默认推荐")
    print("  2. 包豪斯风格 (Bauhaus) - 功能主义设计")  
    print("  3. 艺术装饰风格 (ArtDeco) - 奢华几何美学")
    print_info("现代科技类型:")
    print("  4. 暗黑科技风格 (Cyberpunk) - 科技感强烈")
    print("  5. 未来科技风格 (Futuristic) - 数字未来美学")
    print("  6. 大胆现代风格 (Bold) - 视觉冲击力强")
    print_info("极简清新类型:")
    print("  7. 极简主义风格 (Minimal) - 简洁专注")
    print("  8. 日式极简风格 (Japanese) - 禅意侘寂")
    print("  9. 斯堪的纳维亚风格 (Scandinavian) - 北欧简约")
    print_info("创意艺术类型:")
    print("  10. 孟菲斯风格 (Memphis) - 后现代叛逆")
    print("  11. 波普艺术风格 (PopArt) - 大众文化美学")
    print("  12. 优雅复古风格 (Elegant) - 经典印刷美学")
    
    styles = [
        ("1", "corporate", "企业商务风格"),
        ("2", "bauhaus", "包豪斯风格"),
        ("3", "artdeco", "艺术装饰风格"),
        ("4", "cyberpunk", "暗黑科技风格"),
        ("5", "futuristic", "未来科技风格"),
        ("6", "bold", "大胆现代风格"),
        ("7", "minimal", "极简主义风格"),
        ("8", "japanese", "日式极简风格"),
        ("9", "scandinavian", "斯堪的纳维亚风格"),
        ("10", "memphis", "孟菲斯风格"),
        ("11", "popart", "波普艺术风格"),
        ("12", "elegant", "优雅复古风格")
    ]
    
    while True:
        choice = safe_input("请输入选择 (1-12)", "1")
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= 12:
                return styles[choice_num - 1][1]  # 返回key
            else:
                print_warning("请输入1-12之间的数字")
        except ValueError:
            print_warning("请输入有效的数字")

def get_generation_mode():
    """获取生成模式"""
    print_info("请选择生成模式:")
    print("  1. fast - 快速验证模式 (5个核心页面)")
    print("  2. full - 完整生产模式 (10个完整页面)")
    
    while True:
        choice = safe_input("请输入选择 (1-2)", "1")
        if choice in ["1", "fast"]:
            return "fast"
        elif choice in ["2", "full"]:
            return "full"
        else:
            print_warning("请输入1或2")

def create_config_file(title, short_title, ui_style, mode, front_tech, backend_tech):
    """创建配置文件"""
    config = {
        "_comment_init": "=== 项目初始化配置（用户设置） ===",
        "front": front_tech,
        "backend": backend_tech,
        "title": title,
        "short_title": short_title,
        "requirements_description": "requires_docs/需求文档.md",
        "dev_tech_stack": "requires_docs/技术栈说明文档.md",
        "ui_design_style": ui_style,
        
        "_comment_fixed": "=== 固定配置（不变） ===",
        "system_prompt_dir": "system_prompts",
        "ui_design_spec_default": f"specs_docs/ui_design_specs/01-UI设计规范_默认_Corporate.md",
        "ui_design_spec": "requires_docs/UI设计规范.md",
        
        "_comment_generation": "=== 生成配置（可调整） ===",
        "page_count_fast": 5,
        "page_count_full": 10,
        "api_count_min": 8,
        "api_count_max": 35,
        "generation_mode": mode,
        
        "_comment_generated": "=== 流程生成配置（自动生成） ===",
        "framework_design": "process_docs/框架设计文档.md",
        "page_list": "process_docs/页面清单.md",
        "database_schema": "output_sourcecode/db/database_schema.sql",
        "copyright_application": "output_docs/软件著作权登记信息表.md"
    }
    
    try:
        with open("ai-copyright-config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print_success("配置文件创建完成: ai-copyright-config.json")
        return True
    except Exception as e:
        print_error(f"创建配置文件失败: {e}")
        return False

def create_directories():
    """创建项目目录结构"""
    dirs = [
        "requires_docs",
        "process_docs", 
        "output_docs",
        "output_sourcecode/front",
        "output_sourcecode/backend",
        "output_sourcecode/db"
    ]
    
    for dir_path in dirs:
        try:
            os.makedirs(dir_path, exist_ok=True)
            print_success(f"创建目录: {dir_path}")
        except Exception as e:
            print_error(f"创建目录失败 {dir_path}: {e}")

def main():
    """主函数"""
    print_message(Colors.BOLD + Colors.CYAN, "🚀 AI驱动的软件著作权申请材料生成系统 - 项目初始化")
    print_message(Colors.CYAN, "=" * 70)
    
    try:
        # 获取项目信息
        print_info("请输入项目配置信息:")
        
        system_title = safe_input("系统完整名称", "我的软件系统")
        if not system_title:
            system_title = "我的软件系统"
            
        short_title = safe_input("系统简称", system_title[:10] if len(system_title) > 10 else system_title)
        if not short_title:
            short_title = system_title[:10] if len(system_title) > 10 else system_title
        
        # 获取技术选择
        print_info("请选择技术栈:")
        front_tech = safe_input("前端技术 (vue/react/angular)", "vue")
        if not front_tech:
            front_tech = "vue"
            
        backend_tech = safe_input("后端技术 (java/nodejs/python)", "java")
        if not backend_tech:
            backend_tech = "java"
        
        # 获取UI风格
        ui_style = get_ui_design_style()
        
        # 获取生成模式
        mode = get_generation_mode()
        
        # 确认信息
        print_info("项目配置信息确认:")
        print(f"  系统名称: {system_title}")
        print(f"  系统简称: {short_title}")
        print(f"  前端技术: {front_tech}")
        print(f"  后端技术: {backend_tech}")
        print(f"  UI风格: {ui_style}")
        print(f"  生成模式: {mode}")
        
        if not safe_yes_no_input("确认以上信息是否正确?", default_no=False):
            print_warning("用户取消操作")
            return
        
        # 创建目录结构
        print_info("创建项目目录结构...")
        create_directories()
        
        # 创建配置文件
        print_info("创建项目配置文件...")
        if create_config_file(system_title, short_title, ui_style, mode, front_tech, backend_tech):
            print_success("项目初始化完成!")
            print_info("下一步请:")
            print("  1. 编辑 requires_docs/需求文档.md 文件")
            print("  2. 运行质量检查: python3 scripts/validators/check_project.py --quick")
        else:
            print_error("项目初始化失败")
            
    except Exception as e:
        print_error(f"初始化过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()