#!/bin/bash

# 前端页面源代码软著申请专用拼接脚本
# 功能：将所有前端HTML文件完整拼接成单一文档，专用于软件著作权申请材料
# 
# 与现有generate_frontend_sourcecode.py的差异：
# - 现有脚本：分批生成，适用于AI对话（避免token超限）
# - 本脚本：  单文件生成，适用于软著申请（便于提交）
# 
# 优点：
# - 生成单一完整文档，符合软著申请要求
# - 保持源代码完整性，无压缩或分批
# - 零token消耗，纯本地文本处理
# - 直接可用于软著申请提交

echo "🔄 开始拼接前端页面源代码..."

# 设置路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
FRONT_DIR="${SCRIPT_DIR}/output_sourcecode/front"
OUTPUT_DIR="${SCRIPT_DIR}/output_docs"
OUTPUT_FILE="${OUTPUT_DIR}/前端源代码.txt"

# 确保输出目录存在
mkdir -p "${OUTPUT_DIR}"

# 检查前端目录
if [ ! -d "${FRONT_DIR}" ]; then
    echo "❌ 前端目录不存在: ${FRONT_DIR}"
    echo "💡 请先生成前端源代码文件"
    exit 1
fi

# 获取所有HTML文件
HTML_FILES=($(find "${FRONT_DIR}" -name "*.html" | sort))

if [ ${#HTML_FILES[@]} -eq 0 ]; then
    echo "❌ 未找到HTML文件"
    echo "💡 请检查 ${FRONT_DIR} 目录"
    exit 1
fi

echo "📁 找到 ${#HTML_FILES[@]} 个HTML文件"

# 清空输出文件
> "${OUTPUT_FILE}"

# 拼接所有文件（不添加头部信息，保持纯代码格式）

for html_file in "${HTML_FILES[@]}"; do
    filename=$(basename "$html_file")
    echo "📄 处理: $filename"
    
    # 添加文件分隔符
    echo "/* ================= $filename ================= */" >> "${OUTPUT_FILE}"
    echo "" >> "${OUTPUT_FILE}"
    
    # 直接追加文件内容
    cat "$html_file" >> "${OUTPUT_FILE}"
    
    # 添加文件结束分隔符
    echo "" >> "${OUTPUT_FILE}"
    echo "/* ================= $filename 结束 ================= */" >> "${OUTPUT_FILE}"
    echo "" >> "${OUTPUT_FILE}"
    echo "" >> "${OUTPUT_FILE}"
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
    echo "   - 此文件包含所有前端页面的完整源代码"
    echo "   - 可直接用于软著申请材料"
    echo "   - 无需AI处理，节省token消耗"
else
    echo "❌ 生成失败"
    exit 1
fi