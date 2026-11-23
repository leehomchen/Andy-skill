#!/usr/bin/env python3
"""视频合成工具 - 把画面、配音、BGM、字幕合成为成片

依赖：ffmpeg（需支持 libx264 或 libopenh264）

用法示例：
  python3 compose.py --video footage.mp4 --audio narration.mp3 \
      --bgm bgm.mp3 --bgm-volume 0.15 --subtitle subtitle.srt --out final.mp4

  # 竖版 9:16（抖音/视频号）
  python3 compose.py --video footage.mp4 --audio narration.mp3 --vertical --out final.mp4

  # 片尾合成品牌文字（避免 AI 渲染错字）
  python3 compose.py --video footage.mp4 --audio narration.mp3 \
      --title "麒运天祥" --title-sub "与AI同行 · 创未来" --out final.mp4
"""
import argparse
import subprocess
import shutil
import sys


def _has_encoder(name):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True)
    return name in r.stdout


def run(cmd):
    print("执行:", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("FFmpeg 报错:\n", result.stderr[-1500:])
        sys.exit(1)
    print("✓ 合成完成:", cmd[-1])


def pick_font():
    candidates = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "C:/Windows/Fonts/msyhbd.ttc",
    ]
    for p in candidates:
        import os
        if os.path.exists(p):
            return p
    return None


def main():
    parser = argparse.ArgumentParser(description="视频合成工具")
    parser.add_argument("--video", required=True, help="画面素材")
    parser.add_argument("--audio", help="配音音频")
    parser.add_argument("--bgm", help="背景音乐")
    parser.add_argument("--bgm-volume", default="0.15", help="BGM 音量 0-1（默认0.15）")
    parser.add_argument("--subtitle", help="SRT 字幕文件")
    parser.add_argument("--vertical", action="store_true", help="转为竖版 9:16")
    parser.add_argument("--title", help="片尾主标题文字")
    parser.add_argument("--title-sub", help="片尾副标题文字")
    parser.add_argument("--out", default="final.mp4", help="输出文件")
    args = parser.parse_args()

    if not shutil.which("ffmpeg"):
        sys.exit("未找到 ffmpeg，请先安装")

    # 构建 filter_complex
    filters = []
    inputs = ["-i", args.video]
    if args.audio:
        inputs += ["-i", args.audio]
    if args.bgm:
        inputs += ["-stream_loop", "-1", "-i", args.bgm]

    audio_idx = 1 if args.audio else None
    bgm_idx = 2 if (args.audio and args.bgm) else (1 if args.bgm else None)

    # 视频处理链
    vchain = ["[0:v]"]
    if args.vertical:
        vchain.append("scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,")
    # 字幕烧录（SRT 路径需转义）
    if args.subtitle:
        srt = args.subtitle.replace("\\", "/").replace(":", "\\:")
        vchain.append(f"subtitles='{srt}':force_style='FontName=Noto Sans CJK SC,FontSize=28',")
    # 片尾标题（在最后 2 秒显示）
    if args.title:
        font = pick_font()
        font_arg = f"fontfile={font}:" if font else ""
        vchain.append(
            f"drawtext={font_arg}text='{args.title}':fontsize=90:fontcolor=0xFFD700:"
            "x=(w-text_w)/2:y=(h-text_h)/2:alpha='if(lt(t,8),0,1)',"
        )
    if args.title_sub:
        font = pick_font()
        font_arg = f"fontfile={font}:" if font else ""
        vchain.append(
            f"drawtext={font_arg}text='{args.title_sub}':fontsize=40:fontcolor=white:"
            "x=(w-text_w)/2:y=(h-text_h)/2+90:alpha='if(lt(t,8.3),0,1)',"
        )

    vstr = "".join(vchain).rstrip(",")
    # 若没有任何滤镜，补一个 null
    if len(vchain) == 1:
        vstr = "[0:v]null"
    filters.append(f"{vstr}[vout]")

    # 音频处理链
    amap = ""
    if args.audio and args.bgm:
        filters.append(
            f"[{audio_idx}:a]aresample=async=1[a1];"
            f"[{bgm_idx}:a]volume={args.bgm_volume}[b1];"
            "[a1][b1]amix=inputs=2:duration=first:dropout_transition=2[aout]"
        )
        amap = "-map [aout]"
    elif args.audio:
        amap = f"-map {audio_idx}:a"
    elif args.bgm:
        filters.append(f"[{bgm_idx}:a]volume={args.bgm_volume}[aout]")
        amap = "-map [aout]"

    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", ";".join(filters),
        "-map", "[vout]",
    ]
    if amap:
        cmd += amap.split()
    # 优先用 libx264，没有则回退 libopenh264
    enc = "libx264" if _has_encoder("libx264") else "libopenh264"
    cmd += [
        "-c:v", enc, "-b:v", "6M", "-c:a", "aac", "-b:a", "128k",
        "-shortest", args.out,
    ]
    run(cmd)


if __name__ == "__main__":
    main()
