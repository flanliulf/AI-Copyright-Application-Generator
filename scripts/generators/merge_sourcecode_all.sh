#!/bin/bash

# 全量源代码拼接脚本
# 功能：将前端和后端所有源代码文件拼接到一个文本文件
# 支持：HTML, CSS, JS, Python, JSON, MD等多种文件类型
# 目标：避免AI处理时的token消耗，直接生成完整的源代码材料

echo "🚀 全量源代码拼接工具"
echo "======================================"

# 设置路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SOURCECODE_DIR="${SCRIPT_DIR}/output_sourcecode"
OUTPUT_DIR="${SCRIPT_DIR}/output_docs"
OUTPUT_FILE="${OUTPUT_DIR}/完整源代码合集.txt"

# 确保目录存在
mkdir -p "${OUTPUT_DIR}"

# 检查源代码目录
if [ ! -d "${SOURCECODE_DIR}" ]; then
    echo "❌ 源代码目录不存在: ${SOURCECODE_DIR}"
    echo "💡 请先生成源代码文件"
    exit 1
fi

# 定义要拼接的文件类型
FILE_EXTENSIONS=(
    # 前端文件
    "*.html" "*.css" "*.js" "*.ts" "*.mjs"
    # 后端文件 - Java相关
    "*.java" "*.jsp" "*.xml"
    # 后端文件 - Python相关
    "*.py"
    # 后端文件 - C#/.NET相关
    "*.cs" "*.csproj" "*.sln"
    # 后端文件 - PHP相关
    "*.php"
    # 后端文件 - Go相关
    "*.go" "*.mod"
    # 配置和数据文件
    "*.json" "*.yml" "*.yaml" "*.properties" "*.env"
    # 构建和部署文件
    "pom.xml" "package.json" "requirements.txt" "Dockerfile" "docker-compose.yml"
    # 文档和其他
    "*.md" "*.txt" "*.cfg" "*.ini" "*.conf" "*.sql"
)

echo "📁 扫描源代码目录: ${SOURCECODE_DIR}"

# 查找所有匹配的文件
ALL_FILES=()
for ext in "${FILE_EXTENSIONS[@]}"; do
    while IFS= read -r -d '' file; do
        ALL_FILES+=("$file")
    done < <(find "${SOURCECODE_DIR}" -type f -name "$ext" -print0 | sort -z)
done

if [ ${#ALL_FILES[@]} -eq 0 ]; then
    echo "❌ 未找到源代码文件"
    echo "💡 请检查 ${SOURCECODE_DIR} 目录中是否存在以下类型的文件:"
    printf "   %s\n" "${FILE_EXTENSIONS[@]}"
    exit 1
fi

echo "📊 找到 ${#ALL_FILES[@]} 个源代码文件"

# 清空输出文件并写入头部信息
cat > "${OUTPUT_FILE}" << EOF
/*
====================================================================
软件著作权申请 - 完整源代码合集
====================================================================
生成时间: $(date '+%Y-%m-%d %H:%M:%S')
文件总数: ${#ALL_FILES[@]}
源代码目录: ${SOURCECODE_DIR}

本文件包含以下类型的源代码文件:
$(printf "  - %s\n" "${FILE_EXTENSIONS[@]}")

文件列表:
$(printf "  - %s\n" "${ALL_FILES[@]#$SOURCECODE_DIR/}")
====================================================================
*/

EOF

# 拼接所有源代码文件
counter=1
for file in "${ALL_FILES[@]}"; do
    relative_path="${file#$SOURCECODE_DIR/}"
    filename=$(basename "$file")
    extension="${filename##*.}"
    
    echo "📄 处理 ($counter/${#ALL_FILES[@]}): $relative_path"
    
    # 根据文件类型设置注释格式（处理特殊文件名）
    if [[ "$filename" == "Dockerfile"* ]] || [[ "$filename" == "docker-compose"* ]]; then
        comment_start="#"
        comment_end=""
    elif [[ "$filename" == "pom.xml" ]] || [[ "$filename" == "package.json" ]] || [[ "$filename" == "requirements.txt" ]]; then
        case "$extension" in
            "xml") comment_start="<!--" && comment_end="-->" ;;
            "json") comment_start="//" && comment_end="" ;;
            "txt") comment_start="#" && comment_end="" ;;
        esac
    else
        case "$extension" in
            # 前端文件
            "html"|"css"|"js"|"ts"|"mjs")
                comment_start="/*"
                comment_end="*/"
                ;;
            # Java相关
            "java"|"jsp")
                comment_start="//"
                comment_end=""
                ;;
            # C#相关
            "cs")
                comment_start="//"
                comment_end=""
                ;;
            # PHP
            "php")
                comment_start="//"
                comment_end=""
                ;;
            # Go
            "go"|"mod")
                comment_start="//"
                comment_end=""
                ;;
            # XML类文件
            "xml"|"csproj"|"sln")
                comment_start="<!--"
                comment_end="-->"
                ;;
            # Shell风格注释
            "py"|"yml"|"yaml"|"cfg"|"ini"|"conf"|"env"|"properties"|"sql")
                comment_start="#"
                comment_end=""
                ;;
            # JSON
            "json")
                comment_start="//"
                comment_end=""
                ;;
            # 其他文件默认使用/**/
            *)
                comment_start="/*"
                comment_end="*/"
                ;;
        esac
    fi
    
    # 写入文件分隔符
    cat >> "${OUTPUT_FILE}" << EOF

$comment_start ==================== $relative_path ==================== $comment_end

EOF
    
    # 写入文件内容（如果文件可读）
    if [ -r "$file" ]; then
        cat "$file" >> "${OUTPUT_FILE}"
    else
        echo "<!-- 无法读取文件: $relative_path -->" >> "${OUTPUT_FILE}"
    fi
    
    # 写入文件结束分隔符
    cat >> "${OUTPUT_FILE}" << EOF

$comment_start ==================== $relative_path 结束 ==================== $comment_end

EOF
    
    ((counter++))
done

# 统计和显示结果
if [ -f "${OUTPUT_FILE}" ]; then
    file_size=$(wc -c < "${OUTPUT_FILE}")
    line_count=$(wc -l < "${OUTPUT_FILE}")
    
    echo ""
    echo "✅ 拼接完成！"
    echo "======================================"
    echo "📁 输出文件: ${OUTPUT_FILE}"
    # 兼容性处理文件大小显示
    if [ $file_size -gt 1048576 ]; then
        size_str="$(awk "BEGIN {printf \"%.2f MB\", $file_size/1048576}")"
    elif [ $file_size -gt 1024 ]; then
        size_str="$(awk "BEGIN {printf \"%.2f KB\", $file_size/1024}")"
    else
        size_str="${file_size} bytes"
    fi
    echo "📊 文件大小: ${size_str}"
    echo "📋 总行数: $line_count"
    echo "📄 源文件数: ${#ALL_FILES[@]}"
    echo ""
    echo "💡 使用说明："
    echo "   ✓ 包含完整的前端和后端源代码"
    echo "   ✓ 适用于软著申请的程序鉴别材料"
    echo "   ✓ 无需AI处理，零token消耗"
    echo "   ✓ 按文件路径有序组织，便于查阅"
    echo ""
    echo "📝 后续步骤："
    echo "   1. 检查生成的文件内容"
    echo "   2. 根据软著要求调整格式（如需要）"
    echo "   3. 提交作为程序鉴别材料"
    
else
    echo "❌ 生成失败"
    exit 1
fi