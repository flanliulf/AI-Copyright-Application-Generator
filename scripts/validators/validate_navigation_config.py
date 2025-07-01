#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
导航配置验证工具
版本: 1.0
描述: 验证导航架构配置文档的完整性和正确性
"""

import os
import sys
import json
import re
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

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

class NavigationConfigValidator:
    """导航配置验证器"""
    
    def __init__(self):
        self.project_root = project_root
        self.config_file = self.project_root / "process_docs" / "导航架构配置.md"
        self.page_list_file = self.project_root / "process_docs" / "页面清单.md"
        self.issues = []
        
    def validate_all(self):
        """执行所有验证检查"""
        print_message(Colors.BOLD + Colors.CYAN, "🔍 导航配置验证工具")
        print_message(Colors.CYAN, "=" * 60)
        
        # 检查配置文件是否存在
        if not self.config_file.exists():
            print_error(f"导航配置文件不存在: {self.config_file}")
            return False
            
        # 读取配置文件
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config_content = f.read()
        except Exception as e:
            print_error(f"读取导航配置文件失败: {e}")
            return False
            
        # 读取页面清单文件
        if self.page_list_file.exists():
            try:
                with open(self.page_list_file, 'r', encoding='utf-8') as f:
                    self.page_list_content = f.read()
            except Exception as e:
                print_warning(f"读取页面清单文件失败: {e}")
                self.page_list_content = ""
        else:
            print_warning("页面清单文件不存在，将跳过相关验证")
            self.page_list_content = ""
            
        # 执行各项验证
        all_passed = True
        all_passed &= self.validate_config_structure()
        all_passed &= self.validate_navigation_json()
        all_passed &= self.validate_route_mapping()
        all_passed &= self.validate_component_templates()
        all_passed &= self.validate_css_javascript_specs()
        all_passed &= self.validate_page_consistency()
        
        # 输出验证结果
        self.print_summary(all_passed)
        return all_passed
        
    def validate_config_structure(self):
        """验证配置文档结构"""
        print_info("验证导航配置文档结构...")
        
        required_sections = [
            "系统导航架构配置",
            "主导航结构",
            "侧边栏导航结构", 
            "面包屑导航配置",
            "页面路由映射表",
            "导航状态管理规范",
            "导航HTML组件模板"
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in self.config_content:
                missing_sections.append(section)
                
        if missing_sections:
            for section in missing_sections:
                print_error(f"  缺少必需章节: {section}")
            return False
        else:
            print_success("配置文档结构完整")
            return True
            
    def validate_navigation_json(self):
        """验证导航JSON配置"""
        print_info("验证导航JSON配置...")
        
        # 查找JSON配置块
        json_pattern = r'```json\s*(\{.*?\})\s*```'
        json_matches = re.findall(json_pattern, self.config_content, re.DOTALL)
        
        if not json_matches:
            print_error("未找到导航JSON配置")
            return False
            
        valid_json_count = 0
        for i, json_str in enumerate(json_matches):
            try:
                config = json.loads(json_str)
                
                # 验证主导航配置
                if 'header' in config:
                    if self.validate_header_config(config['header']):
                        valid_json_count += 1
                        
                # 验证侧边栏配置
                if 'sidebar' in config:
                    if self.validate_sidebar_config(config['sidebar']):
                        valid_json_count += 1
                        
                # 验证面包屑配置
                if 'breadcrumbs' in config:
                    if self.validate_breadcrumb_config(config['breadcrumbs']):
                        valid_json_count += 1
                        
            except json.JSONDecodeError as e:
                print_error(f"  JSON配置 {i+1} 格式错误: {e}")
                
        if valid_json_count > 0:
            print_success(f"找到 {valid_json_count} 个有效的JSON配置")
            return True
        else:
            print_error("未找到有效的JSON配置")
            return False
            
    def validate_header_config(self, header_config):
        """验证头部导航配置"""
        required_fields = ['logo', 'mainMenu', 'userMenu']
        
        for field in required_fields:
            if field not in header_config:
                print_error(f"  头部配置缺少字段: {field}")
                return False
                
        # 验证主菜单结构
        if 'mainMenu' in header_config and isinstance(header_config['mainMenu'], list):
            for menu_item in header_config['mainMenu']:
                if not all(key in menu_item for key in ['id', 'label', 'route']):
                    print_error("  主菜单项缺少必需字段 (id, label, route)")
                    return False
                    
        return True
        
    def validate_sidebar_config(self, sidebar_config):
        """验证侧边栏配置"""
        required_fields = ['collapsible', 'sections']
        
        for field in required_fields:
            if field not in sidebar_config:
                print_error(f"  侧边栏配置缺少字段: {field}")
                return False
                
        # 验证菜单项结构
        if 'sections' in sidebar_config and isinstance(sidebar_config['sections'], list):
            for section in sidebar_config['sections']:
                if 'items' in section and isinstance(section['items'], list):
                    for item in section['items']:
                        if not all(key in item for key in ['id', 'label', 'route']):
                            print_error("  侧边栏菜单项缺少必需字段 (id, label, route)")
                            return False
                            
        return True
        
    def validate_breadcrumb_config(self, breadcrumb_config):
        """验证面包屑配置"""
        if not isinstance(breadcrumb_config, dict):
            print_error("  面包屑配置格式错误")
            return False
            
        # 检查是否有路径映射
        if not breadcrumb_config:
            print_warning("  面包屑配置为空")
            return True
            
        # 验证路径映射格式
        for path, breadcrumb in breadcrumb_config.items():
            if not isinstance(breadcrumb, list):
                print_error(f"  面包屑路径 {path} 配置格式错误")
                return False
                
            for item in breadcrumb:
                if not all(key in item for key in ['label', 'route']):
                    print_error(f"  面包屑项 {path} 缺少必需字段 (label, route)")
                    return False
                    
        return True
        
    def validate_route_mapping(self):
        """验证路由映射表"""
        print_info("验证页面路由映射表...")
        
        # 查找路由映射表
        table_pattern = r'\|[^|]*页面名称[^|]*\|[^|]*路由路径[^|]*\|.*?\n(\|.*?\n)+'
        table_match = re.search(table_pattern, self.config_content)
        
        if not table_match:
            print_error("未找到页面路由映射表")
            return False
            
        # 解析表格内容
        table_content = table_match.group(0)
        rows = [row.strip() for row in table_content.split('\n') if row.strip().startswith('|')]
        
        if len(rows) < 3:  # 至少要有表头、分隔符、一行数据
            print_error("路由映射表内容不足")
            return False
            
        print_success(f"找到路由映射表，包含 {len(rows)-2} 个页面路由")
        return True
        
    def validate_component_templates(self):
        """验证组件模板"""
        print_info("验证导航组件模板...")
        
        required_templates = [
            "Header组件模板",
            "Sidebar组件模板", 
            "Breadcrumb组件模板"
        ]
        
        missing_templates = []
        for template in required_templates:
            if template not in self.config_content:
                missing_templates.append(template)
                
        # 查找HTML代码块
        html_pattern = r'```html\s*(.*?)\s*```'
        html_matches = re.findall(html_pattern, self.config_content, re.DOTALL)
        
        if not html_matches:
            print_error("未找到HTML组件模板")
            return False
            
        valid_templates = 0
        for html_code in html_matches:
            if any(tag in html_code.lower() for tag in ['header', 'aside', 'nav']):
                valid_templates += 1
                
        if missing_templates:
            for template in missing_templates:
                print_warning(f"  缺少模板: {template}")
                
        if valid_templates > 0:
            print_success(f"找到 {valid_templates} 个HTML组件模板")
            return True
        else:
            print_error("未找到有效的HTML组件模板")
            return False
            
    def validate_css_javascript_specs(self):
        """验证CSS和JavaScript规范"""
        print_info("验证CSS和JavaScript规范...")
        
        # 查找CSS类名规范
        css_pattern = r'CSS类名|class|className'
        css_found = re.search(css_pattern, self.config_content, re.IGNORECASE)
        
        # 查找JavaScript规范
        js_pattern = r'JavaScript|javascript|js|Navigation.*Controller'
        js_found = re.search(js_pattern, self.config_content, re.IGNORECASE)
        
        issues = []
        if not css_found:
            issues.append("缺少CSS类名规范说明")
            
        if not js_found:
            issues.append("缺少JavaScript交互规范说明")
            
        if issues:
            for issue in issues:
                print_warning(f"  {issue}")
            return True  # 这些是警告，不是错误
        else:
            print_success("CSS和JavaScript规范说明完整")
            return True
            
    def validate_page_consistency(self):
        """验证与页面清单的一致性"""
        print_info("验证与页面清单的一致性...")
        
        if not self.page_list_content:
            print_warning("无法验证页面一致性：页面清单文件不存在")
            return True
            
        # 从页面清单中提取页面名称
        page_pattern = r'(?:#+\s*)?(\d+\.\s*)?([^#\n]+?)(?:页面|页|Page)'
        page_matches = re.findall(page_pattern, self.page_list_content)
        
        if not page_matches:
            print_warning("未能从页面清单中识别页面名称")
            return True
            
        page_names = [match[1].strip() for match in page_matches if match[1].strip()]
        
        # 检查导航配置中是否包含这些页面
        missing_pages = []
        for page_name in page_names:
            if page_name not in self.config_content:
                missing_pages.append(page_name)
                
        if missing_pages:
            for page in missing_pages:
                print_warning(f"  导航配置中可能缺少页面: {page}")
            return True  # 这是警告，不是错误
        else:
            print_success(f"导航配置与页面清单一致 (检查了 {len(page_names)} 个页面)")
            return True
            
    def print_summary(self, all_passed):
        """打印验证结果摘要"""
        print_message(Colors.CYAN, "=" * 60)
        
        if all_passed:
            print_success("🎉 导航配置验证通过！")
            print_info("导航架构配置完整，可以开始页面代码生成")
        else:
            print_error("❌ 发现导航配置问题")
            print_warning("请修复上述问题后再进行页面代码生成")
            print_info("建议：")
            print("  1. 补充缺少的配置章节")
            print("  2. 修复JSON配置格式错误")
            print("  3. 完善组件模板定义")
            print("  4. 确保路由映射表完整")
            
        print_message(Colors.CYAN, "=" * 60)

def main():
    """主函数"""
    try:
        validator = NavigationConfigValidator()
        success = validator.validate_all()
        
        # 返回适当的退出码
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print_error(f"验证过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()