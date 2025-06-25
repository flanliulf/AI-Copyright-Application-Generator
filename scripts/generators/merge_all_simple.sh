#!/bin/bash

# 一键拼接所有源代码脚本
# 功能：批量执行所有源代码拼接脚本，生成完整的软著申请源代码材料
# 
# 执行顺序：
# 1. 前端源代码拼接
# 2. 后端源代码拼接  
# 3. 数据库代码拼接
# 4. 全量源代码拼接（可选）

echo "🚀 开始批量拼接所有源代码..."
echo "=========================================="

# 设置脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
GENERATORS_DIR="${SCRIPT_DIR}/scripts/generators"

# 统计信息
SUCCESS_COUNT=0
TOTAL_COUNT=0
FAILED_SCRIPTS=()

# 执行拼接脚本的函数
run_merge_script() {
    local script_name="$1"
    local script_path="${GENERATORS_DIR}/${script_name}"
    local description="$2"
    
    ((TOTAL_COUNT++))
    
    echo ""
    echo "📋 [$TOTAL_COUNT] 执行: $description"
    echo "🔧 脚本: $script_name"
    echo "----------------------------------------"
    
    if [ -f "$script_path" ] && [ -x "$script_path" ]; then
        if "$script_path"; then
            echo "✅ $description - 完成"
            ((SUCCESS_COUNT++))
        else
            echo "❌ $description - 失败"
            FAILED_SCRIPTS+=("$script_name")
        fi
    else
        echo "❌ 脚本不存在或无执行权限: $script_path"
        FAILED_SCRIPTS+=("$script_name")
    fi
}

# 按顺序执行所有拼接脚本
echo "🎯 开始执行源代码拼接任务..."

# 1. 前端源代码拼接
run_merge_script "merge_frontend_simple.sh" "前端源代码拼接"

# 2. 后端源代码拼接
run_merge_script "merge_backend_simple.sh" "后端源代码拼接"

# 3. 数据库代码拼接
run_merge_script "merge_database_simple.sh" "数据库代码拼接"

# 询问是否执行全量拼接
echo ""
echo "🤔 是否要执行全量源代码拼接？(将所有类型的源代码合并到一个文件)"
echo "   - 优点：一个文件包含所有源代码，方便提交"
echo "   - 缺点：文件较大，可能超过某些系统的限制"
read -p "执行全量拼接吗？[y/N]: " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    run_merge_script "merge_sourcecode_all.sh" "全量源代码拼接"
fi

# 显示执行结果汇总
echo ""
echo "=========================================="
echo "📊 执行结果汇总"
echo "=========================================="
echo "✅ 成功: $SUCCESS_COUNT/$TOTAL_COUNT"

if [ ${#FAILED_SCRIPTS[@]} -gt 0 ]; then
    echo "❌ 失败的脚本:"
    printf "   - %s\n" "${FAILED_SCRIPTS[@]}"
    echo ""
    echo "💡 失败原因可能："
    echo "   1. 源代码目录不存在（需要先生成源代码）"
    echo "   2. 脚本权限问题（运行 chmod +x scripts/generators/*.sh）"
    echo "   3. 依赖的工具未安装"
fi

echo ""
echo "📁 生成的文件位置："
echo "   - output_docs/前端源代码.txt"
echo "   - output_docs/后端源代码.txt"
echo "   - output_docs/数据库代码.txt"
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "   - output_docs/完整源代码合集.txt"
fi

echo ""
echo "💡 使用说明："
echo "   - 生成的文件可直接用于软著申请"
echo "   - 无需AI处理，避免token消耗"
echo "   - 建议检查文件内容完整性后提交"

if [ $SUCCESS_COUNT -eq $TOTAL_COUNT ]; then
    echo ""
    echo "🎉 所有拼接任务执行成功！"
    exit 0
else
    echo ""
    echo "⚠️  部分任务执行失败，请检查上述错误信息"
    exit 1
fi