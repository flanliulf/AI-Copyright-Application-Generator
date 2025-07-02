#!/bin/bash

# AI驱动软件著作权申请材料生成系统 - 项目完整性检查脚本 (Shell版本)
# 版本: 1.0
# 描述: 快速检查项目文件完整性和基本配置

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 计数器
SUCCESS_COUNT=0
WARNING_COUNT=0
ERROR_COUNT=0

# 打印函数
print_colored() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

print_header() {
    local title=$1
    echo
    print_colored $CYAN "============================================================"
    print_colored $CYAN "🔍 $title"
    print_colored $CYAN "============================================================"
}

print_success() {
    local message=$1
    print_colored $GREEN "✅ $message"
    ((SUCCESS_COUNT++))
}

print_warning() {
    local message=$1
    print_colored $YELLOW "⚠️  $message"
    ((WARNING_COUNT++))
}

print_error() {
    local message=$1
    print_colored $RED "❌ $message"
    ((ERROR_COUNT++))
}

print_info() {
    local message=$1
    print_colored $BLUE "ℹ️  $message"
}

# 检查文件是否存在
check_file() {
    local file_path=$1
    local required=${2:-true}
    local description=${3:-$file_path}
    
    if [ -f "$file_path" ]; then
        print_success "文件存在: $description"
        return 0
    else
        if [ "$required" = "true" ]; then
            print_error "必需文件缺失: $description"
        else
            print_warning "可选文件缺失: $description"
        fi
        return 1
    fi
}

# 检查目录是否存在
check_directory() {
    local dir_path=$1
    local required=${2:-true}
    local description=${3:-$dir_path}
    
    if [ -d "$dir_path" ]; then
        print_success "目录存在: $description"
        return 0
    else
        if [ "$required" = "true" ]; then
            print_error "必需目录缺失: $description"
        else
            print_warning "可选目录缺失: $description"
        fi
        return 1
    fi
}

# 检查核心文件
check_core_files() {
    print_header "核心文件完整性检查"
    
    # 配置文件
    check_file "ai-copyright-config.json" true "项目配置文件"
    
    # 初始化脚本
    check_file "init_project.py" true "Python初始化脚本"
    check_file "init_project.sh" true "Shell初始化脚本"
    check_file "create-copyright-project" true "全局创建脚本"
    
    # 生成脚本
    check_file "generate_all_sourcecode.py" true "Python全代码生成脚本"
    check_file "generate_frontend_sourcecode.py" true "Python前端生成脚本"
    check_file "generate_backend_sourcecode.py" true "Python后端生成脚本"
    check_file "generate_all_sourcecode.sh" true "Shell全代码生成脚本"
    check_file "generate_frontend_sourcecode.sh" true "Shell前端生成脚本"
    check_file "generate_backend_sourcecode.sh" true "Shell后端生成脚本"
    
    # 文档文件
    check_file "README.md" true "项目说明文档"
    check_file "01-快速开始.md" true "快速开始指南"
    check_file "02-安装指南.md" true "安装指南"
    check_file "03-使用说明.md" true "使用说明"
    check_file "04-故障排除.md" true "故障排除指南"
    check_file "05-FAQ.md" true "常见问题文档"
    check_file "CLAUDE.md" true "Claude指导文档"
    check_file "CLAUDE_zh.md" true "Claude中文指导文档"
    check_file "ROADMAP.md" true "发展路线图"
    check_file "工作流程.md" true "工作流程文档"
    check_file "执行计划.md" true "执行计划文档"
    check_file "项目检查指南.md" true "项目检查指南文档"
    
    # 检查脚本自身
    check_file "check_project.py" true "Python检查脚本"
}

# 检查目录结构
check_directory_structure() {
    print_header "目录结构完整性检查"
    
    check_directory "specs_docs" true "规范文档目录"
    check_directory "specs_docs/ui_design_specs" true "UI设计规范目录"
    check_directory "specs_docs/tech_stack_specs" true "技术栈规范目录"
    check_directory "system_prompts" true "AI提示词目录"
    check_directory "requires_docs" true "输入文档目录"
    check_directory "process_docs" true "流程文档目录"
    check_directory "output_docs" true "输出文档目录"
    check_directory "output_sourcecode" true "生成代码目录"
    check_directory "output_sourcecode/front" true "前端代码目录"
    check_directory "output_sourcecode/backend" true "后端代码目录"
}

# 检查UI设计规范
check_ui_design_specs() {
    print_header "UI设计规范文件检查"
    
    check_file "specs_docs/ui_design_specs/01-UI设计规范_默认_Corporate.md" true "企业商务风格规范"
    check_file "specs_docs/ui_design_specs/02-UI设计规范_暗黑科技风格_Cyberpunk.md" true "暗黑科技风格规范"
    check_file "specs_docs/ui_design_specs/03-UI设计规范_极简主义风格_Minimal.md" true "极简主义风格规范"
    
    check_file "specs_docs/tech_stack_specs/技术栈说明文档_默认.md" true "默认技术栈说明"
}

# 检查AI系统提示词
check_system_prompts() {
    print_header "AI系统提示词完整性检查"
    
    check_file "system_prompts/01-软著框架系统提示词.md" true "框架设计提示词"
    check_file "system_prompts/02-页面规划系统提示词.md" true "页面规划提示词"
    check_file "system_prompts/03-界面设计系统提示词.md" true "界面设计提示词"
    check_file "system_prompts/04-网页代码生成系统提示词.md" true "前端代码生成提示词"
    check_file "system_prompts/05-数据库代码生成系统提示词.md" true "数据库生成提示词"
    check_file "system_prompts/06-后端代码生成系统提示词.md" true "后端代码生成提示词"
    check_file "system_prompts/07-用户手册系统提示词.md" true "用户手册生成提示词"
    check_file "system_prompts/08-软件著作权登记信息表系统提示词.md" true "软著信息表生成提示词"
}

# 检查配置文件内容
check_config_file() {
    print_header "配置文件内容检查"
    
    if [ ! -f "ai-copyright-config.json" ]; then
        print_error "配置文件 ai-copyright-config.json 不存在"
        return
    fi
    
    # 检查JSON格式
    if command -v jq >/dev/null 2>&1; then
        if jq empty ai-copyright-config.json >/dev/null 2>&1; then
            print_success "配置文件JSON格式正确"
        else
            print_error "配置文件JSON格式错误"
            return
        fi
        
        # 检查关键字段
        local fields=("front" "backend" "title" "short_title" "ui_design_style")
        for field in "${fields[@]}"; do
            if jq -e ".$field" ai-copyright-config.json >/dev/null 2>&1; then
                print_success "配置字段存在: $field"
            else
                print_error "配置字段缺失: $field"
            fi
        done
        
        # 检查UI设计风格值
        local ui_style=$(jq -r '.ui_design_style' ai-copyright-config.json 2>/dev/null)
        case "$ui_style" in
            "corporate"|"cyberpunk"|"minimal"|"bauhaus"|"japanese"|"scandinavian"|"futuristic"|"elegant"|"bold"|"artdeco"|"memphis"|"popart")
                print_success "UI设计风格有效: $ui_style"
                ;;
            *)
                print_warning "UI设计风格可能无效: $ui_style"
                ;;
        esac
    else
        print_warning "未安装jq，跳过JSON内容检查"
        # 简单检查文件是否包含基本字段
        if grep -q '"front"' ai-copyright-config.json && grep -q '"backend"' ai-copyright-config.json; then
            print_success "配置文件包含基本字段"
        else
            print_warning "配置文件可能缺少基本字段"
        fi
    fi
}

# 检查脚本语法
check_script_syntax() {
    print_header "脚本语法检查"
    
    # 检查Python脚本语法
    local python_scripts=("init_project.py" "generate_all_sourcecode.py" "generate_frontend_sourcecode.py" "generate_backend_sourcecode.py" "check_project.py")
    
    for script in "${python_scripts[@]}"; do
        if [ -f "$script" ]; then
            if python3 -m py_compile "$script" 2>/dev/null; then
                print_success "Python脚本语法正确: $script"
            else
                print_error "Python脚本语法错误: $script"
            fi
        fi
    done
    
    # 检查Shell脚本语法
    local shell_scripts=("init_project.sh" "generate_all_sourcecode.sh" "generate_frontend_sourcecode.sh" "generate_backend_sourcecode.sh" "create-copyright-project")
    
    for script in "${shell_scripts[@]}"; do
        if [ -f "$script" ]; then
            if bash -n "$script" 2>/dev/null; then
                print_success "Shell脚本语法正确: $script"
            else
                print_error "Shell脚本语法错误: $script"
            fi
        fi
    done
}

# 检查文档引用一致性
check_document_references() {
    print_header "文档引用一致性检查"
    
    local docs=("README.md" "01-快速开始.md" "03-使用说明.md" "工作流程.md" "04-故障排除.md" "05-FAQ.md" "CLAUDE.md" "CLAUDE_zh.md")
    local old_refs=0
    local new_refs=0
    local problematic_docs=0
    
    for doc in "${docs[@]}"; do
        if [ -f "$doc" ]; then
            # 检查旧配置文件引用（不包括 ai-copyright-config.json）
            # 查找独立的 config.json 引用，不包括 ai-copyright-config.json
            if grep -q "config\.json" "$doc"; then
                # 计算总的 config.json 出现次数
                local total_config=$(grep -c "config\.json" "$doc")
                # 计算 ai-copyright-config.json 出现次数  
                local ai_config=$(grep -c "ai-copyright-config\.json" "$doc" 2>/dev/null || echo 0)
                # 独立的 config.json 引用 = 总数 - ai-copyright-config.json数量
                local isolated_matches=$((total_config - ai_config))
                
                if [ "$isolated_matches" -gt 0 ]; then
                    # 检查是否是说明性文本（更名说明）
                    if grep -q -E "(从.*config\.json.*更名|已从.*config\.json.*更名|config\.json.*更名为|配置文件.*从.*config\.json|原.*config\.json|旧.*config\.json|之前.*config\.json)" "$doc"; then
                        print_success "文档包含配置文件更名说明: $doc"
                    else
                        old_refs=$((old_refs + isolated_matches))
                        problematic_docs=$((problematic_docs + 1))
                        print_warning "文档包含旧配置文件引用: $doc"
                    fi
                fi
            fi
            
            # 检查新配置文件引用
            if grep -q "ai-copyright-config\.json" "$doc"; then
                local count=$(grep -c "ai-copyright-config\.json" "$doc")
                new_refs=$((new_refs + count))
                print_success "文档使用新配置文件名: $doc"
            fi
        fi
    done
    
    if [ $old_refs -eq 0 ]; then
        print_success "所有文档已更新为新配置文件名"
    else
        print_error "发现 $old_refs 处旧配置文件引用需要更新（在 $problematic_docs 个文档中）"
    fi
}

# 检查Git配置
check_git_configuration() {
    print_header "Git配置检查"
    
    # 检查.gitignore
    if [ -f ".gitignore" ]; then
        print_success ".gitignore文件存在"
        
        # 检查关键忽略项
        local ignores=("ai-copyright-config_local.json" ".DS_Store" "__pycache__" "node_modules" "*.log")
        for ignore in "${ignores[@]}"; do
            if grep -q "$ignore" .gitignore; then
                print_success "包含忽略项: $ignore"
            else
                print_warning "缺少忽略项: $ignore"
            fi
        done
    else
        print_warning ".gitignore文件不存在"
    fi
    
    # 检查Git仓库
    if [ -d ".git" ]; then
        print_success "Git仓库已初始化"
    else
        print_warning "未初始化Git仓库"
    fi
}

# 生成检查报告
generate_report() {
    print_header "检查报告汇总"
    
    local total=$((SUCCESS_COUNT + WARNING_COUNT + ERROR_COUNT))
    
    print_colored $CYAN "📊 检查统计:"
    print_colored $GREEN "   ✅ 成功: $SUCCESS_COUNT"
    print_colored $YELLOW "   ⚠️  警告: $WARNING_COUNT"
    print_colored $RED "   ❌ 错误: $ERROR_COUNT"
    print_colored $BLUE "   📋 总计: $total"
    
    # 计算健康度分数
    if [ $total -gt 0 ]; then
        local health_score=$(( (SUCCESS_COUNT * 100) / total ))
        print_colored $PURPLE "   💯 健康度: ${health_score}%"
    fi
    
    echo
    echo "============================================================"
    
    if [ $ERROR_COUNT -eq 0 ]; then
        if [ $WARNING_COUNT -eq 0 ]; then
            print_colored $GREEN "🎉 项目检查完全通过！系统可以正常使用。"
            return 0
        else
            print_colored $YELLOW "✅ 项目检查基本通过，有一些警告需要注意。"
            return 1
        fi
    else
        print_colored $RED "❌ 项目检查发现错误，需要修复后才能正常使用。"
        print_colored $RED "🔧 请运行 Python 版本获取详细错误信息: python3 check_project.py"
        return 2
    fi
}

# 主函数
main() {
    local project_dir=${1:-.}
    local quick_mode=${2:-false}
    
    # 切换到项目目录
    if [ ! -d "$project_dir" ]; then
        print_colored $RED "❌ 项目目录不存在: $project_dir"
        exit 1
    fi
    
    cd "$project_dir"
    
    print_colored $PURPLE "🚀 开始AI软著申请材料生成系统完整性检查 (Shell版本)"
    print_colored $BLUE "📁 检查目录: $(pwd)"
    
    if [ "$quick_mode" = "true" ]; then
        print_colored $YELLOW "⚡ 快速检查模式"
    fi
    
    # 执行检查
    check_core_files
    check_directory_structure
    check_ui_design_specs
    check_system_prompts
    check_config_file
    check_document_references
    check_git_configuration
    
    if [ "$quick_mode" != "true" ]; then
        check_script_syntax
    fi
    
    # 生成报告
    generate_report
    return $?
}

# 显示帮助信息
show_help() {
    echo "AI驱动软件著作权申请材料生成系统 - 项目完整性检查工具 (Shell版本)"
    echo
    echo "用法:"
    echo "  $0 [项目目录] [选项]"
    echo
    echo "参数:"
    echo "  项目目录    项目目录路径（默认为当前目录）"
    echo
    echo "选项:"
    echo "  --quick     快速检查模式（跳过语法检查）"
    echo "  --help      显示此帮助信息"
    echo
    echo "示例:"
    echo "  $0                        # 检查当前目录"
    echo "  $0 /path/to/project       # 检查指定目录"
    echo "  $0 . --quick              # 快速检查当前目录"
    echo
}

# 处理命令行参数
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    show_help
    exit 0
fi

if [ "$2" = "--quick" ] || [ "$1" = "--quick" ]; then
    if [ "$1" = "--quick" ]; then
        main "." true
    else
        main "$1" true
    fi
else
    main "$1" false
fi

exit $?