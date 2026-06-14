"""
多数据源股票分析系统 - HTML报告生成器
"""

import json
from datetime import datetime
from typing import Dict, List
import os


class HTMLReportGenerator:
    """
    HTML报告生成器，将分析结果转换为美观的HTML报告
    """
    
    def __init__(self):
        self.template = self._load_template()
    
    def _load_template(self) -> str:
        """
        加载HTML报告模板
        """
        template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>股票分析报告 - {symbol}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
        }}
        .report-section {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .section-title {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .rating-circle {{
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: conic-gradient(
                #1abc9c 0% {rating_pct}%,
                #e0e0e0 {rating_pct}% 100%
            );
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 20px auto;
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        }}
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .metric-card {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }}
        .risk-high {{ border-left-color: #e74c3c; }}
        .risk-medium {{ border-left-color: #f39c12; }}
        .risk-low {{ border-left-color: #27ae60; }}
        .data-sources {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 15px 0;
        }}
        .source-tag {{
            background: #3498db;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }}
        .recommendation {{
            background: linear-gradient(135deg, #1abc9c, #2ecc71);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            margin: 20px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .disclaimer {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 15px;
            border-radius: 5px;
            margin-top: 30px;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>股票分析报告</h1>
        <h2>{symbol} - {company_name}</h2>
        <p>分析时间: {analysis_time}</p>
    </div>

    <div class="report-section">
        <h3 class="section-title">综合评分</h3>
        <div style="text-align: center;">
            <div class="rating-circle">{rating}/10</div>
            <p>投资评分: {rating}/10</p>
        </div>
    </div>

    <div class="report-section">
        <h3 class="section-title">投资建议</h3>
        <div class="recommendation">{recommendation}</div>
    </div>

    <div class="report-section">
        <h3 class="section-title">数据源信息</h3>
        <div class="data-sources">
            {data_sources_html}
        </div>
        <p>数据质量分数: {data_quality_score}/10</p>
    </div>

    <div class="report-section">
        <h3 class="section-title">技术分析</h3>
        <div class="metric-grid">
            <div class="metric-card">
                <h4>趋势</h4>
                <p>{trend}</p>
            </div>
            <div class="metric-card">
                <h4>动量</h4>
                <p>{momentum}</p>
            </div>
            <div class="metric-card">
                <h4>支撑位</h4>
                <p>{support}</p>
            </div>
            <div class="metric-card">
                <h4>压力位</h4>
                <p>{resistance}</p>
            </div>
        </div>
    </div>

    <div class="report-section">
        <h3 class="section-title">基本面分析</h3>
        <div class="metric-grid">
            <div class="metric-card">
                <h4>估值状态</h4>
                <p>{valuation}</p>
            </div>
        </div>
    </div>

    <div class="report-section">
        <h3 class="section-title">风险评估</h3>
        <table>
            <thead>
                <tr>
                    <th>风险类型</th>
                    <th>等级</th>
                    <th>说明</th>
                </tr>
            </thead>
            <tbody>
                {risk_rows}
            </tbody>
        </table>
    </div>

    <div class="report-section">
        <h3 class="section-title">数据源对比</h3>
        <table>
            <thead>
                <tr>
                    <th>数据源</th>
                    <th>状态</th>
                    <th>主要差异</th>
                </tr>
            </thead>
            <tbody>
                {source_comparison_rows}
            </tbody>
        </table>
    </div>

    <div class="disclaimer">
        <strong>免责声明:</strong> 本报告基于公开数据和算法分析，仅供参考，不构成投资建议。
        投资有风险，入市需谨慎。请结合自身情况做出投资决策。
    </div>
</body>
</html>
        """
        return template

    def generate_report(self, analysis_result: Dict, output_path: str = None) -> str:
        """
        生成HTML报告
        """
        symbol = analysis_result['symbol']
        
        # 准备数据
        rating = analysis_result['detailed_analysis']['investment_rating']
        rating_pct = (rating / 10) * 100  # 转换为百分比
        
        recommendation = analysis_result['recommendation']
        data_quality_score = analysis_result['data_quality_score']
        
        # 技术分析数据
        tech_analysis = analysis_result['detailed_analysis']['technical_analysis']
        trend = tech_analysis['trend']
        momentum = tech_analysis['momentum']
        support = tech_analysis['support_resistance'].get('support', 'N/A')
        resistance = tech_analysis['support_resistance'].get('resistance', 'N/A')
        
        # 基本面分析数据
        fundamental_analysis = analysis_result['detailed_analysis']['fundamental_analysis']
        valuation = fundamental_analysis['valuation']
        
        # 风险评估数据
        risk_assessment = analysis_result['detailed_analysis']['risk_assessment']
        risk_rows = ""
        for risk_type, level in risk_assessment.items():
            risk_class = f"risk-{level}" if level in ['high', 'medium', 'low'] else "risk-medium"
            risk_rows += f"""
                <tr class="{risk_class}">
                    <td>{risk_type}</td>
                    <td>{level}</td>
                    <td>{self._get_risk_description(risk_type)}</td>
                </tr>
            """
        
        # 数据源信息
        sources_data = analysis_result['data_comparison']['sources_data']
        data_sources_html = ""
        for source, data in sources_data.items():
            status = "success" if data.get('success', False) else "failed"
            status_text = "✓ 成功" if data.get('success', False) else "✗ 失败"
            data_sources_html += f'<span class="source-tag" style="background: {"#27ae60" if status == "success" else "#e74c3c"};">{source}: {status_text}</span>'
        
        # 数据源对比
        source_comparison_rows = ""
        for source, data in sources_data.items():
            status = "✓ 成功" if data.get('success', False) else "✗ 失败"
            differences = "无显著差异" if data.get('success', False) else data.get('error', '未知错误')
            source_comparison_rows += f"""
                <tr>
                    <td>{source}</td>
                    <td>{status}</td>
                    <td>{differences}</td>
                </tr>
            """
        
        # 填充模板
        html_content = self.template.format(
            symbol=symbol,
            company_name=f"{symbol}股票分析",  # 在实际应用中，这里应该是公司的实际名称
            analysis_time=analysis_result['analysis_timestamp'],
            rating=rating,
            rating_pct=rating_pct,
            recommendation=recommendation,
            data_quality_score=data_quality_score,
            trend=trend,
            momentum=momentum,
            support=support,
            resistance=resistance,
            valuation=valuation,
            risk_rows=risk_rows,
            data_sources_html=data_sources_html,
            source_comparison_rows=source_comparison_rows
        )
        
        # 保存文件
        if output_path is None:
            output_path = f"output/report_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path

    def _get_risk_description(self, risk_type: str) -> str:
        """
        获取风险类型的描述
        """
        descriptions = {
            'market_risk': '市场整体波动带来的风险',
            'valuation_risk': '估值过高或过低的风险',
            'liquidity_risk': '交易流动性不足的风险',
            'technical_risk': '技术面走势不佳的风险',
            'overall_risk': '综合各类风险的整体评估'
        }
        return descriptions.get(risk_type, '风险类型说明')


def generate_stock_analysis_report(analysis_result: Dict) -> str:
    """
    生成股票分析报告的便捷函数
    """
    generator = HTMLReportGenerator()
    return generator.generate_report(analysis_result)