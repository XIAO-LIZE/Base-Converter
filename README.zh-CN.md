# BaseConverter 进制转换器

一个用于进制转换、ASCII 字符查询和 IPv4 子网计算的桌面工具。仓库包含两个版本，共用同一套逻辑核心，并分别存放在两个版本文件夹中：

| 版本 | 外观 | 入口 |
| ---- | ---- | ---- |
| **主版本（视觉版）** | 无边框 PySide6/QML 界面，Liquid Glass 风格：实时背景模糊、玻璃卡片、动画标签栏、自绘标题栏 | `主版本_Main/main.py` · `主版本_Main/启动_Start.bat` |
| **单文件版本** | 紧凑的 tkinter 界面，仅使用 Python 标准库 | `单文件版本_SingleFile/main.py` · `单文件版本_SingleFile/单文件启动_SingleFileStart.bat` |

[English](README.md) | 简体中文

> **Windows 电脑没有安装 Python？** `.bat` 启动器面向已经安装 Python 的源码环境；
> 普通用户请下载已发布的 Releases 附件：
> `BaseConverter-SingleFile-Windows.exe`（单文件可执行程序）或
> `BaseConverter-Glass-Windows.zip`（解压后运行 exe）。已发布的 Windows 附件
> 内置 Python；主版本还内置了 Qt/PySide6。

## 功能

两个版本共用同一套核心行为，界面分别实现：

- 二进制、八进制、十进制、十六进制实时互转
- 0–127 ASCII 码表，支持字符/编码查询和按列搜索
- IPv4 地址与子网计算：点分、整数、十六进制、二进制形式，前缀/掩码解析，网络地址、广播地址、可用范围和地址分类
- 中英文界面实时切换
- 复制到剪贴板并显示状态反馈
- 解析、格式化、校验逻辑统一放在 `core/`，两个版本结果一致；同义操作的标签、提示与错误文案已对齐

版本差异：

- **主版本**：玻璃面板实时背景模糊、圆角玻璃卡片、无边框自绘标题栏（支持拖动/边缘缩放）、标签切换动画、悬停反馈、ASCII 查询的清空按钮
- **单文件版本**：小体积单窗口、仅依赖 Python 标准库、固定表头且列宽自适应的码表、标签指示条动画和启动淡入
- 两版均带应用图标和 AppUserModelID；单文件版本另外通过 DWM 请求深色原生标题栏与窗口圆角

## 环境要求

| | 主版本（视觉版） | 单文件版本 |
| --- | --- | --- |
| Python | 3.9 或更高 | 3.8 或更高 |
| GUI 工具包 | PySide6 6.8+（Qt 6） | tkinter（Python 官方安装包自带） |
| 第三方依赖 | `PySide6` | 无 |
| 操作系统 | 推荐 Windows 10/11；Qt 6 跨平台 | Windows/macOS/Linux |

单文件版本无需 `pip install`。主版本需要 Qt 运行库：

```bash
python -m pip install -r "主版本_Main/requirements.txt"
```

## 运行

### 单文件版本（tkinter）

```bash
python "单文件版本_SingleFile/main.py"
```

Windows 下可双击 `单文件版本_SingleFile/单文件启动_SingleFileStart.bat`。启动器会依次探测 `py`、`python`、`pyw`、`pythonw`，寻找 Python 3.8+ 且带 tkinter 的解释器；找不到时可通过 winget 安装 Python。传 `--auto` 可跳过确认。

### 主版本（PySide6 + QML）

```bash
python -m pip install -r "主版本_Main/requirements.txt"
python "主版本_Main/main.py"
```

Windows 下可双击 `主版本_Main/启动_Start.bat`。启动器会优先选择已经安装 PySide6 的 Python 3.9+ 解释器；缺少依赖时会询问并通过 pip 安装 `主版本_Main/requirements.txt`。传 `--auto` 可自动确认。

主版本快捷键：`Ctrl+L` 切换中英文。

## 下载单个版本

构建好的版本会发布到仓库的
[Releases](https://github.com/XIAO-LIZE/-Base-Converter/releases) 页面。
GitHub 的 “Download ZIP” 下载的是完整源码（两个版本都有）；如果只需要一个版本，
请到 Releases 下载对应附件。

| 需要的版本 | Release 附件 |
| ---------- | ------------ |
| 单文件版本，无需安装 Python | `BaseConverter-SingleFile-Windows.exe` |
| 主版本，无需安装 Python | `BaseConverter-Glass-Windows.zip`（解压后运行 `BaseConverter-Glass.exe`） |
| 只要单文件版本源码 | `BaseConverter-SingleFile-Source.zip` |
| 只要主版本源码 | `BaseConverter-Main-Source.zip` |

源码包里都包含共享的 `core/` 文件夹。解压后，主版本先安装
`主版本_Main/requirements.txt`，再运行 `python "主版本_Main/main.py"`；
单文件版本直接运行 `python "单文件版本_SingleFile/main.py"`。

构建、发布和维护流程面向开发者，见
[CONTRIBUTING.zh-CN.md](CONTRIBUTING.zh-CN.md)；普通用户无需阅读。

## 界面说明

### 进制转换

选择输入进制后直接输入，其他三种进制随输入实时更新。

支持的输入：

- 当前进制允许的数字（二进制 `0-1`、八进制 `0-7`、十进制 `0-9`、十六进制 `0-9 A-F`）
- 进制前缀：`0b`、`0o`、`0x`
- 数字分隔符：`_` 和空格，例如 `1_000`、`1111 1111`
- 开头 `+` / `-` 符号
- 最长 10,000 字符

负数按“符号 + 绝对值”显示（`-5` → `-101`、`-5`、`-5`、`-5`），不使用补码。二进制结果按 4 位分组。长数值会按可用宽度换行，复制时始终复制完整值。

### ASCII 码表

码表覆盖 0–127，表头固定，内容区域可滚动。

- **字符**：显示输入字符的码值；多个字符会逐个列出（最多 8 个，超出部分省略）。输入框旁有“清空”按钮。
- **十进制编码**：输入 0–127 的编码，显示对应字符；控制字符在码表中显示为助记符（NUL、LF、ESC 等），查询结果中以转义序列显示。输入框旁有“清空”按钮。
- **搜索**：匹配字符、各进制码值和说明。带前缀的查询只匹配对应列：`0x41` 匹配十六进制列、`0o101` 匹配八进制列、`0b1000001` 匹配二进制列、`#41` 匹配十六进制列。输入框右侧显示匹配数量；“显示全部”会清除搜索并恢复完整码表。
- 按 Esc 清空当前输入框。

### IPv4

输入地址，可附加前缀长度或子网掩码。支持以下格式：

| 格式 | 示例 |
| ---- | ---- |
| 点分十进制 | `192.168.1.10` |
| CIDR | `192.168.1.10/24` |
| 地址与点分掩码（空格分隔） | `192.168.1.10 255.255.255.0` |
| 地址与点分掩码（斜杠分隔） | `192.168.1.10/255.255.255.0` |
| 点分二进制（每段 8 位） | `11000000.10101000.00000001.00001010` |
| 空格分组的二进制 | `11000000 10101000 00000001 00001010` |
| 十进制整数 | `3232235786` |
| 十六进制 | `0xC0A8010A` |
| 二进制 | `0b11000000101010000000000100001010` |

地址表示区域始终显示点分十进制、32 位无符号十进制、十六进制、二进制和地址分类；提供前缀或掩码后，子网信息还会显示子网掩码、通配符掩码、网络地址、广播地址、可用地址范围、可用地址数和地址总数。

子网规则：

- 不写前缀：按单主机处理，不计算子网信息。
- `/31`：两个地址都可用，遵循 RFC 3021 点对点链路。
- `/32`：单主机路由，可用地址数为 1。

地址分类依据 RFC 1122（未指定、环回）、RFC 1918（私有）、RFC 6598（运营商级 NAT）、RFC 3927（链路本地）、RFC 6890（协议分配）、RFC 5737（文档示例）、RFC 2544（基准测试）、RFC 5771（组播）和 RFC 1112（保留），其余显示为公网地址。

## 项目结构

`core/` 存放全部与界面无关的逻辑，两个版本共同导入：

“单文件版本”指轻量的 tkinter 界面；其源码需要与根目录的 `core/` 一起使用，
发布包里的 Windows exe 才是真正的单文件。

```
单文件版本_SingleFile/                    单文件版本文件夹
├── main.py                              tkinter 入口
├── icon.ico                             可执行文件图标
└── 单文件启动_SingleFileStart.bat         Windows 启动器（中英文标注）

主版本_Main/                               主版本文件夹
├── main.py                              PySide6 入口
├── backend.py                           QML 与 core 之间的 QObject 桥接
├── requirements.txt                     PySide6 依赖
├── icon.png / icon.ico                  窗口与可执行文件图标
├── 启动_Start.bat                        Windows 启动器（中英文标注）
└── qml/
    ├── Main.qml                         窗口、背景、标签栏、状态栏
    ├── components/                      GlassCard、GlassField、GlassButton、Segmented
    └── pages/                           ConverterPage、AsciiPage、Ipv4Page

core/
├── bases.py                             进制解析/格式化、前缀、错误码
├── ascii_data.py                        ASCII 数据与按列搜索
└── ipv4.py                              IPv4 解析、子网计算、地址分类

tests/test_core.py                       共享核心单元测试
tools/build_light.py                     单文件版本 PyInstaller 打包脚本
tools/build_glass.py                     主版本 PyInstaller onedir 打包脚本
.github/workflows/build-release.yml      CI：构建两个版本并附加到 Release
dist/                                    生成的便携版本（已被 git 忽略）
README.md / README.zh-CN.md               用户文档
CONTRIBUTING.md / CONTRIBUTING.zh-CN.md   面向维护者的构建与发布说明
```

版本文件夹和启动器名称使用下划线代替空格，避免在 shell、脚本和 CI 中因空格
产生路径拆分问题。名称中的中文按 UTF-8 路径处理，现代 Windows 可以正常使用；
`dist/` 下的可执行文件名为纯 ASCII。

## 兼容性与限制

- 仅支持 IPv4，未实现 IPv6 解析和子网划分。
- ASCII 仅覆盖 7 位编码 0–127，不处理扩展代码页。
- 负数按符号 + 绝对值显示，不显示补码。
- 单文件版本默认窗口 760×800 逻辑像素，最小 620×680。
- 主版本默认窗口 1180×940 逻辑像素，最小 980×820。
- 背景模糊依赖 GPU/桌面合成。若环境不支持，玻璃卡片仍会以半透明颜色显示。
- 主版本依赖 PySide6（LGPLv3/GPL）。分发打包版本时需附带 Qt/PySide6 许可说明，并遵守 LGPL 关于 Qt 库可替换性的要求。
- 主版本会在 `%TEMP%\BaseConverter-Glass.log` 写入启动诊断日志；程序不访问网络，也不写配置文件。

## 常见问题

- **缺少 Tk**：使用 `单文件版本_SingleFile/单文件启动_SingleFileStart.bat`；或修复 Python：Windows 重新运行安装程序并勾选 “tcl/tk and IDLE”；Debian/Ubuntu 安装 `python3-tk`；Fedora 安装 `python3-tkinter`；Arch 安装 `tk`；macOS 使用 python.org 安装包或 `brew install python-tk`。
- **缺少 PySide6**：运行 `python -m pip install -r "主版本_Main/requirements.txt"`，然后执行 `python "主版本_Main/main.py"`；主版本启动器也会提示安装。
- **QML 窗口空白或没有模糊效果**：确认安装的是完整 PySide6（包含 Qt Quick Effects 与 Qt5Compat），更新显卡驱动，并尝试在启动前设置 `QT_QUICK_BACKEND=software`。软件渲染可能降低模糊质量。
- **检查单文件版本运行环境**：`python "单文件版本_SingleFile/main.py" --check` 会输出 Python、Tk、平台和解释器信息。
- **启动器找不到 Python**：从 python.org 安装 Python 3.9+ 并勾选 “Add python.exe to PATH”；单文件版本启动器也支持通过 winget 安装。

## 扩展

1. 在 `core/` 中添加共享逻辑，并在 `tests/` 补测试。
2. 接入单文件版本（`单文件版本_SingleFile/main.py` 和 `TR` 字典）。
3. 接入主版本（`主版本_Main/backend.py` 的 `STRINGS`/槽函数以及对应 QML 页面）。
4. 运行 `python -m unittest discover -s tests`，再分别冒烟测试两个版本。

- **新增语言**：在 `单文件版本_SingleFile/main.py` 增加 `TR` 字典；在 `主版本_Main/backend.py` 增加 `STRINGS`；在 `core/bases.py` 的 `BASE_NAMES` 中补充进制名称；ASCII 控制字符名称在 `core/ascii_data.py` 的 `EN_CTRL_NAMES`。
- **新增进制**：扩展 `core/bases.py`（`BASES`、`DIGITS`、`DIGSET`、`PREFIX`、`BASE_NAMES`），并同时更新两个界面的进制选择器。
- **新增 IPv4 特殊网段**：在 `core/ipv4.IP_SCOPES` 中追加条目，并在两套界面文案中加入对应的翻译键。

## 测试

```bash
python -m unittest discover -s tests
```

## 贡献

欢迎提交问题和 Pull Request。请说明受影响的版本与标签页、输入内容以及预期/实际结果。涉及解析或格式化的修改应放在 `core/` 并保证两个版本同步，同时补充共享逻辑的测试。

构建、打包和发布流程见
[CONTRIBUTING.zh-CN.md](CONTRIBUTING.zh-CN.md)。

## 许可证

本仓库目前未包含许可证文件，分发或复用前请先添加许可证。PySide6/Qt 遵循 LGPLv3/GPL，分发打包版本前请阅读 Qt for Python 的许可说明。
