import requests
from bs4 import BeautifulSoup
import time

# 替换为你的 PushPlus token
PUSH_TOKEN = "7a081d9626ca483098b19d4575866508"

# 央行公告页面（公开市场业务公告）
URL = "https://www.pbc.gov.cn/zhengcehuobisi/125207/125213/125431/125475/index.html"

last_title = ""

def get_latest_title():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0"
    }
    try:
        r = requests.get(URL, headers=headers)
        r.encoding = "utf-8"

        soup = BeautifulSoup(r.text, "lxml")

        # 找到所有 istitle="true" 的 a 标签
        first = soup.find("a", attrs={"istitle": "true"})

        title = first.text.strip() if first else None
        link = ("https://www.pbc.gov.cn" + first["href"]) if first and first.has_attr("href") else None

        print("标题:", title)
        print("链接:", link)
        return title, link
    except Exception as e:
        print(f"获取标题时出错: {e}")
        return None, None

def send_push(title, link):
    if not title or not link:
        return

    api = "http://www.pushplus.plus/send"

    content = f"""
    <b>{title}</b><br><br>
    <a href="{link}">点击查看央行原文公告</a>
    """

    data = {
        "token": PUSH_TOKEN,
        "title": "央行公开市场公告更新",
        "content": content,
        "template": "html"
    }

    try:
        response = requests.post(api, json=data, timeout=10)
        print("推送结果:", response.text)
    except Exception as e:
        print("推送失败:", e)

while True:
    try:
        title, link = get_latest_title()
        if title:
            print("当前公告为:", title)
            send_push(title, link)
            if title != last_title:
                print("发现新公告:", title)
                # send_push(title, link)
                last_title = title
            else:
                print("公告标题未更新")
        else:
            print("未能获取到最新公告标题")

        time.sleep(30)

    except Exception as e:
        print("循环中发生错误:", e)
        time.sleep(10)