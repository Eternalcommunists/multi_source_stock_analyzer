"""
多数据源股票分析系统 - 核心分析引擎
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
import json
import os
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data-sources'))
from data_adapter import DataSourceAdapter, StockAnalyzer


class MultiDataSourceAnalyzer:
    """
    多数据源股票分析器，支持多个数据源对比分析
    """
    
    def __init__(self):
        self.data_adapter = DataSourceAdapter()
        self.analyzer = StockAnalyzer()
        self.output_dir = "d:/Codex/multi_source_stock_analyzer/output"
        
        # 创建输出目录
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def compare_sources(self, symbol: str, sources: List[str] = None) -> Dict:
        """
        对比不同数据源的数据
        """
        if sources is None:
            sources = ['akshare']
        
        results = {
            'symbol': symbol,
            'comparison_timestamp': datetime.now().isoformat(),
            'sources_data': {},
            'discrepancies': [],
            'consensus': {}
        }
        
        for source in sources:
            try:
                data = self.data_adapter.get_stock_data(symbol, source)
                results['sources_data'][source] = data
                
                if data['success']:
                    # 检查数据一致性
                    self._check_data_consistency(results, source, data)
            except Exception as e:
                results['sources_data'][source] = {
                    'success': False,
                    'error': str(e)
                }
        
        # 生成共识数据
        results['consensus'] = self._generate_consensus(results['sources_data'])
        
        return results
    
    def _check_data_consistency(self, results: Dict, source: str, data: Dict):
        """
        检查数据一致性
        """
        discrepancies = results['discrepancies']
        
        # 检查价格数据的一致性
        if 'quote' in data and data['quote']:
            quote = data['quote']
            
            # 检查价格字段是否存在显著差异
            for field in ['current_price', 'open', 'high', 'low', 'prev_close']:
                if field in quote:
                    # 在多源对比中检查该字段的差异
                    pass  # 实际实现中会与其他源对比
    
    def _generate_consensus(self, sources_data: Dict) -> Dict:
        """
        生成共识数据（多数源一致的数据）
        """
        consensus = {}
        
        # 获取所有成功的数据源
        successful_sources = {
            src: data for src, data in sources_data.items() 
            if data.get('success', False)
        }
        
        if not successful_sources:
            return consensus
        
        # 对于报价数据，取多个源的平均值或中位数
        quote_fields = ['current_price', 'change_percent', 'volume', 'pe', 'pb']
        quote_data = {}
        
        for field in quote_fields:
            values = []
            for data in successful_sources.values():
                quote = data.get('quote', {})
                if field in quote and quote[field] is not None:
                    try:
                        values.append(float(quote[field]))
                    except (ValueError, TypeError):
                        continue
            
            if values:
                # 使用中位数以减少异常值影响
                quote_data[field] = float(np.median(values))
        
        consensus['quote'] = quote_data
        
        # 对于K线数据，优先使用数据最完整的源
        kline_sources = {}
        for src, data in successful_sources.items():
            klines = data.get('kline', [])
            kline_sources[src] = len(klines)
        
        if kline_sources:
            primary_source = max(kline_sources, key=kline_sources.get)
            consensus['kline'] = successful_sources[primary_source].get('kline', [])
        
        return consensus
    
    def comprehensive_analysis(self, symbol: str, sources: List[str] = None) -> Dict:
        """
        综合分析（使用多数据源）
        """
        if sources is None:
            sources = ['akshare']
        
        # 获取多源数据
        comparison_result = self.compare_sources(symbol, sources)
        
        # 使用共识数据进行分析
        consensus_data = comparison_result['consensus']
        
        # 构建统一的分析输入
        analysis_input = {
            'symbol': symbol,
            'data_source': 'consensus',
            'timestamp': datetime.now().isoformat(),
            'basic_info': {},
            'quote': consensus_data.get('quote', {}),
            'kline': consensus_data.get('kline', []),
            'success': bool(consensus_data)  # 如果有共识数据则为成功
        }
        
        # 如果共识数据不可用，使用第一个成功源的数据
        if not analysis_input['success'] and comparison_result['sources_data']:
            for source, data in comparison_result['sources_data'].items():
                if data.get('success', False):
                    analysis_input = data
                    break
        
        # 进行详细分析
        detailed_analysis = self._perform_detailed_analysis(analysis_input)
        
        # 整合结果
        result = {
            'symbol': symbol,
            'analysis_timestamp': datetime.now().isoformat(),
            'data_comparison': comparison_result,
            'detailed_analysis': detailed_analysis,
            'recommendation': self._generate_final_recommendation(detailed_analysis),
            'data_quality_score': self._calculate_data_quality(comparison_result)
        }
        
        return result
    
    def _perform_detailed_analysis(self, data: Dict) -> Dict:
        """
        执行详细分析
        """
        # 使用现有分析器进行分析
        # 由于分析器期望特定格式，我们需要适配
        processed_data = {
            'basic_info': data.get('basic_info', {}),
            'quote': self._adapt_quote_data(data.get('quote', {})),
            'kline': self._adapt_kline_data(data.get('kline', []))
        }
        
        # 计算技术指标
        if processed_data['kline']:
            processed_data['technical_indicators'] = self._calculate_technical_indicators(processed_data['kline'])
        else:
            processed_data['technical_indicators'] = {}
        
        # 提取基本面指标
        processed_data['fundamental_metrics'] = self._extract_fundamental_metrics(processed_data['quote'])
        
        # 评分计算
        rating = self._calculate_comprehensive_rating(processed_data)
        
        # 技术分析
        tech_analysis = self._analyze_technical_signals(processed_data)
        
        # 基本面分析
        fundamental_analysis = self._analyze_fundamentals(processed_data)
        
        # 风险评估
        risk_assessment = self._assess_risks(processed_data)
        
        return {
            'investment_rating': rating,
            'technical_analysis': tech_analysis,
            'fundamental_analysis': fundamental_analysis,
            'risk_assessment': risk_assessment,
            'processed_data': processed_data
        }
    
    def _adapt_quote_data(self, quote: Dict) -> Dict:
        """
        适配报价数据格式
        """
        adapted = {
            'current_price': quote.get('current_price', 0),
            'change_amount': quote.get('change_amount', 0),
            'change_percent': quote.get('change_percent', 0),
            'volume': quote.get('volume', 0),
            'turnover': quote.get('turnover', 0),
            'open': quote.get('open', 0),
            'high': quote.get('high', 0),
            'low': quote.get('low', 0),
            'prev_close': quote.get('prev_close', 0),
            'pe': quote.get('pe', 0),
            'pb': quote.get('pb', 0)
        }
        return adapted
    
    def _adapt_kline_data(self, kline: List[Dict]) -> List[Dict]:
        """
        适配K线数据格式
        """
        # 确保数据格式一致
        adapted = []
        for k in kline:
            adapted_k = {
                'date': k.get('date', ''),
                'open': float(k.get('open', 0)),
                'high': float(k.get('high', 0)),
                'low': float(k.get('low', 0)),
                'close': float(k.get('close', 0)),
                'volume': k.get('volume', 0),
                'turnover': k.get('turnover', 0)
            }
            adapted.append(adapted_k)
        return adapted
    
    def _calculate_technical_indicators(self, kline_data: List[Dict]) -> Dict:
        """
        计算技术指标
        """
        if len(kline_data) < 30:
            return {}
        
        closes = [float(k['close']) for k in kline_data]
        highs = [float(k['high']) for k in kline_data]
        lows = [float(k['low']) for k in kline_data]
        volumes = [k['volume'] for k in kline_data]
        
        indicators = {}
        
        # 计算移动平均线
        if len(closes) >= 5:
            indicators['ma5'] = sum(closes[-5:]) / 5
        if len(closes) >= 20:
            indicators['ma20'] = sum(closes[-20:]) / 20
        if len(closes) >= 60:
            indicators['ma60'] = sum(closes[-60:]) / 60
        
        # 计算RSI (相对强弱指数)
        if len(closes) >= 14:
            deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
            gains = [delta if delta > 0 else 0 for delta in deltas[-14:]]
            losses = [-delta if delta < 0 else 0 for delta in deltas[-14:]]
            
            avg_gain = sum(gains) / 14
            avg_loss = sum(losses) / 14
            
            if avg_loss != 0:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
            else:
                rsi = 100  # 如果没有损失，则为超买状态
            
            indicators['rsi'] = rsi
        
        # 计算MACD (简化版)
        if len(closes) >= 26:
            # EMA12
            ema12_multi = 2 / (12 + 1)
            ema12 = closes[0]  # 初始值
            for i in range(1, min(12, len(closes))):
                ema12 = (closes[i] - ema12) * ema12_multi + ema12
            for i in range(12, min(26, len(closes))):
                ema12 = (closes[i] - ema12) * ema12_multi + ema12
            
            # EMA26
            ema26_multi = 2 / (26 + 1)
            ema26 = closes[0]  # 初始值
            for i in range(1, 26):
                ema26 = (closes[i] - ema26) * ema26_multi + ema26
            for i in range(26, len(closes)):
                ema26 = (closes[i] - ema26) * ema26_multi + ema26
            
            macd = ema12 - ema26
            indicators['macd'] = macd
        
        return indicators
    
    def _extract_fundamental_metrics(self, quote_data: Dict) -> Dict:
        """
        提取基本面指标
        """
        metrics = {
            'pe': quote_data.get('pe', 0),
            'pb': quote_data.get('pb', 0),
            'current_price': quote_data.get('current_price', 0)
        }
        
        return metrics
    
    def _calculate_comprehensive_rating(self, processed_data: Dict) -> float:
        """
        计算综合评分
        """
        rating = 5.0  # 基础分
        
        # 技术面评分
        tech_indicators = processed_data.get('technical_indicators', {})
        current_price = processed_data['quote'].get('current_price', 0)
        
        if 'ma5' in tech_indicators and 'ma20' in tech_indicators:
            if tech_indicators['ma5'] > tech_indicators['ma20']:
                rating += 1.0  # 短期均线上穿长期均线
            else:
                rating -= 0.5  # 短期均线下穿长期均线
        
        # 基本面评分
        pe = processed_data['fundamental_metrics'].get('pe', 0)
        pb = processed_data['fundamental_metrics'].get('pb', 0)
        
        if 0 < pe < 15:
            rating += 1.0  # PE合理区间
        elif pe > 30:
            rating -= 1.0  # PE过高
        
        if 0 < pb < 1.5:
            rating += 0.5  # PB合理区间
        elif pb > 3:
            rating -= 0.5  # PB过高
        
        # RSI评分
        if 'rsi' in tech_indicators:
            rsi = tech_indicators['rsi']
            if 30 <= rsi <= 70:
                rating += 0.5  # RSI在合理区间
            elif rsi < 30 or rsi > 70:
                rating -= 0.2  # RSI超买超卖
        
        # MACD评分
        if 'macd' in tech_indicators:
            macd = tech_indicators['macd']
            if macd > 0:
                rating += 0.3  # MACD正值
            else:
                rating -= 0.1  # MACD负值
        
        # 限制评分范围
        rating = max(1.0, min(10.0, rating))
        
        return round(rating, 1)
    
    def _analyze_technical_signals(self, processed_data: Dict) -> Dict:
        """
        技术面分析
        """
        tech_indicators = processed_data.get('technical_indicators', {})
        current_price = processed_data['quote'].get('current_price', 0)
        
        signals = {
            'trend': 'neutral',
            'support_resistance': {},
            'momentum': 'neutral',
            'volatility': 'normal'
        }
        
        # 趋势判断
        if 'ma5' in tech_indicators and 'ma20' in tech_indicators:
            if tech_indicators['ma5'] > tech_indicators['ma20']:
                signals['trend'] = 'bullish'
            elif tech_indicators['ma5'] < tech_indicators['ma20']:
                signals['trend'] = 'bearish'
            else:
                signals['trend'] = 'neutral'
        
        # 动量判断
        if 'rsi' in tech_indicators:
            rsi = tech_indicators['rsi']
            if rsi < 30:
                signals['momentum'] = 'oversold'
            elif rsi > 70:
                signals['momentum'] = 'overbought'
            else:
                signals['momentum'] = 'normal'
        
        # 支撑阻力位
        kline_data = processed_data.get('kline', [])
        if kline_data:
            recent_highs = [k['high'] for k in kline_data[-10:]]
            recent_lows = [k['low'] for k in kline_data[-10:]]
            signals['support_resistance'] = {
                'resistance': max(recent_highs) if recent_highs else current_price,
                'support': min(recent_lows) if recent_lows else current_price
            }
        
        return signals
    
    def _analyze_fundamentals(self, processed_data: Dict) -> Dict:
        """
        基本面分析
        """
        fundamentals = processed_data.get('fundamental_metrics', {})
        
        analysis = {
            'valuation': 'fair_value',
            'financial_health': 'stable',
            'growth_potential': 'moderate'
        }
        
        # 估值分析
        pe = fundamentals.get('pe', 0)
        if pe <= 0:
            analysis['valuation'] = 'invalid_data'
        elif pe < 10:
            analysis['valuation'] = 'undervalued'
        elif pe > 30:
            analysis['valuation'] = 'overvalued'
        else:
            analysis['valuation'] = 'fair_value'
        
        return analysis
    
    def _assess_risks(self, processed_data: Dict) -> Dict:
        """
        风险评估
        """
        risks = {
            'market_risk': 'medium',
            'valuation_risk': 'medium',
            'liquidity_risk': 'low',
            'technical_risk': 'medium',
            'overall_risk': 'medium'
        }
        
        # 基于PE和波动性评估估值风险
        pe = processed_data['fundamental_metrics'].get('pe', 0)
        if pe > 50:
            risks['valuation_risk'] = 'high'
        elif pe < 0 or pe > 30:
            risks['valuation_risk'] = 'medium'
        else:
            risks['valuation_risk'] = 'low'
        
        # 基于成交量评估流动性风险
        volume = processed_data['quote'].get('volume', 0)
        if volume < 1000000:  # 100万股
            risks['liquidity_risk'] = 'high'
        elif volume < 10000000:  # 1000万股
            risks['liquidity_risk'] = 'medium'
        else:
            risks['liquidity_risk'] = 'low'
        
        # 技术面风险
        tech_signals = self._analyze_technical_signals(processed_data)
        if tech_signals['trend'] == 'bearish':
            risks['technical_risk'] = 'high'
        elif tech_signals['momentum'] in ['overbought', 'oversold']:
            risks['technical_risk'] = 'medium'
        else:
            risks['technical_risk'] = 'low'
        
        # 综合风险
        risk_levels = {'low': 1, 'medium': 2, 'high': 3}
        avg_risk = sum(risk_levels[risk] for risk in risks.values() if risk in risk_levels) / len([r for r in risks.values() if r in risk_levels])
        
        if avg_risk <= 1.5:
            risks['overall_risk'] = 'low'
        elif avg_risk <= 2.5:
            risks['overall_risk'] = 'medium'
        else:
            risks['overall_risk'] = 'high'
        
        return risks
    
    def _generate_final_recommendation(self, detailed_analysis: Dict) -> str:
        """
        生成最终投资建议
        """
        rating = detailed_analysis['investment_rating']
        risk_level = detailed_analysis['risk_assessment']['overall_risk']
        
        if rating >= 8.0 and risk_level == 'low':
            return "强烈推荐买入，技术面和基本面均表现优秀，风险较低"
        elif rating >= 7.0 and risk_level in ['low', 'medium']:
            return "推荐买入，技术面和基本面表现良好"
        elif rating >= 6.0:
            return "谨慎关注，有一定投资价值但需注意风险"
        elif rating >= 4.0:
            return "观望为主，当前时机不太理想"
        else:
            return "建议回避，存在较多不确定性因素"
    
    def _calculate_data_quality(self, comparison_result: Dict) -> float:
        """
        计算数据质量分数
        """
        sources_data = comparison_result['sources_data']
        successful_sources = sum(1 for data in sources_data.values() if data.get('success', False))
        total_sources = len(sources_data)
        
        if total_sources == 0:
            return 0.0
        
        # 基础分数基于成功源的数量
        quality_score = (successful_sources / total_sources) * 7  # 最高7分
        
        # 如果有多个源，检查数据一致性
        if successful_sources > 1:
            # 这里可以添加数据一致性检查逻辑
            consistency_bonus = 2.0  # 一致性奖励
            quality_score += consistency_bonus
        
        # 添加时效性分数
        freshness_bonus = 1.0  # 时效性奖励
        quality_score += freshness_bonus
        
        return min(10.0, round(quality_score, 1))
    
    def generate_analysis_report(self, symbol: str, sources: List[str] = None) -> str:
        """
        生成分析报告
        """
        if sources is None:
            sources = ['akshare']
        
        analysis_result = self.comprehensive_analysis(symbol, sources)
        
        # 生成报告内容
        report_content = self._format_analysis_report(analysis_result)
        
        # 保存报告
        report_filename = f"{self.output_dir}/analysis_report_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)
        
        return report_filename
    
    def _format_analysis_report(self, analysis_result: Dict) -> str:
        """
        格式化分析报告
        """
        symbol = analysis_result['symbol']
        rating = analysis_result['detailed_analysis']['investment_rating']
        recommendation = analysis_result['recommendation']
        risk_level = analysis_result['detailed_analysis']['risk_assessment']['overall_risk']
        
        report = f"""
股票代码: {symbol}
分析时间: {analysis_result['analysis_timestamp']}
投资评分: {rating}/10
风险等级: {risk_level}
投资建议: {recommendation}

详细分析:
- 技术趋势: {analysis_result['detailed_analysis']['technical_analysis']['trend']}
- 动量状态: {analysis_result['detailed_analysis']['technical_analysis']['momentum']}
- 估值状况: {analysis_result['detailed_analysis']['fundamental_analysis']['valuation']}
- 数据质量: {analysis_result['data_quality_score']}/10

数据源对比:
"""
        
        for source, data in analysis_result['data_comparison']['sources_data'].items():
            status = "成功" if data.get('success', False) else "失败"
            report += f"  - {source}: {status}\n"
        
        return report


def main():
    """
    主函数，演示多数据源分析系统
    """
    analyzer = MultiDataSourceAnalyzer()
    
    # 测试分析一只股票
    symbol = "000001"  # 平安银行
    sources = ["akshare"]  # 由于其他数据源需要认证，先用akshare测试
    
    print(f"开始分析股票: {symbol}")
    print(f"使用数据源: {sources}")
    
    # 执行综合分析
    result = analyzer.comprehensive_analysis(symbol, sources)
    
    # 输出结果摘要
    print("\n=== 分析结果摘要 ===")
    print(f"股票代码: {result['symbol']}")
    print(f"投资评分: {result['detailed_analysis']['investment_rating']}/10")
    print(f"风险等级: {result['detailed_analysis']['risk_assessment']['overall_risk']}")
    print(f"投资建议: {result['recommendation']}")
    print(f"数据质量分数: {result['data_quality_score']}/10")
    
    # 生成报告
    report_path = analyzer.generate_analysis_report(symbol, sources)
    print(f"\n详细报告已保存至: {report_path}")
    
    # 显示技术分析详情
    tech_analysis = result['detailed_analysis']['technical_analysis']
    print(f"\n技术分析:")
    print(f"  趋势: {tech_analysis['trend']}")
    print(f"  动量: {tech_analysis['momentum']}")
    if tech_analysis['support_resistance']:
        sr = tech_analysis['support_resistance']
        print(f"  支撑位: {sr['support']}")
        print(f"  压力位: {sr['resistance']}")
    
    # 显示基本面分析详情
    fundamental_analysis = result['detailed_analysis']['fundamental_analysis']
    print(f"\n基本面分析:")
    print(f"  估值状态: {fundamental_analysis['valuation']}")
    
    # 显示风险评估
    risk_assessment = result['detailed_analysis']['risk_assessment']
    print(f"\n风险评估:")
    for risk_type, level in risk_assessment.items():
        print(f"  {risk_type}: {level}")


if __name__ == "__main__":
    main()