from moviepy.editor import VideoFileClip
import os

def extract_audio(video_path):
    # 获取视频文件名（不含扩展名）
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    
    # 设置输出音频路径
    audio_path = f"{video_name}.mp3"
    
    # 加载视频并提取音频
    video = VideoFileClip(video_path)
    audio = video.audio
    
    # 保存音频文件
    audio.write_audiofile(audio_path)
    
    # 关闭视频对象
    video.close()
    
    return audio_path

if __name__ == "__main__":
    video_path = "/Users/yao/Downloads/20250215.mp4"
    audio_path = extract_audio(video_path)
    print(f"音频已成功提取并保存到: {audio_path}")
