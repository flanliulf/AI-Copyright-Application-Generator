#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
导航一致性检查工具 (简化版)
版本: 1.0
描述: 检查所有前端页面的导航元素一致性，确保导航结构统一
"""

import os
import sys
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

class SimpleNavigationChecker:
    """简化的导航一致性检查器"""
    
    def __init__(self):
        self.project_root = project_root
        self.front_dir = self.project_root / "output_sourcecode" / "front"
        self.pages_data = {}
        
    def check_all(self):
        """执行所有导航一致性检查"""
        print_message(Colors.BOLD + Colors.CYAN, "🔍 导航一致性检查工具 (简化版)")
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
        all_passed &= self.check_navigation_links()
        all_passed &= self.check_css_consistency()
        
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
                    
                    # 提取导航相关信息
                    page_data = {
                        'file': html_file.name,
                        'path': str(html_file),
                        'has_header': self.has_header_nav(content),
                        'has_sidebar': self.has_sidebar_nav(content),
                        'has_breadcrumb': self.has_breadcrumb_nav(content),
                        'nav_links': self.extract_nav_links(content),
                        'nav_css_classes': self.extract_nav_css_classes(content),
                        'nav_structure': self.extract_nav_structure(content)
                    }
                    
                    self.pages_data[html_file.name] = page_data
                    
            except Exception as e:
                print_error(f"解析页面失败 {html_file.name}: {e}")
                
    def has_header_nav(self, content):
        """检查是否有头部导航"""
        header_patterns = [
            r'<header[^>]*>',
            r'class=["\'][^"\']*header[^"\']*["\']',
            r'id=["\'][^"\']*header[^"\']*["\']',
            r'<nav[^>]*>'
        ]
        return any(re.search(pattern, content, re.IGNORECASE) for pattern in header_patterns)
        
    def has_sidebar_nav(self, content):
        """检查是否有侧边栏导航"""
        sidebar_patterns = [
            r'<aside[^>]*>',
            r'class=["\'][^"\']*sidebar[^"\']*["\']',
            r'id=["\'][^"\']*sidebar[^"\']*["\']',
            r'class=["\'][^"\']*nav[^"\']*["\']'
        ]
        return any(re.search(pattern, content, re.IGNORECASE) for pattern in sidebar_patterns)
        
    def has_breadcrumb_nav(self, content):
        """检查是否有面包屑导航"""
        breadcrumb_patterns = [
            r'class=["\'][^"\']*breadcrumb[^"\']*["\']',
            r'id=["\'][^"\']*breadcrumb[^"\']*["\']',
            r'aria-label=["\'][^"\']*breadcrumb[^"\']*["\']'
        ]
        return any(re.search(pattern, content, re.IGNORECASE) for pattern in breadcrumb_patterns)
        
    def extract_nav_links(self, content):
        """提取导航链接"""
        # 查找HTML文件链接
        link_pattern = r'href=["\']([^"\']*\.html)["\']'
        links = re.findall(link_pattern, content)
        
        # 过滤掉外部链接和锚链接
        internal_links = []
        for link in links:
            if not link.startswith('http') and not link.startswith('#'):
                # 获取文件名
                filename = link.split('/')[-1]
                internal_links.append(filename)
                
        return list(set(internal_links))  # 去重
        
    def extract_nav_css_classes(self, content):
        """提取导航相关的CSS类"""
        nav_keywords = ['nav', 'menu', 'header', 'sidebar', 'breadcrumb']
        nav_classes = []
        
        # 查找class属性
        class_pattern = r'class=["\']([^"\']*)["\']'
        class_matches = re.findall(class_pattern, content)
        
        for classes in class_matches:
            class_list = classes.split()
            for cls in class_list:
                if any(keyword in cls.lower() for keyword in nav_keywords):
                    nav_classes.append(cls)
                    
        return list(set(nav_classes))  # 去重
        
    def extract_nav_structure(self, content):
        """提取导航结构特征"""
        structure = {
            'header_count': len(re.findall(r'<header[^>]*>', content, re.IGNORECASE)),
            'nav_count': len(re.findall(r'<nav[^>]*>', content, re.IGNORECASE)),
            'aside_count': len(re.findall(r'<aside[^>]*>', content, re.IGNORECASE)),
            'menu_class_count': len(re.findall(r'class=["\'][^"\']*menu[^"\']*["\']', content, re.IGNORECASE))
        }
        return structure
        
    def check_header_consistency(self):
        """检查头部导航一致性"""
        print_info("检查头部导航一致性...")
        
        pages_with_header = [name for name, data in self.pages_data.items() if data['has_header']]
        pages_without_header = [name for name, data in self.pages_data.items() if not data['has_header']]
        
        if pages_without_header:
            for page in pages_without_header:
                print_error(f"  {page}: 缺少头部导航")
            return False
        elif pages_with_header:
            print_success(f"所有 {len(pages_with_header)} 个页面都包含头部导航")
            return True
        else:
            print_warning("未检测到任何头部导航")
            return True
            
    def check_sidebar_consistency(self):
        """检查侧边栏一致性"""
        print_info("检查侧边栏导航一致性...")
        
        pages_with_sidebar = [name for name, data in self.pages_data.items() if data['has_sidebar']]
        pages_without_sidebar = [name for name, data in self.pages_data.items() if not data['has_sidebar']]
        
        # 如果大部分页面都有侧边栏，那么没有侧边栏的页面可能有问题
        total_pages = len(self.pages_data)
        sidebar_ratio = len(pages_with_sidebar) / total_pages if total_pages > 0 else 0
        
        if sidebar_ratio > 0.5 and pages_without_sidebar:
            for page in pages_without_sidebar:
                print_warning(f"  {page}: 可能缺少侧边栏导航")
            return True  # 这是警告，不是错误
        elif pages_with_sidebar:
            print_success(f"{len(pages_with_sidebar)} 个页面包含侧边栏导航")
            return True
        else:
            print_info("未检测到侧边栏导航")
            return True
            
    def check_navigation_links(self):
        """检查导航链接有效性"""
        print_info("检查导航链接有效性...")
        
        all_files = set(data['file'] for data in self.pages_data.values())
        issues = []
        
        for page_name, page_data in self.pages_data.items():
            for link in page_data['nav_links']:
                if link not in all_files:
                    issues.append(f"{page_name}: 导航链接指向不存在的文件 '{link}'")
                    
        if issues:
            for issue in issues:
                print_error(f"  {issue}")
            return False
        else:
            print_success("所有导航链接有效")
            return True
            
    def check_css_consistency(self):
        """检查CSS类名一致性"""
        print_info("检查导航CSS类名一致性...")
        
        # 收集所有导航CSS类
        all_nav_classes = set()
        for page_data in self.pages_data.values():
            all_nav_classes.update(page_data['nav_css_classes'])
            
        if not all_nav_classes:
            print_warning("未找到导航相关的CSS类")
            return True
            
        # 检查每个页面的CSS类使用情况
        reference_classes = all_nav_classes
        issues = []
        
        for page_name, page_data in self.pages_data.items():
            page_classes = set(page_data['nav_css_classes'])
            
            # 如果页面缺少太多公共导航类，可能有问题
            missing_ratio = len(reference_classes - page_classes) / len(reference_classes) if reference_classes else 0
            
            if missing_ratio > 0.7:  # 缺少超过70%的导航类
                issues.append(f"{page_name}: 导航CSS类可能不完整")
                
        if issues:
            for issue in issues:
                print_warning(f"  {issue}")
            return True  # 这是警告，不是错误
        else:
            print_success("导航CSS类名使用一致")
            return True
            
    def print_summary(self, all_passed):
        """打印检查结果摘要"""
        print_message(Colors.CYAN, "=" * 60)
        
        if all_passed:
            print_success("🎉 导航一致性检查通过！")
            print_info("页面导航结构基本一致，符合基本质量要求")
        else:
            print_error("❌ 发现导航一致性问题")
            print_warning("请修复上述问题以确保导航的一致性")
            print_info("建议：")
            print("  1. 确保所有页面使用相同的导航组件")
            print("  2. 检查导航链接的有效性")
            print("  3. 统一导航相关的CSS类名")
            print("  4. 确认导航结构的完整性")
            
        print_message(Colors.CYAN, "=" * 60)

def main():
    """主函数"""
    try:
        checker = SimpleNavigationChecker()
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