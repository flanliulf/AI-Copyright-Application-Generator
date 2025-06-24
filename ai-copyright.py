#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI驱动软件著作权申请材料生成系统 - 统一入口脚本
版本: 1.0

这是系统的主入口脚本，提供统一的命令行界面来访问所有功能
"""

import sys
import argparse
import subprocess
from pathlib import Path

class Colors:
    """终端颜色定义"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'

def print_colored(color, message):
    """打印带颜色的消息"""
    print(f"{color}{message}{Colors.NC}")

def print_header():
    """打印系统标题"""
    print_colored(Colors.CYAN, "="*70)
    print_colored(Colors.PURPLE, "🤖 AI驱动软件著作权申请材料生成系统")
    print_colored(Colors.BLUE, "   统一管理工具 v1.0")
    print_colored(Colors.CYAN, "="*70)

def get_script_path():
    """获取脚本根目录"""
    return Path(__file__).parent.absolute()

def run_command(command, description="执行命令"):
    """运行命令并返回结果"""
    print_colored(Colors.BLUE, f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=False, text=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print_colored(Colors.RED, f"❌ 命令执行失败: {e}")
        return False

def init_project(args):
    """初始化新项目"""
    script_path = get_script_path() / "scripts" / "init" / "init_project.py"
    
    if not args.name:
        print_colored(Colors.RED, "❌ 请提供项目名称")
        print("用法: ai-copyright.py init <项目名称>")
        return False
    
    cmd = f"python3 {script_path} {args.name}"
    if args.force:
        cmd += " --force"
    
    return run_command(cmd, f"初始化项目 '{args.name}'")

def generate_code(args):
    """生成源代码"""
    script_path = get_script_path() / "scripts" / "generators"
    
    if args.type == "all":
        script = script_path / "generate_all_sourcecode.py"
        desc = "生成所有源代码"
    elif args.type == "frontend":
        script = script_path / "generate_frontend_sourcecode.py"
        desc = "生成前端源代码"
    elif args.type == "backend":
        script = script_path / "generate_backend_sourcecode.py"
        desc = "生成后端源代码"
    else:
        print_colored(Colors.RED, "❌ 无效的生成类型")
        return False
    
    return run_command(f"python3 {script}", desc)

def check_project(args):
    """检查项目"""
    script_path = get_script_path() / "scripts" / "validators" / "check_project.py"
    
    cmd = f"python3 {script_path}"
    if args.quick:
        cmd += " --quick"
    if args.path:
        cmd += f" {args.path}"
    
    return run_command(cmd, "检查项目完整性")

def run_tests(args):
    """运行测试"""
    script_path = get_script_path() / "scripts" / "validators" / "run_tests.py"
    
    cmd = f"python3 {script_path}"
    if args.path:
        cmd += f" {args.path}"
    
    return run_command(cmd, "运行自动化测试")

def validate_frontend(_args):
    """验证前端页面"""
    script_path = get_script_path() / "scripts" / "validators" / "validate_frontend_pages.py"
    
    return run_command(f"python3 {script_path}", "验证前端页面完整性")

def show_status(_args):
    """显示项目状态"""
    print_colored(Colors.CYAN, "\n📊 项目状态概览")
    print("-" * 50)
    
    # 检查配置文件
    config_file = get_script_path() / "ai-copyright-config.json"
    template_file = get_script_path() / "config" / "ai-copyright-config.example.json"
    
    if config_file.exists():
        print_colored(Colors.GREEN, "✅ 项目配置文件存在")
    elif template_file.exists():
        print_colored(Colors.YELLOW, "⚠️  使用模板配置文件，请复制并自定义")
        print(f"   cp {template_file} {config_file}")
    else:
        print_colored(Colors.RED, "❌ 配置文件缺失")
    
    # 检查关键目录
    dirs_to_check = [
        ("requires_docs", "输入文档目录"),
        ("output_docs", "输出文档目录"),
        ("output_sourcecode", "生成代码目录"),
        ("specs_docs", "规范文档目录"),
        ("system_prompts", "AI提示词目录")
    ]
    
    for dir_name, desc in dirs_to_check:
        dir_path = get_script_path() / dir_name
        if dir_path.exists():
            print_colored(Colors.GREEN, f"✅ {desc} 存在")
        else:
            print_colored(Colors.RED, f"❌ {desc} 缺失")
    
    return True

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='AI驱动软件著作权申请材料生成系统 - 统一管理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s init "我的项目"              # 初始化新项目
  %(prog)s generate all               # 生成所有源代码
  %(prog)s generate frontend          # 生成前端代码
  %(prog)s check --quick              # 快速检查项目
  %(prog)s test                       # 运行自动化测试
  %(prog)s validate-frontend          # 验证前端页面
  %(prog)s status                     # 显示项目状态
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # init 命令
    init_parser = subparsers.add_parser('init', help='初始化新项目')
    init_parser.add_argument('name', help='项目名称')
    init_parser.add_argument('--force', '-f', action='store_true', help='强制覆盖现有目录')
    
    # generate 命令
    gen_parser = subparsers.add_parser('generate', help='生成源代码')
    gen_parser.add_argument('type', choices=['all', 'frontend', 'backend'], 
                           help='生成类型')
    
    # check 命令
    check_parser = subparsers.add_parser('check', help='检查项目完整性')
    check_parser.add_argument('--quick', '-q', action='store_true', help='快速检查')
    check_parser.add_argument('path', nargs='?', help='项目路径')
    
    # test 命令
    test_parser = subparsers.add_parser('test', help='运行自动化测试')
    test_parser.add_argument('path', nargs='?', help='项目路径')
    
    # validate-frontend 命令
    subparsers.add_parser('validate-frontend', help='验证前端页面完整性')
    
    # status 命令
    subparsers.add_parser('status', help='显示项目状态')
    
    args = parser.parse_args()
    
    print_header()
    
    if not args.command:
        print_colored(Colors.YELLOW, "\n⚠️  未指定命令，显示帮助信息:")
        parser.print_help()
        return 0
    
    # 执行对应命令
    command_map = {
        'init': init_project,
        'generate': generate_code,
        'check': check_project,
        'test': run_tests,
        'validate-frontend': validate_frontend,
        'status': show_status
    }
    
    func = command_map.get(args.command)
    if func:
        success = func(args)
        if success:
            print_colored(Colors.GREEN, f"\n✅ 命令 '{args.command}' 执行成功")
        else:
            print_colored(Colors.RED, f"\n❌ 命令 '{args.command}' 执行失败")
        return 0 if success else 1
    else:
        print_colored(Colors.RED, f"❌ 未知命令: {args.command}")
        return 1

if __name__ == "__main__":
    sys.exit(main())