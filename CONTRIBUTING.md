# 贡献指南

感谢您有兴趣为多数据源股票分析系统做出贡献！我们欢迎各种形式的贡献，包括但不限于代码贡献、文档改进、问题报告和功能建议。

## 开发环境设置

1. 克隆仓库
   ```bash
   git clone https://github.com/yourusername/multi-source-stock-analyzer.git
   cd multi-source-stock-analyzer
   ```

2. 安装前端依赖
   ```bash
   cd frontend
   npm install
   ```

3. 安装后端依赖
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

## 分支管理

- `main` - 主分支，用于稳定版本
- `develop` - 开发分支，用于日常开发
- `feature/*` - 功能分支，用于新功能开发
- `bugfix/*` - 修复分支，用于问题修复
- `release/*` - 发布分支，用于版本发布

## 提交规范

请遵循以下提交信息格式：

```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

其中 type 可以是：
- feat: 新功能
- fix: 修复问题
- docs: 文档更新
- style: 代码格式调整
- refactor: 重构
- test: 测试相关
- chore: 构建过程或辅助工具的变动

## 代码风格

### Python
- 遵循 PEP 8 规范
- 使用 black 格式化代码
- 使用 flake8 检查代码质量

### JavaScript/TypeScript
- 遵循 Airbnb JavaScript 规范
- 使用 ESLint 检查代码质量
- 使用 Prettier 格式化代码

## 测试

在提交代码前，请确保所有测试通过：

```bash
# 前端测试
cd frontend
npm test

# 后端测试
cd backend
python -m pytest
```

## 文档

当添加新功能或修改现有功能时，请相应地更新文档。

## 问题报告

报告问题时，请包含以下信息：
- 问题描述
- 重现步骤
- 预期行为
- 实际行为
- 环境信息（操作系统、浏览器、软件版本等）

## 拉取请求

提交拉取请求时：
1. 确保代码通过所有测试
2. 包含适当的测试用例
3. 更新相关文档
4. 遵循代码风格指南
5. 提供清晰的提交信息

## 社区

请遵守我们的《行为准则》，共同营造一个友好的社区环境。

如果您有任何疑问，请随时联系我们。