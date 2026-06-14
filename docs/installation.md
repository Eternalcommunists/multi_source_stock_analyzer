# 安装指南

本指南将帮助您安装和配置多数据源股票分析系统。

## 系统要求

- **操作系统**: Windows 10+, macOS 10.14+, 或 Linux (Ubuntu 18.04+, CentOS 7+)
- **Node.js**: 16.x 或更高版本
- **npm**: 8.x 或更高版本 (或 Yarn 1.22+)
- **Python**: 3.8 或更高版本 (如使用Python后端)
- **内存**: 至少 4GB RAM
- **磁盘空间**: 至少 2GB 可用空间

## 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/stock-analysis-system.git
cd stock-analysis-system
```

### 2. 安装前端依赖

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install
# 或者使用 yarn
yarn install
```

### 3. 安装后端依赖

```bash
# 进入后端目录
cd ../backend

# 安装依赖
npm install
# 或者使用 yarn
yarn install
```

### 4. 配置环境变量

在前端和后端目录中分别创建 `.env` 文件：

**frontend/.env**:
```bash
REACT_APP_API_URL=http://localhost:5000
REACT_APP_DATA_SOURCE=akshare
REACT_APP_REFRESH_INTERVAL=30000  # 30秒刷新一次数据
```

**backend/.env**:
```bash
PORT=5000
NODE_ENV=development
DB_CONNECTION_STRING=mongodb://localhost:27017/stock_analysis
REDIS_URL=redis://localhost:6379
AKSHARE_ENABLED=true
EAST_MONEY_API_KEY=your_east_money_api_key
IFIND_USERNAME=your_ifind_username
IFIND_PASSWORD=your_ifind_password
JQDATA_USERNAME=your_jqdata_username
JQDATA_PASSWORD=your_jqdata_password
```

### 5. 安装Python依赖（如使用Python后端）

```bash
# 进入Python后端目录
cd ../python-backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 6. 启动数据库（如使用）

如果您使用MongoDB作为数据库，请确保MongoDB服务正在运行：

```bash
# Windows (如果使用安装的服务)
net start MongoDB

# macOS (使用Homebrew安装)
brew services start mongodb-community

# Linux
sudo systemctl start mongod
```

### 7. 启动Redis（如使用）

如果您使用Redis作为缓存，请确保Redis服务正在运行：

```bash
# Windows
redis-server

# macOS (使用Homebrew安装)
brew services start redis

# Linux
sudo systemctl start redis
```

## 启动应用

### 开发模式

要同时启动前端和后端进行开发，请打开两个终端窗口：

**终端1 (后端):**
```bash
cd backend
npm run dev
```

**终端2 (前端):**
```bash
cd frontend
npm start
```

### 生产模式

要构建并启动生产版本：

```bash
# 构建前端
cd frontend
npm run build

# 启动后端（假设前端构建产物在backend/public目录下）
cd backend
npm start
```

## 验证安装

1. 打开浏览器并访问 `http://localhost:3000`
2. 您应该看到多数据源股票分析系统的主界面
3. 尝试输入一个股票代码（如 `000001`）并点击"开始分析"
4. 系统应该显示该股票的分析结果

## 常见问题

### 1. 端口已被占用

如果遇到端口占用错误，请修改 `.env` 文件中的端口号：

```bash
# frontend/.env
REACT_APP_API_URL=http://localhost:5001

# backend/.env
PORT=5001
```

### 2. 依赖安装失败

如果遇到依赖安装问题，请尝试：

```bash
# 清理npm缓存
npm cache clean --force

# 删除node_modules并重新安装
rm -rf node_modules package-lock.json
npm install
```

### 3. Python依赖安装失败

如果Python依赖安装失败，请确保使用了正确的Python版本：

```bash
# 检查Python版本
python --version

# 使用特定版本的Python
python3.8 -m pip install -r requirements.txt
```

## 故障排除

如果遇到问题，请检查以下几点：

1. 确保所有必需的软件（Node.js、npm、Python）都已正确安装
2. 确保环境变量已正确配置
3. 确保数据库和缓存服务正在运行（如使用）
4. 查看控制台输出以获取错误信息

如果仍有问题，请在GitHub Issues中提交问题报告。