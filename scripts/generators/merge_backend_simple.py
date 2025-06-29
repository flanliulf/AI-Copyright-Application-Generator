#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
后端源代码软著申请专用拼接脚本 (Python版本)
功能：将所有后端源代码文件完整拼接成单一文档，专用于软件著作权申请材料

特点：
- 支持多种后端语言（Java, Python, Node.js, PHP等）
- 智能识别源代码文件类型
- 保持代码格式和注释完整性
- 跨平台兼容（Windows/Linux/macOS）
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict

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

def get_source_file_extensions() -> Dict[str, List[str]]:
    """获取不同语言的源代码文件扩展名"""
    return {
        'Java': ['.java', '.jsp', '.xml', '.properties'],
        'Python': ['.py', '.pyx', '.pyi', '.pyw'],
        'JavaScript': ['.js', '.ts', '.jsx', '.tsx', '.json'],
        'Node.js': ['.js', '.ts', '.json', '.mjs'],
        'PHP': ['.php', '.php3', '.php4', '.php5', '.phtml'],
        'C#': ['.cs', '.csx', '.vb'],
        'C++': ['.cpp', '.cc', '.cxx', '.c', '.h', '.hpp'],
        'Go': ['.go'],
        'Ruby': ['.rb', '.rbw'],
        'Rust': ['.rs'],
        'Kotlin': ['.kt', '.kts'],
        'Swift': ['.swift'],
        'Common': ['.sql', '.yml', '.yaml', '.txt', '.md', '.xml', '.json', '.properties', '.env']
    }

def collect_source_files(backend_dir: Path, backend_tech: str) -> List[Path]:
    """收集所有源代码文件"""
    if not backend_dir.exists():
        return []
    
    extensions_map = get_source_file_extensions()
    
    # 根据后端技术确定文件扩展名
    target_extensions = set()
    
    # 添加指定技术的扩展名
    if backend_tech in extensions_map:
        target_extensions.update(extensions_map[backend_tech])
    
    # 始终添加通用文件类型
    target_extensions.update(extensions_map['Common'])
    
    # 如果未识别技术，包含更多常见扩展名
    if backend_tech not in extensions_map:
        for exts in extensions_map.values():
            target_extensions.update(exts)
    
    source_files = []
    
    # 递归搜索源代码文件
    for file_path in backend_dir.rglob('*'):
        if file_path.is_file():
            # 检查文件扩展名
            if file_path.suffix.lower() in target_extensions:
                # 排除某些不需要的文件
                if not should_exclude_file(file_path):
                    source_files.append(file_path)
    
    # 按相对路径排序，确保一致的输出顺序
    source_files.sort(key=lambda x: str(x.relative_to(backend_dir)).lower())
    return source_files

def should_exclude_file(file_path: Path) -> bool:
    """判断是否应该排除某个文件"""
    exclude_patterns = [
        '__pycache__',
        '.git',
        '.svn',
        'node_modules',
        '.class',
        '.pyc',
        '.pyo',
        '.log',
        '.tmp',
        '.temp',
        'target',
        'build',
        'dist'
    ]
    
    file_str = str(file_path).lower()
    for pattern in exclude_patterns:
        if pattern in file_str:
            return True
    
    # 排除空文件或过大的文件
    try:
        file_size = file_path.stat().st_size
        if file_size == 0 or file_size > 10 * 1024 * 1024:  # 10MB限制
            return True
    except:
        return True
    
    return False

def read_source_file(file_path: Path) -> str:
    """安全读取源代码文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # 尝试其他编码
        encodings = ['gb2312', 'gbk', 'iso-8859-1', 'latin-1']
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except:
                continue
        
        print_warning(f"无法读取文件 {file_path.name}: 编码问题")
        return f"// 文件读取失败: {file_path.name} (编码问题)"
    except Exception as e:
        print_warning(f"无法读取文件 {file_path.name}: {e}")
        return f"// 文件读取失败: {file_path.name}"

def generate_header(config: dict, file_count: int, backend_tech: str) -> str:
    """生成文档头部信息"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    header = f"""
{'-' * 80}
软件著作权申请材料 - 后端源代码文档
{'-' * 80}

软件名称: {config.get('title', '未设置')}
软件简称: {config.get('short_title', config.get('title', '未设置'))}
后端技术: {backend_tech}
生成模式: {config.get('generation_mode', '未设置')}

文档生成信息:
- 生成时间: {current_time}
- 源代码文件数量: {file_count}
- 文档类型: 后端源代码完整文档
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

def merge_backend_files():
    """主要的后端文件合并逻辑"""
    print_info("🔄 开始拼接后端源代码...")
    
    # 1. 确定项目根目录
    script_dir = Path(__file__).parent.parent.parent
    backend_dir = script_dir / "output_sourcecode" / "backend"
    output_dir = script_dir / "output_docs"
    output_file = output_dir / "后端源代码.txt"
    
    print_info(f"项目根目录: {script_dir}")
    print_info(f"后端目录: {backend_dir}")
    print_info(f"输出文件: {output_file}")
    
    # 2. 检查后端目录
    if not backend_dir.exists():
        print_error(f"后端目录不存在: {backend_dir}")
        print_info("💡 请先生成后端源代码文件")
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
            'backend': 'Java',
            'generation_mode': 'fast'
        }
    
    backend_tech = config.get('backend', 'Java')
    
    # 5. 收集源代码文件
    source_files = collect_source_files(backend_dir, backend_tech)
    if not source_files:
        print_error(f"在 {backend_dir} 中未发现源代码文件")
        print_info("💡 请先生成后端源代码文件")
        return False
    
    print_success(f"发现 {len(source_files)} 个源代码文件 (技术栈: {backend_tech})")
    
    # 6. 按文件类型分组统计
    file_stats = {}
    for file_path in source_files:
        ext = file_path.suffix.lower()
        if ext not in file_stats:
            file_stats[ext] = 0
        file_stats[ext] += 1
    
    print_info("文件类型统计:")
    for ext, count in sorted(file_stats.items()):
        print_info(f"  {ext or '(无扩展名)'}: {count} 个文件")
    
    # 7. 开始合并文件
    try:
        with open(output_file, 'w', encoding='utf-8') as output:
            # 写入文档头部
            output.write(generate_header(config, len(source_files), backend_tech))
            
            # 逐个处理源代码文件
            for i, source_file in enumerate(source_files, 1):
                rel_path = source_file.relative_to(backend_dir)
                print_info(f"处理文件 {i}/{len(source_files)}: {rel_path}")
                
                # 添加文件分隔标识
                separator = f"""
{'=' * 80}
文件 {i}: {source_file.name}
文件路径: output_sourcecode/backend/{rel_path}
文件类型: {source_file.suffix or '(无扩展名)'}
文件大小: {source_file.stat().st_size} 字节
{'=' * 80}

"""
                output.write(separator)
                
                # 读取并写入文件内容
                content = read_source_file(source_file)
                output.write(content)
                
                # 确保文件内容以换行结束
                if content and not content.endswith('\n'):
                    output.write('\n')
                
                # 添加文件结束标识
                output.write(f"\n\n{'=' * 80}\n文件 {i} 结束: {source_file.name}\n{'=' * 80}\n\n")
            
            # 写入文档尾部
            output.write(generate_footer())
        
        # 8. 输出统计信息
        file_size = output_file.stat().st_size
        file_size_mb = file_size / (1024 * 1024)
        
        print_success("✅ 后端源代码拼接完成")
        print_info(f"📄 输出文件: {output_file}")
        print_info(f"📊 文件统计:")
        print_info(f"   - 源代码文件数量: {len(source_files)}")
        print_info(f"   - 总文件大小: {file_size:,} 字节 ({file_size_mb:.2f} MB)")
        print_info(f"   - 平均文件大小: {file_size // len(source_files):,} 字节")
        
        # 9. 生成详细报告
        with open(output_dir / "后端拼接报告.txt", 'w', encoding='utf-8') as report:
            report.write(f"后端源代码拼接报告\n")
            report.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            report.write(f"后端技术: {backend_tech}\n\n")
            
            report.write(f"文件类型统计:\n")
            for ext, count in sorted(file_stats.items()):
                report.write(f"  {ext or '(无扩展名)'}: {count} 个文件\n")
            
            report.write(f"\n文件列表:\n")
            for i, source_file in enumerate(source_files, 1):
                rel_path = source_file.relative_to(backend_dir)
                file_size = source_file.stat().st_size
                report.write(f"{i:3d}. {rel_path} ({file_size:,} 字节)\n")
            
            total_size = sum(f.stat().st_size for f in source_files)
            report.write(f"\n总计: {len(source_files)} 个文件，{total_size:,} 字节\n")
        
        print_success("📋 生成详细报告: 后端拼接报告.txt")
        return True
        
    except Exception as e:
        print_error(f"文件合并过程中发生错误: {e}")
        return False

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("后端源代码拼接脚本 (Python版本)")
        print("\n用法:")
        print("  python3 merge_backend_simple.py")
        print("\n说明:")
        print("  将 output_sourcecode/backend/ 目录下的所有源代码文件")
        print("  拼接成单一的源代码文档用于软著申请")
        print("\n支持的技术栈:")
        extensions_map = get_source_file_extensions()
        for tech in sorted(extensions_map.keys()):
            if tech != 'Common':
                print(f"  - {tech}")
        print("\n输出:")
        print("  output_docs/后端源代码.txt")
        print("  output_docs/后端拼接报告.txt")
        return
    
    success = merge_backend_files()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()