# 当前 deck 使用的媒体

这里只保留“纵置二轮车自动驾驶技术”deck 当前引用的素材。`slides.md` 中的 `src`、`poster`、`href` 是清理依据；点击打开的原始文件也属于有效引用。

| 目录 | 内容 |
| --- | --- |
| `videos/terrain/` | 道路、砾石、草地、坡道、台阶、负载实车视频 |
| `videos/simulation/` | 平坦地形与台阶仿真视频 |
| `videos/platforms/` | E-bike 与电摩演示 |
| `videos/navigation/` | 视觉车道保持视频 |
| `videos/showcase/` | 科交会综合演示视频 |
| `posters/` | 对应视频封面帧，按同样的用途分类 |
| `images/cover/` | 封面拼图 |
| `diagrams/` | 可编辑 SVG 示意图 |
| `figures/comparison/` | 技术路线对比配图 |
| `figures/cyclex/` | CycleX 论文配图与可点击的图表 PDF |
| `profiles/` | 使用中的透明背景人物照片 |
| `logos/` | 院系标识 |
| `patents/previews/` | 四张专利首页预览 |
| `awards/documents/` | 可点击的原始证书 PDF |
| `awards/previews/` | 四张证书预览 |
| `awards/photos/` | 两张颁奖现场照片 |

## 维护

- 视频使用 H.264 / yuv420p MP4，最高 720p，不放大低分辨率素材，保留时长与音轨；`faststart` 优化网页加载。
- 压缩结果只有在体积更小时才替换现有文件；现有链接与文件名保持稳定。
- 新文件按用途分类，优先采用英文小写连字符命名；中文原有名称保持可追溯。
- 视频和封面帧尽量同名；`posters/platforms/LEQI.jpg` 对应 `videos/platforms/e-bike-demo.mp4`。
- 未引用的原片、人物原图、补充图片和专利 PDF 已删除。证书 PDF 和 CycleX 图表 PDF 因被链接引用而保留。
- 删除素材前检查所有实际引用；证书 PDF 链接中的 `#page=1` / `#page=2` 应保留。

[视频压缩记录](../docs/media-optimization.json) · [删除记录](../docs/media-cleanup.json) · [历史路径迁移记录](../docs/media-path-map.json)

历史提纲、旧快照及既有 QA 文件描述的是当时的素材；其中的原件路径可能已失效。
