# Backend Deployment Guide

本文档说明如何将Harmony Helper后端部署到云平台。

## 部署到 Railway

### 前提条件
- GitHub账号
- Railway账号（可以用GitHub登录）

### 步骤

1. **推送代码到GitHub**
   ```bash
   # 已经完成，代码在 https://github.com/LLuCCKKyyyy/harmony-helper
   ```

2. **在Railway创建项目**
   - 访问 [railway.app](https://railway.app/)
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择 `harmony-helper` 仓库
   - 选择 `backend` 目录作为根目录

3. **配置环境变量**（可选）
   - 在Railway项目设置中添加环境变量：
   - `ALLOWED_ORIGINS`: 前端域名（例如：`https://predeploy-70a4a84a-harmonygen-asrpupeb.manus.space`）
   - 如果不设置，默认允许所有域名

4. **部署**
   - Railway会自动检测Python项目
   - 自动安装依赖（requirements.txt）
   - 自动运行启动命令（railway.json或Procfile）
   - 部署完成后会提供一个公开URL

5. **获取API URL**
   - 部署完成后，在Railway项目页面可以看到公开URL
   - 例如：`https://harmony-helper-production.up.railway.app`
   - 将这个URL配置到前端的环境变量 `VITE_API_URL`

## 部署到 Render

### 步骤

1. **在Render创建Web Service**
   - 访问 [render.com](https://render.com/)
   - 点击 "New +" → "Web Service"
   - 连接GitHub仓库 `harmony-helper`

2. **配置服务**
   - **Name**: harmony-helper-api
   - **Root Directory**: `backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **环境变量**（可选）
   - 添加 `ALLOWED_ORIGINS` 环境变量

4. **部署**
   - 点击 "Create Web Service"
   - 等待部署完成
   - 获取公开URL

## 部署到 Heroku

### 步骤

1. **安装Heroku CLI**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **登录Heroku**
   ```bash
   heroku login
   ```

3. **创建应用**
   ```bash
   cd backend
   heroku create harmony-helper-api
   ```

4. **部署**
   ```bash
   git subtree push --prefix backend heroku main
   ```

5. **配置环境变量**
   ```bash
   heroku config:set ALLOWED_ORIGINS=https://your-frontend-domain.com
   ```

## 本地测试部署配置

在部署前，可以本地测试：

```bash
cd backend
pip install -r requirements.txt
export PORT=8000
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

访问 http://localhost:8000/docs 查看API文档。

## 配置前端连接后端

部署后端后，需要在前端项目中配置后端URL：

### Manus部署
在项目的Settings → Secrets中添加：
- Key: `VITE_API_URL`
- Value: `https://your-backend-url.railway.app`（你的后端URL）

### 本地开发
创建 `.env.local` 文件：
```
VITE_API_URL=http://localhost:8000
```

## 验证部署

部署完成后，访问以下端点验证：

- `GET /health` - 健康检查
- `GET /harmony-types` - 获取和声类型列表
- `GET /docs` - API文档

## 故障排除

### 问题：CORS错误
**解决方案**：确保设置了正确的 `ALLOWED_ORIGINS` 环境变量

### 问题：music21导入错误
**解决方案**：确保 `requirements.txt` 包含所有依赖

### 问题：端口绑定错误
**解决方案**：确保使用 `$PORT` 环境变量，不要硬编码端口号

## 成本估算

- **Railway**: 免费额度 $5/月，足够小型项目
- **Render**: 免费层级可用，但可能有冷启动延迟
- **Heroku**: 免费层级已取消，最低 $7/月

推荐使用 **Railway** 进行部署。
