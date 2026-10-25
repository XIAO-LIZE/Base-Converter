# 贡献与发布

[English](CONTRIBUTING.md) | 简体中文

本文面向开发者和维护者。普通用户不需要阅读本文，只需从
[Releases](https://github.com/XIAO-LIZE/-Base-Converter/releases) 下载发布附件。

## 开发环境

- 主版本：Python 3.9+，安装 `pip install -r "主版本_Main/requirements.txt"`
- 单文件版本：Python 3.8+，带 tkinter
- 共享核心：仅使用 Python 标准库

在仓库根目录运行两个版本：

```bash
python "主版本_Main/main.py"
python "单文件版本_SingleFile/main.py"
```

运行共享核心测试：

```bash
python -m unittest discover -s tests
```

各版本文件夹中的 Windows 启动器用于源码环境，会定位 Python 和所需依赖。

## 便携打包

安装 PyInstaller 后构建一个或两个版本：

```bash
python -m pip install pyinstaller
python tools/build_glass.py
python tools/build_light.py
```

输出：

- `dist/BaseConverter-Glass/`：带 Qt 运行库的文件夹版本，需压缩整个文件夹后分发，
  通常为 300–450 MB。
- `dist/BaseConverter-SingleFile.exe`：带 Python 运行时的单文件版本。

这两个版本的目标机器都不需要安装 Python 或 PySide6。

## 发布新版本

`.github/workflows/build-release.yml` 会在 Windows 上构建两个版本，并把四个附件
附加到 GitHub Release。

请先提交并推送工作流，再创建 tag：

```bash
git add .
git commit -m "Release v1.0.0"
git tag v1.0.0
git push origin master --tags
```

工作流生成的发布附件：

- `BaseConverter-SingleFile-Windows.exe`
- `BaseConverter-Glass-Windows.zip`
- `BaseConverter-SingleFile-Source.zip`
- `BaseConverter-Main-Source.zip`

如果只想测试构建、不正式发布，可以在 Actions 页面手动运行工作流。此时四个文件
作为 workflow artifact 提供，仅用于验证，不作为普通用户下载入口。

## 贡献说明

解析、格式化、校验、IPv4 逻辑的修改应放在 `core/`，并保持两个版本同步。共享逻辑
需要补充 `tests/` 下的测试；提交 PR 前运行测试，并对两个版本做一次冒烟测试。
