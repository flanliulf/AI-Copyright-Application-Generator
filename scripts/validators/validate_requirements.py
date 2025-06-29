#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
需求文档质量检查工具
功能：验证需求文档的完整性、质量和规范性，确保AI生成高质量的软著申请材料

检查维度：
1. 文档长度和内容充实度
2. 功能模块完整性
3. 用户角色定义
4. 业务流程描述
5. 技术要求明确性
6. 关键字密度和专业术语使用
"""

import os
import sys
import json
import re
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
    print(f"{Colors.PURPLE}{'=' * 80}{Colors.NC}")
    print(f"{Colors.PURPLE}{message.center(80)}{Colors.NC}")
    print(f"{Colors.PURPLE}{'=' * 80}{Colors.NC}")

class RequirementsValidator:
    """需求文档验证器"""
    
    def __init__(self):
        self.requirements_path = Path("requires_docs/需求文档.md")
        self.config_path = Path("ai-copyright-config.json")
        self.validation_results = []
        self.warnings = []
        self.recommendations = []
        
    def load_config(self) -> Optional[dict]:
        """加载项目配置"""
        if not self.config_path.exists():
            self.add_error("配置文件不存在: ai-copyright-config.json")
            return None
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.add_error(f"配置文件读取失败: {e}")
            return None
    
    def load_requirements(self) -> Optional[str]:
        """加载需求文档"""
        if not self.requirements_path.exists():
            self.add_error("需求文档不存在: requires_docs/需求文档.md")
            return None
        
        try:
            with open(self.requirements_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.add_error(f"需求文档读取失败: {e}")
            return None
    
    def add_success(self, message: str):
        self.validation_results.append(('success', message))
    
    def add_warning(self, message: str):
        self.validation_results.append(('warning', message))
        self.warnings.append(message)
    
    def add_error(self, message: str):
        self.validation_results.append(('error', message))
    
    def add_recommendation(self, message: str):
        self.recommendations.append(message)
    
    def validate_document_length(self, content: str, config: dict) -> Dict[str, any]:
        """验证文档长度"""
        # 统计字符数和词数
        char_count = len(content)
        word_count = len(content.split())
        chinese_char_count = len(re.findall(r'[\u4e00-\u9fa5]', content))
        
        generation_mode = config.get('generation_mode', 'fast')
        
        # 根据生成模式设定标准
        if generation_mode == 'fast':
            min_chars = 500
            recommended_chars = 1000
            min_words = 100
        else:  # full mode
            min_chars = 1500
            recommended_chars = 3000
            min_words = 300
        
        stats = {
            'char_count': char_count,
            'word_count': word_count,
            'chinese_char_count': chinese_char_count,
            'generation_mode': generation_mode,
            'meets_minimum': char_count >= min_chars
        }
        
        if char_count < min_chars:
            self.add_error(f"文档长度不足: {char_count} 字符 (最少需要 {min_chars} 字符)")
            self.add_recommendation(f"建议增加到 {recommended_chars}+ 字符以获得更好的生成效果")
        elif char_count < recommended_chars:
            self.add_warning(f"文档长度偏短: {char_count} 字符 (建议 {recommended_chars}+ 字符)")
            self.add_recommendation("详细描述功能模块、业务流程和技术要求可提升生成质量")
        else:
            self.add_success(f"文档长度充足: {char_count} 字符")
        
        return stats
    
    def validate_functional_modules(self, content: str) -> Dict[str, any]:
        """验证功能模块完整性"""
        # 查找功能相关的关键词和模式
        function_patterns = [
            r'功能[一二三四五六七八九十\d]+[:：]',
            r'\d+\..*功能',
            r'模块[一二三四五六七八九十\d]*[:：]',
            r'系统.*功能',
            r'用户.*功能',
            r'管理.*功能'
        ]
        
        function_matches = []
        for pattern in function_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            function_matches.extend(matches)
        
        # 查找业务流程相关内容
        workflow_keywords = ['流程', '步骤', '操作', '处理', '业务', '逻辑']
        workflow_count = sum(content.count(keyword) for keyword in workflow_keywords)
        
        # 查找具体功能描述
        feature_keywords = ['登录', '注册', '查询', '添加', '修改', '删除', '导入', '导出', '统计', '报表', '审批', '权限']
        feature_count = sum(content.count(keyword) for keyword in feature_keywords)
        
        stats = {
            'function_mentions': len(function_matches),
            'workflow_score': workflow_count,
            'feature_score': feature_count,
            'function_details': function_matches[:10]  # 前10个功能描述
        }
        
        if len(function_matches) < 3:
            self.add_error("功能模块描述不足，至少需要描述3个核心功能模块")
            self.add_recommendation("建议详细描述各功能模块的具体作用和业务价值")
        elif len(function_matches) < 5:
            self.add_warning("功能模块描述偏少，建议增加更多功能模块描述")
        else:
            self.add_success(f"功能模块描述充分: 发现 {len(function_matches)} 个功能描述")
        
        if workflow_count < 5:
            self.add_warning("业务流程描述不足，建议增加详细的业务流程说明")
        
        return stats
    
    def validate_user_roles(self, content: str) -> Dict[str, any]:
        """验证用户角色定义"""
        # 查找用户角色相关内容
        role_patterns = [
            r'用户.*[:：]',
            r'角色.*[:：]',
            r'管理员',
            r'普通用户',
            r'操作员',
            r'审核员',
            r'系统管理员'
        ]
        
        role_matches = []
        for pattern in role_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            role_matches.extend(matches)
        
        # 查找权限相关描述
        permission_keywords = ['权限', '授权', '访问控制', '角色管理', '用户管理']
        permission_count = sum(content.count(keyword) for keyword in permission_keywords)
        
        stats = {
            'role_mentions': len(role_matches),
            'permission_score': permission_count,
            'role_details': list(set(role_matches))  # 去重后的角色列表
        }
        
        if len(role_matches) < 2:
            self.add_warning("用户角色定义不足，建议明确定义系统的用户角色")
            self.add_recommendation("清晰的用户角色定义有助于生成更准确的权限管理功能")
        else:
            self.add_success(f"用户角色定义充分: 发现 {len(role_matches)} 个角色相关描述")
        
        return stats
    
    def validate_technical_requirements(self, content: str, config: dict) -> Dict[str, any]:
        """验证技术要求明确性"""
        # 检查技术栈一致性
        config_front = config.get('front', '').lower()
        config_backend = config.get('backend', '').lower()
        
        # 查找技术相关关键词
        tech_keywords = [
            'javascript', 'java', 'python', 'php', 'nodejs', 'react', 'vue', 'angular',
            'spring', 'django', 'flask', 'laravel', 'express',
            'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite',
            'html', 'css', 'bootstrap', 'jquery'
        ]
        
        mentioned_techs = []
        for keyword in tech_keywords:
            if keyword in content.lower():
                mentioned_techs.append(keyword)
        
        # 检查配置一致性
        front_mentioned = config_front in content.lower() if config_front else False
        backend_mentioned = config_backend in content.lower() if config_backend else False
        
        # 查找非功能需求
        nfr_keywords = ['性能', '安全', '可用性', '扩展性', '兼容性', '响应时间', '并发']
        nfr_count = sum(content.count(keyword) for keyword in nfr_keywords)
        
        stats = {
            'mentioned_technologies': mentioned_techs,
            'front_consistency': front_mentioned,
            'backend_consistency': backend_mentioned,
            'nfr_score': nfr_count
        }
        
        if not front_mentioned and config_front:
            self.add_warning(f"需求文档中未提及配置的前端技术: {config_front}")
        
        if not backend_mentioned and config_backend:
            self.add_warning(f"需求文档中未提及配置的后端技术: {config_backend}")
        
        if nfr_count < 3:
            self.add_warning("非功能需求描述不足，建议增加性能、安全性等要求")
        else:
            self.add_success("非功能需求描述充分")
        
        return stats
    
    def validate_professional_terminology(self, content: str) -> Dict[str, any]:
        """验证专业术语使用"""
        # 软件开发相关专业术语
        professional_terms = [
            '系统架构', '数据库', '接口', 'API', '模块', '组件', '框架',
            '用户界面', '业务逻辑', '数据流', '工作流', '算法', '协议',
            '安全性', '稳定性', '可维护性', '可扩展性', '兼容性',
            '前端', '后端', '服务器', '客户端', '浏览器', '移动端',
            '数据库设计', '表结构', '索引', '事务', '备份', '恢复'
        ]
        
        found_terms = []
        for term in professional_terms:
            if term in content:
                found_terms.append(term)
        
        # 计算专业术语密度
        word_count = len(content.split())
        term_density = len(found_terms) / word_count * 100 if word_count > 0 else 0
        
        stats = {
            'professional_terms': found_terms,
            'term_count': len(found_terms),
            'term_density': term_density
        }
        
        if len(found_terms) < 5:
            self.add_warning("专业术语使用较少，建议增加软件开发相关的专业表述")
            self.add_recommendation("适当使用专业术语有助于体现软件的技术含量")
        elif len(found_terms) >= 10:
            self.add_success(f"专业术语使用充分: 发现 {len(found_terms)} 个专业术语")
        else:
            self.add_success(f"专业术语使用合理: 发现 {len(found_terms)} 个专业术语")
        
        return stats
    
    def generate_improvement_suggestions(self, stats: Dict) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        # 基于各项统计数据生成具体建议
        if stats['length']['char_count'] < 1000:
            suggestions.append("📝 扩充文档内容：详细描述每个功能模块的具体实现方式和用户操作流程")
        
        if stats['functions']['function_mentions'] < 5:
            suggestions.append("🔧 增加功能模块：至少描述5-8个核心功能，包括用户管理、数据管理、系统配置等")
        
        if stats['roles']['role_mentions'] < 3:
            suggestions.append("👥 明确用户角色：定义不同用户角色的权限和操作范围，如管理员、普通用户、审核员等")
        
        if stats['technical']['nfr_score'] < 3:
            suggestions.append("⚡ 补充技术要求：明确性能指标、安全要求、兼容性标准等非功能需求")
        
        if stats['terminology']['term_count'] < 8:
            suggestions.append("💻 使用专业术语：适当使用软件开发领域的专业词汇，提升文档的技术水准")
        
        # 根据生成模式提供针对性建议
        if stats['length']['generation_mode'] == 'full' and stats['length']['char_count'] < 2000:
            suggestions.append("📊 完整模式建议：当前为完整生产模式，建议文档内容达到2000+字符以获得最佳生成效果")
        
        return suggestions
    
    def run_validation(self) -> Dict[str, any]:
        """执行完整验证流程"""
        print_header("需求文档质量检查")
        
        # 加载配置和文档
        config = self.load_config()
        if not config:
            return {'success': False, 'error': '配置文件加载失败'}
        
        content = self.load_requirements()
        if not content:
            return {'success': False, 'error': '需求文档加载失败'}
        
        print_info(f"项目: {config.get('title', '未设置')}")
        print_info(f"生成模式: {config.get('generation_mode', '未设置')}")
        print_info(f"文档路径: {self.requirements_path}")
        print()
        
        # 执行各项验证
        length_stats = self.validate_document_length(content, config)
        function_stats = self.validate_functional_modules(content)
        role_stats = self.validate_user_roles(content)
        technical_stats = self.validate_technical_requirements(content, config)
        terminology_stats = self.validate_professional_terminology(content)
        
        # 汇总统计信息
        stats = {
            'length': length_stats,
            'functions': function_stats,
            'roles': role_stats,
            'technical': technical_stats,
            'terminology': terminology_stats
        }
        
        # 生成改进建议
        improvement_suggestions = self.generate_improvement_suggestions(stats)
        self.recommendations.extend(improvement_suggestions)
        
        # 计算总体质量分数
        quality_score = self.calculate_quality_score(stats)
        
        return {
            'success': True,
            'quality_score': quality_score,
            'stats': stats,
            'validation_results': self.validation_results,
            'warnings': self.warnings,
            'recommendations': self.recommendations
        }
    
    def calculate_quality_score(self, stats: Dict) -> int:
        """计算质量分数 (0-100)"""
        score = 0
        
        # 文档长度 (30分)
        if stats['length']['char_count'] >= 2000:
            score += 30
        elif stats['length']['char_count'] >= 1000:
            score += 20
        elif stats['length']['char_count'] >= 500:
            score += 10
        
        # 功能模块 (25分)
        function_count = stats['functions']['function_mentions']
        if function_count >= 8:
            score += 25
        elif function_count >= 5:
            score += 20
        elif function_count >= 3:
            score += 15
        elif function_count >= 1:
            score += 10
        
        # 用户角色 (15分)
        role_count = stats['roles']['role_mentions']
        if role_count >= 5:
            score += 15
        elif role_count >= 3:
            score += 12
        elif role_count >= 2:
            score += 8
        elif role_count >= 1:
            score += 5
        
        # 技术要求 (15分)
        nfr_score = stats['technical']['nfr_score']
        if nfr_score >= 5:
            score += 15
        elif nfr_score >= 3:
            score += 10
        elif nfr_score >= 1:
            score += 5
        
        # 专业术语 (15分)
        term_count = stats['terminology']['term_count']
        if term_count >= 15:
            score += 15
        elif term_count >= 10:
            score += 12
        elif term_count >= 5:
            score += 8
        elif term_count >= 3:
            score += 5
        
        return min(score, 100)

def generate_validation_report(result: Dict) -> str:
    """生成验证报告"""
    if not result['success']:
        return f"验证失败: {result.get('error', '未知错误')}"
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stats = result['stats']
    quality_score = result['quality_score']
    
    # 确定质量等级
    if quality_score >= 90:
        quality_level = "优秀"
        quality_color = "🟢"
    elif quality_score >= 70:
        quality_level = "良好"
        quality_color = "🟡"
    elif quality_score >= 50:
        quality_level = "及格"
        quality_color = "🟠"
    else:
        quality_level = "需要改进"
        quality_color = "🔴"
    
    report = f"""
{'-' * 80}
需求文档质量检查报告
{'-' * 80}

检查时间: {current_time}
文档路径: requires_docs/需求文档.md

{'-' * 80}
质量评估结果
{'-' * 80}

总体质量分数: {quality_score}/100 {quality_color}
质量等级: {quality_level}

{'-' * 80}
详细统计信息
{'-' * 80}

📄 文档长度分析:
- 总字符数: {stats['length']['char_count']:,}
- 总词数: {stats['length']['word_count']:,}
- 中文字符数: {stats['length']['chinese_char_count']:,}
- 生成模式: {stats['length']['generation_mode']}
- 长度要求: {'✓ 达标' if stats['length']['meets_minimum'] else '✗ 不达标'}

🔧 功能模块分析:
- 功能描述数量: {stats['functions']['function_mentions']}
- 业务流程关键词: {stats['functions']['workflow_score']}
- 功能特性关键词: {stats['functions']['feature_score']}

👥 用户角色分析:
- 角色相关描述: {stats['roles']['role_mentions']}
- 权限管理关键词: {stats['roles']['permission_score']}

💻 技术要求分析:
- 提及的技术: {len(stats['technical']['mentioned_technologies'])}
- 前端技术一致性: {'✓' if stats['technical']['front_consistency'] else '✗'}
- 后端技术一致性: {'✓' if stats['technical']['backend_consistency'] else '✗'}
- 非功能需求关键词: {stats['technical']['nfr_score']}

📚 专业术语分析:
- 专业术语数量: {stats['terminology']['term_count']}
- 术语密度: {stats['terminology']['term_density']:.2f}%

{'-' * 80}
检查结果详情
{'-' * 80}

"""
    
    # 添加验证结果
    success_count = 0
    warning_count = 0
    error_count = 0
    
    for result_type, message in result['validation_results']:
        if result_type == 'success':
            report += f"✓ {message}\n"
            success_count += 1
        elif result_type == 'warning':
            report += f"⚠ {message}\n"
            warning_count += 1
        elif result_type == 'error':
            report += f"✗ {message}\n"
            error_count += 1
    
    report += f"\n统计: 通过 {success_count} | 警告 {warning_count} | 错误 {error_count}\n"
    
    # 添加改进建议
    if result['recommendations']:
        report += f"\n{'-' * 80}\n改进建议\n{'-' * 80}\n\n"
        for i, suggestion in enumerate(result['recommendations'], 1):
            report += f"{i}. {suggestion}\n"
    
    # 添加质量提升指导
    report += f"\n{'-' * 80}\n质量提升指导\n{'-' * 80}\n\n"
    
    if quality_score < 50:
        report += "🔴 当前文档质量较低，强烈建议按照改进建议进行大幅优化\n"
        report += "- 重点补充功能模块的详细描述\n"
        report += "- 明确用户角色和权限设计\n"
        report += "- 增加技术实现细节和非功能需求\n"
    elif quality_score < 70:
        report += "🟠 文档质量一般，建议进一步完善以获得更好的生成效果\n"
        report += "- 扩充现有功能描述的深度和广度\n"
        report += "- 补充遗漏的重要功能模块\n"
        report += "- 增强专业术语的使用\n"
    elif quality_score < 90:
        report += "🟡 文档质量良好，可做适当优化以达到最佳效果\n"
        report += "- 细化业务流程描述\n"
        report += "- 完善边界条件和异常处理说明\n"
        report += "- 增加系统集成和接口要求\n"
    else:
        report += "🟢 文档质量优秀，可以开始生成高质量的软著申请材料\n"
        report += "- 当前文档已具备生成专业软著材料的基础\n"
        report += "- 建议保持现有质量标准\n"
    
    report += f"\n{'-' * 80}\n报告生成时间: {current_time}\n{'-' * 80}\n"
    
    return report

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("需求文档质量检查工具")
        print("\n用法:")
        print("  python3 validate_requirements.py")
        print("\n功能:")
        print("  验证 requires_docs/需求文档.md 的质量和完整性")
        print("  生成详细的质量分析报告和改进建议")
        print("\n检查维度:")
        print("  - 文档长度和内容充实度")
        print("  - 功能模块完整性")
        print("  - 用户角色定义")
        print("  - 技术要求明确性")
        print("  - 专业术语使用")
        print("\n输出:")
        print("  - 终端显示验证结果")
        print("  - 生成详细的质量报告文件")
        return
    
    # 执行验证
    validator = RequirementsValidator()
    result = validator.run_validation()
    
    if not result['success']:
        print_error(f"验证失败: {result.get('error', '未知错误')}")
        sys.exit(1)
    
    # 显示验证结果
    print_header("验证结果")
    
    quality_score = result['quality_score']
    
    for result_type, message in result['validation_results']:
        if result_type == 'success':
            print_success(message)
        elif result_type == 'warning':
            print_warning(message)
        elif result_type == 'error':
            print_error(message)
    
    print()
    print_info(f"文档质量分数: {quality_score}/100")
    
    if quality_score >= 70:
        print_success("文档质量良好，可以开始生成软著申请材料")
    elif quality_score >= 50:
        print_warning("文档质量一般，建议优化后再生成")
    else:
        print_error("文档质量较低，强烈建议先改进文档")
    
    # 生成并保存报告
    print()
    print_info("生成详细质量报告...")
    
    report = generate_validation_report(result)
    
    # 保存报告
    report_file = Path("requires_docs/需求文档质量报告.txt")
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print_success(f"质量报告已保存: {report_file}")
    except Exception as e:
        print_error(f"保存报告失败: {e}")
    
    # 显示改进建议
    if result['recommendations']:
        print()
        print_header("改进建议")
        for i, suggestion in enumerate(result['recommendations'], 1):
            print_info(f"{i}. {suggestion}")
    
    sys.exit(0 if quality_score >= 50 else 1)

if __name__ == "__main__":
    main()