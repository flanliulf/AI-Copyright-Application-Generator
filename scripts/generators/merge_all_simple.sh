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

# 全量拼接函数（内联实现，避免依赖额外脚本）
perform_full_merge() {
    local sourcecode_dir="${SCRIPT_DIR}/output_sourcecode"
    local output_dir="${SCRIPT_DIR}/output_docs"
    local output_file="${output_dir}/完整源代码合集.txt"
    
    # 确保目录存在
    mkdir -p "${output_dir}"
    
    # 检查源代码目录
    if [ ! -d "${sourcecode_dir}" ]; then
        echo "❌ 源代码目录不存在: ${sourcecode_dir}"
        return 1
    fi
    
    # 定义要拼接的文件类型
    local file_extensions=(
        "*.html" "*.css" "*.js" "*.ts" "*.mjs"
        "*.java" "*.jsp" "*.xml" "*.py" "*.cs" "*.csproj" "*.sln"
        "*.php" "*.go" "*.mod" "*.json" "*.yml" "*.yaml" 
        "*.properties" "*.env" "*.sql" "*.md" "*.txt"
    )
    
    # 查找所有匹配的文件
    local all_files=()
    for ext in "${file_extensions[@]}"; do
        while IFS= read -r -d '' file; do
            all_files+=("$file")
        done < <(find "${sourcecode_dir}" -type f -name "$ext" -print0 | sort -z)
    done
    
    if [ ${#all_files[@]} -eq 0 ]; then
        echo "❌ 未找到源代码文件"
        return 1
    fi
    
    echo "📊 找到 ${#all_files[@]} 个源代码文件"
    
    # 清空输出文件
    > "${output_file}"
    
    # 拼接所有源代码文件
    local counter=1
    for file in "${all_files[@]}"; do
        local relative_path="${file#$sourcecode_dir/}"
        local filename=$(basename "$file")
        local extension="${filename##*.}"
        
        echo "📄 处理 ($counter/${#all_files[@]}): $relative_path"
        
        # 根据文件类型设置注释格式
        local comment_start comment_end
        case "$extension" in
            "html"|"css"|"js"|"ts"|"mjs") comment_start="/*" && comment_end="*/" ;;
            "java"|"jsp"|"cs"|"php"|"go"|"mod") comment_start="//" && comment_end="" ;;
            "xml"|"csproj"|"sln") comment_start="<!--" && comment_end="-->" ;;
            "py"|"yml"|"yaml"|"sql"|"properties"|"env") comment_start="#" && comment_end="" ;;
            "json") comment_start="//" && comment_end="" ;;
            *) comment_start="/*" && comment_end="*/" ;;
        esac
        
        # 写入文件分隔符和内容
        cat >> "${output_file}" << EOF

$comment_start ==================== $relative_path ==================== $comment_end

EOF
        
        if [ -r "$file" ]; then
            cat "$file" >> "${output_file}"
        else
            echo "<!-- 无法读取文件: $relative_path -->" >> "${output_file}"
        fi
        
        cat >> "${output_file}" << EOF

$comment_start ==================== $relative_path 结束 ==================== $comment_end

EOF
        
        ((counter++))
    done
    
    # 显示结果
    if [ -f "${output_file}" ]; then
        local file_size=$(wc -c < "${output_file}")
        local line_count=$(wc -l < "${output_file}")
        
        echo "📁 输出文件: ${output_file}"
        echo "📊 文件大小: $(( file_size / 1024 )) KB"
        echo "📋 总行数: $line_count"
        echo "📄 源文件数: ${#all_files[@]}"
        return 0
    else
        echo "❌ 生成失败"
        return 1
    fi
}

# 让用户选择拼接策略（避免重复处理）
echo "🎯 请选择软著申请材料生成策略："
echo ""
echo "📋 [1] 分类拼接 - 生成独立的模块文件"
echo "    ✓ 前端源代码.txt + 后端源代码.txt + 数据库代码.txt"
echo "    ✓ 适合：分模块提交，便于审核人员理解"
echo "    ✓ 文件数量：3个"
echo ""
echo "📦 [2] 全量拼接 - 生成统一的完整文件"  
echo "    ✓ 完整源代码合集.txt（包含所有前端+后端+数据库代码）"
echo "    ✓ 适合：统一提交，单文件管理"
echo "    ✓ 文件数量：1个"
echo ""
read -p "请选择拼接策略 [1-分类/2-全量]: " -n 1 -r
echo
echo

case $REPLY in
    1)
        echo "📋 选择：分类拼接模式"
        echo "========================================"
        
        # 分类拼接：依次执行各个独立脚本
        run_merge_script "merge_frontend_simple.sh" "前端源代码拼接"
        run_merge_script "merge_backend_simple.sh" "后端源代码拼接"
        run_merge_script "merge_database_simple.sh" "数据库代码拼接"
        ;;
    2)
        echo "📦 选择：全量拼接模式"
        echo "========================================"
        
        # 全量拼接：直接扫描并拼接所有源代码文件
        echo "📦 执行全量源代码拼接..."
        echo "----------------------------------------"
        
        # 执行内联的全量拼接逻辑
        if perform_full_merge; then
            echo "✅ 全量源代码拼接 - 完成"
            ((SUCCESS_COUNT++))
        else
            echo "❌ 全量源代码拼接 - 失败"
            FAILED_SCRIPTS+=("全量拼接")
        fi
        ((TOTAL_COUNT++))
        ;;
    *)
        echo "❌ 无效选择，默认使用分类拼接模式"
        echo "========================================"
        
        # 默认分类拼接
        run_merge_script "merge_frontend_simple.sh" "前端源代码拼接"
        run_merge_script "merge_backend_simple.sh" "后端源代码拼接"
        run_merge_script "merge_database_simple.sh" "数据库代码拼接"
        ;;
esac

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
case $REPLY in
    2)
        echo "   - output_docs/完整源代码合集.txt"
        ;;
    *)
        echo "   - output_docs/前端源代码.txt"
        echo "   - output_docs/后端源代码.txt"
        echo "   - output_docs/数据库代码.txt"
        ;;
esac

echo ""
echo "💡 使用说明："
case $REPLY in
    2)
        echo "   ✓ 生成单一完整文件，包含所有前端+后端+数据库代码"
        echo "   ✓ 适合统一提交，便于单文件管理"
        echo "   ✓ 无需AI处理，避免token消耗"
        ;;
    *)
        echo "   ✓ 生成分类文件，便于分模块提交和审核"
        echo "   ✓ 每个模块独立，便于理解项目架构"
        echo "   ✓ 无需AI处理，避免token消耗"
        ;;
esac
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