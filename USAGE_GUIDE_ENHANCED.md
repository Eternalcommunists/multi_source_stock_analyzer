# 多数据源股票分析系统 - 使用说明（增强版）

本文档介绍如何使用包含财报分析、机构持股分析、做多做空分析等专业功能的增强版系统。

## 快速开始

### 1. 安装依赖
```bash
# 安装Python依赖
pip install -r requirements_enhanced.txt

# 或者单独安装关键依赖
pip install akshare yfinance pandas numpy matplotlib plotly
```

### 2. 运行增强版分析系统
```bash
# 基本使用（包含所有分析功能）
python backend/main_enhanced.py --symbol 000001 --sources akshare

# 指定输出格式为增强版（含专业分析）
python backend/main_enhanced.py --symbol 000001 --sources akshare --output-format enhanced

# 生成所有格式报告
python backend/main_enhanced.py --symbol 000001 --sources akshare --output-format all
```

## 增强版分析功能详解

### 1. 财报分析
使用 `AdvancedStockAnalyzer` 的 `analyze_financial_statements` 方法，可获取：

- **财务报表数据**：利润表、资产负债表、现金流量表
- **财务比率计算**：
  - 盈利能力：ROE、ROA、毛利率、净利率等
  - 偿债能力：资产负债率、流动比率、速动比率等
  - 运营效率：资产周转率、存货周转率等
- **财务健康度评估**：基于综合指标的健康度评分

### 2. 机构持股分析
通过 `analyze_institutional_holdings` 方法分析：

- **机构持股比例**：各大机构持有股份比例
- **机构信心度**：基于持仓变化的信心评估
- **持股集中度**：前几大机构的持股集中情况

### 3. 做多做空分析
使用 `analyze_short_interest` 方法获取：

- **做空兴趣度**：当前股票的做空情况
- **做空情绪**：市场对股票的看空程度
- **风险评估**：基于做空数据的风险评级

### 4. 主流机构观点分析
通过 `analyze_wall_street_sentiment` 方法收集：

- **分析师评级**：买入、持有、卖出评级统计
- **目标价预测**：分析师给出的目标价格
- **机构观点**：主流投资机构的投资建议

## 程序结构说明

### 主要模块
1. `advanced_analyzer.py` - 高级分析核心模块
2. `integrated_analyzer.py` - 集成基础和高级分析
3. `main_enhanced.py` - 增强版主程序入口

### 核心类
- `AdvancedStockAnalyzer`: 高级分析功能集合
- `IntegratedStockAnalyzer`: 基础与高级分析集成

## 输出格式说明

### JSON输出
包含完整的分析数据，结构如下：
```json
{
  "symbol": "股票代码",
  "analysis_timestamp": "分析时间戳",
  "basic_analysis": { /* 基础分析结果 */ },
  "advanced_analysis": { /* 高级分析结果 */ },
  "integrated_score": "综合评分",
  "combined_recommendation": "综合建议",
  "risk_summary": "风险汇总"
}
```

### HTML输出（增强版）
包含以下部分：
- 基础技术分析
- 财务健康度分析
- 机构持股分析
- 做空情绪分析
- 市场情绪与投研观点
- 综合评分与建议

## 参数说明

### 主要参数
- `--symbol`: 股票代码（必需）
- `--sources`: 数据源列表（默认：['akshare']）
- `--output-format`: 输出格式（json, html, enhanced, all；默认：all）
- `--output-dir`: 输出目录（默认：'output'）

### 输出格式选项
- `json`: 输出JSON格式数据
- `html`: 输出基础HTML报告
- `enhanced`: 输出增强版HTML报告（含专业分析）
- `all`: 输出所有格式

## 编程接口

可通过编程方式使用增强版分析：

```python
from backend.integrated_analyzer import IntegratedStockAnalyzer

# 创建分析器实例
analyzer = IntegratedStockAnalyzer()

# 执行综合分析
result = analyzer.comprehensive_analysis("000001", ["akshare"])

# 生成增强版报告
html_path, json_path = analyzer.generate_enhanced_report("000001", ["akshare"])

print(f"报告已生成：{html_path}")
```

## 配置文件

系统使用 `config.json` 进行配置，可调整以下参数：
- 数据源启用状态
- 分析深度设置
- 风险阈值配置
- 性能优化参数

## 注意事项

1. **数据准确性**：所有分析仅作参考，不构成投资建议
2. **API限制**：某些数据源可能有请求频率限制
3. **依赖更新**：定期更新依赖包以获得最新数据接口
4. **网络连接**：确保良好的网络连接以便获取实时数据

## 故障排除

### 常见问题
1. **数据获取失败**：检查网络连接和数据源配置
2. **依赖错误**：确认已安装所需Python包
3. **API变更**：第三方数据接口可能随时变更

### 错误日志
分析过程中的错误会被记录，可在输出目录的log文件中查看。

## 更新日志

### v1.1.0 (增强版)
- 新增财报分析功能
- 新增机构持股分析
- 新增做多做空分析
- 新增主流机构观点分析
- 集成综合评分系统
- 增强版报告输出格式

---

如需技术支持或功能定制，请联系项目维护团队。