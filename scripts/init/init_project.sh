#!/bin/bash

# AI驱动的企业级软件开发工作流程 - 项目初始化脚本
# 版本: 1.0
# 描述: 自动创建新项目的目录结构和固定文档

set -e  # 遇到错误时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

print_success() {
    print_message $GREEN "✓ $1"
}

print_info() {
    print_message $BLUE "ℹ $1"
}

print_warning() {
    print_message $YELLOW "⚠ $1"
}

print_error() {
    print_message $RED "✗ $1"
}

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"  # 回到项目根目录

# 检查是否提供了项目名称
if [ $# -eq 0 ]; then
    print_error "请提供项目名称作为参数"
    echo "用法: $0 <项目名称>"
    echo "示例: $0 my-ai-project"
    exit 1
fi

PROJECT_NAME=$1
PROJECT_DIR="${PWD}/${PROJECT_NAME}"

print_info "开始初始化项目: ${PROJECT_NAME}"
print_info "项目目录: ${PROJECT_DIR}"

# 检查目录是否已存在
if [ -d "$PROJECT_DIR" ]; then
    print_warning "目录 ${PROJECT_DIR} 已存在"
    read -p "是否继续并覆盖现有内容? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "操作已取消"
        exit 1
    fi
    rm -rf "$PROJECT_DIR"
fi

# 创建项目根目录
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

print_info "创建目录结构..."

# 创建主要目录结构
mkdir -p specs_docs/ui_design_specs
mkdir -p specs_docs/tech_stack_specs
mkdir -p system_prompts
mkdir -p requires_docs
mkdir -p process_docs
mkdir -p output_docs
mkdir -p output_sourcecode/front
mkdir -p output_sourcecode/backend
mkdir -p output_sourcecode/db
mkdir -p scripts/generators
mkdir -p scripts/validators

print_success "目录结构创建完成"

# 检查源文件是否存在
SPECS_SOURCE="${SCRIPT_DIR}/specs_docs"
if [ ! -d "$SPECS_SOURCE" ]; then
    print_error "源文件目录不存在: ${SPECS_SOURCE}"
    print_info "请确保脚本在包含 specs_docs 目录的项目根目录中运行"
    exit 1
fi

print_info "复制固定文档和系统提示词..."

# 复制选择的UI设计规范文档
print_info "复制UI设计规范: ${UI_FILE}"
cp "${SPECS_SOURCE}/ui_design_specs/${UI_FILE}" specs_docs/ui_design_specs/

# 如果不是企业风格，也复制默认企业风格作为参考
if [ "$UI_DESIGN_STYLE" != "corporate" ]; then
    cp "${SPECS_SOURCE}/ui_design_specs/01-UI设计规范_默认_Corporate.md" specs_docs/ui_design_specs/
fi

# 复制技术栈规范文档
cp "${SPECS_SOURCE}/tech_stack_specs/技术栈说明文档_默认.md" specs_docs/tech_stack_specs/

# 复制系统提示词
cp -r "${SCRIPT_DIR}/system_prompts/"* system_prompts/

# 复制scripts目录（生成和验证脚本）
if [ -d "${SCRIPT_DIR}/scripts/generators" ]; then
    print_info "复制生成脚本..."
    cp "${SCRIPT_DIR}/scripts/generators/"* scripts/generators/
fi

if [ -d "${SCRIPT_DIR}/scripts/validators" ]; then
    print_info "复制验证脚本..."
    cp "${SCRIPT_DIR}/scripts/validators/"* scripts/validators/
fi

# 复制工作流程文档和执行计划文档
if [ -f "${SCRIPT_DIR}/工作流程.md" ]; then
    cp "${SCRIPT_DIR}/工作流程.md" ./
else
    print_warning "工作流程文档不存在: ${SCRIPT_DIR}/工作流程.md"
fi

if [ -f "${SCRIPT_DIR}/执行计划.md" ]; then
    cp "${SCRIPT_DIR}/执行计划.md" ./
else
    print_warning "执行计划文档不存在: ${SCRIPT_DIR}/执行计划.md"
fi

print_success "固定文档复制完成"

print_info "创建配置文件..."

# 获取用户输入的项目配置
echo
print_info "请输入项目配置信息:"

read -p "系统完整名称: " SYSTEM_TITLE
read -p "系统简称 (可选，回车跳过): " SYSTEM_SHORT_TITLE
read -p "前端技术 (默认: JavaScript): " FRONT_TECH
read -p "后端技术 (默认: Java): " BACKEND_TECH

# 设置默认值
FRONT_TECH=${FRONT_TECH:-"JavaScript"}
BACKEND_TECH=${BACKEND_TECH:-"Java"}
SYSTEM_SHORT_TITLE=${SYSTEM_SHORT_TITLE:-"${SYSTEM_TITLE}"}

# 询问是否使用自定义技术栈文档
echo
read -p "是否使用自定义技术栈文档? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    TECH_STACK_PATH="requires_docs/技术栈说明文档.md"
    print_info "请将您的技术栈说明文档放在: ${TECH_STACK_PATH}"
else
    TECH_STACK_PATH="specs_docs/tech_stack_specs/技术栈说明文档_默认.md"
fi

# 选择UI设计风格
echo
print_info "请选择UI设计风格:"
echo " 1. corporate - 企业商务风格（默认）"
echo " 2. cyberpunk - 暗黑科技风格"
echo " 3. minimal - 极简主义风格"
echo " 4. bauhaus - 包豪斯风格"
echo " 5. japanese - 日式极简风格"
echo " 6. scandinavian - 斯堪的纳维亚风格"
echo " 7. futuristic - 未来科技风格"
echo " 8. elegant - 优雅复古风格"
echo " 9. bold - 大胆现代风格"
echo "10. artdeco - 艺术装饰风格"
echo "11. memphis - 孟菲斯风格"
echo "12. popart - 波普艺术风格"
echo

while true; do
    read -p "请输入选择 (1-12，默认为1): " UI_CHOICE
    UI_CHOICE=${UI_CHOICE:-"1"}
    
    case $UI_CHOICE in
        1) UI_DESIGN_STYLE="corporate"; UI_FILE="01-UI设计规范_默认_Corporate.md"; break;;
        2) UI_DESIGN_STYLE="cyberpunk"; UI_FILE="02-UI设计规范_暗黑科技风格_Cyberpunk.md"; break;;
        3) UI_DESIGN_STYLE="minimal"; UI_FILE="03-UI设计规范_极简主义风格_Minimal.md"; break;;
        4) UI_DESIGN_STYLE="bauhaus"; UI_FILE="04-UI设计规范_包豪斯风格_Bauhaus.md"; break;;
        5) UI_DESIGN_STYLE="japanese"; UI_FILE="05-UI设计规范_日式极简风格_Japanese.md"; break;;
        6) UI_DESIGN_STYLE="scandinavian"; UI_FILE="06-UI设计规范_斯堪的纳维亚风格_Scandinavian.md"; break;;
        7) UI_DESIGN_STYLE="futuristic"; UI_FILE="07-UI设计规范_未来科技风格_Futuristic.md"; break;;
        8) UI_DESIGN_STYLE="elegant"; UI_FILE="08-UI设计规范_优雅复古风格_Elegant.md"; break;;
        9) UI_DESIGN_STYLE="bold"; UI_FILE="09-UI设计规范_大胆现代风格_Bold.md"; break;;
        10) UI_DESIGN_STYLE="artdeco"; UI_FILE="10-UI设计规范_艺术装饰风格_ArtDeco.md"; break;;
        11) UI_DESIGN_STYLE="memphis"; UI_FILE="11-UI设计规范_孟菲斯风格_Memphis.md"; break;;
        12) UI_DESIGN_STYLE="popart"; UI_FILE="12-UI设计规范_波普艺术风格_PopArt.md"; break;;
        *) print_warning "无效选择，请输入 1 到 12 之间的数字";;
    esac
done

print_success "已选择UI设计风格: ${UI_DESIGN_STYLE}"

# 选择生成模式配置
echo
print_info "请选择生成模式:"
echo "1. fast - 快速验证模式（5页面，8-15个API，适合快速原型和测试）"
echo "2. full - 完整生产模式（10页面，15-35个API，适合正式申请和完整系统）"
echo

while true; do
    read -p "请输入选择 (1-2，默认为1): " GEN_CHOICE
    GEN_CHOICE=${GEN_CHOICE:-"1"}
    
    case $GEN_CHOICE in
        1) GENERATION_MODE="fast"; PAGE_COUNT=5; API_MIN=8; API_MAX=15; break;;
        2) GENERATION_MODE="full"; PAGE_COUNT=10; API_MIN=15; API_MAX=35; break;;
        *) print_warning "无效选择，请输入 1 或 2";;
    esac
done

print_success "已选择生成模式: ${GENERATION_MODE} (${PAGE_COUNT}页面，${API_MIN}-${API_MAX}个API)"

# 生成 ai-copyright-config.json
cat > ai-copyright-config.json << EOF
{
  "_comment_init": "=== 项目初始化配置（用户设置） ===",
  "front": "${FRONT_TECH}",
  "backend": "${BACKEND_TECH}",
  "title": "${SYSTEM_TITLE}",
  "short_title": "${SYSTEM_SHORT_TITLE}",
  "system_profile": "requires_docs/需求文档.md",
  "dev_tech_stack": "${TECH_STACK_PATH}",
  "ui_design_spec": "specs_docs/ui_design_specs/${UI_FILE}",
  "ui_design_style": "${UI_DESIGN_STYLE}",
  
  "_comment_generation": "=== 生成配置（可调整） ===",
  "page_count_fast": 5,
  "page_count_full": 10,
  "api_count_min": ${API_MIN},
  "api_count_max": ${API_MAX},
  "generation_mode": "${GENERATION_MODE}",
  
  "_comment_usage": "=== 使用说明 ===",
  "_usage_note_1": "1. 请务必修改上方的 title 和 short_title 为您的实际项目名称",
  "_usage_note_2": "2. front 和 backend 可根据实际技术栈修改（如 React, Vue, Python, Node.js 等）",
  "_usage_note_3": "3. UI设计风格已设置为 ${UI_DESIGN_STYLE}，可修改为 corporate、cyberpunk、minimal、bauhaus、japanese、scandinavian、futuristic、elegant、bold、artdeco、memphis、popart",
  "_usage_note_4": "4. 生成配置已设置为 ${GENERATION_MODE} 模式，可调整：generation_mode（fast快速验证/full完整生产），page_count_fast/full（各模式页面数量），api_count_min/max（API数量范围）",
  "_usage_note_5": "5. 详细填写 requires_docs/需求文档.md 文件（必需）",
  "_usage_note_6": "6. 可选填写 requires_docs/技术栈说明文档.md 和 requires_docs/UI设计规范.md（如提供自定义UI规范，需手动修改ui_design_spec路径）",
  "_usage_note_7": "7. 最后按照 工作流程.md 或 01-快速开始.md 执行六阶段生成流程",
  
  "_comment_fixed": "=== 固定配置（请勿修改） ===",
  "system_prompt_dir": "system_prompts",
  "ui_design_spec_default": "specs_docs/ui_design_specs/01-UI设计规范_默认_Corporate.md",
  
  "_comment_generated": "=== 流程生成配置（自动生成） ===",
  "framework_design": "process_docs/${SYSTEM_TITLE}_框架设计文档.md",
  "page_list": "process_docs/页面清单.md",
  "database_schema": "output_sourcecode/db/database_schema.sql",
  "deploy_requirements": "output_docs/${SYSTEM_TITLE}_软件著作权登记信息表.md"
}
EOF

print_success "配置文件创建完成"

print_info "创建说明文件..."

# 创建项目说明文件
cat > README.md << EOF
# ${SYSTEM_TITLE}

这是一个使用AI驱动的企业级软件开发工作流程创建的项目。

## 项目信息

- **系统名称**: ${SYSTEM_TITLE}
- **系统简称**: ${SYSTEM_SHORT_TITLE}
- **前端技术**: ${FRONT_TECH}
- **后端技术**: ${BACKEND_TECH}
- **创建时间**: $(date +"%Y-%m-%d %H:%M:%S")

## 目录结构

\`\`\`
${PROJECT_NAME}/
├── ai-copyright-config.json       # 项目全局配置文件
├── 工作流程.md                    # 工作流程文档
├── 执行计划.md                    # 执行计划文档
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
\`\`\`

## 下一步操作

1. **创建需求文档**: 在 \`requires_docs/\` 目录下创建您的需求文档
2. **技术栈配置**: 如果需要自定义技术栈，请创建 \`requires_docs/技术栈说明文档.md\`
3. **开始开发**: 按照 \`工作流程.md\` 中的六阶段开发流程执行

## 工作流程

详细的开发流程请参考 \`工作流程.md\` 文档，包含以下阶段：

1. 项目初始化和框架设计
2. 系统提示词体系建设
3. 前端页面设计和开发
4. 数据库和后端开发
5. 文档生成
6. 项目整理和交付

## 支持

如有问题，请参考 \`工作流程.md\` 中的详细说明。
EOF

# 创建需求文档模板
cat > requires_docs/需求文档.md << EOF
# ${SYSTEM_TITLE} 需求文档

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

- 前端技术: ${FRONT_TECH}
- 后端技术: ${BACKEND_TECH}
- 其他技术要求

## 用户角色

- 角色一: 描述
- 角色二: 描述

## 业务流程

请描述主要的业务流程。

---

*请根据实际项目需求完善此文档内容*
EOF

# 创建UI设计规范模板
cat > requires_docs/UI设计规范.md << EOF
# UI设计规范 - ${SYSTEM_TITLE}

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
EOF

print_success "项目文档创建完成"

# 创建 .gitignore 文件
cat > .gitignore << EOF
# OS generated files
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

# Backup files
*.backup
*.bak
EOF

print_success "Git忽略文件创建完成"

echo
print_success "项目初始化完成！"
echo
print_info "项目位置: ${PROJECT_DIR}"
print_info "配置文件: ${PROJECT_DIR}/ai-copyright-config.json"
echo
print_info "下一步操作:"
echo "  1. cd ${PROJECT_NAME}"
echo "  2. 编辑 requires_docs/需求文档.md 添加您的项目需求"
echo "  3. 如需自定义技术栈，创建 requires_docs/技术栈说明文档.md"
echo "  4. 参考 工作流程.md 开始开发流程"
echo

# 执行完整性验证
echo
print_info "开始项目完整性验证..."

# 验证关键目录
VALIDATION_ERRORS=0
REQUIRED_DIRS=(
    "specs_docs/ui_design_specs"
    "specs_docs/tech_stack_specs"
    "system_prompts"
    "requires_docs"
    "process_docs"
    "output_docs"
    "output_sourcecode/front"
    "output_sourcecode/backend"
    "output_sourcecode/db"
    "scripts/generators"
    "scripts/validators"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        print_success "目录存在: $dir"
    else
        print_error "目录缺失: $dir"
        ((VALIDATION_ERRORS++))
    fi
done

# 验证配置文件
if [ -f "ai-copyright-config.json" ]; then
    print_success "配置文件存在"
    # 简单JSON格式验证
    if python3 -m json.tool ai-copyright-config.json >/dev/null 2>&1; then
        print_success "配置文件JSON格式正确"
    else
        print_error "配置文件JSON格式错误"
        ((VALIDATION_ERRORS++))
    fi
else
    print_error "配置文件不存在"
    ((VALIDATION_ERRORS++))
fi

# 验证脚本权限
if [ -d "scripts/generators" ]; then
    SCRIPT_COUNT=$(find scripts/generators -name "*.sh" | wc -l)
    if [ $SCRIPT_COUNT -gt 0 ]; then
        print_success "发现 $SCRIPT_COUNT 个生成脚本"
        # 自动修复脚本权限
        chmod +x scripts/generators/*.sh scripts/validators/*.sh 2>/dev/null
        print_success "已设置脚本执行权限"
    else
        print_error "未发现生成脚本"
        ((VALIDATION_ERRORS++))
    fi
fi

# 验证报告
echo
print_info "=== 项目完整性验证报告 ==="
if [ $VALIDATION_ERRORS -eq 0 ]; then
    print_success "项目初始化验证通过！"
    print_info "建议下一步: 详细填写 requires_docs/需求文档.md"
else
    print_error "发现 $VALIDATION_ERRORS 个问题，请检查修复"
fi

# 显示项目结构
echo
print_info "项目目录结构:"
if command -v tree >/dev/null 2>&1; then
    tree "$PROJECT_DIR" -I '__pycache__|*.pyc|.git'
else
    find "$PROJECT_DIR" -type d | sed 's|[^/]*/|  |g'
fi

print_success "初始化脚本执行完成！"