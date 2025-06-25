#!/bin/bash

# 后端源代码简单拼接脚本
# 功能：将所有后端源代码文件简单拼接成一个文本文件，避免AI处理时消耗大量token
# 
# 支持文件类型：
# - Java文件 (.java, .jsp, .xml)
# - Python文件 (.py)
# - C#/.NET文件 (.cs, .csproj, .sln)
# - Node.js文件 (.js, .ts, .mjs)
# - PHP文件 (.php)
# - Go文件 (.go, .mod)
# - 配置文件 (.json, .yml, .yaml, .xml, .properties)
# - 构建文件 (pom.xml, package.json, requirements.txt, Dockerfile)
# - 其他文件 (.txt, .md, .cfg, .ini, .conf, .env)

echo "🔄 开始拼接后端源代码..."

# 设置路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKEND_DIR="${SCRIPT_DIR}/output_sourcecode/backend"
OUTPUT_DIR="${SCRIPT_DIR}/output_docs"
OUTPUT_FILE="${OUTPUT_DIR}/后端源代码.txt"

# 确保输出目录存在
mkdir -p "${OUTPUT_DIR}"

# 检查后端目录
if [ ! -d "${BACKEND_DIR}" ]; then
    echo "❌ 后端目录不存在: ${BACKEND_DIR}"
    echo "💡 请先生成后端源代码文件"
    exit 1
fi

# 定义后端源代码文件扩展名
BACKEND_EXTENSIONS=(
    # Java相关
    "*.java" "*.jsp" "*.xml"
    # Python相关
    "*.py"
    # C#/.NET相关
    "*.cs" "*.csproj" "*.sln"
    # Node.js相关
    "*.js" "*.ts" "*.mjs"
    # PHP相关
    "*.php"
    # Go相关
    "*.go" "*.mod"
    # 配置文件
    "*.json" "*.yml" "*.yaml" "*.properties"
    # 构建和部署文件
    "pom.xml" "package.json" "requirements.txt" "Dockerfile" "docker-compose.yml"
    # 其他文件
    "*.txt" "*.md" "*.cfg" "*.ini" "*.conf" "*.env"
)

# 查找所有后端源代码文件
BACKEND_FILES=()
for ext in "${BACKEND_EXTENSIONS[@]}"; do
    while IFS= read -r -d '' file; do
        BACKEND_FILES+=("$file")
    done < <(find "${BACKEND_DIR}" -name "$ext" -type f -print0 | sort -z)
done

if [ ${#BACKEND_FILES[@]} -eq 0 ]; then
    echo "❌ 未找到后端源代码文件"
    echo "💡 请检查 ${BACKEND_DIR} 目录"
    echo "💡 支持的文件类型: ${BACKEND_EXTENSIONS[*]}"
    exit 1
fi

echo "📁 找到 ${#BACKEND_FILES[@]} 个后端源代码文件"

# 清空输出文件
> "${OUTPUT_FILE}"

# 清空输出文件（不添加头部信息，保持纯代码格式）

# 拼接所有后端文件
counter=1
for file in "${BACKEND_FILES[@]}"; do
    relative_path="${file#$BACKEND_DIR/}"
    filename=$(basename "$file")
    extension="${filename##*.}"
    
    echo "📄 处理 ($counter/${#BACKEND_FILES[@]}): $relative_path"
    
    # 根据文件类型设置注释格式（处理特殊文件名）
    if [[ "$filename" == "Dockerfile"* ]] || [[ "$filename" == "docker-compose"* ]]; then
        comment_prefix="#"
    elif [[ "$filename" == "pom.xml" ]] || [[ "$filename" == "package.json" ]] || [[ "$filename" == "requirements.txt" ]]; then
        case "$extension" in
            "xml") comment_prefix="<!--" ;;
            "json") comment_prefix="//" ;;
            "txt") comment_prefix="#" ;;
        esac
    else
        case "$extension" in
            # C风格语言和JSON
            "java"|"js"|"ts"|"mjs"|"cs"|"php"|"json")
                comment_prefix="//"
                ;;
            # XML类文件
            "xml"|"jsp"|"csproj"|"sln")
                comment_prefix="<!--"
                ;;
            # Shell风格注释
            "py"|"yml"|"yaml"|"cfg"|"ini"|"conf"|"env"|"properties")
                comment_prefix="#"
                ;;
            # Go语言
            "go"|"mod")
                comment_prefix="//"
                ;;
            # 其他文件默认使用#
            *)
                comment_prefix="#"
                ;;
        esac
    fi
    
    # 添加文件分隔符
    cat >> "${OUTPUT_FILE}" << EOF

$comment_prefix ================= $relative_path =================

EOF
    
    # 直接追加文件内容
    if [ -r "$file" ]; then
        cat "$file" >> "${OUTPUT_FILE}"
    else
        echo "$comment_prefix 无法读取文件: $relative_path" >> "${OUTPUT_FILE}"
    fi
    
    # 添加文件结束分隔符
    cat >> "${OUTPUT_FILE}" << EOF

$comment_prefix ================= $relative_path 结束 =================

EOF
    
    ((counter++))
done

# 显示结果
if [ -f "${OUTPUT_FILE}" ]; then
    file_size=$(wc -c < "${OUTPUT_FILE}")
    line_count=$(wc -l < "${OUTPUT_FILE}")
    
    echo "✅ 拼接完成！"
    echo "📁 输出文件: ${OUTPUT_FILE}"
    
    # 兼容性处理文件大小显示
    if [ $file_size -gt 1048576 ]; then
        size_str="$(awk "BEGIN {printf \"%.1f MB\", $file_size/1048576}")"
    elif [ $file_size -gt 1024 ]; then
        size_str="$(awk "BEGIN {printf \"%.1f KB\", $file_size/1024}")"
    else
        size_str="${file_size} bytes"
    fi
    echo "📊 文件大小: ${size_str}"
    echo "📋 总行数: $line_count"
else
    echo "❌ 生成失败"
    exit 1
fi