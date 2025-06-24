#!/bin/bash

# 统一源代码文档生成脚本 (Shell版本)
# 一次性生成前端、后端和数据库的所有源代码文档

echo "================================================================================"
echo "统一源代码文档生成脚本"
echo "================================================================================"
echo "开始时间: $(date '+%Y-%m-%d %H:%M:%S')"

SUCCESS_COUNT=0
TOTAL_COUNT=2

# 执行前端源代码生成
echo ""
echo "============================================================"
echo "正在执行: 前端源代码文档生成"
echo "脚本: generate_frontend_sourcecode.py"
echo "============================================================"
if python3 generate_frontend_sourcecode.py; then
    echo "✅ 前端源代码文档生成 执行成功！"
    ((SUCCESS_COUNT++))
else
    echo "❌ 前端源代码文档生成 执行失败！"
fi

# 执行后端源代码生成
echo ""
echo "============================================================"
echo "正在执行: 后端源代码文档生成"
echo "脚本: generate_backend_sourcecode.py"
echo "============================================================"
if python3 generate_backend_sourcecode.py; then
    echo "✅ 后端源代码文档生成 执行成功！"
    ((SUCCESS_COUNT++))
else
    echo "❌ 后端源代码文档生成 执行失败！"
fi

# 数据库代码由系统提示词直接生成，无需转换脚本

# 输出总结
echo ""
echo "================================================================================"
echo "执行总结"
echo "================================================================================"
echo "总脚本数: ${TOTAL_COUNT}"
echo "成功执行: ${SUCCESS_COUNT}"
echo "失败数量: $((TOTAL_COUNT - SUCCESS_COUNT))"
echo "完成时间: $(date '+%Y-%m-%d %H:%M:%S')"

if [ $SUCCESS_COUNT -eq $TOTAL_COUNT ]; then
    echo ""
    echo "🎉 所有源代码文档生成完成！"
    echo ""
    echo "📁 生成的文档:"
    echo "  - output_docs/前端源代码.txt"
    echo "  - output_docs/后端源代码.txt"
    echo ""
    echo "💡 注意：数据库代码.txt 需要通过系统提示词在AI生成阶段直接创建"
    exit 0
else
    echo ""
    echo "⚠️  有 $((TOTAL_COUNT - SUCCESS_COUNT)) 个脚本执行失败，请检查错误信息"
    exit 1
fi