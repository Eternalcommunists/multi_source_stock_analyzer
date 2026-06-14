// src/services/MultiSourceAnalyzer.ts

import { DataSourceAdapter, AkShareAdapter } from './DataSourceAdapter';
import { StockData, AnalysisResult } from '../types/stock';

export class MultiSourceAnalyzer {
  private adapters: Map<string, DataSourceAdapter> = new Map();
  
  constructor() {
    // 注册可用的数据源适配器
    const akshareAdapter = new AkShareAdapter();
    this.adapters.set(akshareAdapter.getName(), akshareAdapter);
  }
  
  /**
   * 使用多个数据源分析股票
   */
  async analyze(symbol: string): Promise<AnalysisResult> {
    const results: AnalysisResult[] = [];
    let bestResult: AnalysisResult | null = null;
    let highestRating = -1;
    
    // 遍历所有数据源进行分析
    for (const [sourceName, adapter] of this.adapters) {
      try {
        console.log(`正在使用 ${sourceName} 数据源分析 ${symbol}...`);
        
        const stockData = await adapter.fetchStockData(symbol);
        
        const result: AnalysisResult = {
          symbol: symbol,
          success: true,
          data: stockData,
          data_source_used: sourceName,
          analysis_timestamp: new Date().toISOString()
        };
        
        results.push(result);
        
        // 选择评分最高的结果
        if (stockData && stockData.analysis && stockData.analysis.investment_rating > highestRating) {
          highestRating = stockData.analysis.investment_rating;
          bestResult = result;
        }
      } catch (error) {
        console.error(`从 ${sourceName} 获取 ${symbol} 数据失败:`, error);
        
        const errorResult: AnalysisResult = {
          symbol: symbol,
          success: false,
          data: null,
          error: error instanceof Error ? error.message : String(error),
          data_source_used: sourceName,
          analysis_timestamp: new Date().toISOString()
        };
        
        results.push(errorResult);
      }
    }
    
    // 如果没有成功的结果，返回第一个错误结果
    if (!bestResult && results.length > 0) {
      bestResult = results[0];
    }
    
    // 如果没有任何结果，返回错误
    if (!bestResult) {
      return {
        symbol: symbol,
        success: false,
        data: null,
        error: '所有数据源都无法获取有效数据',
        data_source_used: 'none',
        analysis_timestamp: new Date().toISOString()
      };
    }
    
    // 添加多源比较信息
    bestResult.multi_source_comparison = {
      total_sources: this.adapters.size,
      successful_sources: results.filter(r => r.success).length,
      all_results: results
    };
    
    return bestResult;
  }
  
  /**
   * 获取所有可用的数据源
   */
  getAvailableSources(): string[] {
    return Array.from(this.adapters.keys());
  }
  
  /**
   * 添加新的数据源适配器
   */
  addDataSource(adapter: DataSourceAdapter): void {
    this.adapters.set(adapter.getName(), adapter);
  }
  
  /**
   * 移除数据源适配器
   */
  removeDataSource(sourceName: string): boolean {
    return this.adapters.delete(sourceName);
  }
}

/**
 * 数据质量评估器
 */
export class DataQualityEvaluator {
  /**
   * 评估数据质量分数 (0-10)
   */
  static evaluateDataQuality(data: StockData | null): number {
    if (!data) {
      return 0; // 无数据，质量为0
    }
    
    let score = 0;
    const maxScore = 10;
    
    // 检查基本数据完整性
    if (data.quote && data.quote.current_price > 0) {
      score += 2; // 当前价格有效
    }
    
    if (data.quote && data.quote.volume > 0) {
      score += 1; // 成交量有效
    }
    
    if (data.quote && data.quote.pe_ttm > 0 && data.quote.pe_ttm < 100) {
      score += 1; // 市盈率在合理范围
    }
    
    // 检查K线数据
    if (data.kline && data.kline.length > 10) {
      score += 2; // 有足够的历史数据
    }
    
    // 检查分析数据
    if (data.analysis) {
      score += 2; // 有分析数据
      
      // 检查评分合理性
      if (data.analysis.investment_rating >= 0 && data.analysis.investment_rating <= 10) {
        score += 1; // 投资评分在有效范围
      }
    }
    
    // 检查数据新鲜度
    if (data.last_updated) {
      const updateTime = new Date(data.last_updated);
      const now = new Date();
      const hoursDiff = (now.getTime() - updateTime.getTime()) / (1000 * 60 * 60);
      
      if (hoursDiff < 24) { // 24小时内更新的数据
        score += 1;
      }
    }
    
    return Math.min(score, maxScore);
  }
  
  /**
   * 评估数据一致性（跨多个源）
   */
  static evaluateConsistency(results: AnalysisResult[]): number {
    if (results.length < 2) {
      return 5; // 只有一个数据源，无法评估一致性
    }
    
    const validResults = results.filter(r => r.success && r.data);
    
    if (validResults.length < 2) {
      return 5; // 只有一个有效结果，无法评估一致性
    }
    
    // 计算价格一致性（如果多个源都返回价格数据）
    const prices = validResults
      .map(r => r.data?.quote?.current_price)
      .filter(p => typeof p === 'number' && p > 0);
    
    if (prices.length < 2) {
      return 5; // 没有足够价格数据来评估一致性
    }
    
    // 计算价格标准差
    const meanPrice = prices.reduce((sum, price) => sum + price, 0) / prices.length;
    const variance = prices.reduce((sum, price) => sum + Math.pow(price - meanPrice, 2), 0) / prices.length;
    const stdDev = Math.sqrt(variance);
    
    // 标准差越小，一致性越高
    // 一致性分数 = 10 - (stdDev / meanPrice) * 100
    const consistencyScore = Math.max(0, 10 - (stdDev / meanPrice) * 100);
    
    return Math.round(consistencyScore * 10) / 10; // 保留一位小数
  }
}