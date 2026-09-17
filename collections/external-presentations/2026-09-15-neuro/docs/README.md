# 演示稿维护

入口：`../index.html`；正文与备注：`../slides.md`；局部样式/行为：`../presentation.css`、`../presentation.js`。

12页，6个横向位置。`===` 为横向分隔，`==` 为纵向分隔，`Note:` 后为演讲备注。无额外纯章节标题页。

本deck复用仓库共享 `dist/`、`plugin/`；没有改动框架、门户或其他deck。门户原有draft标签本次未修改，以遵守仅在本deck内写入的要求。

- `待补充材料.md`：需团队补充的数据、客户信息、工程和融资资料。
- `证据核对.md`：逐页证据与来源边界。
- `build-diagrams.py`：重新生成6张可编辑SVG；运行前注意保留手工编辑的SVG。
- `qa/check.cjs`：通过本地Chrome检查12页图片加载、溢出、视频播放和Escape概览。默认预览地址为localhost:8017。
- `qa/validation.json`：浏览器验证结果；`qa/slide-*.png`：逐页截图。

本机预览可用仓库根目录 `npm start -- --port 8017 --livereload-port 35731`，然后打开deck路径。若服务已运行，直接复用。Markdown通过HTTP读取，不使用file://。

浏览器原生播放请求在离开视频页或暂停时可能产生AbortError；验证脚本单独记录该取消事件，仍独立验证视频实际自动播放、静音和跨结尾循环。不修改共享Reveal源代码来处理该日志。

## 多主题预览

默认使用 black。可通过 `index.html?theme=white` 或 `index.html?theme=serif` 预览，也支持直接修改 `#theme` 样式表链接；11个内置主题均可使用，幻灯片 hash 可以照常附加。

`presentation.css` 使用语义颜色变量；`presentation.js` 根据 Reveal 的背景色选择浅色或深色配色，并为本 deck 的原创 SVG 生成浅色版本。原始 SVG 保持可编辑，照片、论文图及视频不重新着色。新增原创 SVG 时，在 `diagramNames` 中登记文件名，并按需补充 `lightDiagramColors`。

`docs/qa/themes.cjs` 在本地 8017 端口预览服务下检查全部主题的文本对比度、布局、图片加载、Escape 概览与视频行为。
