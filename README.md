# 边缘计算与物联网融合的智能窗帘机器人装置

当前说明版本：0.3.6-collaboration-docs

## 项目简介

本仓库是一个智能窗帘机器人软硬件一体化项目，包含 STM32 嵌入式固件、Python 边缘控制程序、微信小程序、PCB/EDA 资料和 3D 结构文件。项目目标是在本地边缘端完成窗帘运动控制、传感器感知、串口通信、自动策略和移动端交互，并逐步形成可复现、可联调、可展示的智能窗帘装置。

当前仓库适合用于课程项目、原型验证和后续协作开发。它不是量产级成品，真实安装前仍需要完成硬件联调、结构可靠性测试和安全保护验证。

## 项目入口

- [Quick Start](#quick-start)
- [Demo](#demo)
- [Hardware Overview](#hardware-overview)
- [Software Architecture](#software-architecture)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## Quick Start

1. 阅读 [当前实现状态与后续规划](docs/当前实现状态与后续规划.md)，确认哪些能力已经实现、哪些仍在计划或联调阶段。
2. 按需要进入对应子工程：
   - STM32 固件：`01_软件/STM32嵌入式固件/My_curtain_robotV2_VSCode/`
   - Python 边缘控制：`01_软件/Python控制程序/`
   - 微信小程序：`01_软件/微信小程序/My_Curtain_robot_Wechart/`
   - 硬件资料：`02_硬件/`
3. 开发串口通信、控制指令或跨端联调前，先查看 [串口协议草案](docs/串口协议草案.md)。

本仓库当前更适合作为智能窗帘原型项目的代码与资料基线。复现或演示前，仍需要结合真实电机、电源、传感器、结构件和安装环境完成联调验证。

## Demo

待补充实物演示。

当前仓库尚未提供最终整机实物图或演示视频。现阶段可以先参考：

- `02_硬件/机械结构_3D外壳/` 中的机械结构、SolidWorks 源文件、STL 打印文件和结构参考资料。
- `03_项目报告/` 中的项目报告图片或阶段性说明资料。

## Hardware Overview

硬件资料集中在 `02_硬件/`，主要包括 PCB/EDA 设计资料、机械结构源文件、STL 打印文件和结构参考内容。这些资料可用于理解硬件方案、复查结构设计和后续复现，但 README 不将其描述为已经完成整机验证的量产硬件。

在真实设备上使用前，还需要完成电机负载、限位保护、电源稳定性、结构可靠性、长期运行和安装安全等验证。

## Software Architecture

当前已存在的组成部分包括：

- 微信小程序：已有蓝牙控制原型，尚未完成与 Python 边缘控制层的统一接入。
- Python 边缘控制：程序已存在，用于组织串口通信、自动控制、定时控制、传感器读取和本地策略。
- STM32 固件：已具备电机执行、传感器、RTC 和串口收发等基础能力。
- 电机与机械结构：已有窗帘运动执行机构、外壳结构、PCB/EDA 资料和 3D 打印结构文件。

目标协作架构如下，当前仍在逐步打通各层通信链路：

```text
微信小程序
  -> Python 边缘控制
  -> STM32 固件
  -> 电机与机械结构
```

跨端完整控制闭环尚未完成。串口命令和跨端通信约定见 [串口协议草案](docs/串口协议草案.md)。

## Roadmap

后续开发计划、当前限制和优先级见 [当前实现状态与后续规划](docs/当前实现状态与后续规划.md)。

## 当前状态

### 已实现

- STM32 固件主工程已整理到 VS Code / CMake / STM32Cube 可维护结构。
- STM32 侧已有电机控制、串口收发、RTC、ADC、I2C 和低功耗相关代码基础。
- Python 控制程序已有串口通信、电机控制、光照读取、定时控制、自动控制和测试入口。
- 微信小程序已有基础工程和蓝牙页面代码。
- 硬件目录包含 PCB/EDA 资料、SolidWorks 源文件、STL 打印文件和结构参考资料。
- `docs/串口协议草案.md` 已记录当前串口命令和后续协议方向。

### 部分实现

- STM32 与 Python 之间的串口协议仍处于整理和对齐阶段，已有命令与目标协议需要继续统一。
- Python 自动控制逻辑已有框架，但真实传感器、电机和边缘设备环境仍需联调验证。
- 微信小程序已有入口代码，但与边缘控制层或固件的完整闭环还需要继续打通。
- 结构和 PCB 资料已归档，但整机装配、扭矩、限位、安全保护和续航还需要实物验证。

### 尚未完成

- 量产级异常保护、长时间运行测试和完整验收报告。
- 稳定的设备状态模型、持久化校准数据和统一日志体系。
- 小程序参数配置、状态展示和远程控制闭环。
- 完整 BOM、接线表、测试记录、演示视频和安装说明。

## 仓库结构

```text
.
├── 01_软件/
│   ├── STM32嵌入式固件/
│   │   └── My_curtain_robotV2_VSCode/
│   ├── Python控制程序/
│   └── 微信小程序/
│       └── My_Curtain_robot_Wechart/
├── 02_硬件/
│   ├── PCB_AD工程/
│   ├── 立创EDA工程/
│   └── 机械结构_3D外壳/
├── 03_项目报告/
├── docs/
│   ├── 串口协议草案.md
│   └── 当前实现状态与后续规划.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── .gitignore
└── README.md
```

## 面向使用者

如果你只是想了解项目能做什么，可以先阅读本 README、`docs/当前实现状态与后续规划.md` 和 `docs/串口协议草案.md`。

当前项目可以作为智能窗帘原型参考：

- 了解 STM32 如何承担电机、传感器和串口执行层。
- 了解 Python 边缘端如何组织自动控制、定时控制和串口通信。
- 了解微信小程序作为移动端入口的工程位置。
- 参考 PCB、EDA 和 3D 结构文件进行硬件复现或二次设计。

使用时需要注意：

- 本仓库不是即插即用的量产产品。
- 固件、Python 程序、小程序和硬件之间仍需要根据实际设备进行联调。
- 电机、电源、机械结构和窗帘负载必须做安全测试，避免堵转、拉扯或过热。

## 面向开发者

### STM32 主工程

STM32 主工程路径：

```text
01_软件/STM32嵌入式固件/My_curtain_robotV2_VSCode/
```

推荐开发方式：

- VS Code
- STM32Cube for Visual Studio Code
- CMake Tools
- Ninja
- GNU Arm Embedded Toolchain 或 STM32Cube bundle 内置工具链

命令行构建示例：

```powershell
cd "01_软件\STM32嵌入式固件\My_curtain_robotV2_VSCode"
cmake --preset Debug
cmake --build --preset Debug
```

如果本机没有配置好 CMake、Ninja 或交叉编译工具链，请先在 VS Code 中安装并启用 STM32Cube 相关扩展，或根据本机工具链路径配置环境变量。

### Python 控制程序

Python 控制程序路径：

```text
01_软件/Python控制程序/
```

安装依赖：

```powershell
cd "01_软件\Python控制程序"
python -m pip install -r requirements.txt
```

基础测试命令：

```powershell
python test_curtain.py
```

在没有树莓派 GPIO、串口设备或真实传感器的开发机上，部分测试可能只能验证代码路径，不能代表硬件联调已经通过。

### 微信小程序

小程序工程路径：

```text
01_软件/微信小程序/My_Curtain_robot_Wechart/
```

使用微信开发者工具打开该目录，按实际 AppID、蓝牙设备和控制接口进行配置与联调。

### 协议文档

串口协议草案：

```text
docs/串口协议草案.md
```

开发 STM32、Python 或小程序控制逻辑前，应先确认命令名称、参数格式、返回值和错误处理方式是否与协议文档一致。

## 串口协议

当前固件和边缘控制层围绕窗帘开、关、停、状态查询和位置控制逐步对齐。已有或目标命令包括：

```text
ON / OPEN
OFF / CLOSE
STOP
STATUS
SET:<position>
```

详细命令格式、状态返回和后续扩展请以 `docs/串口协议草案.md` 为准。协议变更应同步更新固件、Python 控制程序、小程序调用逻辑和文档。

## 协作流程

- `main` 分支保持稳定，合入前应能代表一个可说明、可回退的项目状态。
- 每个功能或文档任务使用一个独立分支。
- 每个 PR 只解决一个明确任务，避免把固件、Python、小程序、硬件资料和文档重构混在一起。
- 开发前从最新 `origin/main` 新建分支。
- 提交前运行与改动范围对应的检查：
  - 修改 STM32 固件时，运行对应 CMake 构建。
  - 修改 Python 程序时，运行 `python test_curtain.py` 或更细的相关测试。
  - 修改小程序时，至少用微信开发者工具打开并确认页面可加载。
  - 只修改 README、协作说明、版本记录或 `.gitignore` 时，不需要跑固件或 Python 测试，但应检查 `git diff`。

更多协作约定见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 版本记录

版本号用于描述仓库协作状态，不一定等同于 Python 程序内部的 `PROJECT_VERSION`。

详细记录见 `CHANGELOG.md`。

## Contributing

欢迎围绕固件、边缘控制、小程序、硬件资料、测试记录和文档改进提交 Issue 或 Pull Request。提交前请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)，并保持每个 PR 聚焦一个明确任务。

## License

本项目的开源许可见 [LICENSE](LICENSE)。
