#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
前端页面源代码软著申请专用拼接脚本 (Python版本)
功能：将所有前端HTML文件完整拼接成单一文档，专用于软件著作权申请材料

与现有generate_frontend_sourcecode.py的差异：
- 现有脚本：分批生成，适用于AI对话（避免token超限）
- 本脚本：  单文件生成，适用于软著申请（便于提交）

优点：
- 生成单一完整文档，符合软著申请要求
- 保持源代码完整性，无压缩或分批
- 零token消耗，纯本地文本处理
- 直接可用于软著申请提交
- 跨平台兼容（Windows/Linux/macOS）
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional

# 颜色输出类
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_success(message: str):
    print(f"{Colors.GREEN}✓ {message}{Colors.NC}")

def print_info(message: str):
    print(f"{Colors.BLUE}ℹ {message}{Colors.NC}")

def print_warning(message: str):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.NC}")

def print_error(message: str):
    print(f"{Colors.RED}✗ {message}{Colors.NC}")

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

def collect_html_files(front_dir: Path) -> List[Path]:
    """收集所有HTML文件并排序"""
    if not front_dir.exists():
        return []
    
    html_files = []
    for file_path in front_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() == '.html':
            html_files.append(file_path)
    
    # 按文件名排序，确保一致的输出顺序
    html_files.sort(key=lambda x: x.name.lower())
    return html_files

def read_html_file(file_path: Path) -> str:
    """安全读取HTML文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # 尝试其他编码
        try:
            with open(file_path, 'r', encoding='gb2312') as f:
                return f.read()
        except:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                print_warning(f"无法读取文件 {file_path.name}: {e}")
                return f"<!-- 文件读取失败: {file_path.name} -->"

def generate_header(config: dict, file_count: int) -> str:
    """生成文档头部信息"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    header = f"""
{'-' * 80}
软件著作权申请材料 - 前端源代码文档
{'-' * 80}

软件名称: {config.get('title', '未设置')}
软件简称: {config.get('short_title', config.get('title', '未设置'))}
前端技术: {config.get('front', '未设置')}
UI设计风格: {config.get('ui_design_style', '未设置')}
生成模式: {config.get('generation_mode', '未设置')}

文档生成信息:
- 生成时间: {current_time}
- 页面文件数量: {file_count}
- 文档类型: 前端页面完整源代码
- 编码格式: UTF-8

{'-' * 80}
"""
    return header

def generate_footer() -> str:
    """生成文档尾部信息"""
    footer = f"""

{'-' * 80}
文档结束
生成工具: AI驱动的软件著作权申请材料生成系统 (Python版本)
生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
{'-' * 80}
"""
    return footer

def merge_frontend_files():
    """主要的前端文件合并逻辑"""
    print_info("🔄 开始拼接前端页面源代码...")
    
    # 1. 确定项目根目录
    script_dir = Path(__file__).parent.parent.parent
    front_dir = script_dir / "output_sourcecode" / "front"
    output_dir = script_dir / "output_docs"
    output_file = output_dir / "前端源代码.txt"
    
    print_info(f"项目根目录: {script_dir}")
    print_info(f"前端目录: {front_dir}")
    print_info(f"输出文件: {output_file}")
    
    # 2. 检查前端目录
    if not front_dir.exists():
        print_error(f"前端目录不存在: {front_dir}")
        print_info("💡 请先生成前端源代码文件")
        return False
    
    # 3. 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 4. 读取项目配置
    config = get_project_config()
    if not config:
        print_warning("无法读取项目配置，使用默认配置")
        config = {
            'title': '软件系统',
            'short_title': '软件系统',
            'front': 'JavaScript',
            'ui_design_style': 'corporate',
            'generation_mode': 'fast'
        }
    
    # 5. 收集HTML文件
    html_files = collect_html_files(front_dir)
    if not html_files:
        print_error(f"在 {front_dir} 中未发现HTML文件")
        print_info("💡 请先生成前端页面代码")
        return False
    
    print_success(f"发现 {len(html_files)} 个HTML文件")
    
    # 6. 开始合并文件
    try:
        with open(output_file, 'w', encoding='utf-8') as output:
            # 写入文档头部
            output.write(generate_header(config, len(html_files)))
            
            # 逐个处理HTML文件
            for i, html_file in enumerate(html_files, 1):
                print_info(f"处理文件 {i}/{len(html_files)}: {html_file.name}")
                
                # 添加文件分隔标识
                separator = f"""
{'=' * 80}
文件 {i}: {html_file.name}
文件路径: output_sourcecode/front/{html_file.name}
文件大小: {html_file.stat().st_size} 字节
{'=' * 80}

"""
                output.write(separator)
                
                # 读取并写入文件内容
                content = read_html_file(html_file)
                output.write(content)
                
                # 添加文件结束标识
                output.write(f"\n\n{'=' * 80}\n文件 {i} 结束: {html_file.name}\n{'=' * 80}\n\n")
            
            # 写入文档尾部
            output.write(generate_footer())
        
        # 7. 输出统计信息
        file_size = output_file.stat().st_size
        file_size_mb = file_size / (1024 * 1024)
        
        print_success("✅ 前端源代码拼接完成")
        print_info(f"📄 输出文件: {output_file}")
        print_info(f"📊 文件统计:")
        print_info(f"   - HTML文件数量: {len(html_files)}")
        print_info(f"   - 总文件大小: {file_size:,} 字节 ({file_size_mb:.2f} MB)")
        print_info(f"   - 平均文件大小: {file_size // len(html_files):,} 字节")
        
        # 8. 生成详细报告
        with open(output_dir / "前端拼接报告.txt", 'w', encoding='utf-8') as report:
            report.write(f"前端源代码拼接报告\n")
            report.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            report.write(f"文件列表:\n")
            for i, html_file in enumerate(html_files, 1):
                file_size = html_file.stat().st_size
                report.write(f"{i:2d}. {html_file.name} ({file_size:,} 字节)\n")
            
            report.write(f"\n总计: {len(html_files)} 个文件，{sum(f.stat().st_size for f in html_files):,} 字节\n")
        
        print_success("📋 生成详细报告: 前端拼接报告.txt")
        return True
        
    except Exception as e:
        print_error(f"文件合并过程中发生错误: {e}")
        return False

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("前端页面源代码拼接脚本 (Python版本)")
        print("\n用法:")
        print("  python3 merge_frontend_simple.py")
        print("\n说明:")
        print("  将 output_sourcecode/front/ 目录下的所有HTML文件")
        print("  拼接成单一的源代码文档用于软著申请")
        print("\n输出:")
        print("  output_docs/前端源代码.txt")
        print("  output_docs/前端拼接报告.txt")
        return
    
    success = merge_frontend_files()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()