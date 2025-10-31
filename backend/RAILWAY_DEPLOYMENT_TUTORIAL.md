# Railway 部署教程（图文详解）

## 📋 前提条件
- GitHub 账号
- Railway 账号（可以用 GitHub 登录，免费）

---

## 🚀 步骤 1：登录 Railway

1. 访问 [https://railway.app](https://railway.app)
2. 点击右上角 **"Login"**
3. 选择 **"Login with GitHub"**
4. 授权 Railway 访问你的 GitHub 账号

---

## 📦 步骤 2：创建新项目

1. 登录后，点击 **"New Project"**
2. 选择 **"Deploy from GitHub repo"**
3. 如果是第一次使用，需要点击 **"Configure GitHub App"** 授权仓库访问
4. 在仓库列表中找到 **`harmony-helper`**，点击选择

---

## ⚙️ 步骤 3：配置部署设置

Railway 会自动检测到这是一个 Python 项目，但我们需要指定后端目录：

### 3.1 设置根目录
1. 在项目页面，点击你的服务（会显示为 "harmony-helper"）
2. 切换到 **"Settings"** 标签
3. 找到 **"Root Directory"** 设置
4. 输入：`backend`
5. 点击保存

### 3.2 设置启动命令（可选，已在配置文件中）
Railway 会自动读取 `railway.json`，但你也可以手动设置：
1. 在 Settings 中找到 **"Start Command"**
2. 输入：`uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3.3 设置环境变量（可选）
1. 切换到 **"Variables"** 标签
2. 点击 **"New Variable"**
3. 添加以下变量：
   - **Variable**: `ALLOWED_ORIGINS`
   - **Value**: `*` （或者你的前端域名，例如 `https://predeploy-70a4a84a-harmonygen-asrpupeb.manus.space`）

---

## 🎯 步骤 4：部署

1. 配置完成后，Railway 会自动开始部署
2. 你可以在 **"Deployments"** 标签查看部署进度
3. 等待几分钟，直到显示 **"Success"** ✅

---

## 🌐 步骤 5：获取公开 URL

1. 部署成功后，切换到 **"Settings"** 标签
2. 找到 **"Domains"** 部分
3. 点击 **"Generate Domain"**
4. Railway 会自动生成一个公开 URL，例如：
   ```
   https://harmony-helper-production.up.railway.app
   ```
5. **复制这个 URL**，稍后需要配置到前端

---

## ✅ 步骤 6：验证部署

打开浏览器，访问以下地址验证部署是否成功：

1. **健康检查**：
   ```
   https://your-app-name.up.railway.app/health
   ```
   应该返回：`{"status":"healthy"}`

2. **API 文档**：
   ```
   https://your-app-name.up.railway.app/docs
   ```
   应该显示 FastAPI 自动生成的交互式文档

3. **和声类型列表**：
   ```
   https://your-app-name.up.railway.app/harmony-types
   ```
   应该返回所有支持的和声类型

---

## 🔗 步骤 7：配置前端连接后端

### 在 Manus 平台配置

1. 打开你的前端项目（Harmony Helper Frontend）
2. 点击右上角的设置图标，进入 **Management UI**
3. 导航到 **Settings → Secrets**
4. 添加新的环境变量：
   - **Key**: `VITE_API_URL`
   - **Value**: `https://your-app-name.up.railway.app` （你在步骤5复制的URL）
5. 保存后，前端会自动重新部署并连接到后端

### 本地开发配置

如果你在本地开发，创建 `.env.local` 文件：
```bash
VITE_API_URL=https://your-app-name.up.railway.app
```

---

## 🔄 步骤 8：测试完整功能

1. 打开前端应用
2. 点击几个钢琴键添加音符
3. 选择和声类型
4. 点击 **"生成和声"**
5. 如果成功生成和声，说明前后端连接正常！🎉

---

## 📊 监控和日志

### 查看日志
1. 在 Railway 项目页面，切换到 **"Deployments"** 标签
2. 点击最新的部署
3. 可以看到实时日志输出

### 查看使用量
1. 切换到 **"Metrics"** 标签
2. 可以看到 CPU、内存、网络使用情况

---

## 💰 费用说明

Railway 免费额度：
- **$5 免费额度/月**
- 对于小型项目完全够用
- 超出后按使用量计费（约 $0.000463/GB-hour）

---

## 🛠️ 故障排除

### 问题 1：部署失败
**可能原因**：依赖安装失败
**解决方案**：
1. 检查 `requirements.txt` 是否正确
2. 查看部署日志中的错误信息
3. 确保 Python 版本正确（3.11）

### 问题 2：前端无法连接后端
**可能原因**：CORS 配置或 URL 错误
**解决方案**：
1. 确认 `VITE_API_URL` 配置正确
2. 检查后端 URL 是否可访问
3. 查看浏览器控制台的错误信息

### 问题 3：API 响应慢
**可能原因**：免费层级有冷启动延迟
**解决方案**：
1. 第一次访问可能需要等待几秒
2. 考虑升级到付费计划
3. 或者使用 Railway 的 "Keep Alive" 功能

---

## 📚 相关资源

- [Railway 官方文档](https://docs.railway.app/)
- [FastAPI 部署指南](https://fastapi.tiangolo.com/deployment/)
- [项目 GitHub 仓库](https://github.com/LLuCCKKyyyy/harmony-helper)

---

## 🎓 下一步

部署完成后，你可以：
1. 自定义域名（在 Railway Settings → Domains）
2. 设置自动部署（推送到 GitHub 自动更新）
3. 添加更多和声算法
4. 优化性能和缓存

---

**需要帮助？** 在 GitHub Issues 中提问：https://github.com/LLuCCKKyyyy/harmony-helper/issues
