"""
多数据源股票分析系统 - 集成高级分析模块
整合财报分析、机构持股分析、做多做空分析等专业功能
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from core_analyzer import MultiDataSourceAnalyzer
from advanced_analyzer import AdvancedStockAnalyzer
from html_generator import generate_stock_analysis_report
import json
from datetime import datetime
from typing import Dict, List


class IntegratedStockAnalyzer:
    """
    集成股票分析器，结合基础分析和高级分析功能
    """

    def __init__(self):
        self.basic_analyzer = MultiDataSourceAnalyzer()
        self.advanced_analyzer = AdvancedStockAnalyzer()

    def comprehensive_analysis(self, symbol: str, sources: List[str] = None) -> Dict:
        """
        执行综合分析（包括基础分析和高级分析）
        """
        if sources is None:
            sources = ['akshare']

        # 执行基础多源分析
        basic_result = self.basic_analyzer.comprehensive_analysis(symbol, sources)

        # 执行高级分析
        advanced_result = self.advanced_analyzer.generate_advanced_report(symbol)

        # 合并结果
        integrated_result = {
            'symbol': symbol,
            'analysis_timestamp': datetime.now().isoformat(),
            'basic_analysis': basic_result,
            'advanced_analysis': advanced_result,
            'integrated_score': self._calculate_integrated_score(basic_result, advanced_result),
            'combined_recommendation': self._combine_recommendations(basic_result, advanced_result),
            'risk_summary': self._summarize_risks(basic_result, advanced_result)
        }

        return integrated_result

    def _calculate_integrated_score(self, basic_result: Dict, advanced_result: Dict) -> float:
        """
        计算综合评分（结合基础和高级分析）
        """
        # 基础分析评分
        basic_score = basic_result['detailed_analysis']['investment_rating']  # 1-10分

        # 高级分析评分
        advanced_score = advanced_result['comprehensive_score']  # 1-100分，转为1-10分制
        advanced_score_norm = advanced_score / 10.0

        # 加权平均（可以根据需要调整权重）
        integrated_score = (basic_score * 0.4) + (advanced_score_norm * 0.6)

        return round(integrated_score, 1)

    def _combine_recommendations(self, basic_result: Dict, advanced_result: Dict) -> str:
        """
        结合基础和高级分析给出综合建议
        """
        basic_rec = basic_result['recommendation']
        advanced_rec = advanced_result['recommendation_strength']

        # 根据综合评分给出建议
        integrated_score = self._calculate_integrated_score(basic_result, advanced_result)

        if integrated_score >= 8.0:
            return "强烈推荐关注，综合分析显示该公司基本面强劲，机构看好，具备长期投资价值"
        elif integrated_score >= 7.0:
            return "推荐关注，综合分析显示该公司有一定投资价值，建议逢低布局"
        elif integrated_score >= 5.0:
            return "谨慎关注，综合分析显示存在一定机会，但需密切关注风险"
        elif integrated_score >= 3.0:
            return "建议观望，综合分析显示当前时机不太理想，等待更好入场点"
        else:
            return "建议回避，综合分析显示存在较多不确定性因素，风险大于收益"

    def _summarize_risks(self, basic_result: Dict, advanced_result: Dict) -> Dict:
        """
        汇总风险信息
        """
        risks = {
            'market_risk': basic_result['detailed_analysis']['risk_assessment']['market_risk'],
            'valuation_risk': basic_result['detailed_analysis']['risk_assessment']['valuation_risk'],
            'financial_risk': advanced_result['financial_analysis']['data']['health_assessment']['overall_health'],
            'liquidity_risk': basic_result['detailed_analysis']['risk_assessment']['liquidity_risk'],
            'institutional_risk': advanced_result['institutional_analysis']['data']['trend_analysis']['institutional_confidence'],
            'short_selling_risk': advanced_result['short_analysis']['data']['analysis']['risk_level'],
            'overall_summary': self._generate_overall_risk_summary(basic_result, advanced_result)
        }

        return risks

    def _generate_overall_risk_summary(self, basic_result: Dict, advanced_result: Dict) -> str:
        """
        生成总体风险总结
        """
        basic_risk = basic_result['detailed_analysis']['risk_assessment']['overall_risk']
        advanced_risk_factors = advanced_result['risk_factors']

        if basic_risk == 'high' or advanced_risk_factors:
            return f"风险等级较高，需要注意{basic_risk}风险及{len(advanced_risk_factors)}项特定风险"
        elif basic_risk == 'medium':
            return "存在中等程度风险，建议密切关注基本面变化"
        else:
            return "风险控制良好，但仍需关注市场波动"

    def generate_enhanced_report(self, symbol: str, sources: List[str] = None) -> str:
        """
        生成增强版报告
        """
        if sources is None:
            sources = ['akshare']

        # 执行综合分析
        integrated_result = self.comprehensive_analysis(symbol, sources)

        # 生成HTML报告
        report_path = self._generate_enhanced_html_report(integrated_result)

        # 保存详细JSON报告
        json_path = f"output/integrated_analysis_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs(os.path.dirname(json_path), exist_ok=True)

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(integrated_result, f, ensure_ascii=False, indent=2, default=str)

        return report_path, json_path

    def _generate_enhanced_html_report(self, integrated_result: Dict) -> str:
        """
        生成增强版HTML报告
        """
        # 构造增强版报告数据
        enhanced_data = {
            'symbol': integrated_result['symbol'],
            'analysis_timestamp': integrated_result['analysis_timestamp'],
            'investment_rating': integrated_result['integrated_score'],
            'recommendation': integrated_result['combined_recommendation'],
            'data_quality_score': integrated_result['basic_analysis']['data_quality_score'],
            'detailed_analysis': {
                'technical_analysis': integrated_result['basic_analysis']['detailed_analysis']['technical_analysis'],
                'fundamental_analysis': integrated_result['basic_analysis']['detailed_analysis']['fundamental_analysis'],
                'risk_assessment': integrated_result['risk_summary']
            },
            'advanced_insights': {
                'financial_health': integrated_result['advanced_analysis']['financial_analysis']['data']['health_assessment'],
                'institutional_confidence': integrated_result['advanced_analysis']['institutional_analysis']['data']['trend_analysis'],
                'market_sentiment': integrated_result['advanced_analysis']['wall_street_analysis']['data']['consensus'],
                'short_interest_analysis': integrated_result['advanced_analysis']['short_analysis']['data']['analysis']
            }
        }

        # 使用现有的HTML生成器，但要稍微修改以包含高级分析内容
        return generate_enhanced_stock_analysis_report(enhanced_data)


def generate_enhanced_stock_analysis_report(analysis_result: Dict) -> str:
    """
    生成包含高级分析内容的股票报告
    """
    # 导入HTML生成器类
    from html_generator import HTMLReportGenerator
    import os
    from datetime import datetime

    class EnhancedHTMLReportGenerator(HTMLReportGenerator):
        def generate_enhanced_report(self, analysis_result: Dict, output_path: str = None) -> str:
            """
            生成包含高级分析的报告
            """
            symbol = analysis_result['symbol']

            # 准备基本数据
            rating = analysis_result['investment_rating']
            rating_pct = (rating / 10) * 100

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
                if risk_type != 'overall_summary':  # 排除汇总字段
                    risk_class = f"risk-{level}" if level in ['high', 'medium', 'low', 'critical', 'excellent', 'good', 'fair', 'poor'] else "risk-medium"
                    risk_desc = f"{risk_type}风险" if isinstance(level, str) else "风险"
                    risk_rows += f"""
                        <tr class="{risk_class}">
                            <td>{risk_desc}</td>
                            <td>{level}</td>
                            <td>{self._get_risk_description(risk_type)}</td>
                        </tr>
                    """

            # 高级分析内容
            advanced_insights = analysis_result.get('advanced_insights', {})
            advanced_section = ""

            if advanced_insights:
                financial_health = advanced_insights.get('financial_health', {})
                institutional_conf = advanced_insights.get('institutional_confidence', {})
                market_sentiment = advanced_insights.get('market_sentiment', 'unknown')
                short_analysis = advanced_insights.get('short_interest_analysis', {})

                advanced_section = f"""
                <div class="report-section">
                    <h3 class="section-title">高级分析洞察</h3>

                    <div class="report-section">
                        <h4>财务健康度</h4>
                        <div class="metric-grid">
                            <div class="metric-card">
                                <h5>整体健康</h5>
                                <p>{financial_health.get('overall_health', 'unknown')}</p>
                            </div>
                            <div class="metric-card">
                                <h5>健康得分</h5>
                                <p>{financial_health.get('score', 0)}/100</p>
                            </div>
                        </div>
                        {('<p><strong>财务优势:</strong> ' + ', '.join(financial_health.get('strengths', [])[:3]) + '</p>') if financial_health.get('strengths') else ''}
                        {('<p><strong>财务弱点:</strong> ' + ', '.join(financial_health.get('weaknesses', [])[:3]) + '</p>') if financial_health.get('weaknesses') else ''}
                    </div>

                    <div class="report-section">
                        <h4>机构持股分析</h4>
                        <div class="metric-grid">
                            <div class="metric-card">
                                <h5>机构信心</h5>
                                <p>{institutional_conf.get('institutional_confidence', 'unknown')}</p>
                            </div>
                            <div class="metric-card">
                                <h5>持股集中度</h5>
                                <p>{institutional_conf.get('ownership_concentration', 'unknown')}</p>
                            </div>
                            <div class="metric-card">
                                <h5>前十大占比</h5>
                                <p>{institutional_conf.get('top_holder_percentage', 0):.2%}</p>
                            </div>
                        </div>
                    </div>

                    <div class="report-section">
                        <h4>市场情绪分析</h4>
                        <div class="metric-grid">
                            <div class="metric-card">
                                <h5>分析师共识</h5>
                                <p>{market_sentiment}</p>
                            </div>
                            <div class="metric-card">
                                <h5>做空情绪</h5>
                                <p>{short_analysis.get('sentiment', 'unknown')}</p>
                            </div>
                            <div class="metric-card">
                                <h5>做空风险</h5>
                                <p>{short_analysis.get('risk_level', 'unknown')}</p>
                            </div>
                        </div>
                    </div>
                </div>
                """

            # 数据源信息
            # 注意：在增强版报告中，我们假设使用了基础分析中的数据源信息
            data_sources_html = '<span class="source-tag" style="background: #3498db;">akshare: ✓ 成功</span>'

            # 生成完整HTML
            html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>增强版股票分析报告 - {symbol}</title>
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
        .risk-critical {{ border-left-color: #c0392b; }}
        .risk-excellent {{ border-left-color: #27ae60; }}
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
        .insight-badge {{
            display: inline-block;
            background: #9b59b6;
            color: white;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 12px;
            margin: 0 2px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>增强版股票分析报告</h1>
        <h2>{symbol} - 综合分析报告</h2>
        <p>分析时间: {analysis_result['analysis_timestamp']}</p>
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

    {advanced_section}

    <div class="disclaimer">
        <strong>免责声明:</strong> 本报告基于公开数据和算法分析，仅供参考，不构成投资建议。
        投资有风险，入市需谨慎。请结合自身情况做出投资决策。
        此外，本报告整合了财报分析、机构持股、做多做空等专业分析，提供更多维度的投资参考。
    </div>
</body>
</html>
            """

            # 保存文件
            if output_path is None:
                output_path = f"output/enhanced_report_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            return output_path

    generator = EnhancedHTMLReportGenerator()
    return generator.generate_enhanced_report(analysis_result)


def main():
    """
    主函数，演示集成分析功能
    """
    analyzer = IntegratedStockAnalyzer()

    # 测试分析一只股票
    symbol = "000001"  # 平安银行
    sources = ["akshare"]

    print(f"开始综合分析: {symbol}")
    print(f"使用数据源: {sources}")

    # 执行综合分析
    result = analyzer.comprehensive_analysis(symbol, sources)

    print("\n=== 综合分析报告摘要 ===")
    print(f"股票代码: {result['symbol']}")
    print(f"综合评分: {result['integrated_score']}/10")
    print(f"综合建议: {result['combined_recommendation']}")
    print(f"总体风险: {result['risk_summary']['overall_summary']}")

    # 基础分析摘要
    basic = result['basic_analysis']
    print(f"基础评分: {basic['detailed_analysis']['investment_rating']}/10")
    print(f"基础建议: {basic['recommendation']}")

    # 高级分析摘要
    advanced = result['advanced_analysis']
    print(f"高级评分: {advanced['comprehensive_score']}/100")
    print(f"推荐强度: {advanced['recommendation_strength']}")

    # 生成报告
    html_path, json_path = analyzer.generate_enhanced_report(symbol, sources)
    print(f"\n增强版HTML报告已保存至: {html_path}")
    print(f"详细JSON报告已保存至: {json_path}")


if __name__ == "__main__":
    main()