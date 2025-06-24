#!/bin/bash

# 前端源代码拼接脚本 (Shell版本)
# 将 output_sourcecode/front/ 目录下所有HTML文件内容拼接生成统一的前端源代码文档
#
# CSS处理策略：
# - 彻底移除 <style> 标签及其内容
# - 移除 CSS 外部链接 (rel="stylesheet")  
# - 移除内联样式属性 (style="...")
# - 保留HTML结构和JavaScript逻辑
# - 保留class属性（可能对JavaScript功能重要）
#
# 这样可以显著减少文档长度，突出核心程序逻辑，更适合软著申请材料要求

# 设置脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"  # 回到项目根目录
FRONT_DIR="${SCRIPT_DIR}/output_sourcecode/front"
OUTPUT_DIR="${SCRIPT_DIR}/output_docs"
OUTPUT_FILE="${OUTPUT_DIR}/前端源代码.txt"

# 确保输出目录存在
mkdir -p "${OUTPUT_DIR}"

# 检查前端目录是否存在
if [ ! -d "${FRONT_DIR}" ]; then
    echo "❌ 错误：前端目录不存在 ${FRONT_DIR}"
    exit 1
fi

# 获取HTML文件列表
HTML_FILES=($(find "${FRONT_DIR}" -name "*.html" -type f | sort))

if [ ${#HTML_FILES[@]} -eq 0 ]; then
    echo "❌ 错误：在 ${FRONT_DIR} 目录下没有找到HTML文件"
    exit 1
fi

echo "============================================================"
echo "前端源代码拼接脚本"
echo "============================================================"
echo "找到 ${#HTML_FILES[@]} 个HTML文件:"

for file in "${HTML_FILES[@]}"; do
    echo "  - $(basename "$file")"
done

echo ""
echo "开始生成前端源代码文档..."

# 定义页面映射函数
get_page_title() {
    local filename=$(basename "$1")
    case "$filename" in
        "login.html") echo "登录页面" ;;
        "dashboard.html") echo "仪表盘页面" ;;
        "materials.html") echo "素材库管理页面" ;;
        "ai-assistant.html") echo "AI智能助手页面" ;;
        "users.html") echo "用户权限管理页面" ;;
        "analytics.html") echo "数据统计分析页面" ;;
        "wechat-config.html") echo "企业微信集成配置页面" ;;
        "settings.html") echo "系统设置页面" ;;
        *) echo "${filename%.html}页面" ;;
    esac
}

# 清空输出文件
> "${OUTPUT_FILE}"

# 处理每个HTML文件
counter=1
for html_file in "${HTML_FILES[@]}"; do
    filename=$(basename "$html_file")
    page_title=$(get_page_title "$html_file")
    
    echo "处理文件 ${counter}/${#HTML_FILES[@]}: ${filename}"
    
    # 写入文件分隔标识和源代码
    echo "=== ${filename} ===" >> "${OUTPUT_FILE}"
    
    # 读取HTML内容并彻底移除CSS样式内容，保留HTML结构和JavaScript
    if [ -f "$html_file" ]; then
        # 创建临时文件进行多步处理
        temp_file=$(mktemp)
        
        # 1. 移除<style>标签及其内容
        sed 's/<style[^>]*>.*<\/style>/    <!-- CSS样式已省略，完整CSS请查看原始HTML文件 -->/g' "$html_file" > "$temp_file"
        
        # 2. 移除CSS外部链接
        sed -i.bak 's/<link[^>]*rel=["\x27]stylesheet["\x27][^>]*>/    <!-- CSS外部链接已省略 -->/gi' "$temp_file"
        
        # 3. 移除内联样式属性
        sed -i.bak 's/ style=["\x27][^"\x27]*["\x27]//g' "$temp_file"
        
        # 输出处理后的内容
        cat "$temp_file" >> "${OUTPUT_FILE}"
        
        # 清理临时文件
        rm -f "$temp_file" "$temp_file.bak"
    else
        echo "错误：无法读取文件 ${html_file}" >> "${OUTPUT_FILE}"
    fi
    
    echo "" >> "${OUTPUT_FILE}"
    echo "" >> "${OUTPUT_FILE}"
    
    ((counter++))
done

# 不添加额外说明，只保留纯源代码

echo "✅ 前端源代码文档生成完成！"
echo "📁 输出文件: ${OUTPUT_FILE}"

# 显示文件大小
if [ -f "${OUTPUT_FILE}" ]; then
    file_size=$(stat -f%z "${OUTPUT_FILE}" 2>/dev/null || stat -c%s "${OUTPUT_FILE}" 2>/dev/null)
    if [ $? -eq 0 ]; then
        if [ $file_size -gt 1048576 ]; then
            size_str="$(echo "scale=2; $file_size / 1048576" | bc) MB"
        elif [ $file_size -gt 1024 ]; then
            size_str="$(echo "scale=2; $file_size / 1024" | bc) KB"
        else
            size_str="${file_size} bytes"
        fi
        echo "📊 文件大小: ${size_str}"
    fi
fi

echo ""
echo "============================================================"
echo "脚本执行完成"
echo "============================================================"