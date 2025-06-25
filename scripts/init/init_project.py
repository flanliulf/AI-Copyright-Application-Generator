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
from datetime import datetime
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
    if default:
        user_input = input(f"{prompt} (默认: {default}): ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()

def get_yes_no_input(prompt, default_no=True):
    """获取是/否输入"""
    suffix = "(y/N)" if default_no else "(Y/n)"
    response = input(f"{prompt} {suffix}: ").strip().lower()
    
    if default_no:
        return response in ['y', 'yes', '是']
    else:
        return response not in ['n', 'no', '否']

def get_ui_design_style():
    """获取用户选择的UI设计风格"""
    print_info("请选择UI设计风格:")
    print("1. corporate - 企业商务风格（默认）")
    print("   适用于：企业管理系统、办公软件、政务系统、金融应用等")
    print("   特点：专业稳重、通用性强、符合主流商务审美")
    print()
    print("2. cyberpunk - 暗黑科技风格")
    print("   适用于：开发者工具、数据分析平台、科技产品、游戏相关应用等")
    print("   特点：科技感强、适合夜间使用、吸引年轻用户群体")
    print()
    print("3. minimal - 极简主义风格")
    print("   适用于：内容管理系统、阅读类应用、教育平台、专业工具等")
    print("   特点：简洁优雅、专注内容、永恒的设计价值")
    print()
    
    while True:
        choice = input("请输入选择 (1/2/3，默认为1): ").strip()
        if choice == "" or choice == "1":
            return "corporate"
        elif choice == "2":
            return "cyberpunk"
        elif choice == "3":
            return "minimal"
        else:
            print_warning("无效选择，请输入 1、2 或 3")

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
        "output_sourcecode/backend"
    ]
    
    for directory in directories:
        os.makedirs(project_dir / directory, exist_ok=True)
    
    print_success("目录结构创建完成")

def copy_fixed_documents(script_dir, project_dir):
    """复制固定文档和系统提示词"""
    specs_source = script_dir / "specs_docs"
    
    if not specs_source.exists():
        print_error(f"源文件目录不存在: {specs_source}")
        print_info("请确保脚本在包含 specs_docs 目录的项目根目录中运行")
        sys.exit(1)
    
    # 复制UI设计规范文档
    ui_design_files = [
        "01-UI设计规范_默认_Corporate.md",
        "02-UI设计规范_暗黑科技风格_Cyberpunk.md",
        "03-UI设计规范_极简主义风格_Minimal.md"
    ]
    
    for file_name in ui_design_files:
        src = specs_source / "ui_design_specs" / file_name
        dst = project_dir / "specs_docs" / "ui_design_specs" / file_name
        if src.exists():
            shutil.copy2(src, dst)
    
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
    config_data = {
        "_comment_init": "=== 项目初始化配置（用户设置） ===",
        "front": config['front_tech'],
        "backend": config['backend_tech'],
        "title": config['system_title'],
        "short_title": config['system_short_title'],
        "system_profile": "requires_docs/需求文档.md",
        "dev_tech_stack": config['tech_stack_path'],
        "ui_design_spec": "requires_docs/UI设计规范.md",
        "ui_design_style": config['ui_design_style'],
        
        "_comment_generation": "=== 生成配置（可调整） ===",
        "page_count_fast": 5,
        "page_count_full": 10,
        "api_count_min": 8,
        "api_count_max": 35,
        "generation_mode": "fast",
        
        "_comment_usage": "=== 使用说明 ===",
        "_usage_note_1": "1. 请务必修改上方的 title 和 short_title 为您的实际项目名称",
        "_usage_note_2": "2. front 和 backend 可根据实际技术栈修改（如 React, Vue, Python, Node.js 等）",
        "_usage_note_3": "3. UI设计风格已设置为 " + config['ui_design_style'] + "，可修改为 corporate（企业商务）、cyberpunk（暗黑科技）、minimal（极简主义）",
        "_usage_note_4": "4. 生成配置调整：generation_mode（fast快速验证5页/full完整生产10页），page_count_fast/full（各模式页面数量），api_count_min/max（API数量范围）",
        "_usage_note_5": "5. 详细填写 requires_docs/需求文档.md 文件（必需）",
        "_usage_note_6": "6. 可选填写 requires_docs/技术栈说明文档.md 和 requires_docs/UI设计规范.md（自定义UI规范会覆盖ui_design_style选择）",
        "_usage_note_7": "7. 最后按照 工作流程.md 或 01-快速开始.md 执行六阶段生成流程",
        
        "_comment_fixed": "=== 固定配置（请勿修改） ===",
        "system_prompt_dir": "system_prompts",
        "ui_design_spec_default": "specs_docs/ui_design_specs/01-UI设计规范_默认_Corporate.md",
        
        "_comment_generated": "=== 流程生成配置（自动生成） ===",
        "framework_design": f"process_docs/{config['system_title']}_框架设计文档.md",
        "page_list": "process_docs/页面清单.md",
        "database_schema": "output_sourcecode/db/database_schema.sql",
        "deploy_requirements": f"output_docs/{config['system_title']}_软件著作权登记信息表.md"
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
│   │   ├── 01-UI设计规范_默认_Corporate.md # 默认UI设计规范 (企业商务风格)
│   │   ├── 02-UI设计规范_暗黑科技风格_Cyberpunk.md # 暗黑科技风格 (赛博朋克)
│   │   └── 03-UI设计规范_极简主义风格_Minimal.md # 极简主义风格
│   └── tech_stack_specs/          # 技术栈规范子目录
│       └── 技术栈说明文档_默认.md  # 默认技术栈说明模板
├── system_prompts/                 # 系统提示词目录（固定不变）
├── requires_docs/                 # 输入文档目录
│   └── 需求文档.md                # 核心业务需求规格说明（待创建）
├── process_docs/                  # 流程中间文档目录
├── output_docs/                   # 最终交付文档目录
└── output_sourcecode/             # 生成代码目录
    ├── front/                     # 前端页面代码
    └── backend/                   # 后端项目代码
```

## 下一步操作

1. **创建需求文档**: 在 `requires_docs/` 目录下创建您的需求文档
2. **技术栈配置**: 如果需要自定义技术栈，请创建 `requires_docs/技术栈说明文档.md`
3. **开始开发**: 按照 `workflow.md` 中的六阶段开发流程执行

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
    
    print_info("复制固定文档和系统提示词...")
    copy_fixed_documents(script_dir, project_dir)
    
    print_info("创建配置文件...")
    
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
    
    # 配置对象
    config = {
        'project_name': project_name,
        'system_title': system_title,
        'system_short_title': system_short_title,
        'front_tech': front_tech,
        'backend_tech': backend_tech,
        'tech_stack_path': tech_stack_path,
        'ui_design_style': ui_design_style
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
    
    # 显示项目结构
    print_directory_tree(project_dir)
    
    print_success("初始化脚本执行完成！")

if __name__ == "__main__":
    main()