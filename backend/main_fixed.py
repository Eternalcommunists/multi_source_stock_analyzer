"""
多数据源股票分析系统 - 主程序（最终修复版）
"""

import argparse
import sys
import os
import json
from datetime import datetime, date
sys.path.append(os.path.dirname(__file__))
from core_analyzer import MultiDataSourceAnalyzer
from html_generator import generate_stock_analysis_report


class DateTimeEncoder(json.JSONEncoder):
    """
    自定义JSON编码器，处理datetime和date对象
    """
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


def main():
    """
    主程序入口
    """
    parser = argparse.ArgumentParser(description='多数据源股票分析系统')
    parser.add_argument('--symbol', type=str, required=True, help='股票代码，例如: 000001')
    parser.add_argument('--sources', type=str, nargs='+', 
                       default=['akshare'], 
                       help='数据源列表，可选项: akshare, east_money, ifind, jqdata')
    parser.add_argument('--output-format', type=str, choices=['json', 'html', 'both'], 
                       default='both', help='输出格式: json, html, or both')
    parser.add_argument('--output-dir', type=str, 
                       default='output',
                       help='输出目录路径')
    
    args = parser.parse_args()
    
    # 创建分析器实例
    analyzer = MultiDataSourceAnalyzer()
    
    print(f"开始分析股票: {args.symbol}")
    print(f"使用数据源: {args.sources}")
    
    try:
        # 对每个数据源执行分析
        all_results = []
        for source in args.sources:
            print(f"\n正在使用 {source} 数据源进行分析...")
            analysis_result = analyzer.comprehensive_analysis(args.symbol, [source])
            all_results.append({
                'data_source': source,
                'result': analysis_result
            })
        
        # 选择最优结果（基于评分和数据完整性）
        best_result = None
        best_score = -1
        
        for result_info in all_results:
            result = result_info['result']
            if result.get('success', False):
                score = result.get('detailed_analysis', {}).get('investment_rating', 0)
                if score > best_score:
                    best_score = score
                    best_result = result
        
        # 如果没有成功的结果，使用第一个结果
        if best_result is None and all_results:
            best_result = all_results[0]['result']
        
        # 创建输出目录
        os.makedirs(args.output_dir, exist_ok=True)
        
        output_files = []
        
        # 输出JSON格式
        if args.output_format in ['json', 'both']:
            json_path = f"{args.output_dir}/analysis_{args.symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(best_result, f, ensure_ascii=False, indent=2, cls=DateTimeEncoder)
            output_files.append(json_path)
            print(f"JSON报告已保存至: {json_path}")
        
        # 输出HTML格式
        if args.output_format in ['html', 'both']:
            html_path = generate_stock_analysis_report(best_result)
            output_files.append(html_path)
            print(f"HTML报告已保存至: {html_path}")
        
        # 输出分析摘要
        print("\n" + "="*60)
        print("股票分析报告摘要")
        print("="*60)
        if best_result and best_result.get('success', False):
            print(f"股票代码: {best_result['symbol']}")
            print(f"分析时间: {best_result['analysis_timestamp']}")
            print(f"投资评分: {best_result['detailed_analysis']['investment_rating']}/10")
            print(f"风险等级: {best_result['detailed_analysis']['risk_assessment']['overall_risk']}")
            print(f"投资建议: {best_result['recommendation']}")
            
            tech_analysis = best_result['detailed_analysis']['technical_analysis']
            print(f"技术趋势: {tech_analysis['trend']}")
            print(f"动量状态: {tech_analysis['momentum']}")
            
            fundamental_analysis = best_result['detailed_analysis']['fundamental_analysis']
            print(f"估值状态: {fundamental_analysis['valuation']}")
        else:
            print(f"股票代码: {args.symbol}")
            print(f"分析时间: {datetime.now().isoformat()}")
            print("分析结果: 数据获取失败")
            print(f"错误信息: {best_result.get('error', '未知错误') if best_result else '无结果数据'}")
        
        print(f"\n输出文件: {', '.join(output_files)}")
        print("="*60)
        
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
    
    analyzer = MultiDataSourceAnalyzer()
    results = []
    
    for source in sources:
        result = analyzer.comprehensive_analysis(symbol, [source])
        results.append({'data_source': source, 'result': result})
    
    # 选择最好的结果
    best_result = None
    best_score = -1
    
    for result_info in results:
        result = result_info['result']
        if result.get('success', False):
            score = result.get('detailed_analysis', {}).get('investment_rating', 0)
            if score > best_score:
                best_score = score
                best_result = result
    
    # 如果没有成功的结果，使用第一个结果
    if best_result is None and results:
        best_result = results[0]['result']
    
    # 生成报告
    html_report_path = generate_stock_analysis_report(best_result)
    
    return best_result, html_report_path


if __name__ == "__main__":
    main()