#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
导航一致性检查工具
版本: 1.0
描述: 检查所有前端页面的导航元素一致性，确保导航结构统一
"""

import os
import sys
import json
import re
from pathlib import Path
import html.parser
import difflib

class SimpleHTMLParser(html.parser.HTMLParser):
    """简单的HTML解析器，用于提取导航结构"""
    
    def __init__(self):
        super().__init__()
        self.current_tag = None
        self.nav_elements = []
        self.current_element = None
        self.nav_tags = {'header', 'nav', 'aside', 'div'}
        self.nav_classes = {'header', 'navigation', 'nav', 'sidebar', 'breadcrumb', 'menu'}
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = attrs_dict.get('class', '').split()
        element_id = attrs_dict.get('id', '')
        
        # 检查是否是导航相关元素
        if (tag in self.nav_tags or 
            any(nav_class in classes for nav_class in self.nav_classes) or
            any(nav_class in element_id.lower() for nav_class in self.nav_classes)):
            
            self.current_element = {
                'tag': tag,
                'classes': classes,
                'id': element_id,
                'attrs': attrs_dict
            }
            
    def handle_endtag(self, tag):
        if self.current_element and self.current_element['tag'] == tag:
            self.nav_elements.append(self.current_element)
            self.current_element = None

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

class NavigationConsistencyChecker:
    """导航一致性检查器"""
    
    def __init__(self):
        self.project_root = project_root
        self.front_dir = self.project_root / "output_sourcecode" / "front"
        self.navigation_issues = []
        self.pages_data = {}
        
    def check_all(self):
        """执行所有导航一致性检查"""
        print_message(Colors.BOLD + Colors.CYAN, "🔍 导航一致性检查工具")
        print_message(Colors.CYAN, "=" * 60)
        
        if not self.front_dir.exists():
            print_error(f"前端页面目录不存在: {self.front_dir}")
            return False
            
        # 获取所有HTML文件
        html_files = list(self.front_dir.glob("*.html"))
        if not html_files:
            print_error("未找到任何HTML页面文件")
            return False
            
        print_info(f"找到 {len(html_files)} 个HTML页面文件")
        
        # 解析所有页面
        self.parse_all_pages(html_files)
        
        # 执行各项检查
        all_passed = True
        all_passed &= self.check_header_consistency()
        all_passed &= self.check_sidebar_consistency()
        all_passed &= self.check_breadcrumb_consistency()
        all_passed &= self.check_navigation_links()
        all_passed &= self.check_css_class_consistency()
        all_passed &= self.check_javascript_consistency()
        
        # 输出检查结果
        self.print_summary(all_passed)
        return all_passed
        
    def parse_all_pages(self, html_files):
        """解析所有页面的导航结构"""
        print_info("解析页面导航结构...")
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # 使用简单的正则表达式和字符串匹配来提取导航结构
                    page_data = {
                        'file': html_file.name,
                        'path': str(html_file),
                        'header': self.extract_header_structure(content),
                        'sidebar': self.extract_sidebar_structure(content),
                        'breadcrumb': self.extract_breadcrumb_structure(content),
                        'navigation_links': self.extract_navigation_links(content),
                        'css_classes': self.extract_navigation_css_classes(content),
                        'javascript': self.extract_navigation_javascript(content)
                    }
                    
                    self.pages_data[html_file.name] = page_data
                    
            except Exception as e:
                print_error(f"解析页面失败 {html_file.name}: {e}")
                
    def extract_header_structure(self, soup):
        """提取头部导航结构"""
        header_selectors = ['header', '.header', '.app-header', '#header', '#app-header']
        
        for selector in header_selectors:
            header = soup.select_one(selector)
            if header:
                return {
                    'tag': header.name,
                    'classes': header.get('class', []),
                    'id': header.get('id', ''),
                    'structure': self.get_element_structure(header),
                    'menu_items': self.extract_menu_items(header)
                }
        return None
        
    def extract_sidebar_structure(self, soup):
        """提取侧边栏导航结构"""
        sidebar_selectors = ['.sidebar', '.app-sidebar', '#sidebar', '#app-sidebar', 'aside']
        
        for selector in sidebar_selectors:
            sidebar = soup.select_one(selector)
            if sidebar:
                return {
                    'tag': sidebar.name,
                    'classes': sidebar.get('class', []),
                    'id': sidebar.get('id', ''),
                    'structure': self.get_element_structure(sidebar),
                    'menu_items': self.extract_menu_items(sidebar)
                }
        return None
        
    def extract_breadcrumb_structure(self, soup):
        """提取面包屑导航结构"""
        breadcrumb_selectors = ['.breadcrumb', '.breadcrumb-nav', '#breadcrumb', 'nav[aria-label*="breadcrumb"]']
        
        for selector in breadcrumb_selectors:
            breadcrumb = soup.select_one(selector)
            if breadcrumb:
                return {
                    'tag': breadcrumb.name,
                    'classes': breadcrumb.get('class', []),
                    'id': breadcrumb.get('id', ''),
                    'structure': self.get_element_structure(breadcrumb),
                    'items': self.extract_breadcrumb_items(breadcrumb)
                }
        return None
        
    def extract_navigation_links(self, soup):
        """提取导航链接"""
        links = []
        nav_areas = soup.select('header a, .sidebar a, .breadcrumb a, nav a')
        
        for link in nav_areas:
            href = link.get('href', '')
            if href and not href.startswith('#') and not href.startswith('http'):
                links.append({
                    'href': href,
                    'text': link.get_text(strip=True),
                    'classes': link.get('class', [])
                })
        return links
        
    def extract_navigation_css_classes(self, soup):
        """提取导航相关的CSS类名"""
        nav_classes = set()
        nav_elements = soup.select('header, header *, .sidebar, .sidebar *, .breadcrumb, .breadcrumb *, nav, nav *')
        
        for element in nav_elements:
            classes = element.get('class', [])
            nav_classes.update(classes)
            
        return sorted(list(nav_classes))
        
    def extract_navigation_javascript(self, content):
        """提取导航相关的JavaScript"""
        # 查找导航相关的JavaScript代码
        js_patterns = [
            r'navigation|Navigation',
            r'sidebar|Sidebar',
            r'menu|Menu',
            r'breadcrumb|Breadcrumb'
        ]
        
        js_found = []
        for pattern in js_patterns:
            matches = re.findall(rf'{pattern}[^;]*', content, re.IGNORECASE)
            js_found.extend(matches)
            
        return js_found
        
    def get_element_structure(self, element):
        """获取元素的结构特征"""
        if not element:
            return None
            
        return {
            'tag': element.name,
            'classes': element.get('class', []),
            'id': element.get('id', ''),
            'children_count': len(element.find_all()),
            'children_tags': [child.name for child in element.children if hasattr(child, 'name') and child.name]
        }
        
    def extract_menu_items(self, nav_element):
        """提取菜单项"""
        if not nav_element:
            return []
            
        menu_items = []
        links = nav_element.find_all('a')
        
        for link in links:
            menu_items.append({
                'href': link.get('href', ''),
                'text': link.get_text(strip=True),
                'classes': link.get('class', [])
            })
            
        return menu_items
        
    def extract_breadcrumb_items(self, breadcrumb_element):
        """提取面包屑项"""
        if not breadcrumb_element:
            return []
            
        items = []
        links = breadcrumb_element.find_all(['a', 'span', 'li'])
        
        for item in links:
            items.append({
                'tag': item.name,
                'href': item.get('href', '') if item.name == 'a' else '',
                'text': item.get_text(strip=True),
                'classes': item.get('class', [])
            })
            
        return items
        
    def check_header_consistency(self):
        """检查头部导航一致性"""
        print_info("检查头部导航一致性...")
        
        headers = [page['header'] for page in self.pages_data.values() if page['header']]
        
        if not headers:
            print_error("未找到任何头部导航结构")
            return False
            
        # 检查结构一致性
        reference_header = headers[0]
        issues = []
        
        for page_name, page_data in self.pages_data.items():
            header = page_data['header']
            if not header:
                issues.append(f"{page_name}: 缺少头部导航")
                continue
                
            # 检查基本结构
            if header['tag'] != reference_header['tag']:
                issues.append(f"{page_name}: 头部标签不一致 ({header['tag']} vs {reference_header['tag']})")
                
            if set(header['classes']) != set(reference_header['classes']):
                issues.append(f"{page_name}: 头部CSS类不一致")
                
            # 检查菜单项数量
            if len(header['menu_items']) != len(reference_header['menu_items']):
                issues.append(f"{page_name}: 头部菜单项数量不一致")
                
        if issues:
            for issue in issues:
                print_error(f"  {issue}")
            return False
        else:
            print_success("头部导航结构一致")
            return True
            
    def check_sidebar_consistency(self):
        """检查侧边栏一致性"""
        print_info("检查侧边栏导航一致性...")
        
        sidebars = [page['sidebar'] for page in self.pages_data.values() if page['sidebar']]
        
        if not sidebars:
            print_warning("未找到侧边栏导航结构")
            return True  # 如果没有侧边栏，不算错误
            
        # 检查结构一致性
        reference_sidebar = sidebars[0]
        issues = []
        
        for page_name, page_data in self.pages_data.items():
            sidebar = page_data['sidebar']
            if not sidebar and sidebars:
                issues.append(f"{page_name}: 缺少侧边栏导航")
                continue
                
            if sidebar:
                # 检查基本结构
                if sidebar['tag'] != reference_sidebar['tag']:
                    issues.append(f"{page_name}: 侧边栏标签不一致")
                    
                if set(sidebar['classes']) != set(reference_sidebar['classes']):
                    issues.append(f"{page_name}: 侧边栏CSS类不一致")
                    
        if issues:
            for issue in issues:
                print_error(f"  {issue}")
            return False
        else:
            print_success("侧边栏导航结构一致")
            return True
            
    def check_breadcrumb_consistency(self):
        """检查面包屑一致性"""
        print_info("检查面包屑导航一致性...")
        
        breadcrumbs = [page['breadcrumb'] for page in self.pages_data.values() if page['breadcrumb']]
        
        if not breadcrumbs:
            print_warning("未找到面包屑导航结构")
            return True  # 如果没有面包屑，不算错误
            
        # 检查结构一致性
        reference_breadcrumb = breadcrumbs[0]
        issues = []
        
        for page_name, page_data in self.pages_data.items():
            breadcrumb = page_data['breadcrumb']
            if not breadcrumb and breadcrumbs:
                issues.append(f"{page_name}: 缺少面包屑导航")
                continue
                
            if breadcrumb:
                # 检查基本结构
                if breadcrumb['tag'] != reference_breadcrumb['tag']:
                    issues.append(f"{page_name}: 面包屑标签不一致")
                    
                if set(breadcrumb['classes']) != set(reference_breadcrumb['classes']):
                    issues.append(f"{page_name}: 面包屑CSS类不一致")
                    
        if issues:
            for issue in issues:
                print_error(f"  {issue}")
            return False
        else:
            print_success("面包屑导航结构一致")
            return True
            
    def check_navigation_links(self):
        """检查导航链接有效性"""
        print_info("检查导航链接有效性...")
        
        issues = []
        all_files = set(page_data['file'] for page_data in self.pages_data.values())
        
        for page_name, page_data in self.pages_data.items():
            for link in page_data['navigation_links']:
                href = link['href']
                if href.endswith('.html'):
                    # 检查相对路径
                    target_file = href.split('/')[-1]  # 获取文件名
                    if target_file not in all_files:
                        issues.append(f"{page_name}: 导航链接指向不存在的文件 '{href}'")
                        
        if issues:
            for issue in issues:
                print_error(f"  {issue}")
            return False
        else:
            print_success("所有导航链接有效")
            return True
            
    def check_css_class_consistency(self):
        """检查CSS类名一致性"""
        print_info("检查导航CSS类名一致性...")
        
        # 收集所有页面的导航CSS类
        all_nav_classes = set()
        for page_data in self.pages_data.values():
            all_nav_classes.update(page_data['css_classes'])
            
        # 检查每个页面是否包含核心导航类
        core_nav_classes = {
            'header', 'app-header', 'nav', 'navigation',
            'sidebar', 'app-sidebar', 'menu',
            'breadcrumb', 'breadcrumb-nav'
        }
        
        issues = []
        for page_name, page_data in self.pages_data.items():
            page_classes = set(page_data['css_classes'])
            missing_core_classes = core_nav_classes - page_classes
            
            # 如果页面缺少太多核心导航类，可能存在问题
            if len(missing_core_classes) > len(core_nav_classes) * 0.7:
                issues.append(f"{page_name}: 可能缺少导航相关的CSS类")
                
        if issues:
            for issue in issues:
                print_warning(f"  {issue}")
            return True  # 这是警告，不是错误
        else:
            print_success("导航CSS类名使用合理")
            return True
            
    def check_javascript_consistency(self):
        """检查JavaScript一致性"""
        print_info("检查导航JavaScript一致性...")
        
        # 这是一个简化的检查，主要确保页面包含导航相关的JavaScript
        issues = []
        
        for page_name, page_data in self.pages_data.items():
            js_code = page_data['javascript']
            if not js_code:
                issues.append(f"{page_name}: 可能缺少导航相关的JavaScript代码")
                
        if issues:
            for issue in issues:
                print_warning(f"  {issue}")
            return True  # 这是警告，不是错误
        else:
            print_success("导航JavaScript代码存在")
            return True
            
    def print_summary(self, all_passed):
        """打印检查结果摘要"""
        print_message(Colors.CYAN, "=" * 60)
        
        if all_passed:
            print_success("🎉 所有导航一致性检查通过！")
            print_info("页面导航结构完全一致，符合软著申请质量要求")
        else:
            print_error("❌ 发现导航一致性问题")
            print_warning("请修复上述问题以确保导航的一致性")
            print_info("建议：")
            print("  1. 确保所有页面使用相同的导航组件模板")
            print("  2. 检查CSS类名和ID的一致性")
            print("  3. 验证所有导航链接的有效性")
            print("  4. 确认当前页面在导航中的正确标识")
            
        print_message(Colors.CYAN, "=" * 60)

def main():
    """主函数"""
    try:
        checker = NavigationConsistencyChecker()
        success = checker.check_all()
        
        # 返回适当的退出码
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print_error(f"检查过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()