#!/bin/bash

# 数据库代码拼接脚本
# 功能：将 output_sourcecode/db/ 目录下的SQL文件拼接成软著申请材料
# 
# 主要处理文件类型：
# - SQL表结构文件 (.sql)
# - 数据定义文件 (.ddl)
# - 数据库架构文件 (*schema*, *database*)
# 
# 目标：生成包含完整表注释和字段注释的纯SQL代码文档

echo "🔄 开始拼接数据库相关代码..."

# 设置路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DB_DIR="${SCRIPT_DIR}/output_sourcecode/db"
OUTPUT_DIR="${SCRIPT_DIR}/output_docs"
OUTPUT_FILE="${OUTPUT_DIR}/数据库代码.txt"

# 确保输出目录存在
mkdir -p "${OUTPUT_DIR}"

# 主要查找数据库SQL文件目录
SEARCH_DIRS=("${DB_DIR}")

# 数据库相关文件模式（主要关注SQL文件）
DB_PATTERNS=("*.sql" "*.ddl" "*schema*" "*database*")

# 查找所有数据库相关文件
DB_FILES=()
for search_dir in "${SEARCH_DIRS[@]}"; do
    if [ -d "$search_dir" ]; then
        for pattern in "${DB_PATTERNS[@]}"; do
            while IFS= read -r -d '' file; do
                # 跳过二进制文件和缓存文件
                if [[ ! "$file" =~ \.(pyc|pyo|pyd|__pycache__)$ ]]; then
                    DB_FILES+=("$file")
                fi
            done < <(find "$search_dir" -name "$pattern" -type f -print0 2>/dev/null | sort -z)
        done
    fi
done

# 去重并排序
DB_FILES=($(printf '%s\n' "${DB_FILES[@]}" | sort -u))

if [ ${#DB_FILES[@]} -eq 0 ]; then
    echo "❌ 未找到数据库SQL文件"
    echo "💡 查找路径: ${DB_DIR}"
    echo "💡 查找模式: ${DB_PATTERNS[*]}"
    echo ""
    echo "💡 提示：如果还没有生成数据库代码，请先："
    echo "   1. 使用AI生成数据库SQL代码到 output_sourcecode/db/ 目录"
    echo "   2. 确保生成的SQL文件包含完整的表注释和字段注释"
    echo "   3. 推荐文件名：database_schema.sql, init_data.sql, indexes.sql"
    exit 1
fi

echo "📁 找到 ${#DB_FILES[@]} 个数据库相关文件"

# 显示找到的文件
echo "📋 数据库文件列表："
for file in "${DB_FILES[@]}"; do
    echo "   - ${file#$SCRIPT_DIR/}"
done
echo ""

# 清空输出文件（不添加头部信息，保持纯代码格式）
> "${OUTPUT_FILE}"

# 拼接所有数据库文件
counter=1
for file in "${DB_FILES[@]}"; do
    relative_path="${file#$SCRIPT_DIR/}"
    filename=$(basename "$file")
    extension="${filename##*.}"
    
    echo "📄 处理 ($counter/${#DB_FILES[@]}): $relative_path"
    
    # 根据文件类型设置注释格式
    case "$extension" in
        "sql")
            comment_prefix="--"
            ;;
        "py")
            comment_prefix="#"
            ;;
        "json")
            comment_prefix="//"
            ;;
        "yml"|"yaml")
            comment_prefix="#"
            ;;
        *)
            comment_prefix="#"
            ;;
    esac
    
    # 添加文件分隔符
    cat >> "${OUTPUT_FILE}" << EOF

$comment_prefix ================= $relative_path =================

EOF
    
    # 直接追加文件内容
    if [ -r "$file" ]; then
        # 检查是否是文本文件
        if file "$file" | grep -q "text"; then
            cat "$file" >> "${OUTPUT_FILE}"
        else
            echo "$comment_prefix 二进制文件，内容省略: $relative_path" >> "${OUTPUT_FILE}"
        fi
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