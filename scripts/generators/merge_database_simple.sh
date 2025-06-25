#!/bin/bash

# 数据库代码简单拼接脚本
# 功能：将数据库相关文件拼接成一个文本文件，用于软著申请
# 
# 支持文件类型：
# - SQL文件 (.sql)
# - 数据库迁移文件 (migrations/)
# - 数据库配置文件 (.json, .yml, .yaml)
# - Python数据库模型文件 (models.py, database.py)

echo "🔄 开始拼接数据库相关代码..."

# 设置路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKEND_DIR="${SCRIPT_DIR}/output_sourcecode/backend"
PROCESS_DIR="${SCRIPT_DIR}/process_docs"
OUTPUT_DIR="${SCRIPT_DIR}/output_docs"
OUTPUT_FILE="${OUTPUT_DIR}/数据库代码.txt"

# 确保输出目录存在
mkdir -p "${OUTPUT_DIR}"

# 数据库相关文件的查找路径
SEARCH_DIRS=("${BACKEND_DIR}" "${PROCESS_DIR}")

# 数据库相关文件模式
DB_PATTERNS=("*.sql" "*models.py" "*database.py" "*db.py" "migrations/*" "*schema*" "*数据库*")

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
    echo "❌ 未找到数据库相关文件"
    echo "💡 查找路径: ${SEARCH_DIRS[*]}"
    echo "💡 查找模式: ${DB_PATTERNS[*]}"
    echo ""
    echo "💡 提示：如果还没有生成数据库代码，请先："
    echo "   1. 运行数据库代码生成流程"
    echo "   2. 或手动创建数据库相关文件"
    exit 1
fi

echo "📁 找到 ${#DB_FILES[@]} 个数据库相关文件"

# 显示找到的文件
echo "📋 数据库文件列表："
for file in "${DB_FILES[@]}"; do
    echo "   - ${file#$SCRIPT_DIR/}"
done
echo ""

# 清空输出文件并写入头部信息
cat > "${OUTPUT_FILE}" << EOF
====================================================================
数据库代码合集
====================================================================
生成时间: $(date '+%Y-%m-%d %H:%M:%S')
文件数量: ${#DB_FILES[@]}
用途: 软件著作权申请 - 数据库设计和实现代码

包含内容:
- 数据库表结构设计
- 数据模型定义
- 数据库操作代码
- 配置和迁移文件

文件列表:
$(printf "  - %s\n" "${DB_FILES[@]#$SCRIPT_DIR/}")
====================================================================

EOF

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
    echo ""
    echo "💡 使用说明："
    echo "   - 此文件包含完整的数据库设计和实现代码"
    echo "   - 可直接用于软著申请的技术文档部分"
    echo "   - 体现数据库架构设计和技术实现能力"
    echo "   - 无需AI处理，节省token消耗"
else
    echo "❌ 生成失败"
    exit 1
fi