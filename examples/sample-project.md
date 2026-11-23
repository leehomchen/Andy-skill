# 完整示例：30 秒企业品牌宣传片

以虚构品牌「麒运天祥」为例，演示从选题到成片的全流程。

## ① 策划简报

| 要素 | 内容 |
|---|---|
| 目标 | 品牌宣传，塑造大气、科技、有活力的企业形象 |
| 平台 | 企业微信群 + 视频号（16:9 横版，另出 9:16 竖版） |
| 时长 | 30 秒 |
| 风格 | 激情燃向 · 黑金电影质感 |
| 受众 | 客户、合作伙伴、求职者 |
| 画面 | 纯 AI 生成 + 后期文字合成 |

## ② 分镜脚本

| 镜号 | 时长 | 画面描述 | 口播/文案 | 字幕 | 音效/BGM |
|---|---|---|---|---|---|
| 1 | 0-4s | 深空黑金，星尘旋转汇聚，一道金光划破夜幕 | （无口播，纯音乐） | — | 低频轰鸣 + 鼓点起 |
| 2 | 4-10s | 金色麒麟踏火焰光轨从远处奔来，鳞片流光 | 麒麟踏光而来 | 麒麟踏光而来 | 弦乐渐强 |
| 3 | 10-16s | 麒麟跃起，化作漫天金色光屑炸开 | 汇聚成势，一往无前 | 汇聚成势 | 鼓点密集 |
| 4 | 16-23s | 光屑旋转汇聚成能量漩涡，光芒万丈 | 麒运汇聚，运势腾飞 | 麒运汇聚 | 高潮 |
| 5 | 23-30s | 金色大字 Logo 定格 + 副标题 | 麒运天祥，与AI同行 | 麒运天祥 | 有力收束 |

## ③ 配音

```bash
python3 scripts/tts.py --file script.txt --voice zh-CN-YunjianNeural --rate +8% --out narration.mp3
```

script.txt 内容（仅口播部分，逐行）：
```
麒麟踏光而来
汇聚成势，一往无前
麒运汇聚，运势腾飞
麒运天祥，与AI同行
```

## ④ 字幕

```bash
python3 scripts/subtitle.py --from-script script_timed.txt --out subtitle.srt
```

script_timed.txt：
```
4.0|10.0|麒麟踏光而来
10.0|16.0|汇聚成势，一往无前
16.0|23.0|麒运汇聚，运势腾飞
23.0|30.0|麒运天祥，与AI同行
```

## ⑤ 合成

```bash
# 画面素材 footage.mp4 由视频生成工具产出（提示词见分镜"画面描述"列）
python3 scripts/compose.py \
  --video footage.mp4 \
  --audio narration.mp3 \
  --bgm epic_bgm.mp3 --bgm-volume 0.15 \
  --subtitle subtitle.srt \
  --title "麒运天祥" --title-sub "与AI同行 · 创未来" \
  --out final.mp4

# 另出竖版
python3 scripts/compose.py --video footage.mp4 --audio narration.mp3 --vertical --out final_vertical.mp4
```

## 关键经验

1. **文字不交给 AI 渲染**：片尾「麒运天祥」用 `--title` 参数后期合成，字形准确
2. **BGM 压低**：0.15 音量，人声清晰
3. **卡点**：转场对齐鼓点（4s/10s/16s/23s）
4. **竖版适配**：横版素材裁成 9:16 时主体要居中，避免裁掉主体
