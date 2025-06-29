#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
全部源代码软著申请专用拼接脚本 (Python版本)
功能：一键执行前端、后端、数据库所有代码的拼接，并生成完整的申请材料包

特点：
- 一键执行所有合并脚本
- 生成完整的申请材料清单
- 跨平台兼容（Windows/Linux/macOS）
- 智能错误处理和恢复
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# 颜色输出类
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color

def print_success(message: str):
    print(f"{Colors.GREEN}✓ {message}{Colors.NC}")

def print_info(message: str):
    print(f"{Colors.BLUE}ℹ {message}{Colors.NC}")

def print_warning(message: str):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.NC}")

def print_error(message: str):
    print(f"{Colors.RED}✗ {message}{Colors.NC}")

def print_header(message: str):
    print(f"{Colors.PURPLE}{'=' * 80}{Colors.NC}")
    print(f"{Colors.PURPLE}{message.center(80)}{Colors.NC}")
    print(f"{Colors.PURPLE}{'=' * 80}{Colors.NC}")

def get_project_config() -> Optional[dict]:
    """读取项目配置文件"""
    config_file = Path("ai-copyright-config.json")
    if not config_file.exists():
        print_error("配置文件不存在: ai-copyright-config.json")
        return None
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print_error(f"配置文件JSON格式错误: {e}")
        return None
    except Exception as e:
        print_error(f"读取配置文件失败: {e}")
        return None

def run_merge_script(script_name: str, script_path: Path) -> Dict[str, any]:
    """运行单个合并脚本"""
    result = {
        'script': script_name,
        'success': False,
        'output': '',
        'error': '',
        'execution_time': 0
    }
    
    try:
        print_info(f"执行脚本: {script_name}")
        start_time = datetime.now()
        
        # 运行Python脚本
        process = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
            timeout=300  # 5分钟超时
        )
        
        end_time = datetime.now()
        result['execution_time'] = (end_time - start_time).total_seconds()
        result['output'] = process.stdout
        result['error'] = process.stderr
        result['success'] = process.returncode == 0
        
        if result['success']:
            print_success(f"{script_name} 执行成功 (用时: {result['execution_time']:.1f}秒)")
        else:
            print_error(f"{script_name} 执行失败")
            if result['error']:
                print_error(f"错误信息: {result['error']}")
    
    except subprocess.TimeoutExpired:
        print_error(f"{script_name} 执行超时")
        result['error'] = "执行超时"
    except Exception as e:
        print_error(f"{script_name} 执行异常: {e}")
        result['error'] = str(e)
    
    return result

def check_generated_files() -> Dict[str, Dict[str, any]]:
    """检查生成的文件"""
    output_dir = Path("output_docs")
    expected_files = {
        "前端源代码.txt": "前端页面源代码文档",
        "后端源代码.txt": "后端业务逻辑源代码文档", 
        "数据库源代码.txt": "数据库设计和建表语句文档"
    }
    
    file_status = {}
    
    for filename, description in expected_files.items():
        file_path = output_dir / filename
        status = {
            'exists': file_path.exists(),
            'size': 0,
            'size_mb': 0,
            'description': description,
            'path': str(file_path)
        }
        
        if status['exists']:
            try:
                status['size'] = file_path.stat().st_size
                status['size_mb'] = status['size'] / (1024 * 1024)
            except:
                status['size'] = 0
        
        file_status[filename] = status
    
    return file_status

def generate_application_summary(config: dict, file_status: Dict, execution_results: List[Dict]) -> str:
    """生成申请材料总结报告"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    summary = f"""
{'-' * 80}
软件著作权申请材料生成总结报告
{'-' * 80}

项目信息:
- 软件名称: {config.get('title', '未设置')}
- 软件简称: {config.get('short_title', config.get('title', '未设置'))}
- 前端技术: {config.get('front', '未设置')}
- 后端技术: {config.get('backend', '未设置')}
- UI设计风格: {config.get('ui_design_style', '未设置')}
- 生成模式: {config.get('generation_mode', '未设置')}

生成时间: {current_time}

{'-' * 80}
申请材料文档清单
{'-' * 80}

"""
    
    total_size = 0
    total_files = 0
    
    for filename, status in file_status.items():
        if status['exists']:
            summary += f"✓ {filename}\n"
            summary += f"  描述: {status['description']}\n"
            summary += f"  大小: {status['size']:,} 字节 ({status['size_mb']:.2f} MB)\n"
            summary += f"  路径: {status['path']}\n\n"
            total_size += status['size']
            total_files += 1
        else:
            summary += f"✗ {filename} (文件不存在)\n"
            summary += f"  描述: {status['description']}\n\n"
    
    summary += f"总计: {total_files} 个文件，{total_size:,} 字节 ({total_size / (1024 * 1024):.2f} MB)\n\n"
    
    # 执行结果统计
    summary += f"{'-' * 80}\n执行结果统计\n{'-' * 80}\n\n"
    
    success_count = sum(1 for r in execution_results if r['success'])
    total_time = sum(r['execution_time'] for r in execution_results)
    
    summary += f"执行脚本数量: {len(execution_results)}\n"
    summary += f"成功执行: {success_count}\n"
    summary += f"失败执行: {len(execution_results) - success_count}\n"
    summary += f"总执行时间: {total_time:.1f} 秒\n\n"
    
    for result in execution_results:
        status_symbol = "✓" if result['success'] else "✗"
        summary += f"{status_symbol} {result['script']} (用时: {result['execution_time']:.1f}秒)\n"
        if not result['success'] and result['error']:
            summary += f"  错误: {result['error']}\n"
    
    # 申请建议
    summary += f"\n{'-' * 80}\n申请材料使用建议\n{'-' * 80}\n\n"
    
    if total_files == 3:
        summary += "✅ 所有必需的源代码文档已生成完成\n\n"
        summary += "下一步操作:\n"
        summary += "1. 检查各文档内容的完整性和准确性\n"
        summary += "2. 根据需要生成用户手册和软件著作权登记信息表\n"
        summary += "3. 准备其他申请材料（申请表、身份证明等）\n"
        summary += "4. 提交至软件著作权登记机构\n\n"
        
        if total_size > 1024 * 1024:  # 大于1MB
            summary += "📊 文档规模良好，内容充实，有利于申请通过\n"
        else:
            summary += "⚠️  文档规模较小，建议检查内容是否完整\n"
    else:
        summary += "❌ 部分源代码文档生成失败，请检查并重新生成\n\n"
        summary += "故障排除建议:\n"
        summary += "1. 确认 output_sourcecode/ 目录下已生成相应的代码文件\n"
        summary += "2. 检查Python环境和脚本权限\n"
        summary += "3. 查看详细错误信息进行针对性修复\n"
    
    summary += f"\n{'-' * 80}\n报告生成时间: {current_time}\n{'-' * 80}\n"
    
    return summary

def merge_all_sources():
    """执行所有源代码合并"""
    print_header("开始执行完整软著申请材料生成")
    
    # 1. 读取项目配置
    config = get_project_config()
    if not config:
        print_warning("无法读取项目配置，使用默认配置")
        config = {
            'title': '软件系统',
            'short_title': '软件系统',
            'front': 'JavaScript',
            'backend': 'Java',
            'ui_design_style': 'corporate',
            'generation_mode': 'fast'
        }
    
    print_info(f"项目: {config.get('title', '未设置')}")
    print_info(f"技术栈: {config.get('front', '未设置')} + {config.get('backend', '未设置')}")
    print_info(f"生成模式: {config.get('generation_mode', '未设置')}")
    print()
    
    # 2. 定义合并脚本
    script_dir = Path(__file__).parent
    merge_scripts = [
        ("前端代码合并", script_dir / "merge_frontend_simple.py"),
        ("后端代码合并", script_dir / "merge_backend_simple.py"),
        ("数据库代码合并", script_dir / "merge_database_simple.py")
    ]
    
    # 3. 检查脚本存在性
    available_scripts = []
    for name, script_path in merge_scripts:
        if script_path.exists():
            available_scripts.append((name, script_path))
            print_success(f"脚本就绪: {name}")
        else:
            print_warning(f"脚本不存在: {name} ({script_path})")
    
    if not available_scripts:
        print_error("未发现任何合并脚本")
        return False
    
    print()
    
    # 4. 逐个执行合并脚本
    execution_results = []
    
    for i, (name, script_path) in enumerate(available_scripts, 1):
        print_header(f"第 {i}/{len(available_scripts)} 步: {name}")
        result = run_merge_script(name, script_path)
        execution_results.append(result)
        print()
    
    # 5. 检查生成的文件
    print_header("检查生成的申请材料文档")
    file_status = check_generated_files()
    
    for filename, status in file_status.items():
        if status['exists']:
            print_success(f"{filename} - {status['size_mb']:.2f} MB")
        else:
            print_error(f"{filename} - 文件不存在")
    
    print()
    
    # 6. 生成总结报告
    print_info("生成申请材料总结报告...")
    
    output_dir = Path("output_docs")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    summary = generate_application_summary(config, file_status, execution_results)
    
    # 保存总结报告
    summary_file = output_dir / "软著申请材料总结报告.txt"
    try:
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        print_success(f"总结报告已保存: {summary_file}")
    except Exception as e:
        print_error(f"保存总结报告失败: {e}")
    
    # 7. 输出最终结果
    success_count = sum(1 for r in execution_results if r['success'])
    total_scripts = len(execution_results)
    existing_files = sum(1 for s in file_status.values() if s['exists'])
    
    print_header("申请材料生成完成")
    
    if success_count == total_scripts and existing_files == len(file_status):
        print_success("🎉 所有申请材料已成功生成!")
        print_info("📋 请查看 output_docs/ 目录下的所有文档")
        print_info("📄 详细信息请参考: 软著申请材料总结报告.txt")
        return True
    else:
        print_warning(f"⚠️  部分材料生成失败 ({success_count}/{total_scripts} 脚本成功, {existing_files}/{len(file_status)} 文件存在)")
        print_info("🔧 请检查错误信息并重新生成失败的部分")
        return False

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("全部源代码拼接脚本 (Python版本)")
        print("\n用法:")
        print("  python3 merge_all_simple.py")
        print("\n功能:")
        print("  一键执行前端、后端、数据库所有代码的拼接")
        print("  生成完整的软著申请材料包")
        print("\n输出文件:")
        print("  output_docs/前端源代码.txt")
        print("  output_docs/后端源代码.txt")
        print("  output_docs/数据库源代码.txt")
        print("  output_docs/软著申请材料总结报告.txt")
        print("  output_docs/*拼接报告.txt")
        print("\n注意:")
        print("  请确保已生成前端、后端、数据库代码文件")
        print("  运行前请检查 output_sourcecode/ 目录内容")
        return
    
    success = merge_all_sources()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()