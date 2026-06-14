"""
多数据源股票分析系统 - 数据源适配层
"""

import akshare as ak
import pandas as pd
import numpy as np
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union


class DataSourceAdapter:
    """
    数据源适配器，统一接口访问不同的数据源
    """
    
    def __init__(self):
        self.data_sources = {
            'akshare': self._fetch_akshare_data,
            'east_money': self._fetch_eastmoney_data,  # 东方财富
            'ifind': self._fetch_ifind_data,           # 同花顺iFinD
            'jqdata': self._fetch_jqdata_data          # jqdatasdk
        }
    
    def get_stock_data(self, symbol: str, data_source: str = 'akshare') -> Dict:
        """
        获取股票数据，支持多种数据源
        """
        if data_source not in self.data_sources:
            raise ValueError(f"不支持的数据源: {data_source}")
        
        return self.data_sources[data_source](symbol)
    
    def _fetch_akshare_data(self, symbol: str) -> Dict:
        """
        通过akshare获取数据
        """
        try:
            # 获取股票基本信息
            stock_info = ak.stock_individual_info_em(symbol=symbol)
            
            # 获取实时行情
            quote_data = ak.stock_zh_a_spot_em()
            stock_quote = quote_data[quote_data['代码'] == symbol].to_dict('records')
            
            # 获取历史K线数据
            kline_data = ak.stock_zh_a_hist(symbol=symbol, period="daily", adjust="")
            
            # 构建统一数据格式
            result = {
                'symbol': symbol,
                'data_source': 'akshare',
                'timestamp': datetime.now().isoformat(),
                'basic_info': stock_info.to_dict() if not stock_info.empty else {},
                'quote': stock_quote[0] if stock_quote else {},
                'kline': kline_data.to_dict('records')[-30:] if not kline_data.empty else [],  # 最近30个交易日
                'success': True,
                'error': None
            }
            
            return result
            
        except Exception as e:
            return {
                'symbol': symbol,
                'data_source': 'akshare',
                'timestamp': datetime.now().isoformat(),
                'data': {},
                'success': False,
                'error': str(e)
            }
    
    def _fetch_eastmoney_data(self, symbol: str) -> Dict:
        """
        通过东方财富API获取数据
        """
        try:
            # 东方财富的API接口需要构造特定的URL
            # 这里使用模拟数据结构，实际应用中需要替换为真实API调用
            result = {
                'symbol': symbol,
                'data_source': 'east_money',
                'timestamp': datetime.now().isoformat(),
                'basic_info': {},
                'quote': {},
                'kline': [],
                'success': True,
                'error': None
            }
            
            # 实际实现需要根据东方财富API接口进行调用
            # 示例：获取实时行情
            # url = f"https://push2.eastmoney.com/api/qt/stock/get?secid=0.{symbol}&..."
            # response = requests.get(url)
            # data = response.json()
            
            return result
            
        except Exception as e:
            return {
                'symbol': symbol,
                'data_source': 'east_money',
                'timestamp': datetime.now().isoformat(),
                'data': {},
                'success': False,
                'error': str(e)
            }
    
    def _fetch_ifind_data(self, symbol: str) -> Dict:
        """
        通过同花顺iFinD获取数据
        """
        try:
            # iFinD通常需要认证和订阅服务
            # 这里使用模拟数据结构，实际应用中需要替换为真实API调用
            result = {
                'symbol': symbol,
                'data_source': 'ifind',
                'timestamp': datetime.now().isoformat(),
                'basic_info': {},
                'quote': {},
                'kline': [],
                'success': True,
                'error': None
            }
            
            # 实际实现需要根据iFinD API接口进行调用
            # 示例：ifindpy库的使用
            # import ifind
            # data = ifind.wsd(symbol, "close,pe_ttm,pb_lf", ...)
            
            return result
            
        except Exception as e:
            return {
                'symbol': symbol,
                'data_source': 'ifind',
                'timestamp': datetime.now().isoformat(),
                'data': {},
                'success': False,
                'error': str(e)
            }
    
    def _fetch_jqdata_data(self, symbol: str) -> Dict:
        """
        通过jqdatasdk获取数据
        """
        try:
            # jqdatasdk需要账户认证
            # 这里使用模拟数据结构，实际应用中需要替换为真实API调用
            result = {
                'symbol': symbol,
                'data_source': 'jqdata',
                'timestamp': datetime.now().isoformat(),
                'basic_info': {},
                'quote': {},
                'kline': [],
                'success': True,
                'error': None
            }
            
            # 实际实现需要根据jqdatasdk接口进行调用
            # 示例：
            # import jqdatasdk as jq
            # jq.auth('username', 'password')
            # quote = jq.get_price(symbol, ...)
            
            return result
            
        except Exception as e:
            return {
                'symbol': symbol,
                'data_source': 'jqdata',
                'timestamp': datetime.now().isoformat(),
                'data': {},
                'success': False,
                'error': str(e)
            }


class StockAnalyzer:
    """
    股票分析器，基于统一格式的数据进行分析
    """
    
    def __init__(self):
        self.adapter = DataSourceAdapter()
    
    def analyze_stock(self, symbol: str, data_source: str = 'akshare') -> Dict:
        """
        分析股票，返回综合分析结果
        """
        # 获取数据
        raw_data = self.adapter.get_stock_data(symbol, data_source)
        
        if not raw_data['success']:
            return {
                'symbol': symbol,
                'analysis_timestamp': datetime.now().isoformat(),
                'error': raw_data['error'],
                'success': False
            }
        
        # 数据处理和分析
        processed_data = self._process_data(raw_data)
        analysis_result = self._perform_analysis(processed_data)
        
        return {
            'symbol': symbol,
            'analysis_timestamp': datetime.now().isoformat(),
            'raw_data': raw_data,
            'processed_data': processed_data,
            'analysis': analysis_result,
            'success': True
        }
    
    def _process_data(self, raw_data: Dict) -> Dict:
        """
        处理原始数据，转换为标准格式
        """
        processed = {
            'basic_info': raw_data.get('basic_info', {}),
            'quote': self._normalize_quote_data(raw_data.get('quote', {})),
            'kline': self._normalize_kline_data(raw_data.get('kline', [])),
            'technical_indicators': {},
            'fundamental_metrics': {}
        }
        
        # 计算技术指标
        if processed['kline']:
            processed['technical_indicators'] = self._calculate_technical_indicators(processed['kline'])
        
        # 提取基本面指标
        processed['fundamental_metrics'] = self._extract_fundamental_metrics(raw_data.get('quote', {}))
        
        return processed
    
    def _normalize_quote_data(self, quote_data: Dict) -> Dict:
        """
        标准化报价数据
        """
        normalized = {
            'current_price': quote_data.get('最新价', quote_data.get('close', 0)),
            'change_amount': quote_data.get('涨跌额', 0),
            'change_percent': quote_data.get('涨跌幅', 0),
            'volume': quote_data.get('成交量', 0),
            'turnover': quote_data.get('成交额', 0),
            'open': quote_data.get('开盘', 0),
            'high': quote_data.get('最高', 0),
            'low': quote_data.get('最低', 0),
            'prev_close': quote_data.get('昨收', 0),
            'pe': quote_data.get('市盈率', 0),
            'pb': quote_data.get('市净率', 0)
        }
        
        return normalized
    
    def _normalize_kline_data(self, kline_data: List[Dict]) -> List[Dict]:
        """
        标准化K线数据
        """
        normalized = []
        for kline in kline_data:
            normalized_kline = {
                'date': kline.get('日期', kline.get('date', '')),
                'open': float(kline.get('开盘', kline.get('open', 0))),
                'high': float(kline.get('最高', kline.get('high', 0))),
                'low': float(kline.get('最低', kline.get('low', 0))),
                'close': float(kline.get('收盘', kline.get('close', 0))),
                'volume': kline.get('成交量', kline.get('volume', 0)),
                'turnover': kline.get('成交额', kline.get('turnover', 0))
            }
            normalized.append(normalized_kline)
        
        return normalized
    
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
        
        # 计算布林带
        if len(closes) >= 20:
            ma20 = indicators.get('ma20', sum(closes[-20:]) / 20)
            variance = sum((close - ma20) ** 2 for close in closes[-20:]) / 20
            std_dev = variance ** 0.5
            
            indicators['boll_upper'] = ma20 + 2 * std_dev
            indicators['boll_lower'] = ma20 - 2 * std_dev
            indicators['boll_middle'] = ma20
        
        return indicators
    
    def _extract_fundamental_metrics(self, quote_data: Dict) -> Dict:
        """
        提取基本面指标
        """
        metrics = {
            'pe': quote_data.get('市盈率', quote_data.get('pe', 0)),
            'pb': quote_data.get('市净率', quote_data.get('pb', 0)),
            'pe_ttm': quote_data.get('市盈率TTM', 0),
            'dividend_yield': quote_data.get('股息率', 0),
            'total_market_cap': quote_data.get('总市值', 0),
            'circulating_market_cap': quote_data.get('流通市值', 0)
        }
        
        return metrics
    
    def _perform_analysis(self, processed_data: Dict) -> Dict:
        """
        执行综合分析
        """
        analysis = {
            'investment_rating': self._calculate_investment_rating(processed_data),
            'technical_analysis': self._analyze_technical_signals(processed_data),
            'fundamental_analysis': self._analyze_fundamentals(processed_data),
            'risk_assessment': self._assess_risks(processed_data),
            'recommendation': self._generate_recommendation(processed_data)
        }
        
        return analysis
    
    def _calculate_investment_rating(self, processed_data: Dict) -> float:
        """
        计算投资评级 (1-10分)
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
        
        return risks
    
    def _generate_recommendation(self, processed_data: Dict) -> str:
        """
        生成投资建议
        """
        rating = processed_data['analysis']['investment_rating']
        tech_signals = processed_data['analysis']['technical_analysis']
        fundamentals = processed_data['analysis']['fundamental_analysis']
        risks = processed_data['analysis']['risk_assessment']
        
        if rating >= 7.5:
            return "强烈推荐关注，技术面和基本面均表现良好"
        elif rating >= 6.0:
            return "推荐关注，有一定投资价值"
        elif rating >= 4.0:
            return "谨慎观望，需进一步观察"
        else:
            return "暂时回避，存在较多不确定因素"


def main():
    """
    主函数，演示系统功能
    """
    analyzer = StockAnalyzer()
    
    # 测试分析一只股票
    symbol = "000001"  # 平安银行
    result = analyzer.analyze_stock(symbol, data_source='akshare')
    
    if result['success']:
        print(f"股票代码: {result['symbol']}")
        print(f"投资评级: {result['analysis']['investment_rating']}/10")
        print(f"技术趋势: {result['analysis']['technical_analysis']['trend']}")
        print(f"估值状况: {result['analysis']['fundamental_analysis']['valuation']}")
        print(f"总体风险: {result['analysis']['risk_assessment']['overall_risk']}")
        print(f"投资建议: {result['analysis']['recommendation']}")
    else:
        print(f"分析失败: {result['error']}")


if __name__ == "__main__":
    main()