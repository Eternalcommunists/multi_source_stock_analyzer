# 启动多数据源股票分析系统

## 系统已成功部署！

您的增强版多数据源股票分析系统已成功安装和测试。以下是启动说明：

## 快速测试（已完成）
系统已成功运行测试，验证了以下功能：
- ✅ 基础分析功能
- ✅ 高级分析功能（财报、机构持股、做空分析）
- ✅ 综合评分系统
- ✅ 报告生成功能
- ✅ 所有依赖包已安装

## 运行系统

### 1. 运行后端分析系统
```bash
cd D:/Codex/multi_source_stock_analyzer
python backend/main_enhanced.py --symbol 000001 --output-format all
```

### 2. 命令行参数
- `--symbol`: 股票代码（必需）
- `--sources`: 数据源列表（默认：['akshare']）
- `--output-format`: 输出格式（json, html, enhanced, all；默认：all）
- `--output-dir`: 输出目录（默认：'output'）

### 3. 使用示例
```bash
# 分析单个股票（含所有专业分析）
python backend/main_enhanced.py --symbol 000001 --sources akshare --output-format all

# 分析并只输出增强版报告
python backend/main_enhanced.py --symbol 000001 --output-format enhanced

# 分析多个股票
for stock in 000001 600036 000858; do
    python backend/main_enhanced.py --symbol $stock --output-format enhanced
done
```

### 4. 编程接口
```python
from backend.main_enhanced import quick_analyze

# 快速分析单个股票
result, html_report, json_report = quick_analyze('000001', ['akshare'])

# 或使用集成分析器
from backend.integrated_analyzer import IntegratedStockAnalyzer
analyzer = IntegratedStockAnalyzer()
result = analyzer.comprehensive_analysis('000001', ['akshare'])
```

## Web前端设置（可选）

如需启动Web界面：

1. 安装Node.js（v16+）
2. 安装前端依赖：
```bash
cd D:/Codex/multi_source_stock_analyzer/frontend
npm install
```

3. 启动前端：
```bash
npm start
```

4. 启动后端API服务：
```bash
cd D:/Codex/multi_source_stock_analyzer
python -m http.server 8000  # 或使用您喜欢的WSGI服务器
```

## 生成的报告文件
- JSON格式：包含完整的分析数据
- HTML格式：基础分析报告
- 增强版HTML：包含专业分析内容
- 所有文件保存在 `output/` 目录

## 增强功能说明
- 财报分析：财务报表深度解析与健康度评估
- 机构持股分析：追踪机构投资者行为
- 做多做空分析：市场情绪与风险评估
- 主流机构观点：整合专业投资意见
- 综合评分系统：多维度评分体系

系统现已准备就绪，可以进行专业的股票分析！