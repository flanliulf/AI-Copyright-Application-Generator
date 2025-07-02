#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
软著项目诊断和自动修复工具
功能：全面诊断项目状态，自动修复常见问题，提供用户友好的操作指导

修复功能：
1. 自动检测和修复常见配置问题
2. 恢复缺失的文件和目录
3. 修复权限和编码问题
4. 提供智能操作建议
5. 一键式问题解决方案
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# 颜色输出类
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
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
    print(f"{Colors.PURPLE}{Colors.BOLD}{'=' * 80}{Colors.NC}")
    print(f"{Colors.PURPLE}{Colors.BOLD}{message.center(80)}{Colors.NC}")
    print(f"{Colors.PURPLE}{Colors.BOLD}{'=' * 80}{Colors.NC}")

def print_fix(message: str):
    print(f"{Colors.CYAN}🔧 {message}{Colors.NC}")

class ProjectDoctor:
    """项目诊断和修复工具"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.original_template_dir = None
        self.issues_found = []
        self.fixes_applied = []
        self.recommendations = []
        
        # 查找原始模板目录
        possible_template_dirs = [
            Path.home() / "AI-Copyright-Application-Generator",
            Path("/usr/local/AI-Copyright-Application-Generator"),
            Path("../AI-Copyright-Application-Generator"),
            Path("../../AI-Copyright-Application-Generator")
        ]
        
        for template_dir in possible_template_dirs:
            if template_dir.exists() and (template_dir / "scripts").exists():
                self.original_template_dir = template_dir
                break
    
    def add_issue(self, severity: str, description: str):
        """添加发现的问题"""
        self.issues_found.append({'severity': severity, 'description': description})
    
    def add_fix(self, description: str):
        """添加应用的修复"""
        self.fixes_applied.append(description)
    
    def add_recommendation(self, description: str):
        """添加建议"""
        self.recommendations.append(description)
    
    def check_project_structure(self) -> bool:
        """检查项目目录结构"""
        print_info("检查项目目录结构...")
        
        required_dirs = [
            "specs_docs/ui_design_specs",
            "specs_docs/tech_stack_specs",
            "system_prompts",
            "requires_docs",
            "process_docs",
            "output_docs",
            "output_sourcecode/front",
            "output_sourcecode/backend",
            "output_sourcecode/db",
            "scripts/generators",
            "scripts/validators"
        ]
        
        missing_dirs = []
        for directory in required_dirs:
            dir_path = self.project_root / directory
            if not dir_path.exists():
                missing_dirs.append(directory)
                self.add_issue("error", f"缺失关键目录: {directory}")
        
        if missing_dirs:
            return self.fix_missing_directories(missing_dirs)
        else:
            print_success("目录结构完整")
            return True
    
    def fix_missing_directories(self, missing_dirs: List[str]) -> bool:
        """修复缺失的目录"""
        print_fix("正在修复缺失的目录...")
        
        try:
            for directory in missing_dirs:
                dir_path = self.project_root / directory
                dir_path.mkdir(parents=True, exist_ok=True)
                print_success(f"创建目录: {directory}")
                self.add_fix(f"创建缺失目录: {directory}")
            return True
        except Exception as e:
            print_error(f"目录修复失败: {e}")
            return False
    
    def check_config_file(self) -> bool:
        """检查配置文件"""
        print_info("检查配置文件...")
        
        config_file = self.project_root / "ai-copyright-config.json"
        
        if not config_file.exists():
            self.add_issue("error", "配置文件不存在")
            return self.fix_missing_config()
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 检查必需的配置项
            required_keys = ['title', 'ui_design_style', 'generation_mode', 'ui_design_spec']
            missing_keys = [key for key in required_keys if key not in config]
            
            if missing_keys:
                self.add_issue("warning", f"配置文件缺少必要字段: {', '.join(missing_keys)}")
                return self.fix_config_keys(config, missing_keys)
            
            print_success("配置文件正常")
            return True
            
        except json.JSONDecodeError:
            self.add_issue("error", "配置文件JSON格式错误")
            return self.fix_config_format()
        except Exception as e:
            self.add_issue("error", f"配置文件读取失败: {e}")
            return False
    
    def fix_missing_config(self) -> bool:
        """修复缺失的配置文件"""
        print_fix("正在生成默认配置文件...")
        
        default_config = {
            "_comment_init": "=== 项目初始化配置（用户设置） ===",
            "front": "JavaScript",
            "backend": "Java",
            "title": "软件系统",
            "short_title": "软件系统",
            "requirements_description": "requires_docs/需求文档.md",
            "dev_tech_stack": "specs_docs/tech_stack_specs/技术栈说明文档_默认.md",
            "ui_design_spec": "specs_docs/ui_design_specs/01-UI设计规范_默认_Corporate.md",
            "ui_design_style": "corporate",
            
            "_comment_generation": "=== 生成配置（可调整） ===",
            "page_count_fast": 5,
            "page_count_full": 10,
            "api_count_min": 8,
            "api_count_max": 35,
            "generation_mode": "fast",
            
            "_comment_usage": "=== 使用说明 ===",
            "_usage_note_1": "请修改 title 和 short_title 为您的实际项目名称",
            "_usage_note_2": "可根据实际情况调整技术栈和UI设计风格",
            "_usage_note_3": "详细说明请参考项目文档",
            
            "_comment_fixed": "=== 固定配置（请勿修改） ===",
            "system_prompt_dir": "system_prompts",
            "ui_design_spec_default": "specs_docs/ui_design_specs/01-UI设计规范_默认_Corporate.md"
        }
        
        try:
            config_file = self.project_root / "ai-copyright-config.json"
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=2)
            
            print_success("已生成默认配置文件")
            self.add_fix("生成默认配置文件")
            self.add_recommendation("请修改配置文件中的项目名称和技术栈信息")
            return True
            
        except Exception as e:
            print_error(f"配置文件生成失败: {e}")
            return False
    
    def fix_config_keys(self, config: dict, missing_keys: List[str]) -> bool:
        """修复配置文件缺失的键"""
        print_fix("正在补充配置文件缺失字段...")
        
        defaults = {
            'title': '软件系统',
            'ui_design_style': 'corporate',
            'generation_mode': 'fast',
            'ui_design_spec': 'specs_docs/ui_design_specs/01-UI设计规范_默认_Corporate.md'
        }
        
        for key in missing_keys:
            if key in defaults:
                config[key] = defaults[key]
                print_success(f"添加配置项: {key} = {defaults[key]}")
        
        try:
            config_file = self.project_root / "ai-copyright-config.json"
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            self.add_fix(f"补充配置文件字段: {', '.join(missing_keys)}")
            return True
            
        except Exception as e:
            print_error(f"配置文件更新失败: {e}")
            return False
    
    def check_scripts(self) -> bool:
        """检查脚本文件"""
        print_info("检查脚本文件...")
        
        script_dirs = ["scripts/generators", "scripts/validators"]
        missing_scripts = []
        
        for script_dir in script_dirs:
            dir_path = self.project_root / script_dir
            if not dir_path.exists():
                missing_scripts.append(script_dir)
                continue
            
            # 检查是否有脚本文件
            script_files = list(dir_path.glob("*.py")) + list(dir_path.glob("*.sh"))
            if not script_files:
                missing_scripts.append(f"{script_dir} (空目录)")
        
        if missing_scripts:
            self.add_issue("error", f"缺失脚本: {', '.join(missing_scripts)}")
            return self.fix_missing_scripts()
        else:
            print_success("脚本文件完整")
            return True
    
    def fix_missing_scripts(self) -> bool:
        """修复缺失的脚本"""
        if not self.original_template_dir:
            print_error("未找到原始模板目录，无法自动修复脚本")
            self.add_recommendation("请手动从原始项目复制 scripts/ 目录")
            return False
        
        print_fix("正在从模板恢复脚本文件...")
        
        try:
            source_scripts = self.original_template_dir / "scripts"
            target_scripts = self.project_root / "scripts"
            
            if source_scripts.exists():
                # 确保目标目录存在
                target_scripts.mkdir(exist_ok=True)
                
                # 复制generators目录
                source_gen = source_scripts / "generators"
                target_gen = target_scripts / "generators"
                if source_gen.exists():
                    target_gen.mkdir(exist_ok=True)
                    for script_file in source_gen.iterdir():
                        if script_file.is_file():
                            shutil.copy2(script_file, target_gen / script_file.name)
                    print_success("恢复 generators 脚本")
                
                # 复制validators目录
                source_val = source_scripts / "validators"
                target_val = target_scripts / "validators"
                if source_val.exists():
                    target_val.mkdir(exist_ok=True)
                    for script_file in source_val.iterdir():
                        if script_file.is_file():
                            shutil.copy2(script_file, target_val / script_file.name)
                    print_success("恢复 validators 脚本")
                
                # 设置执行权限
                self.fix_script_permissions()
                
                self.add_fix("从模板恢复脚本文件")
                return True
            else:
                print_error("模板目录中未找到scripts文件夹")
                return False
                
        except Exception as e:
            print_error(f"脚本恢复失败: {e}")
            return False
    
    def fix_script_permissions(self) -> bool:
        """修复脚本权限"""
        print_fix("设置脚本执行权限...")
        
        script_dirs = ["scripts/generators", "scripts/validators"]
        
        try:
            for script_dir in script_dirs:
                dir_path = self.project_root / script_dir
                if dir_path.exists():
                    for script_file in dir_path.iterdir():
                        if script_file.is_file() and script_file.suffix in ['.py', '.sh']:
                            script_file.chmod(0o755)
            
            print_success("脚本权限设置完成")
            self.add_fix("设置脚本执行权限")
            return True
            
        except Exception as e:
            print_error(f"权限设置失败: {e}")
            return False
    
    def check_system_prompts(self) -> bool:
        """检查系统提示词"""
        print_info("检查系统提示词...")
        
        prompt_dir = self.project_root / "system_prompts"
        if not prompt_dir.exists():
            self.add_issue("error", "系统提示词目录不存在")
            return False
        
        expected_prompts = [
            "01-软著框架系统提示词.md",
            "02-页面规划系统提示词.md",
            "03-界面设计系统提示词.md",
            "04-网页代码生成系统提示词.md",
            "05-数据库代码生成系统提示词.md",
            "06-后端代码生成系统提示词.md",
            "07-用户手册系统提示词.md",
            "08-软件著作权登记信息表系统提示词.md"
        ]
        
        missing_prompts = []
        for prompt_file in expected_prompts:
            if not (prompt_dir / prompt_file).exists():
                missing_prompts.append(prompt_file)
        
        if missing_prompts:
            self.add_issue("error", f"缺失系统提示词: {len(missing_prompts)}/{len(expected_prompts)}")
            return self.fix_missing_prompts(missing_prompts)
        else:
            print_success("系统提示词完整")
            return True
    
    def fix_missing_prompts(self, missing_prompts: List[str]) -> bool:
        """修复缺失的系统提示词"""
        if not self.original_template_dir:
            print_error("未找到原始模板目录，无法自动修复提示词")
            self.add_recommendation("请手动从原始项目复制 system_prompts/ 目录")
            return False
        
        print_fix("正在从模板恢复系统提示词...")
        
        try:
            source_prompts = self.original_template_dir / "system_prompts"
            target_prompts = self.project_root / "system_prompts"
            
            if source_prompts.exists():
                target_prompts.mkdir(exist_ok=True)
                
                for prompt_file in missing_prompts:
                    source_file = source_prompts / prompt_file
                    target_file = target_prompts / prompt_file
                    
                    if source_file.exists():
                        shutil.copy2(source_file, target_file)
                        print_success(f"恢复: {prompt_file}")
                
                self.add_fix(f"恢复 {len(missing_prompts)} 个系统提示词文件")
                return True
            else:
                print_error("模板目录中未找到system_prompts文件夹")
                return False
                
        except Exception as e:
            print_error(f"系统提示词恢复失败: {e}")
            return False
    
    def check_requirements_doc(self) -> bool:
        """检查需求文档"""
        print_info("检查需求文档...")
        
        req_file = self.project_root / "requires_docs" / "需求文档.md"
        
        if not req_file.exists():
            self.add_issue("warning", "需求文档不存在")
            return self.fix_missing_requirements()
        
        try:
            with open(req_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content.strip()) < 100:
                self.add_issue("warning", "需求文档内容过少")
                self.add_recommendation("建议详细填写需求文档以获得更好的生成效果")
            else:
                print_success("需求文档存在且有内容")
            
            return True
            
        except Exception as e:
            self.add_issue("error", f"需求文档读取失败: {e}")
            return False
    
    def fix_missing_requirements(self) -> bool:
        """修复缺失的需求文档"""
        print_fix("正在创建需求文档模板...")
        
        template_content = f"""# 软件系统需求文档

## 项目背景

请在此描述项目的背景、目标和价值。

## 功能需求

### 核心功能

1. 用户管理功能
   - 用户注册、登录、注销
   - 用户信息管理和权限控制
   - 密码修改和找回

2. 数据管理功能
   - 数据录入、查询、修改、删除
   - 数据导入和导出
   - 数据统计和报表

3. 系统管理功能
   - 系统配置和参数设置
   - 日志管理和监控
   - 备份和恢复

### 非功能需求

- 性能要求：系统响应时间不超过3秒
- 安全要求：数据加密存储，支持HTTPS访问
- 可用性要求：系统可用性达到99%以上
- 兼容性要求：支持主流浏览器

## 技术要求

- 前端技术：JavaScript, HTML5, CSS3
- 后端技术：Java Spring Boot
- 数据库：MySQL
- 部署环境：Linux服务器

## 用户角色

- 系统管理员：具有所有权限，负责系统维护
- 普通用户：具有基本操作权限
- 访客用户：只能查看公开信息

## 业务流程

1. 用户登录系统
2. 选择相应功能模块
3. 执行具体操作
4. 系统返回操作结果
5. 记录操作日志

---

*请根据实际项目需求完善此文档内容*
"""
        
        try:
            req_file = self.project_root / "requires_docs" / "需求文档.md"
            req_file.parent.mkdir(exist_ok=True)
            
            with open(req_file, 'w', encoding='utf-8') as f:
                f.write(template_content)
            
            print_success("已创建需求文档模板")
            self.add_fix("创建需求文档模板")
            self.add_recommendation("请详细填写需求文档内容")
            return True
            
        except Exception as e:
            print_error(f"需求文档创建失败: {e}")
            return False
    
    def generate_diagnostic_report(self) -> str:
        """生成诊断报告"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
{'-' * 80}
软著项目诊断报告
{'-' * 80}

诊断时间: {current_time}
项目路径: {self.project_root}

{'-' * 80}
问题诊断结果
{'-' * 80}

发现问题总数: {len(self.issues_found)}

"""
        
        # 按严重程度分组问题
        errors = [issue for issue in self.issues_found if issue['severity'] == 'error']
        warnings = [issue for issue in self.issues_found if issue['severity'] == 'warning']
        
        if errors:
            report += "🔴 严重问题:\n"
            for i, issue in enumerate(errors, 1):
                report += f"  {i}. {issue['description']}\n"
            report += "\n"
        
        if warnings:
            report += "🟡 警告问题:\n"
            for i, issue in enumerate(warnings, 1):
                report += f"  {i}. {issue['description']}\n"
            report += "\n"
        
        if not self.issues_found:
            report += "✅ 未发现问题，项目状态良好\n\n"
        
        # 修复结果
        if self.fixes_applied:
            report += f"{'-' * 80}\n自动修复结果\n{'-' * 80}\n\n"
            report += f"成功修复: {len(self.fixes_applied)} 个问题\n\n"
            for i, fix in enumerate(self.fixes_applied, 1):
                report += f"  {i}. {fix}\n"
            report += "\n"
        
        # 建议
        if self.recommendations:
            report += f"{'-' * 80}\n改进建议\n{'-' * 80}\n\n"
            for i, rec in enumerate(self.recommendations, 1):
                report += f"  {i}. {rec}\n"
            report += "\n"
        
        # 下一步操作
        report += f"{'-' * 80}\n下一步操作建议\n{'-' * 80}\n\n"
        
        remaining_errors = len([issue for issue in self.issues_found if issue['severity'] == 'error']) - len([fix for fix in self.fixes_applied if '严重' in fix or '关键' in fix])
        
        if remaining_errors > 0:
            report += "🔴 仍有严重问题未解决:\n"
            report += "  1. 手动检查并修复剩余的严重问题\n"
            report += "  2. 重新运行诊断工具验证修复效果\n"
            report += "  3. 联系技术支持获取帮助\n"
        else:
            report += "✅ 项目已就绪，可以开始软著申请材料生成:\n"
            report += "  1. 详细填写 requires_docs/需求文档.md\n"
            report += "  2. 运行质量检查: python3 scripts/validators/validate_requirements.py\n"
            report += "  3. 开始按照工作流程生成申请材料\n"
            report += "  4. 定期运行质量监控: python3 scripts/validators/quality_monitor.py\n"
        
        report += f"\n{'-' * 80}\n诊断完成时间: {current_time}\n{'-' * 80}\n"
        
        return report
    
    def run_full_diagnosis(self) -> Dict[str, any]:
        """执行完整诊断"""
        print_header("软著项目健康诊断")
        
        print_info(f"项目路径: {self.project_root}")
        if self.original_template_dir:
            print_info(f"模板路径: {self.original_template_dir}")
        print()
        
        # 执行各项检查
        checks = [
            ("项目目录结构", self.check_project_structure),
            ("配置文件", self.check_config_file),
            ("脚本文件", self.check_scripts),
            ("系统提示词", self.check_system_prompts),
            ("需求文档", self.check_requirements_doc)
        ]
        
        check_results = {}
        
        for check_name, check_func in checks:
            print(f"\n{'-' * 40}")
            result = check_func()
            check_results[check_name] = result
            if result:
                print_success(f"{check_name}: 检查通过")
            else:
                print_error(f"{check_name}: 检查失败")
        
        print(f"\n{'-' * 40}")
        
        # 统计结果
        total_checks = len(checks)
        passed_checks = sum(check_results.values())
        
        print_header("诊断结果概览")
        print_info(f"检查项目: {passed_checks}/{total_checks} 通过")
        print_info(f"发现问题: {len(self.issues_found)} 个")
        print_info(f"自动修复: {len(self.fixes_applied)} 个")
        
        if passed_checks == total_checks and not self.issues_found:
            print_success("🎉 项目状态优秀，可以开始生成软著申请材料!")
        elif passed_checks >= total_checks * 0.8:
            print_warning("⚠️ 项目状态良好，有少量问题已自动修复")
        else:
            print_error("❌ 项目存在较多问题，请根据报告进行修复")
        
        return {
            'total_checks': total_checks,
            'passed_checks': passed_checks,
            'issues_found': len(self.issues_found),
            'fixes_applied': len(self.fixes_applied),
            'check_results': check_results,
            'health_score': (passed_checks / total_checks) * 100
        }

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("软著项目诊断和自动修复工具")
        print("\n用法:")
        print("  python3 project_doctor.py")
        print("\n功能:")
        print("  - 全面诊断项目状态")
        print("  - 自动修复常见问题")
        print("  - 恢复缺失的文件和配置")
        print("  - 生成详细的诊断报告")
        print("\n检查项目:")
        print("  - 项目目录结构")
        print("  - 配置文件完整性")
        print("  - 脚本文件和权限")
        print("  - 系统提示词文件")
        print("  - 需求文档状态")
        print("\n输出:")
        print("  - 终端显示诊断过程和结果")
        print("  - 生成详细的诊断报告文件")
        return
    
    # 执行诊断
    doctor = ProjectDoctor()
    result = doctor.run_full_diagnosis()
    
    # 生成并保存报告
    print()
    print_info("生成详细诊断报告...")
    
    report = doctor.generate_diagnostic_report()
    
    # 保存报告
    report_file = Path("项目诊断报告.txt")
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print_success(f"诊断报告已保存: {report_file}")
    except Exception as e:
        print_error(f"保存报告失败: {e}")
    
    # 显示关键建议
    if doctor.recommendations:
        print()
        print_header("重要建议")
        for i, rec in enumerate(doctor.recommendations[:3], 1):  # 显示前3条
            print_info(f"{i}. {rec}")
    
    # 返回状态码
    health_score = result['health_score']
    if health_score >= 90:
        sys.exit(0)  # 优秀
    elif health_score >= 70:
        sys.exit(1)  # 良好但有改进空间
    else:
        sys.exit(2)  # 需要重要改进

if __name__ == "__main__":
    main()