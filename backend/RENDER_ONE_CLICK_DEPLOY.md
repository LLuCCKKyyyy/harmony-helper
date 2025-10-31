# Render 一键部署教程

## 🚀 一键部署按钮

点击下面的按钮，一键部署到 Render：

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/LLuCCKKyyyy/harmony-helper)

---

## 📋 手动部署步骤

如果一键部署按钮不工作，可以按照以下步骤手动部署：

### 步骤 1：登录 Render

1. 访问 [https://render.com](https://render.com)
2. 点击 **"Get Started"** 或 **"Sign Up"**
3. 选择 **"Sign up with GitHub"**
4. 授权 Render 访问你的 GitHub 账号

---

### 步骤 2：创建 Web Service

1. 登录后，点击右上角的 **"New +"** 按钮
2. 选择 **"Web Service"**
3. 点击 **"Connect a repository"**
4. 如果是第一次使用，点击 **"Configure account"** 授权访问
5. 在仓库列表中找到 **`harmony-helper`**，点击 **"Connect"**

---

### 步骤 3：配置服务

在配置页面填写以下信息：

#### 基本设置
- **Name**: `harmony-helper-api` （或任何你喜欢的名字）
- **Region**: 选择离你最近的区域（例如 `Oregon (US West)`）
- **Branch**: `master`
- **Root Directory**: `backend` ⚠️ **重要：必须填写**

#### 运行时设置
- **Runtime**: `Python 3`
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

#### 计费方案
- **Instance Type**: 选择 **"Free"** （免费层级）

---

### 步骤 4：添加环境变量（可选）

1. 在配置页面向下滚动，找到 **"Environment Variables"** 部分
2. 点击 **"Add Environment Variable"**
3. 添加以下变量：
   - **Key**: `PYTHON_VERSION`
   - **Value**: `3.11.0`
4. 再添加一个（可选）：
   - **Key**: `ALLOWED_ORIGINS`
   - **Value**: `*` （或你的前端域名）

---

### 步骤 5：创建并部署

1. 检查所有配置是否正确
2. 点击页面底部的 **"Create Web Service"** 按钮
3. Render 会开始构建和部署你的应用
4. 等待几分钟，直到状态变为 **"Live"** 🟢

---

### 步骤 6：获取公开 URL

1. 部署成功后，在服务页面顶部可以看到你的应用 URL
2. 格式类似：
   ```
   https://harmony-helper-api.onrender.com
   ```
3. **复制这个 URL**，稍后需要配置到前端

---

### 步骤 7：验证部署

打开浏览器，访问以下地址验证：

1. **健康检查**：
   ```
   https://harmony-helper-api.onrender.com/health
   ```
   应该返回：`{"status":"healthy"}`

2. **API 文档**：
   ```
   https://harmony-helper-api.onrender.com/docs
   ```
   应该显示交互式 API 文档

3. **和声类型**：
   ```
   https://harmony-helper-api.onrender.com/harmony-types
   ```
   应该返回和声类型列表

---

### 步骤 8：配置前端

#### 在 Manus 平台
1. 打开前端项目的 Management UI
2. 进入 **Settings → Secrets**
3. 添加环境变量：
   - **Key**: `VITE_API_URL`
   - **Value**: `https://harmony-helper-api.onrender.com` （你的后端 URL）
4. 保存并等待前端重新部署

#### 本地开发
创建 `.env.local` 文件：
```
VITE_API_URL=https://harmony-helper-api.onrender.com
```

---

### 步骤 9：测试

1. 打开前端应用
2. 添加音符并生成和声
3. 如果成功，说明部署完成！🎉

---

## ⚠️ Render 免费层级注意事项

### 冷启动延迟
- 免费层级的服务在15分钟无活动后会自动休眠
- 下次访问时需要等待30秒左右唤醒
- 这是正常现象，不是错误

### 解决方案
1. **接受延迟**：适合演示和测试
2. **升级到付费计划**：$7/月，无冷启动
3. **使用 UptimeRobot**：免费服务，每5分钟 ping 一次保持唤醒

---

## 🔄 自动部署

Render 默认启用自动部署：
- 推送到 GitHub `master` 分支时自动重新部署
- 可以在服务设置中关闭此功能

---

## 📊 监控

### 查看日志
1. 在服务页面，点击 **"Logs"** 标签
2. 可以看到实时日志输出
3. 用于调试和监控

### 查看指标
1. 点击 **"Metrics"** 标签
2. 查看 CPU、内存、请求量等指标

---

## 💰 费用

- **免费层级**：完全免费
- **限制**：
  - 750小时/月运行时间
  - 冷启动延迟
  - 共享 CPU
- **付费计划**：$7/月起，无冷启动

---

## 🛠️ 故障排除

### 问题：构建失败
**解决方案**：
1. 检查 `requirements.txt` 是否正确
2. 确认 Root Directory 设置为 `backend`
3. 查看构建日志中的错误信息

### 问题：服务启动失败
**解决方案**：
1. 检查 Start Command 是否正确
2. 确认使用了 `$PORT` 环境变量
3. 查看运行日志

### 问题：CORS 错误
**解决方案**：
1. 设置 `ALLOWED_ORIGINS` 环境变量
2. 或者在代码中允许所有来源（已默认配置）

---

## 📚 相关资源

- [Render 官方文档](https://render.com/docs)
- [Render Python 部署指南](https://render.com/docs/deploy-fastapi)
- [项目 GitHub](https://github.com/LLuCCKKyyyy/harmony-helper)

---

## 🆚 Render vs Railway

| 特性 | Render | Railway |
|------|--------|---------|
| 免费额度 | 750小时/月 | $5/月 |
| 冷启动 | 有（15分钟） | 无 |
| 配置复杂度 | 中等 | 简单 |
| 自动部署 | ✅ | ✅ |
| 自定义域名 | ✅ | ✅ |
| 推荐场景 | 演示、测试 | 生产、开发 |

---

**需要帮助？** 在 GitHub Issues 提问：https://github.com/LLuCCKKyyyy/harmony-helper/issues
