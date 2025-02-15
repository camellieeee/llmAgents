from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import os

class WechatVideoDownloader:
    def __init__(self):
        print("正在初始化下载器...")
        # 配置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')  # 禁用扩展
        chrome_options.add_argument('--disable-software-rasterizer')  # 禁用软件光栅化
        
        # 特别针对 M1/M2 Mac 的配置
        chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        
        # 初始化Chrome浏览器
        try:
            print("正在启动Chrome浏览器...")
            from webdriver_manager.chrome import ChromeDriverManager
            
            # 使用简化的 ChromeDriver 初始化方式
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("Chrome浏览器启动成功！")
        except Exception as e:
            print(f"初始化Chrome浏览器失败: {str(e)}")
            print("错误详情:", e.__class__.__name__)
            print("请确保已经安装了Chrome浏览器")
            raise
            
        self.wait = WebDriverWait(self.driver, 10)
        
    def login(self):
        """登录微信视频号"""
        print("正在打开微信视频号登录页面...")
        self.driver.get("https://channels.weixin.qq.com/")
        print("请在浏览器中扫描二维码登录...")
        # 等待用户手动扫码登录
        time.sleep(20)
        print("登录等待时间结束，继续执行...")
        
    def download_video(self, video_url, save_path="downloads"):
        """下载指定URL的视频"""
        try:
            # 创建保存目录
            if not os.path.exists(save_path):
                os.makedirs(save_path)
                
            # 打开视频页面
            self.driver.get(video_url)
            
            # 等待视频元素加载
            video_element = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "video"))
            )
            
            # 获取视频源URL
            video_src = video_element.get_attribute("src")
            
            if video_src:
                # 生成文件名
                filename = f"video_{int(time.time())}.mp4"
                filepath = os.path.join(save_path, filename)
                
                # 下载视频
                print(f"开始下载视频: {filename}")
                response = requests.get(video_src, stream=True)
                
                with open(filepath, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            
                print(f"视频下载完成: {filepath}")
                return filepath
            else:
                print("未找到视频源URL")
                return None
                
        except Exception as e:
            print(f"下载视频时出错: {str(e)}")
            return None
            
    def close(self):
        """关闭浏览器"""
        self.driver.quit()

def main():
    # 使用示例
    downloader = WechatVideoDownloader()
    try:
        # 登录
        downloader.login()
        
        # 这里替换为实际的视频URL
        video_url = input("请输入视频号视频链接: ")
        
        # 下载视频
        downloaded_file = downloader.download_video(video_url)
        
        if downloaded_file:
            print(f"视频已保存到: {downloaded_file}")
        
    finally:
        downloader.close()

if __name__ == "__main__":
    main()
