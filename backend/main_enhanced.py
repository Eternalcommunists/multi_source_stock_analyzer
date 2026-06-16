"""
多数据源股票分析系统 - 更新版主程序
集成财报分析、机构持股分析、做多做空分析等专业功能
"""

import argparse
import sys
import os
import json
from datetime import datetime
from typing import Any

sys.path.append(os.path.dirname(__file__))

from integrated_analyzer import IntegratedStockAnalyzer


class DateTimeEncoder(json.JSONEncoder):
    """
    自定义JSON编码器，用于处理datetime对象
    """
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def main():
    """
    主程序入口 - 更新版，支持高级分析功能
    """
    parser = argparse.ArgumentParser(description='多数据源股票分析系统（含高级分析功能）')
    parser.add_argument('--symbol', type=str, required=True, help='股票代码，例如: 000001')
    parser.add_argument('--sources', type=str, nargs='+',
                       default=['akshare'],
                       help='数据源列表，可选项: akshare, east_money, ifind, jqdata')
    parser.add_argument('--output-format', type=str, choices=['json', 'html', 'enhanced', 'all'],
                       default='all', help='输出格式: json, html, enhanced (含专业分析), or all')
    parser.add_argument('--output-dir', type=str,
                       default='output',
                       help='输出目录路径')

    args = parser.parse_args()

    # 创建集成分析器实例
    analyzer = IntegratedStockAnalyzer()

    print(f"开始分析股票: {args.symbol}")
    print(f"使用数据源: {args.sources}")
    print("执行综合分析（包含财报、机构持股、做多做空等专业分析）...")

    try:
        # 执行综合分析
        analysis_result = analyzer.comprehensive_analysis(args.symbol, args.sources)

        # 创建输出目录
        os.makedirs(args.output_dir, exist_ok=True)

        output_files = []

        # 输出JSON格式
        if args.output_format in ['json', 'all']:
            json_path = f"{args.output_dir}/analysis_{args.symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(analysis_result, f, ensure_ascii=False, indent=2, cls=DateTimeEncoder)
            output_files.append(json_path)
            print(f"JSON报告已保存至: {json_path}")

        # 输出HTML格式（基础版）
        if args.output_format in ['html', 'all']:
            from html_generator import generate_stock_analysis_report
            html_path = generate_stock_analysis_report(analysis_result['basic_analysis'])
            output_files.append(html_path)
            print(f"HTML报告已保存至: {html_path}")

        # 输出增强版HTML格式（含专业分析）
        if args.output_format in ['enhanced', 'all']:
            enhanced_html_path, enhanced_json_path = analyzer.generate_enhanced_report(args.symbol, args.sources)
            output_files.extend([enhanced_html_path, enhanced_json_path])
            print(f"增强版HTML报告已保存至: {enhanced_html_path}")
            print(f"增强版JSON报告已保存至: {enhanced_json_path}")

        # 输出分析摘要
        print("\n" + "="*70)
        print("股票综合分析报告摘要（含专业分析）")
        print("="*70)
        print(f"股票代码: {analysis_result['symbol']}")
        print(f"分析时间: {analysis_result['analysis_timestamp']}")
        print(f"综合评分: {analysis_result['integrated_score']}/10")
        print(f"综合建议: {analysis_result['combined_recommendation']}")
        print(f"总体风险: {analysis_result['risk_summary']['overall_summary']}")

        # 基础分析摘要
        basic_analysis = analysis_result['basic_analysis']['detailed_analysis']
        print(f"\n基础分析:")
        print(f"  投资评分: {basic_analysis['investment_rating']}/10")
        print(f"  技术趋势: {basic_analysis['technical_analysis']['trend']}")
        print(f"  动量状态: {basic_analysis['technical_analysis']['momentum']}")
        print(f"  估值状态: {basic_analysis['fundamental_analysis']['valuation']}")
        print(f"  风险等级: {basic_analysis['risk_assessment']['overall_risk']}")

        # 高级分析摘要
        advanced_analysis = analysis_result['advanced_analysis']
        print(f"\n高级分析:")
        print(f"  财务健康度: {advanced_analysis['financial_analysis']['data']['health_assessment']['overall_health']}")
        print(f"  财务健康得分: {advanced_analysis['financial_analysis']['data']['health_assessment']['score']}/100")
        print(f"  机构信心: {advanced_analysis['institutional_analysis']['data']['trend_analysis']['institutional_confidence']}")
        print(f"  做空情绪: {advanced_analysis['short_analysis']['data']['analysis']['sentiment']}")
        print(f"  推荐强度: {advanced_analysis['recommendation_strength']}")

        # 风险因素
        risk_factors = advanced_analysis['risk_factors']
        if risk_factors:
            print(f"\n识别风险因素 ({len(risk_factors)} 项):")
            for i, factor in enumerate(risk_factors[:5]):  # 最多显示5项
                print(f"  {i+1}. {factor}")
        else:
            print(f"\n未识别到显著风险因素")

        print(f"\n输出文件: {', '.join(output_files)}")
        print("="*70)

    except Exception as e:
        print(f"分析过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()


def quick_analyze(symbol: str, sources: list = None):
    """
    快速分析函数，方便在代码中直接调用
    """
    if sources is None:
        sources = ['akshare']

    analyzer = IntegratedStockAnalyzer()
    result = analyzer.comprehensive_analysis(symbol, sources)

    # 生成增强版报告
    html_report_path, json_report_path = analyzer.generate_enhanced_report(symbol, sources)

    return result, html_report_path, json_report_path


if __name__ == "__main__":
    main()