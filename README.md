# 海上丝绸之路 — 航海日志生成器

一个基于Flask的Web应用程序，用户可以点击海上丝绸之路沿线的港口城市，生成具有当地特色的航海日志和相应的图像。

## 功能特点

- **海上丝绸之路航线可视化**：展示从香港到威尼斯的历史贸易航线
- **智能日志生成**：使用AI大模型生成具有当地文化特色的航海日志
- **图像生成**：自动生成与日志内容匹配的港口场景图像
- **双语支持**：支持中文和英文界面切换
- **交互式地图**：点击港口城市即可生成对应的航海日志
- **工业港口风格**：采用现代工业美学设计

## 港口城市

项目包含8个重要的海上丝绸之路港口城市：

1. **香港** - 东方明珠，中西文化交融的国际金融中心
2. **新加坡** - 花园城市，多元文化汇聚的海上枢纽
3. **科伦坡** - 锡兰明珠，香料贸易的古老港口
4. **孟买** - 宝莱坞之都，印度洋贸易的重要门户
5. **迪拜** - 沙漠绿洲，现代商业与传统阿拉伯文化的完美融合
6. **苏伊士** - 运河咽喉，连接东西方文明的重要通道
7. **雅典** - 西方文明摇篮，古希腊哲学与艺术的发源地
8. **威尼斯** - 水城明珠，文艺复兴时期的海上商业帝国

## 技术栈

- **后端**：Flask (Python)
- **前端**：HTML5, CSS3, JavaScript
- **AI集成**：硅基流动API
- **样式**：现代工业风格CSS

## 安装和运行

1. 克隆项目到本地
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 配置环境变量：
   - 复制 `.env.example` 文件并重命名为 `.env`
   - 在 `.env` 文件中配置您的API密钥：
   ```bash
   cp .env.example .env
   ```
   - 编辑 `.env` 文件，将 `your_api_key_here` 替换为您的实际API密钥

4. 运行应用：
   ```bash
   python -m flask run
   ```
   或者：
   ```bash
   python app.py
   ```

5. 在浏览器中访问 `http://127.0.0.1:5000`

## 环境变量配置

为了保护API密钥等敏感信息，本项目使用环境变量进行配置。请按以下步骤设置：

### 1. 创建环境变量文件

复制 `.env.example` 文件并重命名为 `.env`：
```bash
cp .env.example .env
```

### 2. 配置API密钥

编辑 `.env` 文件，填入您的实际配置：
```env
# 硅基流动API配置
SILICONFLOW_API_KEY=your_actual_api_key_here
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1
SILICONFLOW_TEXT_MODEL=deepseek-ai/DeepSeek-V3.2-Exp
SILICONFLOW_IMAGE_MODEL=Kwai-Kolors/Kolors

# Flask配置
FLASK_ENV=development
FLASK_DEBUG=True
```

### 3. 安全注意事项

- ⚠️ **重要**：`.env` 文件包含敏感信息，已被 `.gitignore` 排除，不会上传到Git仓库
- 🔒 **安全**：请勿将真实的API密钥提交到版本控制系统
- 📝 **分享**：如需分享配置格式，请使用 `.env.example` 文件

## 硅基流动API配置

### 获取API密钥

1. 访问 [硅基流动官网](https://siliconflow.cn)
2. 注册账号并获取API密钥
3. 在 `app.py` 中配置您的密钥

### API配置说明

```python
SILICONFLOW_CONFIG = {
    "api_key": "YOUR_API_KEY_HERE",  # 替换为您的API密钥
    "base_url": "https://api.siliconflow.cn/v1",
    "text_model": "Qwen/Qwen2.5-72B-Instruct",  # 文字生成模型
    "image_model": "black-forest-labs/FLUX.1-schnell"  # 图像生成模型
}
```

### 支持的模型

**文字生成模型**：
- `Qwen/Qwen2.5-72B-Instruct`
- `meta-llama/Meta-Llama-3.1-8B-Instruct`
- `deepseek-ai/DeepSeek-V2.5`

**图像生成模型**：
- `black-forest-labs/FLUX.1-schnell`
- `stabilityai/stable-diffusion-3-5-large`
- `stabilityai/stable-diffusion-xl-base-1.0`

### 备用方案

如果没有配置API密钥，应用程序将使用模拟数据和Unsplash图像服务作为备选方案，确保基本功能正常运行。

## 使用方法

1. 打开应用程序
2. 点击地图上的任意港口城市（橙色圆点）
3. 系统将自动生成该城市的航海日志和图像
4. 使用左上角的语言切换按钮在中英文之间切换
5. 点击"下载 txt"按钮可以保存日志到本地

## 项目结构

```
hang_an/
├── app.py                 # Flask应用主文件
├── templates/
│   └── index.html        # 主页面模板
├── static/
│   ├── crane_silhouette.svg      # 起重机剪影
│   └── placeholder_map_800x600.png  # 地图背景
└── README.md             # 项目说明文档
```

## 特色功能

- **智能提示词生成**：根据港口城市的文化特色自动生成图像提示词
- **响应式设计**：支持桌面和移动设备
- **本地存储**：自动保存最近的10条日志记录
- **无障碍支持**：包含适当的ARIA标签和键盘导航支持

## 开发说明

项目采用模块化设计，易于扩展和维护：

- 航线数据和港口信息集中在 `MARITIME_SILK_ROAD` 配置中
- 提示词模板支持多语言和自定义
- API调用封装在独立函数中，便于测试和调试
- 前端使用原生JavaScript，无外部依赖

## 许可证

本项目仅供学习和研究使用。