# Website
个人网站（Jemdoc 生成）

- 线上地址：`https://MurryAir.github.io/`
- 仓库：`https://github.com/MurryAir/MurryAir.github.io`

## 操作与发布记录
- 安装 Git：通过 `winget` 安装 `Git for Windows 2.51.1`。
- 初始化与提交：创建 `.nojekyll`、`.gitignore`，初始化仓库（默认分支 `main`），完成首次提交。
- 关联远端并推送：远端 `origin` 指向 `MurryAir/MurryAir.github.io`，推送 `main` 分支成功。
- 线上可访问验证：主页与各子页面返回 `200 OK`，主页内容包含 “Mu Jia”。
- 更新本地 Git 邮箱：将 `user.email` 更新为 `mujia1@link.cuhk.edu.cn`。
- 头像裁剪与替换：使用 `tools/crop_photo.py` 生成 `280x280` 正方形头像，生成文件 `photos/Mu Jia.jpg`，在 `index.jemdoc` 引用为 `280x280` 后重新生成首页。
- Publications 页面：将 `publications.jemdoc` 按 IEEE 引用格式整理，并为标题添加可点击链接；重新生成 `publications.html`。
- 全站重新编译：执行 `python jemdoc.py` 对 `index.jemdoc`、`publications.jemdoc`、`research_summary.jemdoc`、`awards.jemdoc` 进行重新生成；本地预览确认。
- 备注：`jemdoc.py` 运行过程中出现 `SyntaxWarning`（转义字符相关），但不影响 HTML 生成功能。

## 本地编译与预览
- 生成单页：`python jemdoc.py index.jemdoc`
- 生成多页：`python jemdoc.py index.jemdoc publications.jemdoc research_summary.jemdoc awards.jemdoc`
- 本地预览：`python -m http.server 8000`，浏览器打开 `http://localhost:8000/`

## 发布到 GitHub Pages
- 初始化（仅首次）：
  - `git init -b main`
  - 创建 `.nojekyll`、`.gitignore`（建议包含 `__pycache__/` 等）
  - `git remote add origin https://github.com/MurryAir/MurryAir.github.io.git`
- 推送：
  - `git add .`
  - `git commit -m "Update site content"`
  - `git push -u origin main`
- 生效时间：通常数秒至数分钟。

## Git 设置
- 用户名：`git config user.name "MurryAir"`
- 邮箱（已更新）：`git config user.email "mujia1@link.cuhk.edu.cn"`
- 如果刚安装 Git 后 `git` 命令暂不可用，重开终端或使用绝对路径：`C:\Program Files\Git\cmd\git.exe`

## 目录结构（摘要）
- 源文件：`*.jemdoc`
- 生成页面：`*.html`
- 样式：`jemdoc.css`
- 脚本：`jemdoc.py`、`tools/crop_photo.py`
- 资源：`photos/`