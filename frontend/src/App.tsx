import React, { useState } from 'react';
import { MultiSourceAnalyzer } from './services/MultiSourceAnalyzer';
import { StockData } from './types/stock';
import { StockDataDisplay } from './components/StockDataDisplay';
import { StockSearch } from './components/StockSearch';

const App: React.FC = () => {
  const [stockData, setStockData] = useState<StockData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const analyzer = new MultiSourceAnalyzer();

  const handleSearch = async (symbol: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await analyzer.analyze(symbol);
      if (result.success && result.data) {
        setStockData(result.data);
      } else {
        setError(result.error || '分析失败');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '未知错误');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">多数据源股票分析系统</h1>
          <p className="mt-2 text-gray-600">整合同花顺iFinD、东方财富API、akshare等多数据源的智能股票分析平台</p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <StockSearch onSearch={handleSearch} loading={loading} />
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
            <p className="text-red-800">{error}</p>
          </div>
        )}

        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        ) : (
          <StockDataDisplay data={stockData} />
        )}
      </main>

      <footer className="bg-white mt-12 border-t">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <p className="text-center text-gray-500 text-sm">
            © {new Date().getFullYear()} 多数据源股票分析系统. 仅供学习和研究使用，不构成投资建议.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default App;