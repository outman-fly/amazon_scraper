import requests
import re
import json
import time
import random
from urllib.parse import quote

class AmazonSearchScraper:
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

    RETURN_TYPES = ("STRING", "LIST", "LIST", "LIST",)
    RETURN_NAMES = ("products_json", "image_urls", "detail_urls", "prices",)

    FUNCTION = "scrape_amazon"
    CATEGORY = "Utils/Web"

    def scrape_amazon(self, search_query, max_results):
        encoded_query = quote(search_query)
        search_url = f"https://www.amazon.com/s?k={encoded_query}"

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

        products_data = []
        image_urls = []
        detail_urls = []
        prices = []

        try:
            time.sleep(random.uniform(1, 3))
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()

            img_pattern = re.compile(r'<img[^>]*src="([^"]*\._AC_UL320_[^"]*)"[^>]*>')
            url_pattern = re.compile(r'<a[^>]*class="a-link-normal s-no-outline"[^>]*href="([^"]*)"[^>]*>')
            price_pattern = re.compile(r'<span[^>]*class="a-offscreen"[^>]*>([^<]*)</span>')

            img_matches = img_pattern.findall(response.text)
            url_matches = url_pattern.findall(response.text)
            price_matches = price_pattern.findall(response.text)

            for i in range(min(max_results, len(img_matches))):
                hd_img_url = img_matches[i].replace("._AC_UL320_.", "._AC_UL1500_.")
                detail_url = "https://www.amazon.com" + url_matches[i] if i < len(url_matches) else ""
                price = price_matches[i] if i < len(price_matches) else "N/A"
                
                products_data.append({
                    "image_url": hd_img_url,
                    "detail_url": detail_url,
                    "price": price
                })
                image_urls.append(hd_img_url)
                detail_urls.append(detail_url)
                prices.append(price)

            return (json.dumps(products_data, indent=2), image_urls, detail_urls, prices,)

        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP请求失败: {e}"
            return (json.dumps({"error": error_msg}, indent=2), [], [], [],)
        except requests.exceptions.Timeout as e:
            error_msg = f"请求超时: {e}"
            return (json.dumps({"error": error_msg}, indent=2), [], [], [],)
        except requests.exceptions.RequestException as e:
            error_msg = f"网络请求异常: {e}"
            return (json.dumps({"error": error_msg}, indent=2), [], [], [],)
        except Exception as e:
            error_msg = f"发生错误: {e}"
            return (json.dumps({"error": error_msg}, indent=2), [], [], [],)

# ComfyUI 节点映射
NODE_CLASS_MAPPINGS = {
    "MYJ_FFaceBeautyNode": AmazonSearchScraper
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MYJ_FaceBeautyNode": "AmazonImg"
}
