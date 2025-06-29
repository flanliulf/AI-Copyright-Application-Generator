#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
软著申请材料质量监控和检测工具
功能：全方位监控生成过程的质量，提供实时反馈和智能建议

监控维度：
1. 生成进度跟踪
2. 代码质量检测
3. 文档完整性验证
4. 申请成功率预测
5. 性能指标分析
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 颜色输出类
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
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

class QualityMonitor:
    """质量监控器"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.config_path = self.project_root / "ai-copyright-config.json"
        self.monitoring_results = {}
        
    def load_config(self) -> Optional[dict]:
        """加载项目配置"""
        if not self.config_path.exists():
            return None
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    
    def check_generation_progress(self) -> Dict[str, any]:
        """检查生成进度"""
        progress = {
            'requirements_doc': False,
            'framework_design': False,
            'page_list': False,
            'frontend_code': False,
            'backend_code': False,
            'database_code': False,
            'user_manual': False,
            'registration_form': False,
            'merged_frontend': False,
            'merged_backend': False,
            'merged_database': False
        }
        
        file_mappings = {
            'requirements_doc': 'requires_docs/需求文档.md',
            'framework_design': 'process_docs/*框架设计文档.md',
            'page_list': 'process_docs/页面清单.md',
            'frontend_code': 'output_sourcecode/front/*.html',
            'backend_code': 'output_sourcecode/backend/*',
            'database_code': 'output_sourcecode/db/*.sql',
            'user_manual': 'output_docs/*用户手册.md',
            'registration_form': 'output_docs/*软件著作权登记信息表.md',
            'merged_frontend': 'output_docs/前端源代码.txt',
            'merged_backend': 'output_docs/后端源代码.txt',
            'merged_database': 'output_docs/数据库源代码.txt'
        }
        
        for key, pattern in file_mappings.items():
            if '*' in pattern:
                # 使用glob匹配
                matches = list(self.project_root.glob(pattern))
                progress[key] = len(matches) > 0
            else:
                # 直接检查文件
                file_path = self.project_root / pattern
                progress[key] = file_path.exists()
        
        # 计算完成度
        completed_stages = sum(progress.values())
        total_stages = len(progress)
        completion_rate = (completed_stages / total_stages) * 100
        
        return {
            'progress': progress,
            'completed_stages': completed_stages,
            'total_stages': total_stages,
            'completion_rate': completion_rate
        }
    
    def analyze_code_quality(self) -> Dict[str, any]:
        """分析代码质量"""
        quality_metrics = {
            'frontend': self.analyze_frontend_quality(),
            'backend': self.analyze_backend_quality(),
            'database': self.analyze_database_quality()
        }
        
        # 计算总体质量分数
        quality_scores = [metrics['quality_score'] for metrics in quality_metrics.values() if metrics['quality_score'] > 0]
        overall_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        return {
            'components': quality_metrics,
            'overall_score': overall_score,
            'quality_level': self.get_quality_level(overall_score)
        }
    
    def analyze_frontend_quality(self) -> Dict[str, any]:
        """分析前端代码质量"""
        frontend_dir = self.project_root / "output_sourcecode" / "front"
        
        if not frontend_dir.exists():
            return {'exists': False, 'quality_score': 0}
        
        html_files = list(frontend_dir.glob("*.html"))
        if not html_files:
            return {'exists': False, 'quality_score': 0}
        
        metrics = {
            'file_count': len(html_files),
            'total_size': 0,
            'avg_size': 0,
            'has_css': 0,
            'has_js': 0,
            'has_responsive': 0,
            'has_navigation': 0,
            'html5_compliant': 0,
            'quality_score': 0
        }
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                file_size = len(content)
                metrics['total_size'] += file_size
                
                # 检查各种质量指标
                if '<style>' in content or 'class=' in content:
                    metrics['has_css'] += 1
                
                if '<script>' in content or 'function' in content:
                    metrics['has_js'] += 1
                
                if 'responsive' in content.lower() or '@media' in content:
                    metrics['has_responsive'] += 1
                
                if '<nav>' in content or 'navigation' in content.lower():
                    metrics['has_navigation'] += 1
                
                if '<!DOCTYPE html>' in content:
                    metrics['html5_compliant'] += 1
                    
            except:
                continue
        
        if metrics['file_count'] > 0:
            metrics['avg_size'] = metrics['total_size'] / metrics['file_count']
            
            # 计算质量分数
            score = 0
            score += min(metrics['file_count'] * 10, 50)  # 文件数量 (最多50分)
            score += (metrics['has_css'] / metrics['file_count']) * 15  # CSS使用率 (15分)
            score += (metrics['has_js'] / metrics['file_count']) * 15  # JS使用率 (15分)
            score += (metrics['has_responsive'] / metrics['file_count']) * 10  # 响应式 (10分)
            score += (metrics['has_navigation'] / metrics['file_count']) * 5  # 导航 (5分)
            score += (metrics['html5_compliant'] / metrics['file_count']) * 5  # HTML5 (5分)
            
            metrics['quality_score'] = min(score, 100)
        
        metrics['exists'] = True
        return metrics
    
    def analyze_backend_quality(self) -> Dict[str, any]:
        """分析后端代码质量"""
        backend_dir = self.project_root / "output_sourcecode" / "backend"
        
        if not backend_dir.exists():
            return {'exists': False, 'quality_score': 0}
        
        # 收集源代码文件
        source_extensions = ['.java', '.py', '.js', '.php', '.cs', '.go', '.rb']
        source_files = []
        for ext in source_extensions:
            source_files.extend(backend_dir.rglob(f"*{ext}"))
        
        if not source_files:
            return {'exists': False, 'quality_score': 0}
        
        metrics = {
            'file_count': len(source_files),
            'total_size': 0,
            'avg_size': 0,
            'has_functions': 0,
            'has_classes': 0,
            'has_comments': 0,
            'has_error_handling': 0,
            'complexity_score': 0,
            'quality_score': 0
        }
        
        for source_file in source_files:
            try:
                with open(source_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                file_size = len(content)
                metrics['total_size'] += file_size
                
                # 检查代码特征
                if re.search(r'function\s+\w+|def\s+\w+|public\s+\w+\s+\w+\s*\(', content):
                    metrics['has_functions'] += 1
                
                if re.search(r'class\s+\w+|public\s+class\s+\w+', content):
                    metrics['has_classes'] += 1
                
                if '//' in content or '/*' in content or '#' in content or '"""' in content:
                    metrics['has_comments'] += 1
                
                if re.search(r'try\s*{|except:|catch\s*\(|error|exception', content, re.IGNORECASE):
                    metrics['has_error_handling'] += 1
                
                # 计算复杂度分数（基于关键词密度）
                complexity_keywords = ['if', 'for', 'while', 'switch', 'case', 'else', 'elif']
                complexity_count = sum(content.lower().count(keyword) for keyword in complexity_keywords)
                metrics['complexity_score'] += complexity_count
                
            except:
                continue
        
        if metrics['file_count'] > 0:
            metrics['avg_size'] = metrics['total_size'] / metrics['file_count']
            
            # 计算质量分数
            score = 0
            score += min(metrics['file_count'] * 8, 40)  # 文件数量 (最多40分)
            score += (metrics['has_functions'] / metrics['file_count']) * 20  # 函数定义 (20分)
            score += (metrics['has_classes'] / metrics['file_count']) * 15  # 类定义 (15分)
            score += (metrics['has_comments'] / metrics['file_count']) * 10  # 注释 (10分)
            score += (metrics['has_error_handling'] / metrics['file_count']) * 10  # 错误处理 (10分)
            score += min(metrics['complexity_score'] / metrics['file_count'], 5)  # 复杂度 (5分)
            
            metrics['quality_score'] = min(score, 100)
        
        metrics['exists'] = True
        return metrics
    
    def analyze_database_quality(self) -> Dict[str, any]:
        """分析数据库质量"""
        db_dir = self.project_root / "output_sourcecode" / "db"
        
        if not db_dir.exists():
            return {'exists': False, 'quality_score': 0}
        
        sql_files = list(db_dir.glob("*.sql"))
        if not sql_files:
            return {'exists': False, 'quality_score': 0}
        
        metrics = {
            'file_count': len(sql_files),
            'total_size': 0,
            'create_table_count': 0,
            'index_count': 0,
            'constraint_count': 0,
            'procedure_count': 0,
            'view_count': 0,
            'quality_score': 0
        }
        
        for sql_file in sql_files:
            try:
                with open(sql_file, 'r', encoding='utf-8') as f:
                    content = f.read().upper()
                
                metrics['total_size'] += len(content)
                metrics['create_table_count'] += content.count('CREATE TABLE')
                metrics['index_count'] += content.count('CREATE INDEX')
                metrics['constraint_count'] += content.count('CONSTRAINT') + content.count('PRIMARY KEY') + content.count('FOREIGN KEY')
                metrics['procedure_count'] += content.count('CREATE PROCEDURE') + content.count('CREATE FUNCTION')
                metrics['view_count'] += content.count('CREATE VIEW')
                
            except:
                continue
        
        # 计算质量分数
        score = 0
        score += min(metrics['create_table_count'] * 10, 40)  # 表数量 (最多40分)
        score += min(metrics['index_count'] * 5, 15)  # 索引 (最多15分)
        score += min(metrics['constraint_count'] * 3, 15)  # 约束 (最多15分)
        score += min(metrics['procedure_count'] * 10, 20)  # 存储过程 (最多20分)
        score += min(metrics['view_count'] * 5, 10)  # 视图 (最多10分)
        
        metrics['quality_score'] = min(score, 100)
        metrics['exists'] = True
        return metrics
    
    def get_quality_level(self, score: float) -> str:
        """根据分数获取质量等级"""
        if score >= 90:
            return "优秀"
        elif score >= 75:
            return "良好"
        elif score >= 60:
            return "及格"
        elif score >= 40:
            return "较差"
        else:
            return "很差"
    
    def predict_approval_probability(self, progress_data: Dict, quality_data: Dict) -> Dict[str, any]:
        """预测申请成功率"""
        # 基于进度和质量数据预测成功率
        progress_weight = 0.4
        quality_weight = 0.6
        
        progress_score = progress_data['completion_rate']
        quality_score = quality_data['overall_score']
        
        # 计算加权分数
        weighted_score = (progress_score * progress_weight + quality_score * quality_weight)
        
        # 转换为成功率
        if weighted_score >= 90:
            probability = 0.95
            level = "很高"
        elif weighted_score >= 80:
            probability = 0.85
            level = "高"
        elif weighted_score >= 70:
            probability = 0.70
            level = "中等"
        elif weighted_score >= 60:
            probability = 0.55
            level = "较低"
        else:
            probability = 0.30
            level = "低"
        
        return {
            'probability': probability,
            'percentage': probability * 100,
            'level': level,
            'weighted_score': weighted_score,
            'factors': {
                'progress_contribution': progress_score * progress_weight,
                'quality_contribution': quality_score * quality_weight
            }
        }
    
    def generate_recommendations(self, progress_data: Dict, quality_data: Dict, prediction: Dict) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 基于进度的建议
        progress = progress_data['progress']
        if not progress['requirements_doc']:
            recommendations.append("🔴 紧急：创建需求文档是所有后续工作的基础")
        elif not progress['framework_design']:
            recommendations.append("🔴 重要：生成框架设计文档以指导后续开发")
        elif not progress['frontend_code'] and not progress['backend_code']:
            recommendations.append("🔴 关键：开始生成前端和后端代码")
        elif not progress['merged_frontend'] or not progress['merged_backend']:
            recommendations.append("🟡 建议：执行代码合并以生成申请材料")
        
        # 基于质量的建议
        quality_components = quality_data['components']
        
        if quality_components['frontend']['exists'] and quality_components['frontend']['quality_score'] < 60:
            recommendations.append("🔧 前端代码质量有待提升：增加CSS样式、JavaScript交互和响应式设计")
        
        if quality_components['backend']['exists'] and quality_components['backend']['quality_score'] < 60:
            recommendations.append("🔧 后端代码质量有待提升：增加函数模块化、类设计和错误处理")
        
        if quality_components['database']['exists'] and quality_components['database']['quality_score'] < 60:
            recommendations.append("🔧 数据库设计有待完善：增加表结构、索引和约束设计")
        
        # 基于成功率预测的建议
        if prediction['probability'] < 0.7:
            recommendations.append("⚠️ 当前申请成功率偏低，建议全面提升文档质量后再提交")
        elif prediction['probability'] < 0.85:
            recommendations.append("💡 申请成功率中等，可考虑优化部分薄弱环节")
        
        return recommendations
    
    def run_monitoring(self) -> Dict[str, any]:
        """执行完整监控"""
        print_header("软著申请材料质量监控")
        
        config = self.load_config()
        project_name = config.get('title', '未知项目') if config else '未知项目'
        
        print_info(f"项目: {project_name}")
        print_info(f"监控时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # 检查生成进度
        print_info("检查生成进度...")
        progress_data = self.check_generation_progress()
        
        # 分析代码质量
        print_info("分析代码质量...")
        quality_data = self.analyze_code_quality()
        
        # 预测申请成功率
        print_info("评估申请成功率...")
        prediction = self.predict_approval_probability(progress_data, quality_data)
        
        # 生成改进建议
        recommendations = self.generate_recommendations(progress_data, quality_data, prediction)
        
        return {
            'project_name': project_name,
            'timestamp': datetime.now().isoformat(),
            'progress': progress_data,
            'quality': quality_data,
            'prediction': prediction,
            'recommendations': recommendations
        }

def generate_monitoring_report(monitoring_result: Dict) -> str:
    """生成监控报告"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    project_name = monitoring_result['project_name']
    progress = monitoring_result['progress']
    quality = monitoring_result['quality']
    prediction = monitoring_result['prediction']
    recommendations = monitoring_result['recommendations']
    
    report = f"""
{'-' * 80}
软著申请材料质量监控报告
{'-' * 80}

项目名称: {project_name}
监控时间: {current_time}

{'-' * 80}
生成进度概览
{'-' * 80}

总体完成度: {progress['completion_rate']:.1f}% ({progress['completed_stages']}/{progress['total_stages']})

进度详情:
"""
    
    stage_names = {
        'requirements_doc': '需求文档',
        'framework_design': '框架设计',
        'page_list': '页面清单',
        'frontend_code': '前端代码',
        'backend_code': '后端代码',
        'database_code': '数据库代码',
        'user_manual': '用户手册',
        'registration_form': '登记信息表',
        'merged_frontend': '前端合并文档',
        'merged_backend': '后端合并文档',
        'merged_database': '数据库合并文档'
    }
    
    for key, completed in progress['progress'].items():
        status = "✓" if completed else "✗"
        name = stage_names.get(key, key)
        report += f"  {status} {name}\n"
    
    report += f"""
{'-' * 80}
代码质量分析
{'-' * 80}

总体质量分数: {quality['overall_score']:.1f}/100 ({quality['quality_level']})

组件质量详情:
"""
    
    # 前端质量
    frontend = quality['components']['frontend']
    if frontend['exists']:
        report += f"  ✓ 前端代码: {frontend['quality_score']:.1f}/100\n"
        report += f"    - 页面文件数: {frontend['file_count']}\n"
        report += f"    - 平均文件大小: {frontend['avg_size']:.0f} 字符\n"
        report += f"    - CSS使用率: {frontend['has_css']}/{frontend['file_count']}\n"
        report += f"    - JavaScript使用率: {frontend['has_js']}/{frontend['file_count']}\n"
    else:
        report += "  ✗ 前端代码: 未生成\n"
    
    # 后端质量
    backend = quality['components']['backend']
    if backend['exists']:
        report += f"  ✓ 后端代码: {backend['quality_score']:.1f}/100\n"
        report += f"    - 源文件数: {backend['file_count']}\n"
        report += f"    - 函数定义: {backend['has_functions']}/{backend['file_count']}\n"
        report += f"    - 类定义: {backend['has_classes']}/{backend['file_count']}\n"
        report += f"    - 错误处理: {backend['has_error_handling']}/{backend['file_count']}\n"
    else:
        report += "  ✗ 后端代码: 未生成\n"
    
    # 数据库质量
    database = quality['components']['database']
    if database['exists']:
        report += f"  ✓ 数据库设计: {database['quality_score']:.1f}/100\n"
        report += f"    - 数据表数: {database['create_table_count']}\n"
        report += f"    - 索引数: {database['index_count']}\n"
        report += f"    - 约束数: {database['constraint_count']}\n"
        report += f"    - 存储过程数: {database['procedure_count']}\n"
    else:
        report += "  ✗ 数据库设计: 未生成\n"
    
    report += f"""
{'-' * 80}
申请成功率预测
{'-' * 80}

预测成功率: {prediction['percentage']:.1f}% ({prediction['level']})
加权评分: {prediction['weighted_score']:.1f}/100

评分构成:
  - 进度贡献: {prediction['factors']['progress_contribution']:.1f}分 (权重40%)
  - 质量贡献: {prediction['factors']['quality_contribution']:.1f}分 (权重60%)

"""
    
    # 添加改进建议
    if recommendations:
        report += f"{'-' * 80}\n改进建议\n{'-' * 80}\n\n"
        for i, recommendation in enumerate(recommendations, 1):
            report += f"{i}. {recommendation}\n"
    
    # 添加行动计划
    report += f"""
{'-' * 80}
下一步行动计划
{'-' * 80}

"""
    
    if progress['completion_rate'] < 50:
        report += "🔴 当前处于初期阶段，重点任务:\n"
        report += "  1. 完善需求文档内容\n"
        report += "  2. 生成框架设计文档\n" 
        report += "  3. 开始代码生成工作\n"
    elif progress['completion_rate'] < 80:
        report += "🟡 当前处于开发阶段，重点任务:\n"
        report += "  1. 完成所有代码生成\n"
        report += "  2. 提升代码质量和复杂度\n"
        report += "  3. 准备申请材料合并\n"
    else:
        report += "🟢 当前处于收尾阶段，重点任务:\n"
        report += "  1. 执行代码合并脚本\n"
        report += "  2. 生成用户手册和登记表\n"
        report += "  3. 最终质量检查和提交\n"
    
    if quality['overall_score'] < 60:
        report += "\n🔧 质量提升重点:\n"
        report += "  1. 增加代码的功能复杂度\n"
        report += "  2. 完善错误处理和异常管理\n"
        report += "  3. 增强用户界面和交互设计\n"
        report += "  4. 优化数据库设计和约束\n"
    
    report += f"\n{'-' * 80}\n报告生成时间: {current_time}\n{'-' * 80}\n"
    
    return report

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("软著申请材料质量监控工具")
        print("\n用法:")
        print("  python3 quality_monitor.py")
        print("\n功能:")
        print("  - 监控生成进度和质量")
        print("  - 分析代码复杂度和专业性")
        print("  - 预测申请成功率")
        print("  - 提供改进建议和行动计划")
        print("\n输出:")
        print("  - 终端显示监控结果")
        print("  - 生成详细的质量监控报告")
        return
    
    # 执行监控
    monitor = QualityMonitor()
    result = monitor.run_monitoring()
    
    # 显示关键结果
    print_header("监控结果概览")
    
    progress = result['progress']
    quality = result['quality']
    prediction = result['prediction']
    
    print_info(f"生成进度: {progress['completion_rate']:.1f}% ({progress['completed_stages']}/{progress['total_stages']})")
    print_info(f"代码质量: {quality['overall_score']:.1f}/100 ({quality['quality_level']})")
    
    if prediction['probability'] >= 0.8:
        print_success(f"申请成功率: {prediction['percentage']:.1f}% ({prediction['level']})")
    elif prediction['probability'] >= 0.6:
        print_warning(f"申请成功率: {prediction['percentage']:.1f}% ({prediction['level']})")
    else:
        print_error(f"申请成功率: {prediction['percentage']:.1f}% ({prediction['level']})")
    
    # 显示关键建议
    if result['recommendations']:
        print()
        print_header("关键建议")
        for i, recommendation in enumerate(result['recommendations'][:5], 1):  # 显示前5条
            print_info(f"{i}. {recommendation}")
    
    # 生成并保存报告
    print()
    print_info("生成详细监控报告...")
    
    report = generate_monitoring_report(result)
    
    # 保存报告
    report_file = Path("质量监控报告.txt")
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print_success(f"监控报告已保存: {report_file}")
    except Exception as e:
        print_error(f"保存报告失败: {e}")
    
    # 返回状态码
    if prediction['probability'] >= 0.7:
        sys.exit(0)  # 成功
    else:
        sys.exit(1)  # 需要改进

if __name__ == "__main__":
    main()