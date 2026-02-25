import requests
from bs4 import BeautifulSoup
import time
import os
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 从环境变量读取 PushPlus token（本地测试时如未设置默认值）
PUSH_TOKEN = os.getenv("PUSH_TOKEN", "")

# 央行公告页面（公开市场业务公告）
URL = "https://www.pbc.gov.cn/zhengcehuobisi/125207/125213/125431/125475/index.html"

last_title = ""

def get_latest_title():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0"
    }
    try:
        r = requests.get(URL, headers=headers, timeout=10)
        r.encoding = "utf-8"

        soup = BeautifulSoup(r.text, "lxml")

        # 找到所有 istitle="true" 的 a 标签
        first = soup.find("a", attrs={"istitle": "true"})

        title = first.text.strip() if first else None
        link = ("https://www.pbc.gov.cn" + first["href"]) if first and first.has_attr("href") else None

        logger.info(f"获取到标题: {title}")
        if link:
            logger.info(f"链接: {link}")
        return title, link
    except Exception as e:
        logger.error(f"获取标题时出错: {e}")
        return None, None

def send_push(title, link):
    if nlogger.warning("标题或链接为空，跳过推送")
        return

    if not PUSH_TOKEN:
        logger.warning("PUSH_TOKEN 未设置，跳过推送")
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
def main():
    logger.info("启动央行公告监控服务")
    global last_title
    
    while True:
        try:
            title, link = get_latest_title()
            if title:
                logger.info(f"当前公告为: {title}")
                if title != last_title:
                    logger.info(f"发现新公告: {title}")
                    send_push(title, link)
                    last_title = title
                else:
                    logger.debug("公告标题未更新")
            else:
                logger.warning("未能获取到最新公告标题")

            time.sleep(30)

        except Exception as e:
            logger.error(f"循环中发生错误: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main(
        time.sleep(30)

    except Exception as e:
        print("循环中发生错误:", e)
        time.sleep(10)