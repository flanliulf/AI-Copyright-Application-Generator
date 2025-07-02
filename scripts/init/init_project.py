#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI驱动的企业级软件开发工作流程 - 项目初始化脚本 (Python版本)
版本: 1.0
描述: 自动创建新项目的目录结构和固定文档
"""

import os
import sys
import json
import shutil
import argparse
import locale
from datetime import datetime

# 设置系统编码
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)

# 确保终端编码为UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'
from pathlib import Path

class Colors:
    """终端颜色定义"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_message(color, message):
    """打印带颜色的消息"""
    print(f"{color}{message}{Colors.NC}")

def print_success(message):
    print_message(Colors.GREEN, f"✓ {message}")

def print_info(message):
    print_message(Colors.BLUE, f"ℹ {message}")

def print_warning(message):
    print_message(Colors.YELLOW, f"⚠ {message}")

def print_error(message):
    print_message(Colors.RED, f"✗ {message}")

def get_user_input(prompt, default=""):
    """获取用户输入，支持默认值"""
    try:
        if default:
            user_input = input(f"{prompt} (默认: {default}): ").strip()
            return user_input if user_input else default
        else:
            return input(f"{prompt}: ").strip()
    except UnicodeDecodeError:
        print_error("输入编码错误，请确保终端支持UTF-8编码")
        return default if default else ""
    except KeyboardInterrupt:
        print_error("用户中断操作")
        sys.exit(1)
    except Exception as e:
        print_error(f"输入错误: {e}")
        return default if default else ""

def get_yes_no_input(prompt, default_no=True):
    """获取是/否输入"""
    try:
        suffix = "(y/N)" if default_no else "(Y/n)"
        response = input(f"{prompt} {suffix}: ").strip().lower()
        
        if default_no:
            return response in ['y', 'yes', '是']
        else:
            return response not in ['n', 'no', '否']
    except UnicodeDecodeError:
        print_error("输入编码错误，请确保终端支持UTF-8编码")
        return not default_no
    except KeyboardInterrupt:
        print_error("用户中断操作")
        sys.exit(1)
    except Exception as e:
        print_error(f"输入错误: {e}")
        return not default_no

def get_generation_mode_config():
    """获取用户选择的生成模式配置"""
    print_info("请选择生成模式:")
    print("1. fast - 快速验证模式（5页面，8-15个API，适合快速原型和测试）")
    print("2. full - 完整生产模式（10页面，15-35个API，适合正式申请和完整系统）")
    print()
    
    while True:
        choice = input("请输入选择 (1-2，默认为1): ").strip()
        if choice == "" or choice == "1":
            return {
                "generation_mode": "fast",
                "page_count": 5,
                "api_count_min": 8,
                "api_count_max": 15
            }
        elif choice == "2":
            return {
                "generation_mode": "full", 
                "page_count": 10,
                "api_count_min": 15,
                "api_count_max": 35
            }
        else:
            print_warning("无效选择，请输入 1 或 2")

def get_ui_design_style():
    """获取用户选择的UI设计风格"""
    print_info("请选择UI设计风格:")
    
    styles = [
        ("corporate", "企业商务风格（默认）", "企业管理系统、办公软件、政务系统、金融应用等", "专业稳重、通用性强、符合主流商务审美"),
        ("cyberpunk", "暗黑科技风格", "开发者工具、数据分析平台、科技产品、游戏相关应用等", "科技感强、适合夜间使用、吸引年轻用户群体"),
        ("minimal", "极简主义风格", "内容管理系统、阅读类应用、教育平台、专业工具等", "简洁优雅、专注内容、永恒的设计价值"),
        ("bauhaus", "包豪斯风格", "设计工具平台、建筑设计系统、艺术展览平台、学术研究工具", "功能至上、几何纯粹、理性秩序"),
        ("japanese", "日式极简风格", "冥想禅修应用、文化艺术平台、阅读写作工具、生活方式应用", "侘寂美学、间之道、静谧禅意"),
        ("scandinavian", "斯堪的纳维亚风格", "生活方式应用、健康养生平台、教育学习工具、家庭管理系统", "功能简约、温暖质感、自然和谐"),
        ("futuristic", "未来科技风格", "数据分析平台、开发者工具、网络安全系统、金融交易平台", "数字未来、HUD界面、信息密集"),
        ("elegant", "优雅复古风格", "文化教育平台、学术研究工具、图书馆系统、博物馆应用", "古典雅致、印刷美学、温暖怀旧"),
        ("bold", "大胆现代风格", "创意设计平台、时尚品牌网站、科技创新产品、营销活动平台", "大胆突破、现代前卫、视觉冲击"),
        ("artdeco", "艺术装饰风格", "奢侈品电商、高端酒店餐饮、艺术文化机构、金融投资平台", "装饰艺术、几何奢华、对称美学"),
        ("memphis", "孟菲斯风格", "创意设计平台、娱乐媒体应用、时尚潮流品牌、青年社交应用", "后现代反叛、色彩狂欢、几何拼贴"),
        ("popart", "波普艺术风格", "娱乐媒体平台、时尚购物平台、创意营销工具、社交娱乐应用", "大众文化、明亮色彩、商业美学")
    ]
    
    # 显示所有风格选项
    for i, (key, name, use_cases, features) in enumerate(styles, 1):
        print(f"{i:2d}. {key} - {name}")
        print(f"    适用于：{use_cases}")
        print(f"    特点：{features}")
        print()
    
    # 获取用户选择
    while True:
        choice = input(f"请输入选择 (1-{len(styles)}，默认为1): ").strip()
        if choice == "" or choice == "1":
            return "corporate"
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(styles):
                return styles[choice_num - 1][0]
            else:
                print_warning(f"无效选择，请输入 1 到 {len(styles)} 之间的数字")
        except ValueError:
            print_warning(f"无效输入，请输入 1 到 {len(styles)} 之间的数字")

def create_directory_structure(project_dir):
    """创建项目目录结构"""
    directories = [
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
    
    for directory in directories:
        os.makedirs(project_dir / directory, exist_ok=True)
    
    print_success("目录结构创建完成")

def copy_fixed_documents(script_dir, project_dir, ui_design_style):
    """复制固定文档和系统提示词"""
    specs_source = script_dir / "specs_docs"
    
    if not specs_source.exists():
        print_error(f"源文件目录不存在: {specs_source}")
        print_info("请确保脚本在包含 specs_docs 目录的项目根目录中运行")
        sys.exit(1)
    
    # UI风格映射表
    ui_style_mapping = {
        "corporate": "01-UI设计规范_默认_Corporate.md",
        "cyberpunk": "02-UI设计规范_暗黑科技风格_Cyberpunk.md",
        "minimal": "03-UI设计规范_极简主义风格_Minimal.md",
        "bauhaus": "04-UI设计规范_包豪斯风格_Bauhaus.md",
        "japanese": "05-UI设计规范_日式极简风格_Japanese.md",
        "scandinavian": "06-UI设计规范_斯堪的纳维亚风格_Scandinavian.md",
        "futuristic": "07-UI设计规范_未来科技风格_Futuristic.md",
        "elegant": "08-UI设计规范_优雅复古风格_Elegant.md",
        "bold": "09-UI设计规范_大胆现代风格_Bold.md",
        "artdeco": "10-UI设计规范_艺术装饰风格_ArtDeco.md",
        "memphis": "11-UI设计规范_孟菲斯风格_Memphis.md",
        "popart": "12-UI设计规范_波普艺术风格_PopArt.md"
    }
    
    # 只复制选择的UI设计规范文档和默认的企业风格（作为备用参考）
    ui_design_files_to_copy = [ui_style_mapping[ui_design_style]]
    if ui_design_style != "corporate":
        ui_design_files_to_copy.append(ui_style_mapping["corporate"])  # 添加默认风格作为参考
    
    for file_name in ui_design_files_to_copy:
        src = specs_source / "ui_design_specs" / file_name
        dst = project_dir / "specs_docs" / "ui_design_specs" / file_name
        if src.exists():
            shutil.copy2(src, dst)
            print_info(f"复制UI设计规范: {file_name}")
    
    # 复制技术栈规范文档
    tech_stack_file = "技术栈说明文档_默认.md"
    src = specs_source / "tech_stack_specs" / tech_stack_file
    dst = project_dir / "specs_docs" / "tech_stack_specs" / tech_stack_file
    if src.exists():
        shutil.copy2(src, dst)
    
    # 复制系统提示词
    system_prompt_src = script_dir / "system_prompts"
    system_prompt_dst = project_dir / "system_prompts"
    
    if system_prompt_src.exists():
        for file_path in system_prompt_src.glob("*.md"):
            shutil.copy2(file_path, system_prompt_dst / file_path.name)
    
    # 复制scripts目录（生成和验证脚本）
    scripts_src = script_dir / "scripts"
    scripts_dst = project_dir / "scripts"
    
    if scripts_src.exists():
        # 复制generators目录下的所有脚本
        generators_src = scripts_src / "generators"
        generators_dst = scripts_dst / "generators"
        if generators_src.exists():
            for file_path in generators_src.iterdir():
                if file_path.is_file():
                    shutil.copy2(file_path, generators_dst / file_path.name)
                    print_info(f"复制生成脚本: {file_path.name}")
        
        # 复制validators目录下的所有脚本
        validators_src = scripts_src / "validators"
        validators_dst = scripts_dst / "validators"
        if validators_src.exists():
            for file_path in validators_src.iterdir():
                if file_path.is_file():
                    shutil.copy2(file_path, validators_dst / file_path.name)
                    print_info(f"复制验证脚本: {file_path.name}")
    
    # 复制工作流程文档和执行计划文档
    workflow_files = [
        "工作流程.md",
        "执行计划.md"
    ]
    
    for workflow_file in workflow_files:
        src = script_dir / workflow_file
        if src.exists():
            shutil.copy2(src, project_dir / workflow_file)
        else:
            print_warning(f"工作流程文档不存在: {src}")
    
    print_success("固定文档复制完成")

def create_config_file(project_dir, config):
    """创建配置文件"""
    # UI风格映射到文件路径
    ui_style_file_mapping = {
        "corporate": "specs_docs/ui_design_specs/01-UI设计规范_默认_Corporate.md",
        "cyberpunk": "specs_docs/ui_design_specs/02-UI设计规范_暗黑科技风格_Cyberpunk.md",
        "minimal": "specs_docs/ui_design_specs/03-UI设计规范_极简主义风格_Minimal.md",
        "bauhaus": "specs_docs/ui_design_specs/04-UI设计规范_包豪斯风格_Bauhaus.md",
        "japanese": "specs_docs/ui_design_specs/05-UI设计规范_日式极简风格_Japanese.md",
        "scandinavian": "specs_docs/ui_design_specs/06-UI设计规范_斯堪的纳维亚风格_Scandinavian.md",
        "futuristic": "specs_docs/ui_design_specs/07-UI设计规范_未来科技风格_Futuristic.md",
        "elegant": "specs_docs/ui_design_specs/08-UI设计规范_优雅复古风格_Elegant.md",
        "bold": "specs_docs/ui_design_specs/09-UI设计规范_大胆现代风格_Bold.md",
        "artdeco": "specs_docs/ui_design_specs/10-UI设计规范_艺术装饰风格_ArtDeco.md",
        "memphis": "specs_docs/ui_design_specs/11-UI设计规范_孟菲斯风格_Memphis.md",
        "popart": "specs_docs/ui_design_specs/12-UI设计规范_波普艺术风格_PopArt.md"
    }
    
    config_data = {
        "_comment_init": "=== 项目初始化配置（用户设置） ===",
        "front": config['front_tech'],
        "backend": config['backend_tech'],
        "title": config['system_title'],
        "short_title": config['system_short_title'],
        "requirements_description": "requires_docs/需求文档.md",
        "dev_tech_stack": config['tech_stack_path'],
        "ui_design_spec": ui_style_file_mapping[config['ui_design_style']],
        "ui_design_style": config['ui_design_style'],
        
        "_comment_generation": "=== 生成配置（可调整） ===",
        "page_count_fast": 5,
        "page_count_full": 10,
        "api_count_min": config['api_count_min'],
        "api_count_max": config['api_count_max'],
        "generation_mode": config['generation_mode'],
        
        "_comment_usage": "=== 使用说明 ===",
        "_usage_note_1": "1. 请务必修改上方的 title 和 short_title 为您的实际项目名称",
        "_usage_note_2": "2. front 和 backend 可根据实际技术栈修改（如 React, Vue, Python, Node.js 等）",
        "_usage_note_3": "3. UI设计风格已设置为 " + config['ui_design_style'] + "，可修改为 corporate（企业商务）、cyberpunk（暗黑科技）、minimal（极简主义）、bauhaus（包豪斯）、japanese（日式极简）、scandinavian（斯堪的纳维亚）、futuristic（未来科技）、elegant（优雅复古）、bold（大胆现代）、artdeco（艺术装饰）、memphis（孟菲斯）、popart（波普艺术）",
        "_usage_note_4": "4. 生成配置已设置为 " + config['generation_mode'] + " 模式，可调整：generation_mode（fast快速验证/full完整生产），page_count_fast/full（各模式页面数量），api_count_min/max（API数量范围）",
        "_usage_note_5": "5. 详细填写 requires_docs/需求文档.md 文件（必需）",
        "_usage_note_6": "6. 可选填写 requires_docs/技术栈说明文档.md 和 requires_docs/UI设计规范.md（如提供自定义UI规范，需手动修改ui_design_spec路径）",
        "_usage_note_7": "7. 最后按照 工作流程.md 或 01-快速开始.md 执行八阶段生成流程",
        
        "_comment_fixed": "=== 固定配置（请勿修改） ===",
        "system_prompt_dir": "system_prompts",
        "ui_design_spec_default": "specs_docs/ui_design_specs/01-UI设计规范_默认_Corporate.md",
        
        "_comment_generated": "=== 流程生成配置（自动生成） ===",
        "framework_design": f"process_docs/{config['system_title']}_框架设计文档.md",
        "page_list": "process_docs/页面清单.md",
        "database_schema": "output_sourcecode/db/database_schema.sql",
        "copyright_application": f"output_docs/{config['system_title']}_软件著作权登记信息表.md"
    }
    
    config_file = project_dir / "ai-copyright-config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=2)
    
    print_success("配置文件创建完成")

def create_readme(project_dir, config):
    """创建 README.md 文件"""
    readme_content = f"""# {config['system_title']}

这是一个使用AI驱动的企业级软件开发工作流程创建的项目。

## 项目信息

- **系统名称**: {config['system_title']}
- **系统简称**: {config['system_short_title']}
- **前端技术**: {config['front_tech']}
- **后端技术**: {config['backend_tech']}
- **创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 目录结构

```
{config['project_name']}/
├── ai-copyright-config.json       # 项目全局配置文件
├── workflow.md                    # 工作流程文档
├── specs_docs/                     # 固定规范文档目录
│   ├── ui_design_specs/           # UI设计规范子目录
│   │   └── [选择的UI设计风格文档]   # 根据用户选择的UI风格复制相应文档
│   └── tech_stack_specs/          # 技术栈规范子目录
│       └── 技术栈说明文档_默认.md  # 默认技术栈说明模板
├── system_prompts/                 # 系统提示词目录（固定不变）
├── scripts/                       # 生成和验证脚本目录
│   ├── generators/               # 代码生成和合并脚本
│   └── validators/               # 项目验证脚本
├── requires_docs/                 # 输入文档目录
│   └── 需求文档.md                # 核心业务需求规格说明（待创建）
├── process_docs/                  # 流程中间文档目录
├── output_docs/                   # 最终交付文档目录
└── output_sourcecode/             # 生成代码目录
    ├── front/                     # 前端页面代码
    ├── backend/                   # 后端项目代码
    └── db/                        # 数据库相关文件
```

## 下一步操作

1. **创建需求文档**: 在 `requires_docs/` 目录下创建您的需求文档
2. **技术栈配置**: 如果需要自定义技术栈，请创建 `requires_docs/技术栈说明文档.md`
3. **开始开发**: 按照 `workflow.md` 中的八阶段开发流程执行

## 工作流程

详细的开发流程请参考 `workflow.md` 文档，包含以下阶段：

1. 项目初始化和框架设计
2. 系统提示词体系建设
3. 前端页面设计和开发
4. 数据库和后端开发
5. 文档生成
6. 项目整理和交付

## 支持

如有问题，请参考 `workflow.md` 中的详细说明。
"""
    
    readme_file = project_dir / "README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)

def create_requirements_template(project_dir, config):
    """创建需求文档模板"""
    requirements_content = f"""# {config['system_title']} 需求文档

## 项目背景

请在此描述项目的背景和目标。

## 功能需求

### 核心功能

1. 功能一
   - 详细描述
   - 业务规则
   - 用户角色

2. 功能二
   - 详细描述
   - 业务规则
   - 用户角色

### 非功能需求

- 性能要求
- 安全要求
- 可用性要求

## 技术要求

- 前端技术: {config['front_tech']}
- 后端技术: {config['backend_tech']}
- 其他技术要求

## 用户角色

- 角色一: 描述
- 角色二: 描述

## 业务流程

请描述主要的业务流程。

---

*请根据实际项目需求完善此文档内容*
"""
    
    requirements_file = project_dir / "requires_docs" / "需求文档.md"
    with open(requirements_file, 'w', encoding='utf-8') as f:
        f.write(requirements_content)

def create_ui_design_template(project_dir, config):
    """创建UI设计规范模板"""
    ui_design_content = f"""# UI设计规范 - {config['system_title']}

> 📝 **使用说明**：本文档为可选输入文档。如不提供，系统将使用默认的UI设计规范。
> 
> 🎯 **目的**：定义本软件项目的专属UI设计理念、风格和规范，体现软件的独特性和创新性。

## 项目设计定位

### 设计理念
<!-- 请描述本软件的设计理念，例如：现代简约、科技感、专业商务、友好亲民等 -->

### 目标用户群体
<!-- 请描述主要用户群体，设计风格应该符合用户群体的审美和使用习惯 -->

### 设计创新点
<!-- 请描述本软件在UI设计方面的创新点和特色功能 -->

## 色彩系统

### 主色调
<!-- 请定义软件的主品牌色彩，建议提供具体的色值 -->
- 主色：#[请填写]
- 辅助色：#[请填写]

### 功能色彩
<!-- 定义成功、警告、错误等状态的色彩 -->
- 成功色：#[请填写]
- 警告色：#[请填写]  
- 错误色：#[请填写]

### 中性色
<!-- 定义文字、背景、边框等中性色彩 -->
- 背景色：#[请填写]
- 文字色：#[请填写]
- 边框色：#[请填写]

## 设计风格

### 整体风格
<!-- 选择设计风格：扁平化、拟物化、毛玻璃、渐变、极简等 -->

### 圆角规范
<!-- 定义按钮、卡片等元素的圆角大小 -->

### 阴影效果
<!-- 定义卡片、弹窗等元素的阴影样式 -->

### 字体规范
<!-- 定义标题、正文、说明文字的字体大小和样式 -->

## 组件设计规范

### 按钮设计
<!-- 描述主按钮、次要按钮、文字按钮的设计规范 -->

### 表单设计
<!-- 描述输入框、下拉框、复选框等表单元素的设计 -->

### 导航设计
<!-- 描述顶部导航、侧边栏、面包屑等导航元素的设计 -->

### 数据展示
<!-- 描述表格、图表、卡片等数据展示组件的设计 -->

## 页面布局规范

### 栅格系统
<!-- 定义页面的栅格布局规则 -->

### 间距规范
<!-- 定义元素间的间距标准 -->

### 响应式设计
<!-- 描述在不同屏幕尺寸下的适配方案 -->

## 交互设计

### 动效设计
<!-- 描述页面切换、元素交互的动效规范 -->

### 反馈机制
<!-- 描述加载状态、操作反馈的设计规范 -->

### 错误处理
<!-- 描述错误提示、空状态页面的设计 -->

## 特色功能设计

### 创新交互
<!-- 描述本软件独有的交互方式或界面元素 -->

### 用户体验优化
<!-- 描述针对特定业务场景的UX优化设计 -->

## 设计资源

### 图标风格
<!-- 描述使用的图标库或自定义图标风格 -->

### 插图风格
<!-- 如使用插图，描述插图的风格和应用场景 -->

---

**注意**：
1. 请根据您的软件项目特点填写具体内容
2. 这些设计规范将影响前端页面的生成效果
3. 建议体现软件的独特性和创新性，有助于软著申请
4. 如不提供此文档，系统将使用通用的默认设计规范
"""
    
    ui_design_file = project_dir / "requires_docs" / "UI设计规范.md"
    with open(ui_design_file, 'w', encoding='utf-8') as f:
        f.write(ui_design_content)

def create_gitignore(project_dir):
    """创建 .gitignore 文件"""
    gitignore_content = """# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# IDE files
.vscode/
.idea/
*.swp
*.swo

# Temporary files
*.tmp
*.temp
.temp/

# Logs
*.log
logs/

# Node modules (if applicable)
node_modules/

# Java compiled files
*.class
target/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# Backup files
*.backup
*.bak
"""
    
    gitignore_file = project_dir / ".gitignore"
    with open(gitignore_file, 'w', encoding='utf-8') as f:
        f.write(gitignore_content)

def validate_project_integrity(project_dir, config):
    """初始化后完整性验证"""
    print_info("开始项目完整性验证...")
    validation_results = []
    
    # 1. 验证目录结构
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
    
    for directory in required_dirs:
        dir_path = project_dir / directory
        if dir_path.exists():
            validation_results.append(f"✓ 目录存在: {directory}")
        else:
            validation_results.append(f"✗ 目录缺失: {directory}")
            print_error(f"关键目录缺失: {directory}")
    
    # 2. 验证配置文件
    config_file = project_dir / "ai-copyright-config.json"
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # 检查关键配置项
            required_keys = ['title', 'ui_design_style', 'generation_mode', 'ui_design_spec']
            for key in required_keys:
                if key in config_data:
                    validation_results.append(f"✓ 配置项存在: {key}")
                else:
                    validation_results.append(f"✗ 配置项缺失: {key}")
                    
            # 验证UI设计规范文件存在
            ui_spec_path = project_dir / config_data.get('ui_design_spec', '')
            if ui_spec_path.exists():
                validation_results.append(f"✓ UI设计规范文件存在")
            else:
                validation_results.append(f"✗ UI设计规范文件缺失: {config_data.get('ui_design_spec', '')}")
                
        except json.JSONDecodeError:
            validation_results.append("✗ 配置文件JSON格式错误")
            print_error("配置文件JSON格式错误")
        except Exception as e:
            validation_results.append(f"✗ 配置文件验证失败: {str(e)}")
    else:
        validation_results.append("✗ 配置文件不存在")
        print_error("配置文件不存在")
    
    # 3. 验证系统提示词
    prompt_dir = project_dir / "system_prompts"
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
    
    for prompt_file in expected_prompts:
        prompt_path = prompt_dir / prompt_file
        if prompt_path.exists():
            validation_results.append(f"✓ 系统提示词存在: {prompt_file}")
        else:
            validation_results.append(f"✗ 系统提示词缺失: {prompt_file}")
    
    # 4. 验证脚本权限和可执行性
    script_dir = project_dir / "scripts" / "generators"
    if script_dir.exists():
        bash_scripts = list(script_dir.glob("*.sh"))
        if bash_scripts:
            validation_results.append(f"✓ 发现 {len(bash_scripts)} 个Bash脚本")
            # 检查脚本权限
            for script in bash_scripts[:3]:  # 检查前几个即可
                if os.access(script, os.X_OK):
                    validation_results.append(f"✓ 脚本可执行: {script.name}")
                else:
                    validation_results.append(f"⚠ 脚本需要执行权限: {script.name}")
                    # 自动修复权限
                    try:
                        script.chmod(0o755)
                        validation_results.append(f"✓ 已修复执行权限: {script.name}")
                    except:
                        validation_results.append(f"✗ 权限修复失败: {script.name}")
        else:
            validation_results.append("✗ 未发现生成脚本")
    
    # 5. 生成验证报告
    error_count = len([r for r in validation_results if r.startswith('✗')])
    warning_count = len([r for r in validation_results if r.startswith('⚠')])
    success_count = len([r for r in validation_results if r.startswith('✓')])
    
    print()
    print_info("=== 项目完整性验证报告 ===")
    for result in validation_results:
        if result.startswith('✓'):
            print_success(result[2:])
        elif result.startswith('⚠'):
            print_warning(result[2:])
        elif result.startswith('✗'):
            print_error(result[2:])
    
    print()
    print_info(f"验证统计: 成功 {success_count} | 警告 {warning_count} | 错误 {error_count}")
    
    if error_count == 0:
        print_success("项目初始化验证通过！")
        return True
    else:
        print_error(f"发现 {error_count} 个严重问题，请检查修复后重新验证")
        return False

def print_directory_tree(project_dir):
    """打印目录结构"""
    print_info("项目目录结构:")
    
    def print_tree(directory, prefix=""):
        """递归打印目录树"""
        items = sorted(directory.iterdir())
        for i, item in enumerate(items):
            is_last_item = i == len(items) - 1
            current_prefix = "└── " if is_last_item else "├── "
            print(f"{prefix}{current_prefix}{item.name}")
            
            if item.is_dir() and not item.name.startswith('.'):
                extension = "    " if is_last_item else "│   "
                print_tree(item, prefix + extension)
    
    print_tree(project_dir)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='AI驱动的企业级软件开发工作流程 - 项目初始化脚本')
    parser.add_argument('project_name', help='项目名称')
    parser.add_argument('--force', '-f', action='store_true', help='强制覆盖现有目录')
    
    args = parser.parse_args()
    
    project_name = args.project_name
    script_dir = Path(__file__).parent.parent.parent.absolute()  # 回到项目根目录
    project_dir = Path.cwd() / project_name
    
    print_info(f"开始初始化项目: {project_name}")
    print_info(f"项目目录: {project_dir}")
    
    # 检查目录是否已存在
    if project_dir.exists():
        if not args.force:
            print_warning(f"目录 {project_dir} 已存在")
            if not get_yes_no_input("是否继续并覆盖现有内容?"):
                print_info("操作已取消")
                sys.exit(1)
        shutil.rmtree(project_dir)
    
    # 创建项目目录
    project_dir.mkdir(parents=True, exist_ok=True)
    
    print_info("创建目录结构...")
    create_directory_structure(project_dir)
    
    # 获取用户输入
    print()
    print_info("请输入项目配置信息:")
    
    system_title = get_user_input("系统完整名称")
    if not system_title:
        print_error("系统名称不能为空")
        sys.exit(1)
    
    system_short_title = get_user_input("系统简称 (可选)", system_title)
    front_tech = get_user_input("前端技术", "JavaScript")
    backend_tech = get_user_input("后端技术", "Java")
    
    # 询问是否使用自定义技术栈文档
    print()
    use_custom_tech_stack = get_yes_no_input("是否使用自定义技术栈文档?")
    
    if use_custom_tech_stack:
        tech_stack_path = "requires_docs/技术栈说明文档.md"
        print_info(f"请将您的技术栈说明文档放在: {tech_stack_path}")
    else:
        tech_stack_path = "specs_docs/tech_stack_specs/技术栈说明文档_默认.md"
    
    # 选择UI设计风格
    print()
    ui_design_style = get_ui_design_style()
    print_success(f"已选择UI设计风格: {ui_design_style}")
    
    # 选择生成模式配置
    print()
    generation_config = get_generation_mode_config()
    print_success(f"已选择生成模式: {generation_config['generation_mode']} ({generation_config['page_count']}页面，{generation_config['api_count_min']}-{generation_config['api_count_max']}个API)")
    
    print_info("复制固定文档和系统提示词...")
    copy_fixed_documents(script_dir, project_dir, ui_design_style)
    
    print_info("创建配置文件...")
    
    # 配置对象
    config = {
        'project_name': project_name,
        'system_title': system_title,
        'system_short_title': system_short_title,
        'front_tech': front_tech,
        'backend_tech': backend_tech,
        'tech_stack_path': tech_stack_path,
        'ui_design_style': ui_design_style,
        'generation_mode': generation_config['generation_mode'],
        'page_count': generation_config['page_count'],
        'api_count_min': generation_config['api_count_min'],
        'api_count_max': generation_config['api_count_max']
    }
    
    create_config_file(project_dir, config)
    
    print_info("创建项目文档...")
    create_readme(project_dir, config)
    create_requirements_template(project_dir, config)
    create_ui_design_template(project_dir, config)
    create_gitignore(project_dir)
    
    print_success("项目文档创建完成")
    
    print()
    print_success("项目初始化完成！")
    print()
    print_info(f"项目位置: {project_dir}")
    print_info(f"配置文件: {project_dir}/ai-copyright-config.json")
    print()
    print_info("下一步操作:")
    print(f"  1. cd {project_name}")
    print("  2. 编辑 requires_docs/需求文档.md 添加您的项目需求")
    print("  3. 如需自定义技术栈，创建 requires_docs/技术栈说明文档.md")
    print("  4. 参考 workflow.md 开始开发流程")
    print()
    
    # 执行完整性验证
    print()
    validation_success = validate_project_integrity(project_dir, config)
    
    # 显示项目结构
    print()
    print_directory_tree(project_dir)
    
    print()
    if validation_success:
        print_success("项目初始化完成并通过验证！")
        print_info("建议下一步: 详细填写 requires_docs/需求文档.md")
    else:
        print_error("项目初始化完成但验证发现问题，请修复后继续")
    
    print_success("初始化脚本执行完成！")

if __name__ == "__main__":
    main()