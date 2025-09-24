
import requests
from bs4 import BeautifulSoup
import json
import time
import random
from urllib.parse import quote

class ComfyUIAmazonScraper:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "search_query": ("STRING", {"multiline": False, "default": ""}),
                "max_results": ("INT", {"default": 10, "min": 1, "max": 50, "step": 1}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_output",)

    FUNCTION = "scrape_products"

    CATEGORY = "Amazon"

    def scrape_products(self, search_query, max_results):
        # 编码搜索关键词
        encoded_query = quote(search_query)
        search_url = f"https://www.amazon.com/s?k={encoded_query}"

        # 设置请求头，模拟浏览器访问
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Connection": "keep-alive",
            "Referer": "https://www.amazon.com/",
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1"
        }

        try:
            # 添加随机延迟
            time.sleep(random.uniform(1, 3))

            # 发送HTTP请求
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()

            # 解析HTML
            soup = BeautifulSoup(response.text, "lxml")

            # 提取商品数据
            products = []
            for item in soup.select("div[data-component-type=\'s-search-result\"]")[:max_results]:
                # 获取图片元素
                img_element = item.find("img", {"class": "s-image"})
                if img_element:
                    # 提取高清大图的URL（替换默认的缩略图URL）
                    img_url = img_element.get("src", "").replace("._AC_UL320_.", "._AC_UL1500_.")
                    detail_url = "https://www.amazon.com" + item.find("a", {"class": "a-link-normal s-no-outline"}).get("href", "")
                    name = item.find("span", {"class": "a-size-medium"}).text.strip() if item.find("span", {"class": "a-size-medium"}) else ""
                    price = item.find("span", {"class": "a-offscreen"}).text.strip() if item.find("span", {"class": "a-offscreen"}) else ""

                    products.append({
                        "image_url": img_url,
                        "detail_url": detail_url,
                        "name": name,
                        "price": price
                    })

            return (json.dumps(products, indent=2),)

        except requests.exceptions.HTTPError as e:
            return (json.dumps({"error": f"HTTP请求失败: {e}"}, indent=2),)
        except Exception as e:
            return (json.dumps({"error": f"发生错误: {e}"}, indent=2),)




NODE_CLASS_MAPPINGS = {
    "MYJ_FFaceBeautyNode": ComfyUIAmazonScraper
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MYJ_FaceBeautyNode": "AmazonImg"
}