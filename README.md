# Andy-skill · 视频工厂

> 一站式视频内容生产 Skill：从想法到成片的完整流水线。

## 是什么

这是一个 Agent Skill（智能体技能），让 AI 助手能够帮你完成视频制作的全流程：选题策划 → 脚本分镜 → 配音生成 → 字幕制作 → 画面合成。

## 能做什么

- 🎬 写视频脚本、分镜表、口播文案
- 🎙️ 生成中文配音（edge-tts，多种音色）
- 📝 生成 SRT 字幕（配音自动识别 或 脚本文本）
- 🎞️ 合成视频（画面 + 配音 + BGM + 字幕 + 片尾文字）
- 📱 横版/竖版自适应（抖音、视频号、B站等）

## 快速开始

把 `SKILL.md` 连同 `scripts/`、`references/`、`examples/` 目录一起放入你的 Agent skills 目录即可。AI 会在你说"做视频/写脚本/加字幕/配音"时自动调用。

```bash
# 安装依赖
pip3 install edge-tts faster-whisper
# ffmpeg（系统包管理器安装）
```

## 目录结构

```
.
├── SKILL.md                    # 技能主文件（触发条件 + 工作流）
├── scripts/
│   ├── tts.py                  # 配音生成
│   ├── subtitle.py             # 字幕生成
│   └── compose.py              # 视频合成
├── references/
│   ├── script-template.md      # 分镜脚本模板
│   ├── style-guide.md          # 文案风格指南
│   └── ffmpeg-recipes.md       # FFmpeg 常用配方
└── examples/
    └── sample-project.md       # 完整示例（30秒宣传片）
```

## 核心原则

> ⚠️ 中文字幕/Logo 一律后期用 `drawtext` 合成，**不要让 AI 直接渲染文字**（容易出错字）。

## License

MIT
