---
name: video-factory
description: 一站式视频内容工厂。当用户需要"做视频/生成视频/写视频脚本/写分镜/生成视频文案/加字幕/配音/配乐/剪辑合成视频"时使用本技能。覆盖从选题、脚本、配音、字幕、素材生成到最终合成的完整流水线。适用于短视频、宣传片、口播视频、教程视频、社交媒体内容的生产。
---

# 视频工厂 · Video Factory

把"一个想法"变成"一条成片"的完整流水线。分五个阶段执行，每个阶段都有明确的输入、产出和验收标准。

## 适用场景

- 短视频 / 宣传片 / 企业品牌片
- 口播视频 / 知识科普 / 教程
- 社交媒体内容（抖音、视频号、小红书、B站）
- 带货视频 / 产品介绍

## 五阶段流水线

```
① 选题策划 → ② 脚本分镜 → ③ 配音生成 → ④ 字幕制作 → ⑤ 画面合成
   (创意)       (文案)        (音频)        (文字)        (成片)
```

执行原则：**逐阶段推进，每阶段产出需用户确认后再进入下一阶段**。用户说"一条龙/全自动"时可连续执行，但关键节点（脚本、风格）仍应让用户确认，避免返工。

---

## 阶段 ① 选题策划

明确以下要素，信息不全时主动询问（不要臆造）：

| 要素 | 说明 | 示例 |
|---|---|---|
| 主题/目标 | 这条视频要达成什么 | 宣传品牌、卖货、科普 |
| 目标平台 | 决定画幅和时长 | 抖音=9:16竖版15-60s；B站=16:9横版 |
| 时长 | 短视频15-60s，宣传片30-90s | 30秒 |
| 风格基调 | 情绪和视觉方向 | 激情燃向 / 温情 / 科技感 / 搞笑 |
| 受众 | 影响措辞和节奏 | 年轻人 / 企业客户 / 家长 |
| 是否出镜/真人 | 决定是用 AI 画面还是素材 | 纯 AI 生成 / 真人 + 素材 |

产出：`策划简报`（一段话 + 上述要素表）。

## 阶段 ② 脚本分镜

按 `references/script-template.md` 的模板产出**分镜脚本表**。每一行是一个镜头，包含：

- **镜号**（序号）
- **时长**（秒，累加等于总时长）
- **画面描述**（视觉内容，用于生成素材或指导拍摄）
- **口播/文案**（配音文字）
- **字幕**（屏幕文字，可用关键词）
- **音效/BGM提示**

**文案黄金法则**：
1. 前3秒必须有"钩子"——悬念、冲突、利益点，否则完播率低
2. 一句一意，短句为主（单句≤20字）
3. 口语化，读出来顺口，避免书面长句
4. 结尾有明确 CTA（关注/下单/评论）

参考 `references/style-guide.md` 按风格调整措辞。

## 阶段 ③ 配音生成

优先使用 `scripts/tts.py`（基于 edge-tts，免费、中文音色自然）：

```bash
# 查看可用中文音色
python3 scripts/tts.py --list

# 生成配音（指定音色、语速、输出文件）
python3 scripts/tts.py --text "你的文案" --voice zh-CN-YunxiNeural --rate +10% --out narration.mp3

# 从脚本文案文件批量生成
python3 scripts/tts.py --file script.txt --voice zh-CN-XiaoxiaoNeural --out narration.mp3
```

常用音色：
| 音色 | 特点 | 适用 |
|---|---|---|
| `zh-CN-YunxiNeural` | 年轻男声，活泼 | 青年向、科技、运动 |
| `zh-CN-XiaoxiaoNeural` | 温柔女声 | 情感、生活、种草 |
| `zh-CN-YunjianNeural` | 浑厚男声 | 宣传片、正式、燃向 |
| `zh-CN-liaoning-XiaobeiNeural` | 东北女声 | 搞笑、接地气 |

- 语速 `--rate`：口播 +10%~+20%，宣传片 +0%~+10%
- 需要多角色时，分批生成再合成

## 阶段 ④ 字幕制作

方式 A —— **从配音自动生成字幕**（推荐，需 faster-whisper）：

```bash
python3 scripts/subtitle.py --audio narration.mp4 --lang zh --out subtitle.srt
```

方式 B —— **从脚本文案按时间轴生成**（精准可控）：

```bash
python3 scripts/subtitle.py --from-script script_timed.txt --out subtitle.srt
```

`script_timed.txt` 格式：每行 `开始秒数|结束秒数|文字`，例如：
```
0.0|2.5|你还在为获客发愁吗
2.5|5.0|试试这个AI神器
```

字幕规范参考 `references/ffmpeg-recipes.md`，烧录时中文用思源黑体/苹方，字号按画幅调整。

## 阶段 ⑤ 画面合成

**画面来源**（按优先级）：
1. AI 生成视频/图片（用图像/视频生成工具，注意：**文字不要交给 AI 渲染，易出错字**，改用后期精确合成）
2. 实拍素材 / 用户提供的素材
3. 免版权素材库（Pexels、Pixabay）

**合成命令**（调用 `scripts/compose.py`）：

```bash
# 画面 + 配音 + BGM + 字幕 一条龙合成
python3 scripts/compose.py \
  --video footage.mp4 \
  --audio narration.mp3 \
  --bgm bgm.mp3 --bgm-volume 0.15 \
  --subtitle subtitle.srt \
  --out final.mp4

# 竖版适配（9:16，用于抖音/视频号）
python3 scripts/compose.py --video footage.mp4 --audio narration.mp3 --vertical --out final_vertical.mp4
```

合成要点：
- BGM 音量压低（0.1~0.2），不能盖过人声
- 卡点：转场对齐 BGM 鼓点（在分镜阶段标注时间点）
- 输出 H.264 + AAC，保证各平台兼容
- 片尾 Logo/文字用 `drawtext` 后期合成，确保字形准确

## 重要提醒

1. **AI 渲染中文字易错**：凡是片名、Logo、关键文字，一律后期用 `drawtext` + 系统中文字体合成，不要用图像生成工具直接出字
2. **版权合规**：BGM 用免版权音乐；去水印视频仅供个人欣赏，公开发布需注明出处
3. **算力分工**：视频大模型生成本地吃力，优先调用云端生成 API；本地只做脚本、字幕、配音、剪辑合成
4. **画幅对照**：抖音/视频号/小红书=9:16；B站/YouTube/官网=16:9；朋友圈=1:1 或 9:16

## 配套文件

- `scripts/tts.py` — 配音生成
- `scripts/subtitle.py` — 字幕生成/烧录
- `scripts/compose.py` — 视频合成
- `references/script-template.md` — 分镜脚本模板
- `references/style-guide.md` — 文案风格指南
- `references/ffmpeg-recipes.md` — FFmpeg 常用配方
- `examples/sample-project.md` — 完整示例（30秒宣传片）
