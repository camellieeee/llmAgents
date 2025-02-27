## LLM Agents Collection

This repository contains a collection of custom-built LLM (Language Learning Model) agents designed to perform various tasks. These agents leverage advanced natural language processing techniques and are intended to serve as a flexible, extensible framework for a variety of applications.

## License

This project is licensed under the MIT License.

## 视频转markdown

这个工具使用 OpenAI 的 Whisper 模型将视频文件中的语音内容转录为带时间戳的 Markdown 文档。

### 安装依赖

在使用脚本之前，您需要安装以下依赖项：

1. 安装所需的 Python 包：
   ```bash
   pip install openai tqdm
   ```


注意：Whisper 模型可能需要额外的依赖项，如 FFmpeg。如果您在运行时遇到相关错误，请安装 FFmpeg：

- **Windows**：通过 [官方网站](https://ffmpeg.org/download.html) 下载并添加到系统路径
- **macOS**：`brew install ffmpeg`
- **Linux**：`sudo apt install ffmpeg` 或 `sudo yum install ffmpeg`

### 使用方法

1. 运行 video2md.py 脚本：
    ```bash
    python video2md.py
    ```

2. 当提示输入视频文件路径时，输入您要转录的视频文件的完整路径
3. 脚本将开始处理视频，并显示进度条
4. 处理完成后，转录文本将保存在与视频文件相同目录下的同名 .md 文件中

### 输出格式

生成的 Markdown 文件将包含时间戳和对应的文本内容，格式如下：
00:00:00 - 00:00:05
这是第一段转录的文本内容。
00:00:05 - 00:00:10
这是第二段转录的文本内容。


### 注意事项

- 首次运行时，脚本会下载 Whisper 的 "large" 模型（约 1.5GB），这可能需要一些时间
- 转录过程可能会占用大量 CPU 或 GPU 资源，具体取决于您的硬件配置
- 如果您的视频文件较大，转录过程可能需要较长时间
- 脚本支持多种语言的自动识别和转录