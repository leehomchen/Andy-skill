#!/usr/bin/env python3
"""配音生成工具 - 基于 edge-tts（微软在线 TTS，免费、中文音色自然）

用法示例：
  python3 tts.py --list
  python3 tts.py --text "你好，欢迎观看" --voice zh-CN-YunxiNeural --out narration.mp3
  python3 tts.py --file script.txt --voice zh-CN-XiaoxiaoNeural --rate +10% --out narration.mp3
"""
import argparse
import asyncio
import sys

try:
    import edge_tts
except ImportError:
    sys.exit("缺少依赖，请先运行: pip3 install edge-tts")


async def text_to_speech(text, voice, rate, out):
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(out)
    print(f"✓ 配音已生成: {out}")


async def list_voices():
    voices = await edge_tts.list_voices()
    print("可用中文音色：")
    for v in voices:
        if v["Locale"].startswith("zh-CN"):
            print(f"  {v['ShortName']:<40} {v['Gender']}")


def main():
    parser = argparse.ArgumentParser(description="视频配音生成工具")
    parser.add_argument("--list", action="store_true", help="列出可用中文音色")
    parser.add_argument("--text", help="要配音的文本")
    parser.add_argument("--file", help="从文本文件读取配音内容")
    parser.add_argument("--voice", default="zh-CN-YunxiNeural", help="音色（默认云希）")
    parser.add_argument("--rate", default="+0%", help="语速，如 +10%% / -10%%")
    parser.add_argument("--out", default="narration.mp3", help="输出音频文件")
    args = parser.parse_args()

    if args.list:
        asyncio.run(list_voices())
        return

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        parser.error("请提供 --text 或 --file，或使用 --list 查看音色")

    asyncio.run(text_to_speech(text, args.voice, args.rate, args.out))


if __name__ == "__main__":
    main()
