# 书法生成

18页中文外部报告，约20–25分钟。白底、蓝色标题、1200×700画布。

## 编辑与预览

- `slides.md`：内容和讲稿。`===`分隔六个部分，`==`分隔同一部分的纵向页，`Note:`后为讲者备注。
- `docs/brief.md`：提纲和来源约定。
- `presentation.css` / `presentation.js`：布局、Markdown、备注、批注、放大预览配置。
- `media/diagrams/*.svg`：可编辑的预训练、笔导航、章法示意图。
- `media/data/results.json`：原表数值；`docs/evidence/asset-manifest.json`：源图与裁剪、字形映射。

从仓库根目录运行 `python3 -m http.server 8018 --bind 127.0.0.1`。
预览：http://127.0.0.1:8018/collections/external-presentations/calligraphy-generation/index.html

点击论文图和专利图可放大，Esc关闭；S打开讲者备注，批注插件沿用仓库设置。
所有演示图和字形均本地加载。院系链接需要网络。

验证：`node collections/external-presentations/calligraphy-generation/scripts/qa/check.cjs`（从仓库根目录运行，需Chrome及上述本地服务器）。
18页截图保存在`qa/screenshots/`，浏览器报告保存在`qa/reports/browser.json`。

## 六部分

I封面（1）；II背景（2）；III Fontify（3–8）；IV CalliPhase（9–14）；V下一步（15–17）；VI团队（18）。
Fontify采用KBS稿件；CalliPhase采用AuthorKit27-v2/main(15).tex。
230字体来自论文；20万余字形样本由用户提供。笔导航与章法为未来工作。

横向切换六部分；Fontify、CalliPhase和下一步各为纵向堆栈（6、6、3页），封面、合并后的背景与团队各1页。
