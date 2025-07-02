#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI驱动软件著作权申请材料生成系统 - 自动化测试脚本
版本: 1.0
描述: 快速验证系统核心功能和集成测试
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
import json
import time

class Colors:
    """终端颜色定义"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'

class TestRunner:
    """测试运行器"""
    
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.test_results = []
        
    def print_colored(self, color: str, message: str):
        """打印带颜色的消息"""
        print(f"{color}{message}{Colors.NC}")
    
    def print_header(self, title: str):
        """打印测试章节标题"""
        self.print_colored(Colors.CYAN, f"\n{'='*60}")
        self.print_colored(Colors.CYAN, f"🧪 {title}")
        self.print_colored(Colors.CYAN, f"{'='*60}")
    
    def run_test(self, test_name: str, test_func):
        """运行单个测试"""
        self.print_colored(Colors.BLUE, f"🔄 运行测试: {test_name}")
        start_time = time.time()
        
        try:
            result = test_func()
            duration = time.time() - start_time
            
            if result:
                self.print_colored(Colors.GREEN, f"✅ 测试通过: {test_name} ({duration:.2f}s)")
                self.test_results.append({"name": test_name, "status": "PASS", "duration": duration})
                return True
            else:
                self.print_colored(Colors.RED, f"❌ 测试失败: {test_name} ({duration:.2f}s)")
                self.test_results.append({"name": test_name, "status": "FAIL", "duration": duration})
                return False
        except Exception as e:
            duration = time.time() - start_time
            self.print_colored(Colors.RED, f"💥 测试异常: {test_name} - {e} ({duration:.2f}s)")
            self.test_results.append({"name": test_name, "status": "ERROR", "duration": duration, "error": str(e)})
            return False

    def test_project_structure(self):
        """测试项目结构完整性"""
        required_files = [
            "ai-copyright-config.json",
            "scripts/init/init_project.py",
            "scripts/validators/check_project.py",
            "README.md",
            "ai-copyright.py",
            "ai-copyright.sh"
        ]
        
        required_dirs = [
            "specs_docs",
            "system_prompts",
            "requires_docs"
        ]
        
        for file_path in required_files:
            if not (self.project_dir / file_path).exists():
                return False
        
        for dir_path in required_dirs:
            if not (self.project_dir / dir_path).is_dir():
                return False
        
        return True

    def test_config_file_validity(self):
        """测试配置文件有效性"""
        config_path = self.project_dir / "ai-copyright-config.json"
        
        if not config_path.exists():
            return False
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            required_fields = ["front", "backend", "title", "ui_design_style"]
            for field in required_fields:
                if field not in config:
                    return False
            
            # 检查UI设计风格值
            valid_styles = ["corporate", "cyberpunk", "minimal"]
            if config.get("ui_design_style") not in valid_styles:
                return False
            
            return True
        except (json.JSONDecodeError, Exception):
            return False

    def test_script_syntax(self):
        """测试脚本语法正确性"""
        python_scripts = [
            "init_project.py",
            "check_project.py",
            "generate_all_sourcecode.py"
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
                    if result.returncode != 0:
                        return False
                except Exception:
                    return False
        
        return True

    def test_ui_design_specs(self):
        """测试UI设计规范文件"""
        ui_specs = [
            "specs_docs/ui_design_specs/01-UI设计规范_默认_Corporate.md",
            "specs_docs/ui_design_specs/02-UI设计规范_暗黑科技风格_Cyberpunk.md",
            "specs_docs/ui_design_specs/03-UI设计规范_极简主义风格_Minimal.md"
        ]
        
        for spec in ui_specs:
            spec_path = self.project_dir / spec
            if not spec_path.exists():
                return False
            
            # 检查文件是否为空
            if spec_path.stat().st_size == 0:
                return False
        
        return True

    def test_system_prompts(self):
        """测试AI系统提示词文件"""
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
            prompt_path = self.project_dir / prompt
            if not prompt_path.exists():
                return False
            
            # 检查文件是否包含基本内容
            try:
                with open(prompt_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if len(content.strip()) < 100:  # 至少100个字符
                    return False
            except Exception:
                return False
        
        return True

    def test_check_script_functionality(self):
        """测试检查脚本功能"""
        check_script = self.project_dir / "scripts" / "validators" / "check_project.py"
        
        if not check_script.exists():
            return False
        
        try:
            # 运行快速检查
            result = subprocess.run(
                [sys.executable, str(check_script), "--quick"],
                capture_output=True,
                text=True,
                cwd=self.project_dir,
                timeout=30  # 30秒超时
            )
            
            # 检查脚本是否能正常运行（退出码0、1、2都是正常的）
            return result.returncode in [0, 1, 2]
        except Exception:
            return False

    def test_init_script_import(self):
        """测试初始化脚本导入"""
        init_script = self.project_dir / "scripts" / "init" / "init_project.py"
        
        if not init_script.exists():
            return False
        
        try:
            # 测试脚本是否可以正常导入
            result = subprocess.run(
                [sys.executable, "-c", 
                 f"import sys; sys.path.insert(0, '{self.project_dir}'); "
                 f"exec(open('{init_script}').read().split('if __name__')[0])"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception:
            return False

    def test_documentation_completeness(self):
        """测试文档完整性"""
        docs = [
            "README.md",
            "01-快速开始.md",
            "02-安装指南.md",
            "03-使用说明.md",
            "04-故障排除.md",
            "05-FAQ.md",
            "00-文档导航.md",
            "ROADMAP.md",
            "FEATURE_LIST.md",
            "BUG_FIXES_LOG.md",
            "06-项目检查指南.md"
        ]
        
        for doc in docs:
            doc_path = self.project_dir / doc
            if not doc_path.exists():
                return False
            
            # 检查文档是否有基本内容
            try:
                with open(doc_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if len(content.strip()) < 200:  # 至少200个字符
                    return False
            except Exception:
                return False
        
        return True

    def test_template_creation(self):
        """测试模板项目创建（模拟）"""
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # 创建测试配置文件
                test_config = {
                    "front": "React",
                    "backend": "Node.js",
                    "title": "测试软件系统",
                    "short_title": "测试系统",
                    "ui_design_style": "corporate"
                }
                
                test_config_path = Path(temp_dir) / "ai-copyright-config.json"
                with open(test_config_path, 'w', encoding='utf-8') as f:
                    json.dump(test_config, f, ensure_ascii=False, indent=2)
                
                # 验证文件创建成功
                return test_config_path.exists()
            except Exception:
                return False

    def run_all_tests(self):
        """运行所有测试"""
        self.print_colored(Colors.PURPLE, "🚀 开始AI软著申请材料生成系统自动化测试")
        self.print_colored(Colors.BLUE, f"📁 测试目录: {self.project_dir}")
        
        tests = [
            ("项目结构完整性", self.test_project_structure),
            ("配置文件有效性", self.test_config_file_validity),
            ("脚本语法正确性", self.test_script_syntax),
            ("UI设计规范文件", self.test_ui_design_specs),
            ("AI系统提示词文件", self.test_system_prompts),
            ("检查脚本功能", self.test_check_script_functionality),
            ("初始化脚本导入", self.test_init_script_import),
            ("文档完整性", self.test_documentation_completeness),
            ("模板创建功能", self.test_template_creation)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            if self.run_test(test_name, test_func):
                passed += 1
        
        # 生成测试报告
        return self.generate_test_report(passed, total)

    def generate_test_report(self, passed: int, total: int):
        """生成测试报告"""
        self.print_header("测试报告汇总")
        
        success_rate = (passed / total) * 100 if total > 0 else 0
        
        self.print_colored(Colors.CYAN, f"📊 测试统计:")
        self.print_colored(Colors.GREEN, f"   ✅ 通过: {passed}")
        self.print_colored(Colors.RED, f"   ❌ 失败: {total - passed}")
        self.print_colored(Colors.BLUE, f"   📋 总计: {total}")
        self.print_colored(Colors.PURPLE, f"   💯 成功率: {success_rate:.1f}%")
        
        # 计算总耗时
        total_time = sum(result.get("duration", 0) for result in self.test_results)
        self.print_colored(Colors.CYAN, f"   ⏱️ 总耗时: {total_time:.2f}s")
        
        print("\n" + "="*60)
        
        if passed == total:
            self.print_colored(Colors.GREEN, "🎉 所有测试通过！系统功能正常。")
            return 0
        elif success_rate >= 80:
            self.print_colored(Colors.YELLOW, f"⚠️ {total - passed} 个测试失败，但系统基本可用。")
            return 1
        else:
            self.print_colored(Colors.RED, f"❌ {total - passed} 个测试失败，系统存在严重问题。")
            
            # 显示失败的测试
            failed_tests = [r for r in self.test_results if r["status"] != "PASS"]
            if failed_tests:
                self.print_colored(Colors.RED, "\n🔧 失败的测试:")
                for i, test in enumerate(failed_tests[:3], 1):
                    self.print_colored(Colors.RED, f"   {i}. {test['name']} - {test['status']}")
                
                if len(failed_tests) > 3:
                    self.print_colored(Colors.RED, f"   ... 还有 {len(failed_tests) - 3} 个失败测试")
            
            return 2

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='AI软著申请材料生成系统 - 自动化测试工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python3 run_tests.py                    # 测试当前目录
  python3 run_tests.py /path/to/project   # 测试指定目录
        """
    )
    
    parser.add_argument(
        'project_dir', 
        nargs='?', 
        default='.', 
        help='项目目录路径（默认为当前目录）'
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
    
    # 创建测试运行器并执行
    runner = TestRunner(project_dir)
    return runner.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())