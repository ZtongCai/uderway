# Vercel部署指南

## 前置条件
- GitHub账号
- Vercel账号（可通过GitHub登录）

## 部署步骤

### 1. 准备代码
确保所有文件已提交到GitHub仓库：
- app.py
- requirements.txt
- vercel.json
- runtime.txt
- wsgi.py
- static/ 目录
- templates/ 目录

### 2. 连接Vercel
1. 访问 [vercel.com](https://vercel.com)
2. 使用GitHub账号登录
3. 点击"New Project"
4. 选择您的GitHub仓库

### 3. 配置环境变量
在Vercel项目设置中，添加以下环境变量：
- `SILICONFLOW_API_KEY`: 您的硅基流动API密钥
- `SILICONFLOW_BASE_URL`: https://api.siliconflow.cn/v1
- `SILICONFLOW_TEXT_MODEL`: deepseek-ai/DeepSeek-V3.2-Exp
- `SILICONFLOW_IMAGE_MODEL`: Kwai-Kolors/Kolors
- `FLASK_ENV`: production
- `FLASK_DEBUG`: False

### 4. 部署
Vercel会自动检测到vercel.json配置并开始部署。

## 注意事项
- 确保.env文件已添加到.gitignore
- 首次部署可能需要几分钟时间
- 如果部署失败，检查Vercel的构建日志

## 自定义域名（可选）
部署成功后，可以在Vercel项目设置中绑定自定义域名。