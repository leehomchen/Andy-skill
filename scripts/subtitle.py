#!/usr/bin/env python3
"""字幕生成工具

两种模式：
  A. 从视频/音频用 ASR 自动生成字幕（需 pip install faster-whisper）：
     python3 subtitle.py --audio input.mp4 --lang zh --out subtitle.srt
  B. 从带时间轴的脚本文本生成字幕（精准可控，无需 ASR）：
     python3 subtitle.py --from-script script_timed.txt --out subtitle.srt

  script_timed.txt 每行格式： 开始秒|结束秒|文字
     0.0|2.5|你还在为获客发愁吗
     2.5|5.0|试试这个AI神器
"""
import argparse
import sys


def ts_to_srt(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(segments, out):
    with open(out, "w", encoding="utf-8") as f:
        for i, (start, end, text) in enumerate(segments, 1):
            f.write(f"{i}\n{ts_to_srt(start)} --> {ts_to_srt(end)}\n{text}\n\n")
    print(f"✓ 字幕已生成: {out}（{len(segments)} 条）")


def from_script(path, out):
    segments = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("|", 2)
            if len(parts) != 3:
                print(f"跳过格式错误的行: {line}")
                continue
            try:
                segments.append((float(parts[0]), float(parts[1]), parts[2]))
            except ValueError:
                print(f"跳过时间错误的行: {line}")
    write_srt(segments, out)


def from_asr(audio, lang, out):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("缺少依赖，请先运行: pip3 install faster-whisper")
    print(f"正在识别音频: {audio} ...")
    model = WhisperModel("small", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio, language=lang, beam_size=5)
    result = [(seg.start, seg.end, seg.text.strip()) for seg in segments]
    write_srt(result, out)


def main():
    parser = argparse.ArgumentParser(description="视频字幕生成工具")
    parser.add_argument("--audio", help="视频或音频文件（ASR 模式）")
    parser.add_argument("--lang", default="zh", help="识别语言（默认 zh）")
    parser.add_argument("--from-script", help="带时间轴的脚本文本（精准模式）")
    parser.add_argument("--out", default="subtitle.srt", help="输出 SRT 文件")
    args = parser.parse_args()

    if args.from_script:
        from_script(args.from_script, args.out)
    elif args.audio:
        from_asr(args.audio, args.lang, args.out)
    else:
        parser.error("请提供 --audio 或 --from-script")


if __name__ == "__main__":
    main()
