# 多数据源股票分析系统

一个强大的多数据源股票分析平台，整合同花顺iFinD、东方财富API、akshare和jqdatasdk等多个数据提供商，为用户提供全面的股票分析服务。

## 项目简介

本项目是一个综合性的股票分析系统，利用多个金融数据API，提供实时数据分析、可视化图表和智能投资建议。系统采用现代化架构，支持多种数据源，并提供直观的用户界面。

## 功能特性

### 数据源支持
- ✅ **akshare**: 开源财经数据包（已实现）
- 🔄 **东方财富API**: A股市场数据（预留接口）
- 🔄 **同花顺iFinD**: 专业金融数据服务（预留接口）
- 🔄 **聚宽数据**: 量化交易平台数据（预留接口）

### 分析能力
- 📊 **技术分析**: 趋势、动量、支撑压力、技术指标（MA、RSI、MACD等）
- 💰 **基本面分析**: 估值、财务健康度、增长潜力
- ⚠️ **风险评估**: 市场、估值、流动性、技术面风险
- 📈 **综合评分**: 1-10分制投资评分系统

### 用户体验
- 🎨 **响应式UI**: 支持桌面和移动端访问
- 📉 **交互图表**: K线图、技术指标图
- 📋 **综合看板**: 技术面、基本面、风险评估一体化展示
- 📄 **HTML报告**: 自动生成详细分析报告

## 技术架构

### 前端技术栈
- **React 18**: 现代化UI框架
- **TypeScript**: 类型安全
- **Tailwind CSS**: 样式框架
- **Chart.js/Recharts**: 数据可视化

### 后端技术栈
- **Python**: 核心分析引擎
- **akshare**: 数据获取
- **pandas**: 数据处理
- **Flask/FastAPI**: API服务（预留）

## 安装指南

### 环境要求
- Node.js 16+
- Python 3.8+
- npm 或 yarn

### 前端设置
```bash
# 克隆仓库
git clone https://github.com/yourusername/multi-source-stock-analyzer.git
cd multi-source-stock-analyzer

# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm start
```

### 后端设置
```bash
# 进入后端目录
cd backend

# 安装Python依赖
pip install -r requirements.txt

# 运行分析系统
python main.py --symbol 002490 --sources akshare
```

## 使用方法

### 命令行使用
```bash
# 分析单个股票
python backend/main.py --symbol 002490 --sources akshare

# 指定输出格式
python backend/main.py --symbol 002490 --sources akshare --output-format both

# 指定输出目录
python backend/main.py --symbol 002490 --sources akshare --output-dir ./reports
```

### Web界面使用
1. 启动前端服务器
2. 启动后端API服务
3. 访问 http://localhost:3000
4. 输入股票代码（如 002490）进行分析

## 项目结构

```
multi-source-stock-analyzer/
├── frontend/                 # 前端代码 (React + TypeScript)
│   ├── public/               # 静态资源
│   ├── src/
│   │   ├── components/       # React组件
│   │   ├── services/         # 业务逻辑
│   │   ├── types/           # TypeScript类型定义
│   │   └── styles/          # 样式文件
│   ├── package.json
│   └── ...
├── backend/                  # 后端代码 (Python)
│   ├── core_analyzer.py      # 核心分析器
│   ├── data_adapter.py       # 数据适配器
│   ├── html_generator.py     # HTML报告生成器
│   ├── main.py               # 主程序入口
│   └── requirements.txt      # Python依赖
├── docs/                     # 项目文档
├── .github/                  # GitHub配置
│   └── workflows/            # CI/CD工作流
├── Dockerfile                # Docker配置
├── docker-compose.yml        # 容器编排配置
├── README.md                 # 项目说明
└── LICENSE                   # 许可证
```

## 实际案例分析

系统已成功对山东墨龙(002490)进行了分析：

- **当前价格**: ¥8.81
- **涨跌幅**: +2.92%
- **市盈率(TTM)**: 314.7
- **市净率**: 13.95
- **投资评分**: 4.2/10
- **风险等级**: 中等

分析显示该股票估值偏高，波动较大，投资评分较低，系统建议以观望为主。

## 扩展性设计

系统采用模块化设计，易于扩展：

1. **新增数据源**: 实现DataSourceAdapter接口
2. **添加分析指标**: 扩展AnalysisEngine类
3. **自定义报告模板**: 修改HTML生成器

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进系统：

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 支持

如有问题，请提交Issue或发送邮件至 [1186036686@qq.com](mailto:1186036686@qq.com)

## 致谢

- akshare: 提供开源财经数据
- React: 提供现代化UI框架
- 以及其他开源库和工具的贡献者

---

© 2026 多数据源股票分析系统. 仅供学习和研究使用，不构成投资建议.
