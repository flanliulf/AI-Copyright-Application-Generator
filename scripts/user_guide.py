#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
软著申请材料生成系统 - 用户指导工具
功能：为用户提供友好的交互式指导，简化整个申请流程

特点：
- 交互式菜单系统
- 智能操作建议
- 一键式工具调用
- 实时状态反馈
- 新手友好的操作指导
"""

import sys
import subprocess
from pathlib import Path

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
    print(f"\n{Colors.PURPLE}{Colors.BOLD}{'=' * 80}{Colors.NC}")
    print(f"{Colors.PURPLE}{Colors.BOLD}{message.center(80)}{Colors.NC}")
    print(f"{Colors.PURPLE}{Colors.BOLD}{'=' * 80}{Colors.NC}")

def print_menu_item(number: int, title: str, description: str):
    print(f"{Colors.CYAN}{number:2d}.{Colors.NC} {Colors.BOLD}{title}{Colors.NC}")
    print(f"     {description}")

def print_separator():
    print(f"{Colors.BLUE}{'-' * 80}{Colors.NC}")

class UserGuide:
    """用户指导系统"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        
    def run_tool(self, tool_path: str, tool_name: str) -> bool:
        """运行指定工具"""
        if not Path(tool_path).exists():
            print_error(f"工具不存在: {tool_path}")
            return False
        
        print_info(f"正在运行 {tool_name}...")
        print_separator()
        
        try:
            result = subprocess.run([sys.executable, tool_path], cwd=self.project_root)
            print_separator()
            
            if result.returncode == 0:
                print_success(f"{tool_name} 执行完成")
                return True
            else:
                print_warning(f"{tool_name} 执行完成 (退出码: {result.returncode})")
                return False
                
        except Exception as e:
            print_error(f"{tool_name} 执行失败: {e}")
            return False
    
    def show_main_menu(self):
        """显示主菜单"""
        print_header("软著申请材料生成系统 - 用户指导中心")
        
        print(f"{Colors.GREEN}欢迎使用AI驱动的软件著作权申请材料生成系统！{Colors.NC}")
        print(f"{Colors.BLUE}本系统将帮助您生成专业的软著申请材料，包括源代码文档、用户手册等。{Colors.NC}")
        print()
        
        print_menu_item(1, "🏥 项目健康诊断", "检查项目状态，自动修复常见问题")
        print_menu_item(2, "📝 需求文档质量检查", "验证需求文档质量，获得改进建议")
        print_menu_item(3, "📊 质量监控面板", "监控生成进度和代码质量")
        print_menu_item(4, "🔧 代码合并工具", "将生成的代码合并为申请文档")
        print_menu_item(5, "📋 查看项目状态", "查看当前项目的整体状态")
        print_menu_item(6, "💡 获取操作建议", "根据项目状态获得下一步建议")
        print_menu_item(7, "📚 查看帮助文档", "查看详细的使用说明")
        print_menu_item(0, "🚪 退出系统", "结束使用")
        
        print_separator()
    
    def project_diagnosis(self):
        """项目诊断"""
        print_header("项目健康诊断")
        print_info("这将检查项目的完整性并自动修复发现的问题...")
        
        tool_path = "scripts/validators/project_doctor.py"
        success = self.run_tool(tool_path, "项目诊断工具")
        
        if success:
            print_info("💡 建议查看生成的 '项目诊断报告.txt' 了解详细信息")
        
        input(f"\n{Colors.YELLOW}按回车键返回主菜单...{Colors.NC}")
    
    def requirements_validation(self):
        """需求文档验证"""
        print_header("需求文档质量检查")
        
        req_file = self.project_root / "requires_docs" / "需求文档.md"
        if not req_file.exists():
            print_error("需求文档不存在!")
            print_info("请先创建 requires_docs/需求文档.md 文件")
            print_info("可以运行项目诊断工具自动创建模板")
            input(f"\n{Colors.YELLOW}按回车键返回主菜单...{Colors.NC}")
            return
        
        print_info("正在检查需求文档的质量和完整性...")
        
        tool_path = "scripts/validators/validate_requirements.py"
        success = self.run_tool(tool_path, "需求文档验证工具")
        
        if success:
            print_info("💡 建议查看生成的质量报告了解详细评估结果")
        
        input(f"\n{Colors.YELLOW}按回车键返回主菜单...{Colors.NC}")
    
    def quality_monitoring(self):
        """质量监控"""
        print_header("质量监控面板")
        print_info("正在分析项目进度、代码质量和申请成功率...")
        
        tool_path = "scripts/validators/quality_monitor.py"
        success = self.run_tool(tool_path, "质量监控工具")
        
        if success:
            print_info("💡 建议查看生成的 '质量监控报告.txt' 了解详细分析")
        
        input(f"\n{Colors.YELLOW}按回车键返回主菜单...{Colors.NC}")
    
    def code_merging(self):
        """代码合并"""
        print_header("代码合并工具")
        
        print_info("可用的合并选项:")
        print("1. 合并前端代码")
        print("2. 合并后端代码") 
        print("3. 合并数据库代码")
        print("4. 一键合并所有代码")
        print("0. 返回主菜单")
        
        while True:
            choice = input(f"\n{Colors.CYAN}请选择 (0-4): {Colors.NC}").strip()
            
            if choice == "0":
                return
            elif choice == "1":
                self.run_tool("scripts/generators/merge_frontend_simple.py", "前端代码合并")
                break
            elif choice == "2":
                self.run_tool("scripts/generators/merge_backend_simple.py", "后端代码合并")
                break
            elif choice == "3":
                self.run_tool("scripts/generators/merge_database_simple.py", "数据库代码合并")
                break
            elif choice == "4":
                self.run_tool("scripts/generators/merge_all_simple.py", "全部代码合并")
                break
            else:
                print_warning("无效选择，请输入 0-4")
        
        input(f"\n{Colors.YELLOW}按回车键返回主菜单...{Colors.NC}")
    
    def show_project_status(self):
        """显示项目状态"""
        print_header("项目状态概览")
        
        # 检查关键文件
        status_items = [
            ("配置文件", "ai-copyright-config.json"),
            ("需求文档", "requires_docs/需求文档.md"),
            ("框架设计", "process_docs/*框架设计文档.md"),
            ("页面清单", "process_docs/页面清单.md"),
            ("前端代码", "output_sourcecode/front/*.html"),
            ("后端代码", "output_sourcecode/backend/*"),
            ("数据库代码", "output_sourcecode/db/*.sql"),
            ("前端申请文档", "output_docs/前端源代码.txt"),
            ("后端申请文档", "output_docs/后端源代码.txt"),
            ("数据库申请文档", "output_docs/数据库源代码.txt")
        ]
        
        for name, pattern in status_items:
            if '*' in pattern:
                matches = list(self.project_root.glob(pattern))
                exists = len(matches) > 0
                if exists:
                    print_success(f"{name}: 已生成 ({len(matches)} 个文件)")
                else:
                    print_error(f"{name}: 未生成")
            else:
                file_path = self.project_root / pattern
                if file_path.exists():
                    size = file_path.stat().st_size
                    print_success(f"{name}: 已存在 ({size:,} 字节)")
                else:
                    print_error(f"{name}: 不存在")
        
        input(f"\n{Colors.YELLOW}按回车键返回主菜单...{Colors.NC}")
    
    def show_recommendations(self):
        """显示操作建议"""
        print_header("智能操作建议")
        
        # 简单的状态检查逻辑
        req_file = self.project_root / "requires_docs" / "需求文档.md"
        config_file = self.project_root / "ai-copyright-config.json"
        frontend_files = list(self.project_root.glob("output_sourcecode/front/*.html"))
        backend_files = list(self.project_root.glob("output_sourcecode/backend/*"))
        
        recommendations = []
        
        if not config_file.exists():
            recommendations.append("🔴 首先运行项目诊断工具修复配置问题")
        elif not req_file.exists():
            recommendations.append("🔴 创建并填写需求文档 (requires_docs/需求文档.md)")
        elif req_file.exists():
            try:
                with open(req_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                if len(content.strip()) < 500:
                    recommendations.append("🟡 需求文档内容偏少，建议运行质量检查工具")
                else:
                    recommendations.append("✅ 需求文档质量良好")
            except:
                pass
        
        if not frontend_files and not backend_files:
            recommendations.append("🔴 尚未生成代码，请按照工作流程开始生成")
        elif frontend_files or backend_files:
            merged_frontend = self.project_root / "output_docs" / "前端源代码.txt"
            merged_backend = self.project_root / "output_docs" / "后端源代码.txt"
            
            if not merged_frontend.exists() and frontend_files:
                recommendations.append("🟡 前端代码已生成，建议运行合并工具")
            if not merged_backend.exists() and backend_files:
                recommendations.append("🟡 后端代码已生成，建议运行合并工具")
            
            if merged_frontend.exists() and merged_backend.exists():
                recommendations.append("✅ 申请材料已准备就绪，可以提交申请")
        
        # 定期检查建议
        recommendations.append("💡 建议定期运行质量监控工具跟踪进度")
        recommendations.append("💡 遇到问题时可以运行项目诊断工具")
        
        for i, rec in enumerate(recommendations, 1):
            print(f"{i:2d}. {rec}")
        
        input(f"\n{Colors.YELLOW}按回车键返回主菜单...{Colors.NC}")
    
    def show_help(self):
        """显示帮助信息"""
        print_header("系统帮助文档")
        
        help_text = f"""
{Colors.BOLD}软著申请材料生成系统使用指南{Colors.NC}

{Colors.CYAN}1. 系统概述{Colors.NC}
   本系统使用AI技术自动生成软件著作权申请所需的全套材料，
   包括源代码文档、用户手册、登记信息表等。

{Colors.CYAN}2. 基本工作流程{Colors.NC}
   ① 项目初始化 → ② 填写需求文档 → ③ 生成代码 → ④ 合并申请材料

{Colors.CYAN}3. 主要功能说明{Colors.NC}
   
   🏥 项目诊断: 检查项目完整性，自动修复配置问题
   📝 质量检查: 验证需求文档质量，提供改进建议  
   📊 质量监控: 实时监控生成进度和代码质量
   🔧 代码合并: 将生成的代码整理为申请文档格式

{Colors.CYAN}4. 文件结构说明{Colors.NC}
   
   requires_docs/     - 用户输入的需求文档
   process_docs/      - 中间生成的设计文档
   output_sourcecode/ - AI生成的源代码
   output_docs/       - 最终的申请材料文档
   scripts/           - 系统工具脚本

{Colors.CYAN}5. 使用技巧{Colors.NC}
   
   • 详细填写需求文档可以显著提升生成质量
   • 定期运行质量检查工具确保文档合规
   • 遇到问题优先使用项目诊断工具
   • 生成完成后及时运行合并工具

{Colors.CYAN}6. 常见问题解决{Colors.NC}
   
   • 配置文件错误 → 运行项目诊断工具
   • 脚本权限问题 → 项目诊断工具会自动修复
   • 生成质量不佳 → 改进需求文档后重新生成
   • 文件缺失问题 → 检查目录结构和权限设置

{Colors.CYAN}7. 联系支持{Colors.NC}
   
   如遇到技术问题，请保存诊断报告并联系技术支持。
"""
        
        print(help_text)
        input(f"\n{Colors.YELLOW}按回车键返回主菜单...{Colors.NC}")
    
    def run(self):
        """运行用户指导系统"""
        while True:
            try:
                self.show_main_menu()
                choice = input(f"\n{Colors.CYAN}请选择操作 (0-7): {Colors.NC}").strip()
                
                if choice == "0":
                    print_header("感谢使用软著申请材料生成系统")
                    print_success("祝您申请顺利！")
                    break
                elif choice == "1":
                    self.project_diagnosis()
                elif choice == "2":
                    self.requirements_validation()
                elif choice == "3":
                    self.quality_monitoring()
                elif choice == "4":
                    self.code_merging()
                elif choice == "5":
                    self.show_project_status()
                elif choice == "6":
                    self.show_recommendations()
                elif choice == "7":
                    self.show_help()
                else:
                    print_warning("无效选择，请输入 0-7")
                    input(f"\n{Colors.YELLOW}按回车键继续...{Colors.NC}")
                    
            except KeyboardInterrupt:
                print(f"\n\n{Colors.YELLOW}用户中断操作{Colors.NC}")
                print_success("感谢使用！")
                break
            except Exception as e:
                print_error(f"发生错误: {e}")
                input(f"\n{Colors.YELLOW}按回车键继续...{Colors.NC}")

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("软著申请材料生成系统 - 用户指导工具")
        print("\n用法:")
        print("  python3 user_guide.py")
        print("\n功能:")
        print("  提供交互式用户界面，简化软著申请材料生成流程")
        print("  集成所有系统工具，提供一站式操作体验")
        print("\n特点:")
        print("  - 友好的交互式菜单")
        print("  - 智能操作建议")
        print("  - 一键工具调用")
        print("  - 实时状态反馈")
        return
    
    # 运行用户指导系统
    guide = UserGuide()
    guide.run()

if __name__ == "__main__":
    main()