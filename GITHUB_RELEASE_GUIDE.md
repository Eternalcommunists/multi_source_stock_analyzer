# GitHub发布指南

## 如何将项目发布到GitHub

### 1. 创建GitHub仓库
1. 登录GitHub账户
2. 点击"New repository"按钮
3. 输入仓库名称：`multi-source-stock-analyzer`
4. 添加描述："A comprehensive stock analysis system utilizing multiple data sources including Tong Hua Shun iFinD, East Money API, akshare, and jqdatasdk"
5. 选择"Public"（或"Private"）
6. 不要勾选"Initialize this repository with a README"
7. 点击"Create repository"

### 2. 获取仓库URL
创建仓库后，复制HTTPS URL，格式类似：
```
https://github.com/YOUR_USERNAME/multi-source-stock-analyzer.git
```

### 3. 配置本地仓库
```bash
# 导航到项目目录
cd "d:\Codex\multi_source_stock_analyzer"

# 如果尚未初始化Git
git init

# 添加所有文件
git add .

# 提交更改
git commit -m "Initial commit: Multi-source stock analysis system with akshare, East Money API, Tong Hua Shun iFinD, and jqdatasdk support"

# 重命名主分支为main
git branch -M main

# 添加远程仓库（请将URL替换为您自己的仓库URL）
git remote add origin https://github.com/YOUR_USERNAME/multi-source-stock-analyzer.git

# 推送代码到GitHub
git push -u origin main
```

### 4. 验证发布
访问您的GitHub仓库页面，确认所有文件都已成功上传。

## 项目结构说明

```
multi-source-stock-analyzer/
├── frontend/                 # 前端代码 (React + TypeScript)
│   ├── public/              # 静态资源
│   ├── src/                 # 源代码
│   │   ├── components/      # React组件
│   │   ├── services/        # 业务逻辑
│   │   ├── types/           # TypeScript类型定义
│   │   └── styles/          # 样式文件
│   ├── package.json         # 前端依赖配置
│   └── ...
├── backend/                  # 后端代码 (Python)
│   ├── core_analyzer.py     # 核心分析器
│   ├── data_adapter.py      # 数据适配器
│   ├── html_generator.py    # HTML报告生成器
│   ├── main.py              # 主程序入口
│   └── requirements.txt     # Python依赖
├── data-sources/             # 数据源集成模块
├── docs/                     # 项目文档
├── .github/                  # GitHub配置
│   └── workflows/           # CI/CD工作流
├── output/                   # 分析结果输出目录
├── README.md                 # 项目说明
├── LICENSE                   # 许可证
├── Dockerfile               # Docker配置
├── docker-compose.yml       # Docker Compose配置
└── package.json             # 项目根配置
```

## 功能特性

### 数据源支持
- **akshare**: 开源财经数据包（已实现）
- **东方财富API**: A股市场数据（预留接口）
- **同花顺iFinD**: 专业金融数据服务（预留接口）
- **聚宽数据**: 量化交易平台数据（预留接口）

### 分析能力
- **技术分析**: 趋势、动量、支撑压力、技术指标（MA、RSI、MACD等）
- **基本面分析**: 估值、财务健康度、增长潜力
- **风险评估**: 市场、估值、流动性、技术面风险
- **综合评分**: 1-10分制投资评分系统

### 可视化展示
- **响应式UI**: 支持桌面和移动端访问
- **交互图表**: K线图、技术指标图
- **综合看板**: 技术面、基本面、风险评估一体化展示
- **HTML报告**: 自动生成详细分析报告

## 安装和使用

### 前端设置
```bash
cd frontend
npm install
npm start
```

### 后端设置
```bash
cd backend
pip install -r requirements.txt
python main.py --symbol 002490 --sources akshare
```

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 贡献

欢迎提交Issue和Pull Request来帮助改进系统。

## 支持

如有问题，请提交Issue或发送邮件至 [your-email@example.com](mailto:your-email@example.com)

---

© 2026 多数据源股票分析系统. 仅供学习和研究使用，不构成投资建议.