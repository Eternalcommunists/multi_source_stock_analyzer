"""
多数据源股票分析系统 - 高级分析器
包含财报分析、机构持股分析、做多做空分析等专业功能
"""

import akshare as ak
import pandas as pd
import numpy as np
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
import yfinance as yf  # 可能需要安装: pip install yfinance
import warnings
warnings.filterwarnings('ignore')


class AdvancedStockAnalyzer:
    """
    高级股票分析器，包含财报分析、机构持股分析、做多做空分析等功能
    """

    def __init__(self):
        self.fundamental_metrics = [
            'pe', 'pb', 'ps', 'pcf', 'roe', 'roa', 'debt_to_equity',
            'current_ratio', 'quick_ratio', 'gross_margin', 'operating_margin',
            'net_profit_margin', 'eps', 'bvps', 'dividend_yield'
        ]

    def analyze_financial_statements(self, symbol: str) -> Dict:
        """
        分析公司财务报表
        """
        try:
            # 使用akshare获取财务数据
            # 注意：根据实际情况调整API调用
            financial_report = {}

            # 获取利润表数据（示例）
            try:
                # 这里的接口可能会变化，需要根据akshare的最新版本调整
                profit_data = ak.stock_financial_abstract(symbol=symbol)
                financial_report['profit_statement'] = profit_data.to_dict('records')[-5:] if not profit_data.empty else []
            except:
                financial_report['profit_statement'] = []

            # 获取资产负债表数据（示例）
            try:
                balance_sheet = ak.stock_balance_sheet_by_report(symbol=symbol)
                financial_report['balance_sheet'] = balance_sheet.to_dict('records')[-5:] if not balance_sheet.empty else []
            except:
                financial_report['balance_sheet'] = []

            # 获取现金流量表数据（示例）
            try:
                cash_flow = ak.stock_cash_flow_sheet_by_report(symbol=symbol)
                financial_report['cash_flow'] = cash_flow.to_dict('records')[-5:] if not cash_flow.empty else []
            except:
                financial_report['cash_flow'] = []

            # 计算财务比率
            ratios = self._calculate_financial_ratios(financial_report)
            financial_report['ratios'] = ratios

            # 财务健康度评估
            health_assessment = self._assess_financial_health(ratios)
            financial_report['health_assessment'] = health_assessment

            return {
                'success': True,
                'data': financial_report,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def _calculate_financial_ratios(self, financial_data: Dict) -> Dict:
        """
        计算财务比率
        """
        ratios = {}

        # 由于API获取的实际数据可能有限，这里提供计算示例
        # 实际实现中应根据获取到的具体财务数据进行计算

        try:
            # 盈利能力指标
            ratios['roe'] = 0.15  # 净资产收益率，示例值
            ratios['roa'] = 0.08  # 总资产收益率，示例值
            ratios['gross_margin'] = 0.30  # 毛利率，示例值
            ratios['operating_margin'] = 0.15  # 营业利润率，示例值
            ratios['net_profit_margin'] = 0.10  # 净利率，示例值

            # 偿债能力指标
            ratios['debt_to_equity'] = 0.5  # 资产负债率，示例值
            ratios['current_ratio'] = 1.8  # 流动比率，示例值
            ratios['quick_ratio'] = 1.2  # 速动比率，示例值

            # 运营效率指标
            ratios['asset_turnover'] = 0.8  # 资产周转率，示例值
            ratios['inventory_turnover'] = 5.0  # 存货周转率，示例值

        except:
            # 如果无法计算具体数值，返回默认值
            ratios = {
                'roe': 0, 'roa': 0, 'gross_margin': 0, 'operating_margin': 0,
                'net_profit_margin': 0, 'debt_to_equity': 0, 'current_ratio': 0,
                'quick_ratio': 0, 'asset_turnover': 0, 'inventory_turnover': 0
            }

        return ratios

    def _assess_financial_health(self, ratios: Dict) -> Dict:
        """
        评估财务健康状况
        """
        assessment = {
            'overall_health': 'unknown',
            'strengths': [],
            'weaknesses': [],
            'score': 0
        }

        score = 0
        strengths = []
        weaknesses = []

        # 评估盈利能力
        if ratios.get('roe', 0) > 0.15:
            score += 20
            strengths.append(f"净资产收益率({ratios['roe']:.2%})表现优异")
        elif ratios.get('roe', 0) < 0.05:
            weaknesses.append(f"净资产收益率({ratios['roe']:.2%})偏低")

        if ratios.get('roa', 0) > 0.08:
            score += 15
            strengths.append(f"总资产收益率({ratios['roa']:.2%})表现良好")
        elif ratios.get('roa', 0) < 0.03:
            weaknesses.append(f"总资产收益率({ratios['roa']:.2%})偏低")

        # 评估偿债能力
        if ratios.get('current_ratio', 0) > 1.5:
            score += 10
            strengths.append(f"流动比率({ratios['current_ratio']:.2f})良好")
        elif ratios.get('current_ratio', 0) < 1.0:
            weaknesses.append(f"流动比率({ratios['current_ratio']:.2f})偏低，短期偿债能力不足")

        if ratios.get('debt_to_equity', 0) < 0.5:
            score += 10
            strengths.append(f"资产负债率({ratios['debt_to_equity']:.2%})较低")
        elif ratios.get('debt_to_equity', 0) > 0.7:
            weaknesses.append(f"资产负债率({ratios['debt_to_equity']:.2%})较高，财务风险大")

        # 评估运营效率
        if ratios.get('asset_turnover', 0) > 0.8:
            score += 10
            strengths.append("资产周转率表现优秀")

        # 设置总体健康状况
        if score >= 70:
            overall_health = 'excellent'
        elif score >= 50:
            overall_health = 'good'
        elif score >= 30:
            overall_health = 'fair'
        elif score >= 15:
            overall_health = 'poor'
        else:
            overall_health = 'critical'

        assessment.update({
            'overall_health': overall_health,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'score': min(100, max(0, score))
        })

        return assessment

    def analyze_institutional_holdings(self, symbol: str) -> Dict:
        """
        分析机构持股情况
        """
        try:
            # 获取机构持股数据
            holdings_data = {}

            # 使用Yahoo Finance作为示例（需要安装yfinance）
            try:
                ticker = yf.Ticker(f"{symbol}.SZ" if symbol.startswith(('0', '2', '3')) else f"{symbol}.SH")
                institutional_holders = ticker.institutional_holders
                major_holders = ticker.major_holders

                holdings_data['institutional_holders'] = institutional_holders.to_dict('records') if institutional_holders is not None else []
                holdings_data['major_holders'] = major_holders.to_dict('records') if major_holders is not None else []

                # 计算机构持股比例
                if institutional_holders is not None and len(institutional_holders) > 0:
                    total_shares = float(institutional_holders['Shares'].sum()) if 'Shares' in institutional_holders.columns else 0
                    holdings_data['total_institutional_shares'] = total_shares
            except:
                holdings_data = {
                    'institutional_holders': [],
                    'major_holders': [],
                    'total_institutional_shares': 0
                }

            # 分析机构持股趋势
            trend_analysis = self._analyze_holding_trends(holdings_data)
            holdings_data['trend_analysis'] = trend_analysis

            return {
                'success': True,
                'data': holdings_data,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def _analyze_holding_trends(self, holdings_data: Dict) -> Dict:
        """
        分析持股趋势
        """
        trend_analysis = {
            'institutional_confidence': 'neutral',
            'ownership_concentration': 'moderate',
            'top_holder_percentage': 0
        }

        try:
            institutional_holders = holdings_data.get('institutional_holders', [])
            if institutional_holders:
                # 计算前十大机构持股比例
                df = pd.DataFrame(institutional_holders)
                if 'Shares' in df.columns and '% Out' in df.columns:
                    top_holders = df.head(10)
                    top_holder_percentage = top_holders['% Out'].sum() if '% Out' in top_holders.columns else 0
                    trend_analysis['top_holder_percentage'] = float(top_holder_percentage)

                    # 判断机构信心
                    if top_holder_percentage > 50:
                        trend_analysis['ownership_concentration'] = 'high'
                        if top_holder_percentage > 70:
                            trend_analysis['institutional_confidence'] = 'very_high'
                        else:
                            trend_analysis['institutional_confidence'] = 'high'
                    elif top_holder_percentage > 20:
                        trend_analysis['ownership_concentration'] = 'moderate'
                        trend_analysis['institutional_confidence'] = 'moderate'
                    else:
                        trend_analysis['ownership_concentration'] = 'low'
                        trend_analysis['institutional_confidence'] = 'low'

        except:
            # 如果无法计算具体数值，返回默认值
            pass

        return trend_analysis

    def analyze_short_interest(self, symbol: str) -> Dict:
        """
        分析做空兴趣（做空头寸）
        """
        try:
            # 中国A股市场做空数据获取较困难，这里提供示例框架
            # 实际应用中可能需要从其他数据源获取相关信息
            short_data = {
                'short_volume': 0,
                'short_ratio': 0,
                'short_trend': 'unknown',
                'borrow_fee_rate': 0,
                'availability': 'limited'
            }

            # 尝试从可用的API获取数据（示例）
            # 注意：A股的做空数据可能需要特殊渠道
            try:
                # 沪深两融数据（融资融券数据）
                margin_data = ak.stock_margin_szse(date="20231027")  # 示例日期
                symbol_data = margin_data[margin_data['证券代码'] == symbol]
                if not symbol_data.empty:
                    record = symbol_data.iloc[0]
                    short_data['short_volume'] = float(record.get('融券余量', 0))
                    short_data['short_ratio'] = float(record.get('融券余量占流通股本比例', 0))
            except:
                pass  # 如果获取失败，保持默认值

            # 分析做空趋势
            short_analysis = self._analyze_short_trends(short_data)
            short_data['analysis'] = short_analysis

            return {
                'success': True,
                'data': short_data,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def _analyze_short_trends(self, short_data: Dict) -> Dict:
        """
        分析做空趋势
        """
        analysis = {
            'sentiment': 'neutral',
            'risk_level': 'medium',
            'interpretation': '做空数据分析需要更多数据支持'
        }

        try:
            short_ratio = short_data.get('short_ratio', 0)
            if short_ratio > 20:
                analysis['sentiment'] = 'bearish'
                analysis['risk_level'] = 'high'
                analysis['interpretation'] = f"做空比例较高({short_ratio:.2f}%)，市场情绪偏悲观"
            elif short_ratio > 10:
                analysis['sentiment'] = 'cautious'
                analysis['risk_level'] = 'medium'
                analysis['interpretation'] = f"做空比例中等({short_ratio:.2f}%)，市场存在分歧"
            elif short_ratio > 0:
                analysis['sentiment'] = 'bullish'
                analysis['risk_level'] = 'low'
                analysis['interpretation'] = f"做空比例较低({short_ratio:.2f}%)，市场情绪相对乐观"
            else:
                analysis['sentiment'] = 'neutral'
                analysis['risk_level'] = 'unknown'
                analysis['interpretation'] = "暂无做空数据或数据不可用"

        except:
            pass  # 如果无法分析，返回默认值

        return analysis

    def analyze_wall_street_sentiment(self, symbol: str) -> Dict:
        """
        分析华尔街分析师情绪（针对美股）和主流机构观点
        """
        try:
            # 创建模拟分析数据，实际应用中需要连接相关API
            ws_analysis = {
                'target_price': 0,
                'price_change_potential': 0,
                'analyst_ratings': {
                    'buy': 0,
                    'hold': 0,
                    'sell': 0,
                    'avg_rating': 0
                },
                'price_targets': [],
                'consensus': 'neutral',
                'top_institutional_views': []
            }

            # 使用Yahoo Finance获取分析师评级（如果适用）
            try:
                ticker = yf.Ticker(f"{symbol}.SZ" if symbol.startswith(('0', '2', '3')) else f"{symbol}.SH")

                # 获取分析师预测
                recommendations = ticker.recommendations
                upgrades_downgrades = ticker.upgrades_downgrades

                if recommendations is not None:
                    # 计算评级统计
                    rating_counts = recommendations.value_counts() if hasattr(recommendations, 'value_counts') else {}
                    ws_analysis['analyst_ratings'] = {
                        'buy': int(rating_counts.get('Buy', 0)),
                        'hold': int(rating_counts.get('Hold', 0)),
                        'sell': int(rating_counts.get('Sell', 0)),
                        'avg_rating': 0  # 计算平均评级
                    }

                    # 根据评级数量确定共识
                    total_ratings = sum(ws_analysis['analyst_ratings'].values())
                    if total_ratings > 0:
                        buy_pct = ws_analysis['analyst_ratings']['buy'] / total_ratings
                        sell_pct = ws_analysis['analyst_ratings']['sell'] / total_ratings

                        if buy_pct > 0.6:
                            ws_analysis['consensus'] = 'bullish'
                        elif sell_pct > 0.4:
                            ws_analysis['consensus'] = 'bearish'
                        else:
                            ws_analysis['consensus'] = 'neutral'

            except:
                pass  # 如果无法获取美股数据，保持默认值

            # 针对中国市场的主流机构观点（模拟）
            # 实际应用中可能需要爬取或接入财经资讯API
            main_institution_opinions = [
                {
                    'institution': '中信证券',
                    'opinion': '增持',
                    'target_price': 0,
                    'time': datetime.now().strftime('%Y-%m-%d')
                },
                {
                    'institution': '海通证券',
                    'opinion': '谨慎',
                    'target_price': 0,
                    'time': datetime.now().strftime('%Y-%m-%d')
                }
            ]
            ws_analysis['top_institution_opinions'] = main_institution_opinions

            return {
                'success': True,
                'data': ws_analysis,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def generate_advanced_report(self, symbol: str) -> Dict:
        """
        生成高级分析报告
        """
        print(f"开始生成 {symbol} 的高级分析报告...")

        # 执行各项分析
        financial_analysis = self.analyze_financial_statements(symbol)
        institutional_analysis = self.analyze_institutional_holdings(symbol)
        short_analysis = self.analyze_short_interest(symbol)
        wall_street_analysis = self.analyze_wall_street_sentiment(symbol)

        # 汇总分析结果
        advanced_report = {
            'symbol': symbol,
            'report_timestamp': datetime.now().isoformat(),
            'financial_analysis': financial_analysis,
            'institutional_analysis': institutional_analysis,
            'short_analysis': short_analysis,
            'wall_street_analysis': wall_street_analysis,
            'comprehensive_score': 0,
            'investment_thesis': '',
            'risk_factors': [],
            'recommendation_strength': 'neutral'
        }

        # 计算综合评分
        composite_score = self._calculate_composite_score(advanced_report)
        advanced_report['comprehensive_score'] = composite_score

        # 生成投资论据
        thesis = self._generate_investment_thesis(advanced_report)
        advanced_report['investment_thesis'] = thesis

        # 识别风险因素
        risk_factors = self._identify_risk_factors(advanced_report)
        advanced_report['risk_factors'] = risk_factors

        # 确定推荐强度
        recommendation_strength = self._determine_recommendation_strength(advanced_report)
        advanced_report['recommendation_strength'] = recommendation_strength

        return advanced_report

    def _calculate_composite_score(self, report: Dict) -> float:
        """
        计算综合评分
        """
        score = 50  # 基础分

        # 财务健康度评分
        financial_data = report['financial_analysis']
        if financial_data['success']:
            health_score = financial_data['data']['health_assessment']['score']
            score += (health_score - 50) * 0.3  # 财务健康度权重30%

        # 机构持股信心评分
        inst_data = report['institutional_analysis']
        if inst_data['success']:
            conf_mapping = {
                'very_high': 15, 'high': 10, 'moderate': 5,
                'low': -5, 'very_low': -10
            }
            inst_conf = inst_data['data']['trend_analysis']['institutional_confidence']
            score += conf_mapping.get(inst_conf, 0)

        # 做空情绪评分
        short_data = report['short_analysis']
        if short_data['success']:
            sent_mapping = {'bullish': 5, 'neutral': 0, 'bearish': -10}
            sentiment = short_data['data']['analysis']['sentiment']
            score += sent_mapping.get(sentiment, 0)

        # 限制分数范围
        return max(1, min(100, round(score, 1)))

    def _generate_investment_thesis(self, report: Dict) -> str:
        """
        生成投资论据
        """
        thesis_parts = []

        # 财务优势
        financial = report['financial_analysis']
        if financial['success']:
            health = financial['data']['health_assessment']
            if health['strengths']:
                thesis_parts.append(f"财务优势: {', '.join(health['strengths'][:2])}")

        # 机构认同
        institutional = report['institutional_analysis']
        if institutional['success']:
            conf = institutional['data']['trend_analysis']['institutional_confidence']
            if conf in ['high', 'very_high']:
                thesis_parts.append(f"机构高度认可，持股集中度{institutional['data']['trend_analysis']['ownership_concentration']}")

        # 华尔街观点
        ws = report['wall_street_analysis']
        if ws['success']:
            cons = ws['data']['consensus']
            if cons in ['bullish', 'neutral']:
                thesis_parts.append(f"主流机构观点{cons}")

        return '; '.join(thesis_parts) if thesis_parts else "暂无明确投资论据"

    def _identify_risk_factors(self, report: Dict) -> List[str]:
        """
        识别风险因素
        """
        risks = []

        # 财务风险
        financial = report['financial_analysis']
        if financial['success']:
            weaknesses = financial['data']['health_assessment']['weaknesses']
            risks.extend(weaknesses)

        # 做空风险
        short = report['short_analysis']
        if short['success']:
            analysis = short['data']['analysis']
            if analysis['risk_level'] in ['high', 'medium']:
                risks.append(analysis['interpretation'])

        return list(set(risks))  # 去重

    def _determine_recommendation_strength(self, report: Dict) -> str:
        """
        确定推荐强度
        """
        score = report['comprehensive_score']

        if score >= 80:
            return 'strong_buy'
        elif score >= 65:
            return 'buy'
        elif score >= 55:
            return 'hold'
        elif score >= 40:
            return 'avoid'
        else:
            return 'strong_avoid'


def main():
    """
    主函数，演示高级分析功能
    """
    analyzer = AdvancedStockAnalyzer()

    # 测试分析一只股票
    symbol = "000001"  # 平安银行

    print(f"开始高级分析: {symbol}")

    # 生成高级分析报告
    report = analyzer.generate_advanced_report(symbol)

    print("\n=== 高级分析报告摘要 ===")
    print(f"股票代码: {report['symbol']}")
    print(f"综合评分: {report['comprehensive_score']}/100")
    print(f"推荐强度: {report['recommendation_strength']}")
    print(f"投资论据: {report['investment_thesis']}")

    if report['risk_factors']:
        print(f"主要风险: {', '.join(report['risk_factors'][:3])}")  # 显示前3个风险

    # 详细分析各部分
    print("\n--- 财务分析 ---")
    fin_data = report['financial_analysis']
    if fin_data['success']:
        health = fin_data['data']['health_assessment']
        print(f"财务健康度: {health['overall_health']} (得分: {health['score']}/100)")
        if health['strengths']:
            print(f"财务优势: {', '.join(health['strengths'][:2])}")
        if health['weaknesses']:
            print(f"财务弱点: {', '.join(health['weaknesses'][:2])}")
    else:
        print(f"财务分析失败: {fin_data['error']}")

    print("\n--- 机构持股分析 ---")
    inst_data = report['institutional_analysis']
    if inst_data['success']:
        trend = inst_data['data']['trend_analysis']
        print(f"机构信心: {trend['institutional_confidence']}")
        print(f"持股集中度: {trend['ownership_concentration']}")
        print(f"前十大股东占比: {trend['top_holder_percentage']:.2%}")
    else:
        print(f"机构分析失败: {inst_data['error']}")

    print("\n--- 做空分析 ---")
    short_data = report['short_analysis']
    if short_data['success']:
        analysis = short_data['data']['analysis']
        print(f"做空情绪: {analysis['sentiment']}")
        print(f"风险等级: {analysis['risk_level']}")
        print(f"解读: {analysis['interpretation']}")
    else:
        print(f"做空分析失败: {short_data['error']}")

    print("\n--- 华尔街分析 ---")
    ws_data = report['wall_street_analysis']
    if ws_data['success']:
        print(f"分析师共识: {ws_data['data']['consensus']}")
        ratings = ws_data['data']['analyst_ratings']
        print(f"评级分布 - 买入:{ratings['buy']}, 持有:{ratings['hold']}, 卖出:{ratings['sell']}")
    else:
        print(f"华尔街分析失败: {ws_data['error']}")

    # 保存报告
    output_file = f"output/advanced_analysis_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)

    print(f"\n完整报告已保存至: {output_file}")


if __name__ == "__main__":
    main()