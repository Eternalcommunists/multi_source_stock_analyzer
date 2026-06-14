# 部署指南

本文档介绍如何将多数据源股票分析系统部署到生产环境。

## 部署架构

```
┌─────────────────────────────────────────────────────────────┐
│                    负载均衡器                              │
│                    (Nginx/HAProxy)                        │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    应用服务器集群                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   App-1     │  │   App-2     │  │   App-3     │        │
│  │  (Node.js)  │  │  (Node.js)  │  │  (Node.js)  │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
                                │
                    ┌─────────────────────┐
                    │    数据层           │
        ┌───────────┤                     ├───────────┐
        │           │  ┌─────────────┐    │           │
        │           │  │   数据库     │    │           │
        │           │  │ (MongoDB)   │    │           │
        │           │  └─────────────┘    │           │
        │           └─────────────────────┘           │
        │                                           │
┌─────────────┐                           ┌─────────────────┐
│   缓存层     │                           │   消息队列      │
│  (Redis)    │                           │  (RabbitMQ)    │
└─────────────┘                           └─────────────────┘
```

## 环境准备

### 服务器要求

- **CPU**: 4核或以上
- **内存**: 8GB或以上
- **存储**: 50GB SSD或以上
- **操作系统**: Ubuntu 20.04 LTS 或 CentOS 8
- **网络**: 稳定的互联网连接

### 系统依赖

1. **Docker 和 Docker Compose**
```bash
# Ubuntu
sudo apt update
sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER

# CentOS
sudo yum install docker docker-compose
sudo usermod -aG docker $USER
```

2. **Node.js 和 npm**
```bash
# 使用nvm安装特定版本
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18
```

## 部署步骤

### 1. 获取代码

```bash
git clone https://github.com/yourusername/stock-analysis-system.git
cd stock-analysis-system
```

### 2. 配置环境变量

创建生产环境的环境配置文件：

```bash
# 根目录下创建 .env.production
cat > .env.production << EOF
NODE_ENV=production
PORT=5000
API_RATE_LIMIT_WINDOW_MS=900000  # 15分钟
API_RATE_LIMIT_MAX_REQUESTS=1000
DB_HOST=mongo
DB_PORT=27017
DB_NAME=stock_analysis_prod
REDIS_HOST=redis
REDIS_PORT=6379
JWT_SECRET=your-super-secret-jwt-key-change-in-production
EOF
```

### 3. Docker部署

#### 创建 Docker Compose 文件

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  mongo:
    image: mongo:5.0
    container_name: stock-mongo
    restart: always
    ports:
      - "27017:27017"
    volumes:
      - ./mongo-data:/data/db
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=your_secure_password
    networks:
      - stock-network

  redis:
    image: redis:7-alpine
    container_name: stock-redis
    restart: always
    ports:
      - "6379:6379"
    volumes:
      - ./redis-data:/data
    command: redis-server --appendonly yes
    networks:
      - stock-network

  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    container_name: stock-backend
    restart: always
    ports:
      - "5000:5000"
    environment:
      - NODE_ENV=production
      - DB_HOST=mongo
      - REDIS_HOST=redis
    depends_on:
      - mongo
      - redis
    networks:
      - stock-network
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
      restart_policy:
        condition: on-failure

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: stock-frontend
    restart: always
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - stock-network

  nginx:
    image: nginx:alpine
    container_name: stock-nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
    networks:
      - stock-network

networks:
  stock-network:
    driver: bridge
```

#### 创建 Nginx 配置

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:5000;
    }

    server {
        listen 80;
        server_name your-domain.com;

        # 前端静态文件
        location / {
            root /usr/share/nginx/html;
            try_files $uri $uri/ /index.html;
            expires 1m;
            add_header Cache-Control "public";
        }

        # API 代理
        location /api/ {
            proxy_pass http://backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # WebSocket 支持
        location /ws/ {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
        }
    }
}
```

### 4. 构建和启动

```bash
# 构建并启动服务
docker-compose -f docker-compose.prod.yml up -d --build

# 检查服务状态
docker-compose -f docker-compose.prod.yml ps
```

### 5. SSL证书配置（可选但推荐）

```bash
# 使用Certbot获取SSL证书
sudo apt-get install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com
```

### 6. 数据库初始化

```bash
# 连接到MongoDB容器执行初始化脚本
docker exec -it stock-mongo mongo -u admin -p your_secure_password --eval "
use stock_analysis_prod;
db.createUser({
  user: 'app_user',
  pwd: 'app_password',
  roles: [
    { role: 'readWrite', db: 'stock_analysis_prod' }
  ]
});
"
```

## 生产环境配置

### 安全配置

1. **防火墙设置**
```bash
# 只开放必要的端口
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
```

2. **环境变量安全**
```bash
# 使用Secrets管理敏感信息
# 在Docker Swarm或Kubernetes中使用Secrets
```

3. **API安全**
```bash
# 实现API速率限制
# 配置CORS策略
# 实现认证和授权
```

### 性能优化

1. **数据库优化**
```bash
# 创建数据库索引
db.stocks.createIndex({ "symbol": 1, "timestamp": -1 })
db.quotes.createIndex({ "symbol": 1, "updated_at": -1 })
```

2. **缓存策略**
```bash
# 配置Redis缓存策略
# 设置合适的TTL
# 实现缓存预热
```

3. **CDN配置**
```bash
# 静态资源使用CDN
# 配置缓存头
```

### 监控和日志

1. **应用监控**
```bash
# 配置Prometheus和Grafana
# 监控关键指标
# 设置告警规则
```

2. **日志管理**
```bash
# 配置日志轮转
# 集中化日志收集
# 实现日志分析
```

## 部署验证

### 功能验证

1. **访问主页**
```bash
curl -I http://your-domain.com
```

2. **API测试**
```bash
curl http://your-domain.com/api/health
curl http://your-domain.com/api/stocks/000001/quote
```

3. **前端验证**
- 访问前端界面
- 测试股票搜索功能
- 验证数据加载

### 性能验证

1. **负载测试**
```bash
# 使用Apache Bench进行简单测试
ab -n 1000 -c 10 http://your-domain.com/api/stocks/000001/quote
```

2. **压力测试**
- 逐步增加并发用户数
- 监控系统资源使用
- 验证错误率和响应时间

## 维护和更新

### 日常维护

1. **备份策略**
```bash
# 数据库备份
docker exec stock-mongo mongodump --archive=/backup/dump-$(date +%Y%m%d).gz

# 日志轮转
sudo logrotate -f /etc/logrotate.d/nginx
```

2. **监控检查**
- 检查服务状态
- 查看系统资源使用
- 验证数据源连接

### 更新流程

1. **代码更新**
```bash
# 拉取最新代码
git pull origin main

# 构建新镜像
docker-compose -f docker-compose.prod.yml build --no-cache

# 滚动更新
docker-compose -f docker-compose.prod.yml up -d
```

2. **数据库迁移**
```bash
# 在更新前备份数据库
# 执行迁移脚本
# 验证数据完整性
```

## 故障排除

### 常见问题

1. **服务启动失败**
```bash
# 检查日志
docker-compose -f docker-compose.prod.yml logs -f

# 检查端口占用
sudo netstat -tlnp | grep :5000
```

2. **数据库连接失败**
```bash
# 检查MongoDB状态
docker exec stock-mongo mongo --eval "db.runCommand('ping')"

# 检查网络连接
docker exec stock-backend ping mongo
```

3. **性能问题**
```bash
# 检查资源使用
docker stats

# 检查慢查询
docker exec stock-mongo mongo --eval "db.setProfilingLevel(2, {slowms: 100})"
```

### 应急预案

1. **回滚策略**
```bash
# 从备份恢复数据库
gunzip -c backup-file.gz | mongorestore --drop

# 回滚到之前的镜像版本
docker-compose -f docker-compose.prod.yml down
git checkout previous-commit
docker-compose -f docker-compose.prod.yml up -d
```

2. **灾备恢复**
- 数据库定期备份
- 配置文件版本控制
- 多地域部署（高级选项）

## 安全加固

### 系统安全

1. **SSH安全**
```bash
# 禁用密码登录
# 使用密钥认证
# 更改默认端口
```

2. **容器安全**
```bash
# 使用非root用户运行
# 限制容器权限
# 定期更新基础镜像
```

### 应用安全

1. **输入验证**
- 严格的参数验证
- 防止SQL注入
- 防止XSS攻击

2. **认证授权**
- JWT令牌管理
- 角色权限控制
- 会话管理

通过遵循此部署指南，您可以成功将多数据源股票分析系统部署到生产环境。记得定期更新和维护系统以保持最佳性能和安全性。