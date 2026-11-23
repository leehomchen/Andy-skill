# FFmpeg 常用配方

本机 ffmpeg 若无 libx264，用 libopenh264（`-c:v libopenh264 -b:v 6M`）替代即可。

## 视频裁剪 / 拼接

```bash
# 截取前 N 秒
ffmpeg -i in.mp4 -t 10 -c copy out.mp4

# 去掉片尾（保留前 17 秒）
ffmpeg -i in.mp4 -t 17 -c:v libx264 -c:a aac out.mp4

# 拼接多个片段（先写列表文件 list.txt）
# file '1.mp4'
# file '2.mp4'
ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4
```

## 画幅处理

```bash
# 竖版 9:16（居中裁切到 1080x1920）
ffmpeg -i in.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" out.mp4

# 横版 16:9
ffmpeg -i in.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080" out.mp4

# 压缩到 720P（手机流畅播放）
ffmpeg -i in.mp4 -vf "scale=1280:720" -c:v libx264 -b:v 3M -c:a aac -b:a 96k out.mp4
```

## 字幕烧录

```bash
# 烧录 SRT（中文字体需系统中存在）
ffmpeg -i in.mp4 -vf "subtitles=sub.srt:force_style='FontName=Noto Sans CJK SC,FontSize=28'" out.mp4
```

## 音频处理

```bash
# 提取音频
ffmpeg -i in.mp4 -vn -c:a libmp3lame out.mp3

# 音量调节（BGM 压到 0.15）
ffmpeg -i bgm.mp3 -af "volume=0.15" bgm_quiet.mp3

# 配音 + BGM 混合
ffmpeg -i voice.mp3 -i bgm.mp3 -filter_complex \
  "[1:a]volume=0.15[b];[0:a][b]amix=inputs=2:duration=first[a]" -map "[a]" out.mp3

# 去原声（用新音频替换）
ffmpeg -i video.mp4 -i new_audio.mp3 -c:v copy -map 0:v -map 1:a -shortest out.mp4
```

## 文字合成（避免 AI 渲染错字）

```bash
# 片尾金色标题（思源宋体）
ffmpeg -i in.mp4 -vf "drawtext=fontfile=/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc:text='麒运天祥':fontsize=140:fontcolor=0xFFD700:x=(w-text_w)/2:y=(h-text_h)/2:shadowcolor=black@0.7:shadowx=4:shadowy=5" out.mp4

# 带淡入（8 秒后显现）
...:alpha='if(lt(t,8),0,if(lt(t,9),t-8,1))'
```

## 去水印（无 delogo 滤镜时）

```bash
# 局部重度模糊（把水印区域缩放极小再放大铺回）
ffmpeg -i in.mp4 -filter_complex \
  "[0:v]split=2[a][b];[a]crop=340:85:380:322,scale=42:11,scale=340:85[patch];[b][patch]overlay=380:322" \
  -c:v libx264 out.mp4
```

## 排查

```bash
# 查看视频信息
ffprobe -v error -show_format -show_streams in.mp4

# 查看支持的编码器
ffmpeg -hide_banner -encoders | grep 264

# 查看支持的滤镜
ffmpeg -hide_banner -filters | grep -i subtitles
```
