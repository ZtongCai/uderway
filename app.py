from flask import Flask, render_template, jsonify, request
import random
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# 海上丝绸之路航线数据
MARITIME_SILK_ROAD = {
    "main_route": {
        "zh": "新海上丝绸之路",
        "en": "New Maritime Silk Road",
        "waypoints": [
            # 中国
            {"name_zh": "青岛", "name_en": "Qingdao", "coord": [120.3826, 36.0671], "is_strategic": False, "culture": "德式建筑与现代港口的完美融合，青岛啤酒的故乡", "country_zh": "中国", "country_en": "China"},
            {"name_zh": "上海", "name_en": "Shanghai", "coord": [121.4737, 31.2304], "is_strategic": True, "culture": "国际金融中心，东西方文化交汇的现代化大都市", "country_zh": "中国", "country_en": "China"},
            {"name_zh": "厦门", "name_en": "Xiamen", "coord": [118.1102, 24.4905], "is_strategic": True, "culture": "海上花园，鼓浪屿的浪漫风情与现代化的港口城市", "country_zh": "中国", "country_en": "China"},
            {"name_zh": "香港", "name_en": "Hong Kong", "coord": [114.1694, 22.3193], "is_strategic": True, "culture": "东西方文化交融的国际金融中心，维多利亚港的璀璨夜景", "country_zh": "中国", "country_en": "China"},
            {"name_zh": "广州", "name_en": "Guangzhou", "coord": [113.2644, 23.1291], "is_strategic": True, "culture": "千年商都，海上丝绸之路的起点之一，美食与文化的交融之地", "country_zh": "中国", "country_en": "China"},
            
            # 南海航道
            {"name_zh": "三沙市", "name_en": "Sansha City", "coord": [112.3389, 16.8311], "is_strategic": True, "culture": "这里是珊瑚的故乡，海水的颜色随深度变幻，从清澈的蓝到深邃的绿。每一寸土地都承载着历史的记忆，每一片海域都讲述着主权的故事。", "country_zh": "中国", "country_en": "China"},
            
            # 东南亚（按地理位置重新排序）
            {"name_zh": "胡志明市港", "name_en": "Ho Chi Minh City Port", "coord": [106.7000, 10.7500], "is_strategic": False, "culture": "越南的经济中心，充满法国殖民风情的港口", "country_zh": "越南", "country_en": "Vietnam"},
            
            # 泰国湾航道
            {"name_zh": "泰国湾", "name_en": "Gulf of Thailand", "coord": [101.0000, 9.0000], "is_strategic": False, "culture": "连接泰国与马来西亚的重要海域", "country_zh": "公海", "country_en": "International Waters", "is_hidden": True},
            
            {"name_zh": "林查班港", "name_en": "Laem Chabang Port", "coord": [100.8833, 13.0833], "is_strategic": False, "culture": "泰国最大的深水港，佛教文化与现代贸易的交汇", "country_zh": "泰国", "country_en": "Thailand"},
            
            # 马六甲海峡北部
            {"name_zh": "马六甲海峡北部", "name_en": "Northern Strait of Malacca", "coord": [100.0000, 6.0000], "is_strategic": True, "culture": "世界最繁忙的海上通道之一", "country_zh": "公海", "country_en": "International Waters", "is_hidden": True},
            
            {"name_zh": "巴生港", "name_en": "Port Klang", "coord": [101.3833, 3.0000], "is_strategic": False, "culture": "马来西亚最大港口，多元文化交融的贸易枢纽", "country_zh": "马来西亚", "country_en": "Malaysia"},
            
            # 马六甲海峡中部
            {"name_zh": "马六甲海峡中部", "name_en": "Central Strait of Malacca", "coord": [102.0000, 2.0000], "is_strategic": True, "culture": "连接印度洋与太平洋的咽喉要道", "country_zh": "公海", "country_en": "International Waters", "is_hidden": True},
            
            {"name_zh": "新加坡港", "name_en": "Port of Singapore", "coord": [103.8211, 1.2646], "is_strategic": True, "culture": "世界级枢纽港，现代化的花园城市", "country_zh": "新加坡", "country_en": "Singapore"},
            
            # 爪哇海航道
            {"name_zh": "爪哇海", "name_en": "Java Sea", "coord": [108.0000, -4.0000], "is_strategic": False, "culture": "印尼群岛间的重要海上通道", "country_zh": "公海", "country_en": "International Waters", "is_hidden": True},
            
            {"name_zh": "丹戎不碌港", "name_en": "Tanjung Priok Port", "coord": [106.8833, -6.1000], "is_strategic": False, "culture": "印尼最大港口，群岛国家的门户", "country_zh": "印度尼西亚", "country_en": "Indonesia"},
            
            # 印度洋航道
            {"name_zh": "印度洋东部", "name_en": "Eastern Indian Ocean", "coord": [85.0000, 0.0000], "is_strategic": False, "culture": "连接东南亚与南亚的广阔海域", "country_zh": "公海", "country_en": "International Waters", "is_hidden": True},
            
            # 南亚
            {"name_zh": "科伦坡", "name_en": "Colombo", "coord": [79.8612, 6.9271], "is_strategic": False, "culture": "殖民建筑、寺庙和现代商业的混合体", "country_zh": "斯里兰卡", "country_en": "Sri Lanka"},
            {"name_zh": "汉班托塔港", "name_en": "Hambantota Port", "coord": [81.1185, 6.1243], "is_strategic": True, "culture": "斯里兰卡的新兴战略港口", "country_zh": "斯里兰卡", "country_en": "Sri Lanka"},
            {"name_zh": "孟买", "name_en": "Mumbai", "coord": [72.8777, 19.0760], "is_strategic": False, "culture": "印度的金融之都和宝莱坞的故乡", "country_zh": "印度", "country_en": "India"},
            {"name_zh": "卡拉奇", "name_en": "Karachi", "coord": [67.0011, 24.8607], "is_strategic": False, "culture": "巴基斯坦的经济中心，充满活力的港口城市", "country_zh": "巴基斯坦", "country_en": "Pakistan"},
            {"name_zh": "瓜达尔港", "name_en": "Gwadar Port", "coord": [62.3254, 25.1264], "is_strategic": True, "culture": "位于阿拉伯海的战略深水港", "country_zh": "巴基斯坦", "country_en": "Pakistan"},
            
            # 西亚与非洲
            {"name_zh": "霍尔木兹海峡", "name_en": "Strait of Hormuz", "coord": [56.2500, 26.5667], "is_strategic": True, "culture": "连接波斯湾与阿拉伯海的重要海上通道", "country_zh": "阿联酋", "country_en": "UAE"},
            {"name_zh": "迪拜", "name_en": "Dubai", "coord": [55.0667, 25.0167], "is_strategic": False, "culture": "现代奢华与传统阿拉伯文化的结合", "country_zh": "阿联酋", "country_en": "UAE"},
            {"name_zh": "亚丁湾", "name_en": "Gulf of Aden", "coord": [48.0000, 12.5000], "is_strategic": True, "culture": "红海与阿拉伯海之间的重要海上通道", "country_zh": "也门", "country_en": "Yemen"},
            {"name_zh": "吉达港", "name_en": "Jeddah Port", "coord": [39.1925, 21.4858], "is_strategic": False, "culture": "通往麦加的门户，红海上的历史名城", "country_zh": "沙特阿拉伯", "country_en": "Saudi Arabia"},
            {"name_zh": "苏伊士运河", "name_en": "Suez Canal", "coord": [32.2549, 30.5852], "is_strategic": True, "culture": "连接地中海和红海的世界重要航道", "country_zh": "埃及", "country_en": "Egypt"},
            {"name_zh": "亚历山大", "name_en": "Alexandria", "coord": [29.9187, 31.2001], "is_strategic": False, "culture": "地中海的明珠，拥有悠久的历史和文化遗产", "country_zh": "埃及", "country_en": "Egypt"},
            
            # 欧洲
            {"name_zh": "比雷埃夫斯港", "name_en": "Piraeus Port", "coord": [23.6471, 37.9429], "is_strategic": True, "culture": "欧洲最大的客运港之一，通往希腊群岛的门户", "country_zh": "希腊", "country_en": "Greece"},
            {"name_zh": "威尼斯", "name_en": "Venice", "coord": [12.3155, 45.4408], "is_strategic": False, "culture": "水城，贡多拉和文艺复兴艺术的故乡", "country_zh": "意大利", "country_en": "Italy"},
            {"name_zh": "鹿特丹港", "name_en": "Port of Rotterdam", "coord": [4.4792, 51.9225], "is_strategic": False, "culture": "欧洲最大的港口，现代建筑的典范", "country_zh": "荷兰", "country_en": "Netherlands"}
        ]
    }
}

# 硅基流动API配置
SILICONFLOW_CONFIG = {
    "api_key": os.getenv("SILICONFLOW_API_KEY", "YOUR_API_KEY_HERE"),
    "base_url": os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1"),
    "text_model": os.getenv("SILICONFLOW_TEXT_MODEL", "deepseek-ai/DeepSeek-V3.2-Exp"),
    "image_model": os.getenv("SILICONFLOW_IMAGE_MODEL", "Kwai-Kolors/Kolors")
}

# 航海日志提示词模板
# 简短版航海日志模板（15-25字）
LOG_PROMPT_SHORT = {
    "zh": """你是一位船员，现在在{location}。天气{weather}，时间是{time_period}。
请写一句15-25字的简短感慨，就像发朋友圈一样自然随意。可以是：
- 对港口风景的感叹
- 对港口繁忙程度的观察  
- 对港口文化的印象
- 对港口特色的描述

不要用"你见过...吗"这种模板句式，要真实自然，像普通人的随口一句话。""",
    
    "en": """You're a seafarer at {location}. Weather: {weather}, Time: {time_period}.
Write a brief 15-25 word casual remark, like a social media post. Could be:
- Port scenery impression
- Port activity observation
- Port culture impression  
- Port characteristics description

Be natural and authentic, like a spontaneous comment."""
}

# 详细版航海日志模板（150-200字）
LOG_PROMPT_DETAILED = {
    "zh": """你是一位船员，在{location}已经待了{random_days}天。现在是{time_period}，天气{weather}。

请写一段150-200字的航海日志，就像在和朋友聊天：

从当下的真实感受开始 - 可能是累了、兴奋、想家、或者被什么打动了。

然后自然地聊聊：
- 今天具体几点做了什么工作（比如：早上6点开始装货、下午2点值班、晚上8点维修等）
- 这个地方给你的印象：{culture}
- 遇到的人或事
- 工作中的小细节（不用刻意解释专业术语）

最后可以是对未来的期待、对家人的思念，或者就是当下的心情。

语言要像微信聊天一样自然，不要太正式，可以有些口语化的表达。""",
    
    "en": """You're a seafarer at {location} for {random_days} days. It's {time_period}, weather is {weather}.

Write a 150-200 word maritime log like chatting with friends:

Start with how you're really feeling right now - tired, excited, homesick, or moved by something.

Then naturally talk about:
- What specific time you did work today (e.g., started loading at 6am, watch duty at 2pm, maintenance at 8pm, etc.)
- Your impression of this place: {culture}
- People or things you encountered
- Work details (no need to over-explain technical terms)

End with hopes for the future, missing family, or just your current mood.

Write like texting a friend - natural, not too formal, with casual expressions."""
}

# 图像生成提示词模板
IMAGE_PROMPT_TEMPLATE = {
    "zh": "照片级真实感，4K高清，{location}港口，{weather}，{time_period}。{cultural_elements}。专业摄影，细节丰富。",
    "en": "Photorealistic, 4K, hyper-detailed photo of {location} port during {time_period}, {weather}. Featuring {cultural_elements}. Professional photography."
}

# 模拟数据
MOCK_WEATHER = ["晴朗", "多云", "微风", "海雾", "细雨"]
MOCK_WEATHER_EN = ["sunny", "cloudy", "breezy", "foggy", "light rain"]
MOCK_TIME = ["黎明", "上午", "正午", "黄昏", "夜晚"]
MOCK_TIME_EN = ["dawn", "morning", "noon", "dusk", "night"]

# 硅基流动API调用函数
def call_siliconflow_text(prompt, language='zh'):
    """调用硅基流动文字生成API"""
    headers = {
        'Authorization': f'Bearer {SILICONFLOW_CONFIG["api_key"]}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "model": SILICONFLOW_CONFIG["text_model"],
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 800,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(
            f'{SILICONFLOW_CONFIG["base_url"]}/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            print(f"API调用失败: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"API调用异常: {str(e)}")
        return None

def call_siliconflow_image(prompt):
    """调用硅基流动图像生成API"""
    headers = {
        'Authorization': f'Bearer {SILICONFLOW_CONFIG["api_key"]}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "model": SILICONFLOW_CONFIG["image_model"],
        "prompt": prompt,
        "image_size": "1024x1024",
        "batch_size": 1
    }
    
    try:
        response = requests.post(
            f'{SILICONFLOW_CONFIG["base_url"]}/images/generations',
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['data'][0]['url']
        else:
            print(f"图像API调用失败: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"图像API调用异常: {str(e)}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/routes')
def get_routes():
    main_route = MARITIME_SILK_ROAD["main_route"]
    # 动态生成coordinates
    main_route["coordinates"] = [waypoint["coord"] for waypoint in main_route["waypoints"]]
    return jsonify(main_route)

@app.route('/generate_log')
def generate_log():
    waypoint_index = request.args.get('waypoint_index', type=int)
    language = request.args.get('language', 'en')
    
    if waypoint_index is None or waypoint_index >= len(MARITIME_SILK_ROAD["main_route"]["waypoints"]):
        waypoint_index = random.randint(0, len(MARITIME_SILK_ROAD["main_route"]["waypoints"]) - 1)
    
    waypoint = MARITIME_SILK_ROAD["main_route"]["waypoints"][waypoint_index]
    
    # 随机选择天气和时间
    weather = random.choice(MOCK_WEATHER if language == 'zh' else MOCK_WEATHER_EN)
    time_period = random.choice(MOCK_TIME if language == 'zh' else MOCK_TIME_EN)
    
    # 生成航海日志
    location = waypoint[f"name_{language}"]
    culture = waypoint["culture"]
    
    # 生成随机航海天数（1-365天）
    random_days = random.randint(1, 365)
    
    # 构建简短版提示词
    short_prompt = LOG_PROMPT_SHORT[language].format(
        location=location,
        weather=weather,
        time_period=time_period
    )
    
    # 构建详细版提示词
    detailed_prompt = LOG_PROMPT_DETAILED[language].format(
        location=location,
        culture=culture,
        random_days=random_days,
        weather=weather,
        time_period=time_period
    )
    
    # 调用硅基流动API生成两种版本的日志内容
    if SILICONFLOW_CONFIG["api_key"] != "YOUR_API_KEY_HERE":
        short_content = call_siliconflow_text(short_prompt, language)
        detailed_content = call_siliconflow_text(detailed_prompt, language)
    else:
        # 如果没有配置API密钥，使用模拟数据
        short_content = f"{location}的{weather}天，心情不错" if language == 'zh' else f"Nice {weather} day at {location}"
        detailed_content = f"船长日志 - {location}\n\n今日{weather}，{time_period}时分抵达{location}。{culture}\n\n这里的文化氛围让我印象深刻，当地人民热情好客。船只状况良好，补给充足。明日将继续我们的航程。"
    
    # 生成图像提示词
    cultural_elements = {
        "青岛": "德式建筑，青岛啤酒厂，红瓦绿树，海滨栈桥" if language == 'zh' else "German architecture, Tsingtao brewery, red tiles and green trees, seaside pier",
        "上海": "外滩万国建筑，东方明珠塔，黄浦江夜景，现代摩天大楼" if language == 'zh' else "Bund international architecture, Oriental Pearl Tower, Huangpu River night view, modern skyscrapers",
        "厦门": "鼓浪屿，南普陀寺，环岛路，闽南建筑" if language == 'zh' else "Gulangyu Island, Nanputuo Temple, Huandao Road, Minnan architecture",
        "广州": "广州塔，珠江夜景，骑楼建筑，早茶文化" if language == 'zh' else "Canton Tower, Pearl River night view, Qilou architecture, morning tea culture",
        "南海中部": "蔚蓝海水，海鸥飞翔，远山如黛，海天一色" if language == 'zh' else "azure waters, seagulls flying, distant mountains, sea and sky merge",
        "胡志明市港": "法式殖民建筑，湄公河三角洲，热带植物，摩托车流" if language == 'zh' else "French colonial architecture, Mekong Delta, tropical plants, motorcycle traffic",
        "泰国湾": "椰林海滩，渔船点点，热带风情，碧海蓝天" if language == 'zh' else "coconut palm beaches, fishing boats, tropical atmosphere, blue sea and sky",
        "林查班港": "佛教寺庙，现代集装箱码头，热带花卉，泰式建筑" if language == 'zh' else "Buddhist temples, modern container terminals, tropical flowers, Thai architecture",
        "马六甲海峡北部": "繁忙航道，货轮如织，海上丝路，国际贸易" if language == 'zh' else "busy shipping lanes, cargo ships, maritime silk road, international trade",
        "巴生港": "马来传统建筑，清真寺尖塔，热带雨林，多元文化" if language == 'zh' else "traditional Malay architecture, mosque minarets, tropical rainforest, multicultural",
        "马六甲海峡中部": "历史航道，古代商船，香料贸易，文化交融" if language == 'zh' else "historic shipping route, ancient merchant ships, spice trade, cultural fusion",
        "爪哇海": "印尼群岛，火山岛屿，热带海洋，传统帆船" if language == 'zh' else "Indonesian archipelago, volcanic islands, tropical ocean, traditional sailing boats",
        "丹戎不碌港": "印尼传统建筑，热带港口，香料市场，群岛风情" if language == 'zh' else "Indonesian traditional architecture, tropical port, spice markets, archipelago atmosphere",
        "印度洋东部": "广阔海域，季风云彩，海豚跃起，无垠蓝色" if language == 'zh' else "vast ocean, monsoon clouds, dolphins leaping, endless blue",
        "香港": "维多利亚港夜景，摩天大楼，中式帆船，天星小轮" if language == 'zh' else "Victoria Harbor night view, skyscrapers, Chinese junks, Star Ferry",
        "新加坡": "滨海湾金沙，鱼尾狮，热带植物" if language == 'zh' else "Marina Bay Sands, Merlion, tropical plants",
        "科伦坡": "佛教寺庙，香料市场，锡兰茶园" if language == 'zh' else "Buddhist temples, spice markets, Ceylon tea gardens",
        "孟买": "宝莱坞电影海报，印度门，彩色纱丽" if language == 'zh' else "Bollywood movie posters, Gateway of India, colorful saris",
        "霍尔木兹海峡": "蔚蓝海水，油轮船队，波斯湾风光，海上贸易通道" if language == 'zh' else "azure waters, oil tanker fleets, Persian Gulf scenery, maritime trade corridor",
        "迪拜": "哈利法塔，黄金市场，阿拉伯帆船" if language == 'zh' else "Burj Khalifa, gold souk, Arabian dhows",
        "亚丁湾": "红海入口，商船队列，海上丝路，阿拉伯海风光" if language == 'zh' else "Red Sea entrance, merchant ship convoys, maritime silk road, Arabian Sea scenery",
        "苏伊士运河": "运河船闸，沙漠骆驼，古埃及元素" if language == 'zh' else "canal locks, desert camels, ancient Egyptian elements",
        "比雷埃夫斯港": "帕特农神庙，橄榄树，古希腊柱式" if language == 'zh' else "Parthenon temple, olive trees, ancient Greek columns",
        "威尼斯": "贡多拉，圣马可广场，文艺复兴建筑" if language == 'zh' else "gondolas, St. Mark's Square, Renaissance architecture"
    }
    
    cultural_element = cultural_elements.get(location, "传统建筑，当地特色" if language == 'zh' else "traditional architecture, local characteristics")
    
    image_prompt = IMAGE_PROMPT_TEMPLATE[language].format(
        location=location,
        weather=weather,
        time_period=time_period,
        cultural_elements=cultural_element
    )
    
    # 调用硅基流动API生成图像
    image_url = None
    if SILICONFLOW_CONFIG["api_key"] != "YOUR_API_KEY_HERE":
        image_url = call_siliconflow_image(image_prompt)
    
    return jsonify({
        'waypoint_index': waypoint_index,
        'location': location,
        'culture': culture,
        'weather': weather,
        'time_period': time_period,
        'short_content': short_content,  # 简短版日志（15-25字）
        'detailed_content': detailed_content,  # 详细版日志（150-200字）
        'content': detailed_content,  # 保持向后兼容
        'log_content': detailed_content,  # 保持向后兼容
        'image_prompt': image_prompt,
        'image_url': image_url,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    app.run(debug=True)