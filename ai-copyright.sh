#!/bin/bash

# AI驱动软件著作权申请材料生成系统 - 统一入口脚本 (Shell版本)
# 版本: 1.0

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

print_colored() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

print_header() {
    print_colored $CYAN "======================================================================"
    print_colored $PURPLE "🤖 AI驱动软件著作权申请材料生成系统"
    print_colored $BLUE "   统一管理工具 v1.0 (Shell版本)"
    print_colored $CYAN "======================================================================"
}

show_help() {
    echo "用法: $0 <命令> [选项]"
    echo
    echo "可用命令:"
    echo "  init <项目名称>              初始化新项目"
    echo "  generate <all|frontend|backend>  生成源代码"
    echo "  check [--quick] [路径]       检查项目完整性"
    echo "  test [路径]                  运行自动化测试"
    echo "  validate-frontend            验证前端页面完整性"
    echo "  status                       显示项目状态"
    echo
    echo "示例:"
    echo "  $0 init \"我的项目\""
    echo "  $0 generate all"
    echo "  $0 check --quick"
    echo "  $0 test"
}

init_project() {
    local project_name=$1
    local force_flag=$2
    
    if [ -z "$project_name" ]; then
        print_colored $RED "❌ 请提供项目名称"
        echo "用法: $0 init <项目名称>"
        return 1
    fi
    
    local cmd="python3 ${SCRIPT_DIR}/scripts/init/init_project.py '$project_name'"
    if [ "$force_flag" = "--force" ]; then
        cmd="$cmd --force"
    fi
    
    print_colored $BLUE "🔄 初始化项目 '$project_name'..."
    eval $cmd
}

generate_code() {
    local type=$1
    
    case $type in
        "all")
            script="generate_all_sourcecode.py"
            desc="生成所有源代码"
            ;;
        "frontend")
            script="generate_frontend_sourcecode.py"
            desc="生成前端源代码"
            ;;
        "backend")
            script="generate_backend_sourcecode.py"
            desc="生成后端源代码"
            ;;
        *)
            print_colored $RED "❌ 无效的生成类型: $type"
            echo "可用类型: all, frontend, backend"
            return 1
            ;;
    esac
    
    print_colored $BLUE "🔄 $desc..."
    python3 "${SCRIPT_DIR}/scripts/generators/$script"
}

check_project() {
    local quick_flag=$1
    local project_path=$2
    
    local cmd="python3 ${SCRIPT_DIR}/scripts/validators/check_project.py"
    
    if [ "$quick_flag" = "--quick" ]; then
        cmd="$cmd --quick"
        if [ -n "$project_path" ]; then
            cmd="$cmd '$project_path'"
        fi
    elif [ -n "$quick_flag" ] && [ "$quick_flag" != "--quick" ]; then
        # quick_flag实际上是路径
        cmd="$cmd '$quick_flag'"
    fi
    
    print_colored $BLUE "🔄 检查项目完整性..."
    eval $cmd
}

run_tests() {
    local project_path=$1
    
    local cmd="python3 ${SCRIPT_DIR}/scripts/validators/run_tests.py"
    if [ -n "$project_path" ]; then
        cmd="$cmd '$project_path'"
    fi
    
    print_colored $BLUE "🔄 运行自动化测试..."
    eval $cmd
}

validate_frontend() {
    print_colored $BLUE "🔄 验证前端页面完整性..."
    python3 "${SCRIPT_DIR}/scripts/validators/validate_frontend_pages.py"
}

show_status() {
    print_colored $CYAN "\n📊 项目状态概览"
    echo "----------------------------------------------------"
    
    # 检查配置文件
    if [ -f "${SCRIPT_DIR}/ai-copyright-config.json" ]; then
        print_colored $GREEN "✅ 项目配置文件存在"
    elif [ -f "${SCRIPT_DIR}/config/ai-copyright-config.example.json" ]; then
        print_colored $YELLOW "⚠️  使用模板配置文件，请复制并自定义"
        echo "   cp ${SCRIPT_DIR}/config/ai-copyright-config.example.json ${SCRIPT_DIR}/ai-copyright-config.json"
    else
        print_colored $RED "❌ 配置文件缺失"
    fi
    
    # 检查关键目录
    local dirs=("requires_docs:输入文档目录" "output_docs:输出文档目录" "output_sourcecode:生成代码目录" "specs_docs:规范文档目录" "system_prompts:AI提示词目录")
    
    for dir_info in "${dirs[@]}"; do
        local dir_name="${dir_info%:*}"
        local desc="${dir_info#*:}"
        
        if [ -d "${SCRIPT_DIR}/$dir_name" ]; then
            print_colored $GREEN "✅ $desc 存在"
        else
            print_colored $RED "❌ $desc 缺失"
        fi
    done
}

main() {
    print_header
    
    if [ $# -eq 0 ]; then
        print_colored $YELLOW "\n⚠️  未指定命令，显示帮助信息:"
        show_help
        return 0
    fi
    
    local command=$1
    shift
    
    case $command in
        "init")
            init_project "$@"
            ;;
        "generate")
            generate_code "$@"
            ;;
        "check")
            check_project "$@"
            ;;
        "test")
            run_tests "$@"
            ;;
        "validate-frontend")
            validate_frontend
            ;;
        "status")
            show_status
            ;;
        "help"|"--help"|"-h")
            show_help
            ;;
        *)
            print_colored $RED "❌ 未知命令: $command"
            echo
            show_help
            return 1
            ;;
    esac
}

main "$@"