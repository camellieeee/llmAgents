import json
import requests
import time
import os
from flask import Flask, request

app = Flask(__name__)

class WeworkBot:
    def __init__(self):
        # 企业微信配置
        self.corp_id = "wwada01e259cf439be"
        self.secret = "IPQ9ZpO2TF7hmoTaKGW8l_obi6gDYzxHSeBHwI0r_ec"
        self.token = None
        self.token_expires_time = 0
        
    def get_access_token(self):
        """获取访问令牌"""
        if self.token and time.time() < self.token_expires_time:
            return self.token
            
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.corp_id}&corpsecret={self.secret}"
        response = requests.get(url)
        data = response.json()
        
        if data["errcode"] == 0:
            self.token = data["access_token"]
            self.token_expires_time = time.time() + data["expires_in"] - 200  # 提前200秒更新
            return self.token
        else:
            raise Exception(f"获取access_token失败: {data}")
            
    def download_video(self, media_id, save_path="downloads"):
        """下载视频"""
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            
        access_token = self.get_access_token()
        url = f"https://qyapi.weixin.qq.com/cgi-bin/media/get?access_token={access_token}&media_id={media_id}"
        
        response = requests.get(url)
        
        # 从响应头中获取文件名
        content_disposition = response.headers.get('content-disposition')
        if content_disposition:
            filename = content_disposition.split('filename=')[-1].strip('"')
        else:
            filename = f"video_{int(time.time())}.mp4"
            
        filepath = os.path.join(save_path, filename)
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
            
        return filepath

bot = WeworkBot()

@app.route('/webhook', methods=['POST'])
def webhook():
    """处理企业微信消息"""
    data = request.json
    
    # 处理视频消息
    if data.get('MsgType') == 'video':
        media_id = data.get('MediaId')
        if media_id:
            try:
                filepath = bot.download_video(media_id)
                return json.dumps({
                    "errcode": 0,
                    "errmsg": "ok",
                    "filepath": filepath
                })
            except Exception as e:
                return json.dumps({
                    "errcode": 1,
                    "errmsg": str(e)
                })
                
    return json.dumps({"errcode": 0, "errmsg": "ok"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000) 