# API参考文档

## 概述

多数据源股票分析系统提供了一套RESTful API，用于获取股票数据、技术指标和分析结果。

## 基础URL

```
https://api.stock-analyzer.com/v1
```

## 认证

大多数API端点需要API密钥进行认证。请在请求头中包含：

```
Authorization: Bearer YOUR_API_KEY
```

## 错误处理

API使用HTTP状态码来表示请求的成功或失败：

- `200 OK` - 请求成功
- `400 Bad Request` - 请求格式错误或参数无效
- `401 Unauthorized` - 缺少或无效的认证
- `404 Not Found` - 请求的资源不存在
- `500 Internal Server Error` - 服务器内部错误

## API端点

### 获取股票基本信息

```
GET /stocks/{symbol}
```

获取指定股票的基本信息。

**参数：**

- `symbol` (路径参数): 股票代码，例如 "000001"

**响应示例：**

```json
{
  "symbol": "000001",
  "name": "平安银行",
  "exchange": "SZSE",
  "currency": "CNY",
  "last_updated": "2023-06-11T15:00:00Z"
}
```

### 获取实时报价

```
GET /stocks/{symbol}/quote
```

获取指定股票的实时报价数据。

**参数：**

- `symbol` (路径参数): 股票代码
- `source` (查询参数, 可选): 数据源，可选值: "akshare", "eastmoney", "ifind", "jqdata" (默认: "akshare")

**响应示例：**

```json
{
  "symbol": "000001",
  "current_price": 15.23,
  "change_amount": 0.45,
  "change_percent": 3.04,
  "volume": 25678900,
  "turnover": 389234567,
  "open": 14.98,
  "high": 15.35,
  "low": 14.92,
  "prev_close": 14.78,
  "pe_ttm": 8.23,
  "pb": 0.85,
  "data_source": "akshare",
  "timestamp": "2023-06-11T14:45:30Z"
}
```

### 获取历史K线数据

```
GET /stocks/{symbol}/history
```

获取指定股票的历史K线数据。

**参数：**

- `symbol` (路径参数): 股票代码
- `period` (查询参数, 可选): 时间周期，可选值: "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "max" (默认: "1mo")
- `interval` (查询参数, 可选): K线间隔，可选值: "1m", "5m", "15m", "30m", "1h", "1d", "1wk", "1mo" (默认: "1d")
- `source` (查询参数, 可选): 数据源 (默认: "akshare")

**响应示例：**

```json
{
  "symbol": "000001",
  "period": "1mo",
  "interval": "1d",
  "data_source": "akshare",
  "kline_data": [
    {
      "date": "2023-05-11",
      "open": 14.85,
      "high": 15.12,
      "low": 14.75,
      "close": 15.05,
      "volume": 18765432,
      "turnover": 280456789
    },
    {
      "date": "2023-05-12",
      "open": 15.05,
      "high": 15.30,
      "low": 14.95,
      "close": 15.25,
      "volume": 21098765,
      "turnover": 320123456
    }
  ]
}
```

### 获取技术指标

```
GET /stocks/{symbol}/indicators
```

获取指定股票的技术指标。

**参数：**

- `symbol` (路径参数): 股票代码
- `indicators` (查询参数, 可选): 技术指标列表，逗号分隔，如 "ma,rsi,macd,boll" (默认: "all")
- `source` (查询参数, 可选): 数据源 (默认: "akshare")

**响应示例：**

```json
{
  "symbol": "000001",
  "data_source": "akshare",
  "indicators": {
    "ma": {
      "ma5": 15.12,
      "ma10": 14.98,
      "ma20": 14.75
    },
    "rsi": {
      "rsi6": 62.34,
      "rsi14": 58.21
    },
    "macd": {
      "dif": 0.23,
      "dea": 0.18,
      "macd": 0.05
    },
    "boll": {
      "upper": 16.25,
      "mid": 15.20,
      "lower": 14.15
    }
  },
  "timestamp": "2023-06-11T14:45:30Z"
}
```

### 获取综合分析

```
GET /stocks/{symbol}/analysis
```

获取指定股票的综合分析报告。

**参数：**

- `symbol` (路径参数): 股票代码
- `sources` (查询参数, 可选): 数据源列表，逗号分隔，如 "akshare,eastmoney" (默认: "akshare")
- `include_comparison` (查询参数, 可选): 是否包含多源数据对比 (默认: false)

**响应示例：**

```json
{
  "symbol": "000001",
  "analysis": {
    "investment_rating": 7.5,
    "technical_analysis": {
      "trend": "bullish",
      "momentum": "moderate",
      "support_resistance": {
        "support": 14.50,
        "resistance": 16.00
      },
      "indicators": {
        "ma5": 15.12,
        "ma20": 14.75,
        "rsi": 58.21,
        "macd": 0.05
      }
    },
    "fundamental_analysis": {
      "valuation": "fair_value",
      "financial_health": "strong",
      "growth_potential": "moderate"
    },
    "risk_assessment": {
      "market_risk": "medium",
      "valuation_risk": "low",
      "liquidity_risk": "low",
      "technical_risk": "medium",
      "overall_risk": "medium"
    },
    "recommendation": "建议关注，技术面和基本面均表现良好，适合中长期投资",
    "data_quality_score": 8.5
  },
  "data_sources_used": ["akshare"],
  "analysis_timestamp": "2023-06-11T14:45:30Z"
}
```

### 获取同行对比

```
GET /stocks/{symbol}/compare
```

获取与指定股票相似的同行股票对比。

**参数：**

- `symbol` (路径参数): 股票代码
- `count` (查询参数, 可选): 返回股票数量 (默认: 5, 最大: 10)
- `source` (查询参数, 可选): 数据源 (默认: "akshare")

**响应示例：**

```json
{
  "reference_symbol": "000001",
  "comparison_stocks": [
    {
      "symbol": "601328",
      "name": "交通银行",
      "current_price": 5.23,
      "change_percent": 1.23,
      "pe_ttm": 4.85,
      "pb": 0.45,
      "market_cap": 2345.67
    },
    {
      "symbol": "601939",
      "name": "建设银行",
      "current_price": 6.15,
      "change_percent": 0.85,
      "pe_ttm": 4.92,
      "pb": 0.52,
      "market_cap": 2567.89
    }
  ],
  "data_source": "akshare",
  "timestamp": "2023-06-11T14:45:30Z"
}
```

## 速率限制

API对每个IP地址实施以下速率限制：

- 每分钟最多 100 个请求
- 每小时最多 1000 个请求

超出限制的请求将返回 `429 Too Many Requests` 状态码。

## 数据更新频率

- 实时报价: 每5秒更新一次
- K线数据: 每分钟更新一次（分钟线），每日更新一次（日线）
- 技术指标: 每5分钟更新一次
- 综合分析: 每15分钟更新一次
- 同行对比: 每小时更新一次