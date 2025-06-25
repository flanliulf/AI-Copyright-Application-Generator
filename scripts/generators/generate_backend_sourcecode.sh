#!/bin/bash

# 后端源代码拼接脚本 (Shell版本)
# 将 output_sourcecode/backend/ 目录下所有Java文件及配置文件内容拼接生成统一的后端源代码文档

# 设置脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"  # 回到项目根目录
BACKEND_DIR="${SCRIPT_DIR}/output_sourcecode/backend"
OUTPUT_DIR="${SCRIPT_DIR}/output_docs"
OUTPUT_FILE="${OUTPUT_DIR}/后端源代码.txt"

# 确保输出目录存在
mkdir -p "${OUTPUT_DIR}"

# 检查后端目录是否存在
if [ ! -d "${BACKEND_DIR}" ]; then
    echo "❌ 错误：后端目录不存在 ${BACKEND_DIR}"
    exit 1
fi

# 获取后端文件列表（按类型优先级排序）
get_backend_files() {
    local files=()
    
    # 优先级文件顺序
    # 1. pom.xml
    find "${BACKEND_DIR}" -name "pom.xml" -type f | while read file; do
        echo "1:$file"
    done
    
    # 2. 配置文件
    find "${BACKEND_DIR}" -name "*.yml" -o -name "*.yaml" -o -name "*.properties" | while read file; do
        echo "2:$file"
    done
    
    # 3. Application.java
    find "${BACKEND_DIR}" -name "Application.java" -type f | while read file; do
        echo "3:$file"
    done
    
    # 4. Entity类
    find "${BACKEND_DIR}" -path "*/entity/*" -name "*.java" -type f | while read file; do
        echo "4:$file"
    done
    
    # 5. Mapper类
    find "${BACKEND_DIR}" -path "*/mapper/*" -name "*.java" -type f | while read file; do
        echo "5:$file"
    done
    
    # 6. Service类
    find "${BACKEND_DIR}" -path "*/service/*" -name "*.java" -type f | while read file; do
        echo "6:$file"
    done
    
    # 7. Controller类
    find "${BACKEND_DIR}" -path "*/controller/*" -name "*.java" -type f | while read file; do
        echo "7:$file"
    done
    
    # 8. DTO类
    find "${BACKEND_DIR}" -path "*/dto/*" -name "*.java" -type f | while read file; do
        echo "8:$file"
    done
    
    # 9. VO类
    find "${BACKEND_DIR}" -path "*/vo/*" -name "*.java" -type f | while read file; do
        echo "9:$file"
    done
    
    # 10. 其他Java文件
    find "${BACKEND_DIR}" -name "*.java" -type f | while read file; do
        # 排除已经处理的文件
        if [[ ! "$file" =~ /entity/ ]] && [[ ! "$file" =~ /mapper/ ]] && [[ ! "$file" =~ /service/ ]] && [[ ! "$file" =~ /controller/ ]] && [[ ! "$file" =~ /dto/ ]] && [[ ! "$file" =~ /vo/ ]] && [[ ! "$file" =~ Application.java ]]; then
            echo "10:$file"
        fi
    done
}

# 获取排序后的文件列表
BACKEND_FILES=($(get_backend_files | sort -t: -k1,1n -k2,2 | cut -d: -f2-))

if [ ${#BACKEND_FILES[@]} -eq 0 ]; then
    echo "❌ 错误：在 ${BACKEND_DIR} 目录下没有找到后端源代码文件"
    exit 1
fi

echo "============================================================"
echo "后端源代码生成脚本 (用于AI分析和代码审查)"
echo "============================================================"
echo "找到 ${#BACKEND_FILES[@]} 个后端源代码文件:"

for file in "${BACKEND_FILES[@]}"; do
    rel_path=$(realpath --relative-to="${BACKEND_DIR}" "$file" 2>/dev/null || python -c "import os; print(os.path.relpath('$file', '${BACKEND_DIR}'))")
    echo "  - ${rel_path}"
done

echo ""
echo "开始生成后端源代码文档..."

# 清空输出文件
> "${OUTPUT_FILE}"

# 处理每个后端文件
counter=1
for backend_file in "${BACKEND_FILES[@]}"; do
    rel_path=$(realpath --relative-to="${BACKEND_DIR}" "$backend_file" 2>/dev/null || python -c "import os; print(os.path.relpath('$backend_file', '${BACKEND_DIR}'))")
    
    echo "处理文件 ${counter}/${#BACKEND_FILES[@]}: ${rel_path}"
    
    # 写入文件分隔标识和源代码
    echo "=== ${rel_path} ===" >> "${OUTPUT_FILE}"
    
    # 读取文件内容
    if [ -f "$backend_file" ]; then
        cat "$backend_file" >> "${OUTPUT_FILE}"
    else
        echo "错误：无法读取文件 ${backend_file}" >> "${OUTPUT_FILE}"
    fi
    
    echo "" >> "${OUTPUT_FILE}"
    echo "" >> "${OUTPUT_FILE}"
    
    ((counter++))
done

echo "✅ 后端源代码文档生成完成！"
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