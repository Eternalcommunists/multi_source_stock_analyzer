// src/components/StockDataDisplay.tsx
import React from 'react';
import { StockData } from '../types/stock';

interface StockDataDisplayProps {
  data: StockData | null;
}

export const StockDataDisplay: React.FC<StockDataDisplayProps> = ({ data }) => {
  if (!data) {
    return (
      <div className="text-center py-12">
        <div className="bg-white rounded-xl shadow-md p-8 max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">股票数据分析看板</h2>
          <p className="text-gray-600 mb-6">
            欢迎使用多数据源股票分析系统！请输入股票代码以获取详细分析报告。
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
            <div className="bg-blue-50 p-4 rounded-lg">
              <h3 className="font-semibold text-blue-800">技术分析</h3>
              <p className="text-sm text-blue-600">趋势、支撑压力、技术指标</p>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <h3 className="font-semibold text-green-800">基本面分析</h3>
              <p className="text-sm text-green-600">财务状况、估值分析</p>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <h3 className="font-semibold text-purple-800">风险评估</h3>
              <p className="text-sm text-purple-600">市场、估值、流动性风险</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const isPositive = data.quote.change_percent >= 0;
  const changeColor = isPositive ? 'text-green-600' : 'text-red-600';
  const changeSign = isPositive ? '+' : '';

  return (
    <div className="space-y-6">
      {/* 股票基本信息 */}
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="p-6 border-b border-gray-200">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">{data.symbol} - {data.name}</h2>
              <p className="text-gray-600 mt-1">实时数据分析报告</p>
            </div>
            <div className="mt-4 md:mt-0 text-right">
              <div className="text-3xl font-bold text-gray-900">¥{data.quote.current_price.toFixed(2)}</div>
              <div className={`${changeColor} text-lg font-semibold`}>
                {changeSign}{data.quote.change_percent.toFixed(2)}%
              </div>
            </div>
          </div>
        </div>
        
        {/* 关键指标 */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-6 bg-gray-50">
          <div className="text-center">
            <div className="text-sm text-gray-500">成交量</div>
            <div className="text-lg font-semibold text-gray-900">
              {(data.quote.volume / 1000000).toFixed(2)}M
            </div>
          </div>
          <div className="text-center">
            <div className="text-sm text-gray-500">市盈率(TTM)</div>
            <div className="text-lg font-semibold text-gray-900">
              {data.quote.pe_ttm ? data.quote.pe_ttm.toFixed(2) : 'N/A'}
            </div>
          </div>
          <div className="text-center">
            <div className="text-sm text-gray-500">市净率</div>
            <div className="text-lg font-semibold text-gray-900">
              {data.quote.pb ? data.quote.pb.toFixed(2) : 'N/A'}
            </div>
          </div>
          <div className="text-center">
            <div className="text-sm text-gray-500">投资评分</div>
            <div className="text-lg font-semibold text-blue-600">
              {data.analysis.investment_rating ? data.analysis.investment_rating.toFixed(1) : 'N/A'}/10
            </div>
          </div>
        </div>
      </div>

      {/* 综合分析 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 技术分析 */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <svg className="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
            技术分析
          </h3>
          
          <div className="space-y-4">
            <div className="flex justify-between">
              <span className="text-gray-600">趋势</span>
              <span className="font-medium">{data.analysis.technical_analysis.trend}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">动量</span>
              <span className="font-medium">{data.analysis.technical_analysis.momentum}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">支撑位</span>
              <span className="font-medium">
                ¥{data.analysis.technical_analysis.support_resistance.support.toFixed(2)}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">压力位</span>
              <span className="font-medium">
                ¥{data.analysis.technical_analysis.support_resistance.resistance.toFixed(2)}
              </span>
            </div>
          </div>
        </div>

        {/* 基本面分析 */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <svg className="w-5 h-5 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2m0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
            基本面分析
          </h3>
          
          <div className="space-y-4">
            <div className="flex justify-between">
              <span className="text-gray-600">估值状态</span>
              <span className="font-medium">{data.analysis.fundamental_analysis.valuation}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">财务健康度</span>
              <span className="font-medium">{data.analysis.fundamental_analysis.financial_health}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">增长潜力</span>
              <span className="font-medium">{data.analysis.fundamental_analysis.growth_potential}</span>
            </div>
          </div>
        </div>
      </div>

      {/* 风险评估和投资建议 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 风险评估 */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <svg className="w-5 h-5 mr-2 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
            </svg>
            风险评估
          </h3>
          
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">市场风险</span>
              <span className={`font-medium ${
                data.analysis.risk_assessment.market_risk === 'high' ? 'text-red-600' :
                data.analysis.risk_assessment.market_risk === 'medium' ? 'text-yellow-600' : 'text-green-600'
              }`}>
                {data.analysis.risk_assessment.market_risk}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">估值风险</span>
              <span className={`font-medium ${
                data.analysis.risk_assessment.valuation_risk === 'high' ? 'text-red-600' :
                data.analysis.risk_assessment.valuation_risk === 'medium' ? 'text-yellow-600' : 'text-green-600'
              }`}>
                {data.analysis.risk_assessment.valuation_risk}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">流动性风险</span>
              <span className={`font-medium ${
                data.analysis.risk_assessment.liquidity_risk === 'high' ? 'text-red-600' :
                data.analysis.risk_assessment.liquidity_risk === 'medium' ? 'text-yellow-600' : 'text-green-600'
              }`}>
                {data.analysis.risk_assessment.liquidity_risk}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">技术面风险</span>
              <span className={`font-medium ${
                data.analysis.risk_assessment.technical_risk === 'high' ? 'text-red-600' :
                data.analysis.risk_assessment.technical_risk === 'medium' ? 'text-yellow-600' : 'text-green-600'
              }`}>
                {data.analysis.risk_assessment.technical_risk}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">综合风险</span>
              <span className={`font-medium ${
                data.analysis.risk_assessment.overall_risk === 'high' ? 'text-red-600' :
                data.analysis.risk_assessment.overall_risk === 'medium' ? 'text-yellow-600' : 'text-green-600'
              }`}>
                {data.analysis.risk_assessment.overall_risk}
              </span>
            </div>
          </div>
        </div>

        {/* 投资建议 */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <svg className="w-5 h-5 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
            </svg>
            投资建议
          </h3>
          
          <div>
            <div className="text-lg font-semibold text-gray-900 mb-2">综合评级</div>
            <div className="text-3xl font-bold text-indigo-600 mb-4">
              {data.analysis.investment_rating ? data.analysis.investment_rating.toFixed(1) : 'N/A'}/10
            </div>
            <p className="text-gray-700 bg-blue-50 p-4 rounded-lg">
              <strong>建议:</strong> {data.analysis.recommendation}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};