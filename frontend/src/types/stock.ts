// src/types/stock.ts

// 股票基本数据接口
export interface StockData {
  symbol: string;              // 股票代码
  name: string;                // 股票名称
  quote: QuoteData;            // 报价数据
  kline: KLineData[];          // K线数据
  analysis: AnalysisData;      // 分析数据
  data_sources: string[];      // 数据来源
  last_updated: string;        // 最后更新时间
}

// 报价数据接口
export interface QuoteData {
  current_price: number;       // 当前价格
  change_amount: number;       // 涨跌额
  change_percent: number;      // 涨跌幅
  volume: number;              // 成交量
  turnover: number;            // 成交额
  open: number;                // 开盘价
  high: number;                // 最高价
  low: number;                 // 最低价
  prev_close: number;          // 昨收价
  pe_ttm: number;              // 市盈率(TTM)
  pb: number;                  // 市净率
}

// K线数据接口
export interface KLineData {
  date: string;                // 日期
  open: number;                // 开盘价
  high: number;                // 最高价
  low: number;                 // 最低价
  close: number;               // 收盘价
  volume: number;              // 成交量
}

// 技术指标接口
export interface TechnicalIndicators {
  ma5: number;                 // 5日均线
  ma20: number;                // 20日均线
  ma60: number;                // 60日均线
  rsi: number;                 // RSI指标
  macd: number;                // MACD指标
  boll_upper: number;          // 布林带上轨
  boll_lower: number;          // 布林带下轨
}

// 技术分析接口
export interface TechnicalAnalysis {
  trend: 'bullish' | 'bearish' | 'neutral';  // 趋势
  momentum: 'strong' | 'moderate' | 'weak' | 'neutral';  // 动量
  support_resistance: {
    support: number;           // 支撑位
    resistance: number;        // 压力位
  };
  indicators: TechnicalIndicators;  // 技术指标
}

// 基本面分析接口
export interface FundamentalAnalysis {
  valuation: 'overvalued' | 'fair_value' | 'undervalued' | 'invalid_data';  // 估值状态
  financial_health: 'strong' | 'stable' | 'weak' | 'unknown';  // 财务健康度
  growth_potential: 'high' | 'moderate' | 'low' | 'unknown';  // 增长潜力
}

// 风险评估接口
export interface RiskAssessment {
  market_risk: 'high' | 'medium' | 'low';      // 市场风险
  valuation_risk: 'high' | 'medium' | 'low';   // 估值风险
  liquidity_risk: 'high' | 'medium' | 'low';   // 流动性风险
  technical_risk: 'high' | 'medium' | 'low';   // 技术面风险
  overall_risk: 'high' | 'medium' | 'low';     // 综合风险
}

// 分析数据接口
export interface AnalysisData {
  investment_rating: number;           // 投资评分 (1-10)
  technical_analysis: TechnicalAnalysis;  // 技术分析
  fundamental_analysis: FundamentalAnalysis;  // 基本面分析
  risk_assessment: RiskAssessment;     // 风险评估
  recommendation: string;              // 投资建议
}

// 分析结果接口
export interface AnalysisResult {
  symbol: string;                      // 股票代码
  success: boolean;                    // 是否成功
  data: StockData | null;              // 分析数据
  error?: string;                      // 错误信息
  data_source_used: string;            // 使用的数据源
  analysis_timestamp: string;          // 分析时间戳
  multi_source_comparison?: {         // 多源比较信息（可选）
    total_sources: number;
    successful_sources: number;
    all_results: AnalysisResult[];
  };
}