#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据库源代码软著申请专用拼接脚本 (Python版本)
功能：将所有数据库相关文件完整拼接成单一文档，专用于软件著作权申请材料

特点：
- 支持SQL文件、建表语句、存储过程等
- 智能识别数据库文件类型
- 保持SQL代码格式完整性
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

def collect_database_files(db_dir: Path) -> List[Path]:
    """收集所有数据库相关文件"""
    if not db_dir.exists():
        return []
    
    # 数据库文件扩展名
    db_extensions = {
        '.sql', '.ddl', '.dml', '.plsql', '.psql', 
        '.mysql', '.pgsql', '.sqlite', '.db',
        '.mdb', '.accdb', '.dbf'
    }
    
    db_files = []
    
    # 递归搜索数据库文件
    for file_path in db_dir.rglob('*'):
        if file_path.is_file():
            # 检查文件扩展名或包含SQL关键词的文件
            if (file_path.suffix.lower() in db_extensions or 
                'sql' in file_path.name.lower() or
                'database' in file_path.name.lower() or
                'schema' in file_path.name.lower()):
                
                if not should_exclude_file(file_path):
                    db_files.append(file_path)
    
    # 按相对路径排序，确保一致的输出顺序
    db_files.sort(key=lambda x: str(x.relative_to(db_dir)).lower())
    return db_files

def should_exclude_file(file_path: Path) -> bool:
    """判断是否应该排除某个文件"""
    exclude_patterns = [
        '.git',
        '.svn',
        '.log',
        '.tmp',
        '.temp',
        '.bak',
        '.backup'
    ]
    
    file_str = str(file_path).lower()
    for pattern in exclude_patterns:
        if pattern in file_str:
            return True
    
    # 排除空文件或过大的文件
    try:
        file_size = file_path.stat().st_size
        if file_size == 0 or file_size > 50 * 1024 * 1024:  # 50MB限制
            return True
    except:
        return True
    
    return False

def read_database_file(file_path: Path) -> str:
    """安全读取数据库文件内容"""
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
        return f"-- 文件读取失败: {file_path.name} (编码问题)"
    except Exception as e:
        print_warning(f"无法读取文件 {file_path.name}: {e}")
        return f"-- 文件读取失败: {file_path.name}"

def analyze_sql_content(content: str) -> Dict[str, int]:
    """分析SQL内容，统计各种语句类型"""
    content_upper = content.upper()
    stats = {
        'CREATE TABLE': content_upper.count('CREATE TABLE'),
        'CREATE VIEW': content_upper.count('CREATE VIEW'),
        'CREATE INDEX': content_upper.count('CREATE INDEX'),
        'CREATE PROCEDURE': content_upper.count('CREATE PROCEDURE'),
        'CREATE FUNCTION': content_upper.count('CREATE FUNCTION'),
        'INSERT INTO': content_upper.count('INSERT INTO'),
        'UPDATE': content_upper.count('UPDATE'),
        'DELETE FROM': content_upper.count('DELETE FROM'),
        'SELECT': content_upper.count('SELECT'),
        'ALTER TABLE': content_upper.count('ALTER TABLE'),
        'DROP TABLE': content_upper.count('DROP TABLE'),
    }
    return {k: v for k, v in stats.items() if v > 0}

def generate_header(config: dict, file_count: int) -> str:
    """生成文档头部信息"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    header = f"""
{'-' * 80}
软件著作权申请材料 - 数据库源代码文档
{'-' * 80}

软件名称: {config.get('title', '未设置')}
软件简称: {config.get('short_title', config.get('title', '未设置'))}
后端技术: {config.get('backend', '未设置')}
生成模式: {config.get('generation_mode', '未设置')}

文档生成信息:
- 生成时间: {current_time}
- 数据库文件数量: {file_count}
- 文档类型: 数据库设计和建表语句
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

def merge_database_files():
    """主要的数据库文件合并逻辑"""
    print_info("🔄 开始拼接数据库源代码...")
    
    # 1. 确定项目根目录
    script_dir = Path(__file__).parent.parent.parent
    db_dir = script_dir / "output_sourcecode" / "db"
    output_dir = script_dir / "output_docs"
    output_file = output_dir / "数据库源代码.txt"
    
    print_info(f"项目根目录: {script_dir}")
    print_info(f"数据库目录: {db_dir}")
    print_info(f"输出文件: {output_file}")
    
    # 2. 检查数据库目录
    if not db_dir.exists():
        print_error(f"数据库目录不存在: {db_dir}")
        print_info("💡 请先生成数据库源代码文件")
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
    
    # 5. 收集数据库文件
    db_files = collect_database_files(db_dir)
    if not db_files:
        print_error(f"在 {db_dir} 中未发现数据库文件")
        print_info("💡 请先生成数据库源代码文件")
        return False
    
    print_success(f"发现 {len(db_files)} 个数据库文件")
    
    # 6. 按文件类型分组统计
    file_stats = {}
    for file_path in db_files:
        ext = file_path.suffix.lower() or '(无扩展名)'
        if ext not in file_stats:
            file_stats[ext] = 0
        file_stats[ext] += 1
    
    print_info("文件类型统计:")
    for ext, count in sorted(file_stats.items()):
        print_info(f"  {ext}: {count} 个文件")
    
    # 7. 开始合并文件
    total_sql_stats = {}
    
    try:
        with open(output_file, 'w', encoding='utf-8') as output:
            # 写入文档头部
            output.write(generate_header(config, len(db_files)))
            
            # 逐个处理数据库文件
            for i, db_file in enumerate(db_files, 1):
                rel_path = db_file.relative_to(db_dir)
                print_info(f"处理文件 {i}/{len(db_files)}: {rel_path}")
                
                # 读取文件内容
                content = read_database_file(db_file)
                
                # 分析SQL内容
                sql_stats = analyze_sql_content(content)
                for stmt_type, count in sql_stats.items():
                    if stmt_type not in total_sql_stats:
                        total_sql_stats[stmt_type] = 0
                    total_sql_stats[stmt_type] += count
                
                # 添加文件分隔标识
                separator = f"""
{'=' * 80}
文件 {i}: {db_file.name}
文件路径: output_sourcecode/db/{rel_path}
文件类型: {db_file.suffix or '(无扩展名)'}
文件大小: {db_file.stat().st_size} 字节
{'=' * 80}

"""
                output.write(separator)
                
                # 如果有SQL统计信息，添加到分隔符中
                if sql_stats:
                    output.write("SQL语句统计:\n")
                    for stmt_type, count in sql_stats.items():
                        output.write(f"  {stmt_type}: {count}\n")
                    output.write("\n")
                
                # 写入文件内容
                output.write(content)
                
                # 确保文件内容以换行结束
                if content and not content.endswith('\n'):
                    output.write('\n')
                
                # 添加文件结束标识
                output.write(f"\n\n{'=' * 80}\n文件 {i} 结束: {db_file.name}\n{'=' * 80}\n\n")
            
            # 写入总体SQL统计
            if total_sql_stats:
                output.write(f"""
{'-' * 80}
整体SQL语句统计
{'-' * 80}

""")
                for stmt_type, count in sorted(total_sql_stats.items()):
                    output.write(f"{stmt_type}: {count}\n")
                output.write(f"\n{'-' * 80}\n")
            
            # 写入文档尾部
            output.write(generate_footer())
        
        # 8. 输出统计信息
        file_size = output_file.stat().st_size
        file_size_mb = file_size / (1024 * 1024)
        
        print_success("✅ 数据库源代码拼接完成")
        print_info(f"📄 输出文件: {output_file}")
        print_info(f"📊 文件统计:")
        print_info(f"   - 数据库文件数量: {len(db_files)}")
        print_info(f"   - 总文件大小: {file_size:,} 字节 ({file_size_mb:.2f} MB)")
        
        if total_sql_stats:
            print_info("📊 SQL语句统计:")
            for stmt_type, count in sorted(total_sql_stats.items()):
                print_info(f"   - {stmt_type}: {count}")
        
        # 9. 生成详细报告
        with open(output_dir / "数据库拼接报告.txt", 'w', encoding='utf-8') as report:
            report.write(f"数据库源代码拼接报告\n")
            report.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            report.write(f"文件类型统计:\n")
            for ext, count in sorted(file_stats.items()):
                report.write(f"  {ext}: {count} 个文件\n")
            
            if total_sql_stats:
                report.write(f"\nSQL语句统计:\n")
                for stmt_type, count in sorted(total_sql_stats.items()):
                    report.write(f"  {stmt_type}: {count}\n")
            
            report.write(f"\n文件列表:\n")
            for i, db_file in enumerate(db_files, 1):
                rel_path = db_file.relative_to(db_dir)
                file_size = db_file.stat().st_size
                report.write(f"{i:3d}. {rel_path} ({file_size:,} 字节)\n")
            
            total_size = sum(f.stat().st_size for f in db_files)
            report.write(f"\n总计: {len(db_files)} 个文件，{total_size:,} 字节\n")
        
        print_success("📋 生成详细报告: 数据库拼接报告.txt")
        return True
        
    except Exception as e:
        print_error(f"文件合并过程中发生错误: {e}")
        return False

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("数据库源代码拼接脚本 (Python版本)")
        print("\n用法:")
        print("  python3 merge_database_simple.py")
        print("\n说明:")
        print("  将 output_sourcecode/db/ 目录下的所有数据库文件")
        print("  拼接成单一的源代码文档用于软著申请")
        print("\n支持的文件类型:")
        print("  - .sql, .ddl, .dml - SQL脚本文件")
        print("  - .plsql, .psql - 存储过程文件") 
        print("  - .mysql, .pgsql - 数据库特定文件")
        print("  - database_schema.sql - 建表语句")
        print("\n输出:")
        print("  output_docs/数据库源代码.txt")
        print("  output_docs/数据库拼接报告.txt")
        return
    
    success = merge_database_files()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()