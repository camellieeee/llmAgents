import warnings
import whisper
import os
from datetime import timedelta
from tqdm import tqdm

# Suppress FP16 warning on CPU
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

def extract_audio_to_md(video_path):
    # 检查文件是否存在
    if not os.path.exists(video_path):
        print(f"错误: 文件 '{video_path}' 不存在")
        return
    
    # 加载模型
    model = whisper.load_model("large")
    
    # 转录音频
    result = model.transcribe(video_path, verbose=False)
    
    # 生成markdown文件路径（与视频文件同目录）
    video_dir = os.path.dirname(video_path)
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    md_file = os.path.join(video_dir, f"{base_name}.md")
    
    # 写入markdown文件并显示进度条
    with open(md_file, "w", encoding="utf-8") as f:
        with tqdm(total=len(result["segments"]), desc="Transcribing", unit="segment") as pbar:
            for segment in result["segments"]:
                start_time = str(timedelta(seconds=int(segment["start"])))
                end_time = str(timedelta(seconds=int(segment["end"])))
                text = segment["text"]
                
                f.write(f"### {start_time} - {end_time}\n")
                f.write(f"{text}\n\n")
                pbar.update(1)
    
    print(f"音频已成功转录并保存为 {md_file}")

if __name__ == "__main__":
    video_path = input("请输入视频文件路径: ")
    # 去除可能的引号
    video_path = video_path.strip("'\"")
    extract_audio_to_md(video_path)
