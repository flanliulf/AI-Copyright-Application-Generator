#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI驱动软件著作权申请材料生成系统 - 项目完整性检查脚本
版本: 1.0
描述: 全面检查项目文件完整性、配置正确性和功能可用性
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import tempfile
import shutil

class Colors:
    """终端颜色定义"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color

class ProjectChecker:
    """项目检查器"""
    
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.errors = []
        self.warnings = []
        self.successes = []
        
    def print_colored(self, color: str, message: str):
        """打印带颜色的消息"""
        print(f"{color}{message}{Colors.NC}")
    
    def print_header(self, title: str):
        """打印章节标题"""
        self.print_colored(Colors.CYAN, f"\n{'='*60}")
        self.print_colored(Colors.CYAN, f"🔍 {title}")
        self.print_colored(Colors.CYAN, f"{'='*60}")
    
    def print_success(self, message: str):
        """打印成功消息"""
        self.print_colored(Colors.GREEN, f"✅ {message}")
        self.successes.append(message)
    
    def print_warning(self, message: str):
        """打印警告消息"""
        self.print_colored(Colors.YELLOW, f"⚠️  {message}")
        self.warnings.append(message)
    
    def print_error(self, message: str):
        """打印错误消息"""
        self.print_colored(Colors.RED, f"❌ {message}")
        self.errors.append(message)
    
    def print_info(self, message: str):
        """打印信息消息"""
        self.print_colored(Colors.BLUE, f"ℹ️  {message}")

    def check_file_exists(self, file_path: str, required: bool = True) -> bool:
        """检查文件是否存在"""
        full_path = self.project_dir / file_path
        if full_path.exists():
            self.print_success(f"文件存在: {file_path}")
            return True
        else:
            if required:
                self.print_error(f"必需文件缺失: {file_path}")
            else:
                self.print_warning(f"可选文件缺失: {file_path}")
            return False
    
    def check_directory_exists(self, dir_path: str, required: bool = True) -> bool:
        """检查目录是否存在"""
        full_path = self.project_dir / dir_path
        if full_path.exists() and full_path.is_dir():
            self.print_success(f"目录存在: {dir_path}")
            return True
        else:
            if required:
                self.print_error(f"必需目录缺失: {dir_path}")
            else:
                self.print_warning(f"可选目录缺失: {dir_path}")
            return False

    def check_core_files(self):
        """检查核心文件完整性"""
        self.print_header("核心文件完整性检查")
        
        # 核心配置文件
        self.check_file_exists("ai-copyright-config.json")
        
        # 统一入口脚本
        self.check_file_exists("ai-copyright.py")
        self.check_file_exists("ai-copyright.sh")
        self.check_file_exists("create-copyright-project")
        
        # 初始化脚本（新目录）
        self.check_file_exists("scripts/init/init_project.py")
        self.check_file_exists("scripts/init/init_project.sh")
        
        # 生成脚本（新目录）
        generation_scripts = [
            "scripts/generators/generate_all_sourcecode.py",
            "scripts/generators/generate_frontend_sourcecode.py", 
            "scripts/generators/generate_backend_sourcecode.py",
            "scripts/generators/generate_all_sourcecode.sh",
            "scripts/generators/generate_frontend_sourcecode.sh",
            "scripts/generators/generate_backend_sourcecode.sh"
        ]
        for script in generation_scripts:
            self.check_file_exists(script)
        
        # 验证脚本（新目录）
        validation_scripts = [
            "scripts/validators/check_project.py",
            "scripts/validators/check_project.sh", 
            "scripts/validators/run_tests.py",
            "scripts/validators/validate_frontend_pages.py"
        ]
        for script in validation_scripts:
            self.check_file_exists(script)
        
        # 文档文件
        docs = [
            "README.md",
            "01-快速开始.md",
            "02-安装指南.md", 
            "03-使用说明.md",
            "04-故障排除.md",
            "05-FAQ.md",
            "00-文档导航.md",
            "CLAUDE.md",
            "CLAUDE_zh.md",
            "ROADMAP.md",
            "FEATURE_LIST.md",
            "BUG_FIXES_LOG.md",
            "工作流程.md",
            "执行计划.md",
            "06-项目检查指南.md"
        ]
        for doc in docs:
            self.check_file_exists(doc)

    def check_directory_structure(self):
        """检查目录结构完整性"""
        self.print_header("目录结构完整性检查")
        
        # 核心目录
        core_dirs = [
            "specs_docs",
            "specs_docs/ui_design_specs",
            "specs_docs/tech_stack_specs", 
            "system_prompts",
            "requires_docs",
            "process_docs",
            "output_docs",
            "output_sourcecode",
            "output_sourcecode/front",
            "output_sourcecode/backend"
        ]
        
        for dir_path in core_dirs:
            self.check_directory_exists(dir_path)

    def check_ui_design_specs(self):
        """检查UI设计规范文件"""
        self.print_header("UI设计规范文件检查")
        
        ui_specs = [
            "specs_docs/ui_design_specs/01-UI设计规范_默认_Corporate.md",
            "specs_docs/ui_design_specs/02-UI设计规范_暗黑科技风格_Cyberpunk.md",
            "specs_docs/ui_design_specs/03-UI设计规范_极简主义风格_Minimal.md"
        ]
        
        for spec in ui_specs:
            self.check_file_exists(spec)

    def check_system_prompts(self):
        """检查AI系统提示词完整性"""
        self.print_header("AI系统提示词完整性检查")
        
        prompts = [
            "system_prompts/01-软著框架系统提示词.md",
            "system_prompts/02-页面规划系统提示词.md",
            "system_prompts/03-界面设计系统提示词.md",
            "system_prompts/04-网页代码生成系统提示词.md",
            "system_prompts/05-数据库代码生成系统提示词.md",
            "system_prompts/06-后端代码生成系统提示词.md",
            "system_prompts/07-用户手册系统提示词.md",
            "system_prompts/08-软件著作权登记信息表系统提示词.md"
        ]
        
        for prompt in prompts:
            self.check_file_exists(prompt)

    def check_config_file(self):
        """检查配置文件内容"""
        self.print_header("配置文件内容检查")
        
        config_path = self.project_dir / "ai-copyright-config.json"
        if not config_path.exists():
            self.print_error("配置文件不存在")
            return
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 检查必需字段
            required_fields = [
                "front", "backend", "title", "short_title",
                "requirements_description", "dev_tech_stack", "ui_design_spec",
                "ui_design_style", "system_prompt_dir", "ui_design_spec_default"
            ]
            
            for field in required_fields:
                if field in config:
                    self.print_success(f"配置字段存在: {field}")
                else:
                    self.print_error(f"配置字段缺失: {field}")
            
            # 检查UI设计风格值
            if "ui_design_style" in config:
                valid_styles = ["corporate", "cyberpunk", "minimal", "bauhaus", "japanese", "scandinavian", "futuristic", "elegant", "bold", "artdeco", "memphis", "popart"]
                if config["ui_design_style"] in valid_styles:
                    self.print_success(f"UI设计风格有效: {config['ui_design_style']}")
                else:
                    self.print_warning(f"UI设计风格可能无效: {config['ui_design_style']}")
            
        except json.JSONDecodeError as e:
            self.print_error(f"配置文件JSON格式错误: {e}")
        except Exception as e:
            self.print_error(f"配置文件读取错误: {e}")

    def check_script_syntax(self):
        """检查脚本语法"""
        self.print_header("脚本语法检查")
        
        # 检查Python脚本
        python_scripts = [
            "init_project.py",
            "generate_all_sourcecode.py",
            "generate_frontend_sourcecode.py",
            "generate_backend_sourcecode.py"
        ]
        
        for script in python_scripts:
            script_path = self.project_dir / script
            if script_path.exists():
                try:
                    result = subprocess.run(
                        [sys.executable, "-m", "py_compile", str(script_path)],
                        capture_output=True,
                        text=True,
                        cwd=self.project_dir
                    )
                    if result.returncode == 0:
                        self.print_success(f"Python脚本语法正确: {script}")
                    else:
                        self.print_error(f"Python脚本语法错误: {script}\n{result.stderr}")
                except Exception as e:
                    self.print_error(f"Python脚本检查失败: {script} - {e}")
        
        # 检查Shell脚本
        shell_scripts = [
            "init_project.sh",
            "generate_all_sourcecode.sh", 
            "generate_frontend_sourcecode.sh",
            "generate_backend_sourcecode.sh",
            "create-copyright-project"
        ]
        
        for script in shell_scripts:
            script_path = self.project_dir / script
            if script_path.exists():
                try:
                    result = subprocess.run(
                        ["bash", "-n", str(script_path)],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        self.print_success(f"Shell脚本语法正确: {script}")
                    else:
                        self.print_error(f"Shell脚本语法错误: {script}\n{result.stderr}")
                except Exception as e:
                    self.print_error(f"Shell脚本检查失败: {script} - {e}")

    def check_document_references(self):
        """检查文档中的配置文件引用一致性"""
        self.print_header("文档引用一致性检查")
        
        docs_to_check = [
            "README.md", "01-快速开始.md", "03-使用说明.md", 
            "工作流程.md", "04-故障排除.md", "05-FAQ.md",
            "CLAUDE.md", "CLAUDE_zh.md"
        ]
        
        old_config_refs = 0
        new_config_refs = 0
        problematic_refs = []
        
        # 定义说明性文本模式，这些不算作问题引用
        explanatory_patterns = [
            "从.*config\.json.*更名",
            "已从.*config\.json.*更名", 
            "config\.json.*更名为",
            "配置文件.*从.*config\.json",
            "原.*config\.json",
            "旧.*config\.json",
            "之前.*config\.json"
        ]
        
        import re
        
        for doc in docs_to_check:
            doc_path = self.project_dir / doc
            if doc_path.exists():
                try:
                    with open(doc_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 检查旧配置文件引用（但不包括 ai-copyright-config.json）
                    # 计算独立的 config.json 引用，排除 ai-copyright-config.json
                    total_config_count = content.count("config.json")
                    ai_config_count = content.count("ai-copyright-config.json")
                    independent_config_count = total_config_count - ai_config_count
                    
                    if independent_config_count > 0:
                        # 检查是否是说明性文本
                        is_explanatory = False
                        for pattern in explanatory_patterns:
                            if re.search(pattern, content, re.IGNORECASE):
                                is_explanatory = True
                                break
                        
                        if is_explanatory:
                            self.print_success(f"文档包含配置文件更名说明: {doc}")
                        else:
                            old_config_refs += independent_config_count
                            problematic_refs.append(doc)
                            self.print_warning(f"文档包含旧配置文件引用: {doc}")
                    
                    # 检查新配置文件引用  
                    if "ai-copyright-config.json" in content:
                        new_config_refs += content.count("ai-copyright-config.json")
                        self.print_success(f"文档使用新配置文件名: {doc}")
                        
                except Exception as e:
                    self.print_error(f"文档读取失败: {doc} - {e}")
        
        if old_config_refs == 0:
            self.print_success("所有文档已更新为新配置文件名")
        else:
            self.print_error(f"发现 {old_config_refs} 处旧配置文件引用需要更新（在 {len(problematic_refs)} 个文档中）")

    def test_project_initialization(self):
        """测试项目初始化功能"""
        self.print_header("项目初始化功能测试")
        
        # 创建临时测试目录
        with tempfile.TemporaryDirectory() as temp_dir:
            test_project_name = "test-ai-copyright-project"
            test_project_path = Path(temp_dir) / test_project_name
            
            try:
                # 测试Python初始化脚本
                init_script = self.project_dir / "init_project.py"
                if init_script.exists():
                    # 模拟非交互式运行
                    env = os.environ.copy()
                    env['PYTHONPATH'] = str(self.project_dir)
                    
                    # 这里我们只测试脚本是否能正常导入和基础语法
                    result = subprocess.run(
                        [sys.executable, "-c", 
                         f"import sys; sys.path.insert(0, '{self.project_dir}'); "
                         f"exec(open('{init_script}').read().split('if __name__')[0])"],
                        capture_output=True,
                        text=True,
                        cwd=temp_dir
                    )
                    
                    if result.returncode == 0:
                        self.print_success("初始化脚本语法和导入测试通过")
                    else:
                        self.print_error(f"初始化脚本测试失败: {result.stderr}")
                else:
                    self.print_error("初始化脚本不存在")
                    
            except Exception as e:
                self.print_error(f"项目初始化测试失败: {e}")

    def check_git_configuration(self):
        """检查Git配置"""
        self.print_header("Git配置检查")
        
        # 检查.gitignore
        gitignore_path = self.project_dir / ".gitignore"
        if gitignore_path.exists():
            self.print_success(".gitignore文件存在")
            
            try:
                with open(gitignore_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查关键忽略项
                key_ignores = [
                    "ai-copyright-config_local.json",
                    ".DS_Store",
                    "__pycache__",
                    "node_modules",
                    "*.log"
                ]
                
                for ignore_item in key_ignores:
                    if ignore_item in content:
                        self.print_success(f"包含忽略项: {ignore_item}")
                    else:
                        self.print_warning(f"缺少忽略项: {ignore_item}")
                        
            except Exception as e:
                self.print_error(f".gitignore读取失败: {e}")
        else:
            self.print_warning(".gitignore文件不存在")
        
        # 检查是否为Git仓库
        git_dir = self.project_dir / ".git"
        if git_dir.exists():
            self.print_success("Git仓库已初始化")
        else:
            self.print_warning("未初始化Git仓库")

    def generate_report(self):
        """生成检查报告"""
        self.print_header("检查报告汇总")
        
        total_checks = len(self.successes) + len(self.warnings) + len(self.errors)
        
        self.print_colored(Colors.CYAN, f"📊 检查统计:")
        self.print_colored(Colors.GREEN, f"   ✅ 成功: {len(self.successes)}")
        self.print_colored(Colors.YELLOW, f"   ⚠️  警告: {len(self.warnings)}")
        self.print_colored(Colors.RED, f"   ❌ 错误: {len(self.errors)}")
        self.print_colored(Colors.BLUE, f"   📋 总计: {total_checks}")
        
        # 计算健康度分数
        if total_checks > 0:
            health_score = (len(self.successes) / total_checks) * 100
            self.print_colored(Colors.PURPLE, f"   💯 健康度: {health_score:.1f}%")
        
        print("\n" + "="*60)
        
        if len(self.errors) == 0:
            if len(self.warnings) == 0:
                self.print_colored(Colors.GREEN, "🎉 项目检查完全通过！系统可以正常使用。")
                return 0
            else:
                self.print_colored(Colors.YELLOW, "✅ 项目检查基本通过，有一些警告需要注意。")
                return 1
        else:
            self.print_colored(Colors.RED, "❌ 项目检查发现错误，需要修复后才能正常使用。")
            
            self.print_colored(Colors.RED, "\n🔧 需要修复的错误:")
            for i, error in enumerate(self.errors[:5], 1):  # 只显示前5个错误
                self.print_colored(Colors.RED, f"   {i}. {error}")
            
            if len(self.errors) > 5:
                self.print_colored(Colors.RED, f"   ... 还有 {len(self.errors) - 5} 个错误")
            
            return 2

    def run_all_checks(self):
        """运行所有检查"""
        self.print_colored(Colors.PURPLE, "🚀 开始AI软著申请材料生成系统完整性检查")
        self.print_colored(Colors.BLUE, f"📁 检查目录: {self.project_dir}")
        
        # 执行各项检查
        self.check_core_files()
        self.check_directory_structure()
        self.check_ui_design_specs()
        self.check_system_prompts()
        self.check_config_file()
        self.check_script_syntax()
        self.check_document_references()
        self.test_project_initialization()
        self.check_git_configuration()
        
        # 生成报告
        return self.generate_report()

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='AI驱动软件著作权申请材料生成系统 - 项目完整性检查工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python3 check_project.py                    # 检查当前目录
  python3 check_project.py /path/to/project   # 检查指定目录
  python3 check_project.py --quick            # 快速检查（跳过某些耗时检查）
        """
    )
    
    parser.add_argument(
        'project_dir', 
        nargs='?', 
        default='.', 
        help='项目目录路径（默认为当前目录）'
    )
    
    parser.add_argument(
        '--quick', '-q',
        action='store_true',
        help='快速检查模式（跳过语法检查和初始化测试）'
    )
    
    args = parser.parse_args()
    
    # 解析项目目录
    project_dir = Path(args.project_dir).resolve()
    
    if not project_dir.exists():
        print(f"{Colors.RED}❌ 项目目录不存在: {project_dir}{Colors.NC}")
        sys.exit(1)
    
    if not project_dir.is_dir():
        print(f"{Colors.RED}❌ 指定路径不是目录: {project_dir}{Colors.NC}")
        sys.exit(1)
    
    # 创建检查器并运行
    checker = ProjectChecker(project_dir)
    
    if args.quick:
        checker.print_colored(Colors.YELLOW, "⚡ 快速检查模式（跳过语法检查和初始化测试）")
        # 在快速模式下跳过某些检查
        checker.check_core_files()
        checker.check_directory_structure()
        checker.check_ui_design_specs()
        checker.check_system_prompts()
        checker.check_config_file()
        checker.check_document_references()
        checker.check_git_configuration()
        return checker.generate_report()
    else:
        return checker.run_all_checks()

if __name__ == "__main__":
    sys.exit(main())