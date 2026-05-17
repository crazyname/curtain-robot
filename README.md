# 边缘计算与物联网融合的智能窗帘机器人装置

当前说明版本：0.3.5-vscode-docs

本仓库是智能窗帘机器人装置的软硬件一体化工程，当前已经包含 STM32 固件、Python 边缘控制程序、微信小程序、PCB 工程和 3D 结构文件。

STM32 固件当前以 VS Code + STM32Cube 扩展 + CMake + Ninja + GCC 作为开发方式。后续 AI 或开发者优先维护 VSCode 工程，不要把它删除成只剩 Keil 工程。

旧版 Keil/CubeMX 工程和历史原始资料已集中放入本地备份目录 `04_本地备份/`，该目录不提交到 git。仓库内只保留 `My_curtain_robotV2_VSCode` 作为 STM32 固件开发工程。

## 当前版本定位

当前版本不是从零开始的概念验证，而是已经整理成一个可继续开发的综合项目：

- `01_软件\STM32嵌入式固件\My_curtain_robotV2_VSCode`：底层嵌入式固件工程，负责传感器、电机、串口和实时控制。
- `01_软件\Python控制程序`：树莓派或边缘端 Python 控制程序，已有电机控制、光照读取、串口通信、定时控制和校准逻辑。
- `01_软件\微信小程序`：手机端控制入口，当前重点用于蓝牙或远程交互扩展。
- `02_硬件`：PCB、原理图、立创 EDA、SolidWorks 和 STL 结构文件。

后续开发目标是把现有工程从“能控制窗帘的分散模块”重构成“有感知、有本地决策、有联网控制、有结构装配、有验收闭环”的完整智能窗帘机器人装置。

## 总体目标架构

推荐按三层协同实现：

```text
微信小程序 / 手机端
        |
蓝牙 / Wi-Fi / MQTT / HTTP
        |
Python 边缘计算控制层
        |
UART 串口 / GPIO
        |
STM32 固件 + 电机驱动 + 光照传感器
        |
窗帘机械结构
```

各层职责如下：

- STM32 层：负责电机正反转、PWM 调速、停止保护、传感器读取、串口命令响应。
- Python 边缘层：负责规则判断、定时策略、光照策略、状态管理、日志记录和对外 API。
- 小程序层：负责用户控制、设备连接、参数配置、状态展示。
- 硬件结构层：负责电源、电机驱动、传感器接口、外壳固定、滚轮传动和安全安装。

## 后续开发计划

### 第一阶段：固件与基础运动控制

目标：让 STM32 工程成为稳定的底层执行器。

需要完成：

- 整理 STM32 引脚定义，明确电机驱动、光照传感器、串口、按键或限位开关连接。
- 实现并验证基础命令：打开、关闭、停止、查询状态。
- 增加电机运行超时保护，避免堵转或持续拉扯窗帘。
- 如果硬件支持 PWM，加入速度控制和软启动，减少启动冲击。
- 固化串口协议，至少支持：

```text
OPEN
CLOSE
STOP
SET:50
STATUS
```

验收标准：

- VSCode/CMake 工程可以稳定构建。
- 电机可以可靠正转、反转、停止。
- 串口能收到命令并返回状态。
- 异常情况下能停止电机。

### 第二阶段：位置校准与百分比控制

目标：从简单开关升级为可控位置。

需要完成：

- 首次使用时校准全开、全关运行时间。
- 保存当前位置、全开时间、全关时间。
- 支持打开到指定百分比，例如 30%、50%、100%。
- 断电重启后读取上次保存状态。
- 如果后续加入编码器、霍尔或限位开关，优先用真实位置反馈修正时间估算误差。

验收标准：

- 可以完成一次完整校准。
- 可以从当前位置移动到目标百分比。
- 重启后不会丢失校准数据。

### 第三阶段：边缘计算自动控制

目标：突出“边缘计算”，让设备断网也能智能运行。

需要完成：

- 在 Python 控制程序中维护统一状态：
  - 当前窗帘百分比
  - 电机运行状态
  - 光照值
  - 自动模式开关
  - 最近一次控制来源
- 实现本地规则：
  - 定时打开和关闭。
  - 光照超过阈值时自动关闭或半关闭。
  - 手动控制后短时间内暂停自动控制，避免用户刚操作完又被自动策略覆盖。
- 增加运行日志，记录命令、传感器值、动作结果和异常原因。
- 后续可扩展用户习惯学习，例如统计常用开关时间并给出推荐。

验收标准：

- 不连接云端时，设备仍能按时间和光照自动控制。
- 手动控制和自动控制不会频繁互相打架。
- 日志中能追溯每次动作原因。

### 第四阶段：物联网与小程序控制

目标：完成手机端控制和设备状态反馈。

需要完成：

- 小程序首页提供打开、关闭、停止、百分比滑块。
- 小程序显示当前状态、光照值、自动模式、电机状态。
- 小程序支持修改自动控制参数：
  - 早晨打开时间
  - 晚上关闭时间
  - 光照阈值
  - 自动模式开关
- 通信方式优先级：
  - 近距离演示优先打通蓝牙。
  - 局域网控制可使用 HTTP API。
  - 云端或智能家居集成可使用 MQTT。
- Python 边缘层建议提供 API：

```text
GET  /api/status
POST /api/curtain/open
POST /api/curtain/close
POST /api/curtain/stop
POST /api/curtain/position
POST /api/auto/enable
POST /api/auto/config
```

验收标准：

- 手机可以控制窗帘开、关、停。
- 手机可以查看实时状态。
- 手机修改的自动控制参数能被边缘端保存并生效。

### 第五阶段：硬件、结构与整机安全

目标：让项目从软件演示走向可安装实物。

需要完成：

- 检查 PCB 电源、电机驱动、传感器和通信接口是否与固件定义一致。
- 验证 N20 电机扭矩是否足够，滚轮或拉绳是否打滑。
- 优化 3D 外壳安装方式，确保能稳定固定在窗帘轨道或窗帘杆附近。
- 增加机械保护：弹性缓冲、离合、限位或可拆卸安装结构。
- 做连续运行测试，观察发热、松动、噪声和电池续航。

验收标准：

- 装置可以完成多次连续开合。
- 机械结构不明显松动或卡滞。
- 异常阻力出现时软件或结构能保护电机和窗帘。

### 第六阶段：文档、测试与展示材料

目标：形成可以提交、展示、复现的完整项目。

需要完成：

- 补充系统架构图、硬件连接图、软件流程图。
- 整理 BOM 表、引脚表、串口协议表、API 文档。
- 增加功能测试表：
  - 电机控制测试
  - 串口通信测试
  - 光照自动控制测试
  - 定时控制测试
  - 小程序控制测试
  - 异常保护测试
- 准备演示材料：
  - 实物照片
  - 小程序截图
  - 运行日志截图
  - 演示视频

验收标准：

- 其他开发者按 README 可以打开、构建、运行主要工程。
- 项目能用一套清晰材料说明“边缘计算”和“物联网融合”的实现方式。

## 当前优先级

短期优先做这几件事：

1. 保持 STM32 VSCode 工程可构建，这是底层可靠性的基础。
2. 固化 STM32 与 Python 之间的串口协议。
3. 打通 Python 边缘控制程序到真实电机或 STM32 的完整链路。
4. 在 Python 层补齐状态管理、校准数据和自动控制日志。
5. 再把小程序接入到边缘控制层。

暂时不要急着重构硬件目录或迁移工作区；当前仓库已经按软件、硬件、文档和本地备份分区，后续开发应在现有结构上渐进推进。

## 必须打开的工程

在 VS Code 中打开下面这个目录，而不是只打开仓库根目录：

```text
D:\enze\Documents\智能窗帘\01_软件\STM32嵌入式固件\My_curtain_robotV2_VSCode
```

这个目录里必须存在这些关键文件：

```text
CMakeLists.txt
CMakePresets.json
.vscode/tasks.json
cmake/gcc-arm-none-eabi.cmake
cmake/stm32cubemx/CMakeLists.txt
My_curtain_robotV2.ioc
STM32L051XX_FLASH.ld
Src/
Inc/
Drivers/
startup_stm32l051xx.s
```

如果没有 `CMakeLists.txt`，说明当前目录不是 VSCode/CMake 工程，不能直接执行 `cmake --build`。

## VSCode 里怎么编译

1. 打开 VS Code。
2. 选择 `文件 -> 打开文件夹`。
3. 打开：

```text
D:\enze\Documents\智能窗帘\01_软件\STM32嵌入式固件\My_curtain_robotV2_VSCode
```

4. 安装并启用这些 VS Code 扩展：

```text
STM32Cube for Visual Studio Code
STM32Cube CMake Support
CMake Tools
C/C++
```

5. 如果 VS Code 提示安装 STM32Cube bundle，选择 `Yes`。
6. 如果提示 `Configure discovered CMake project(s) as STM32Cube project(s)?`，选择 `Yes`。
7. 按 `Ctrl+Shift+P`，执行：

```text
Tasks: Run Build Task
```

8. 选择或默认运行：

```text
STM32: Build Debug
```

这个任务会先配置 CMake，再执行构建。

## 命令行编译

如果 VS Code 任务卡住，可以在 PowerShell 里手动运行下面命令。

先进入工程目录：

```powershell
cd "D:\enze\Documents\智能窗帘\01_软件\STM32嵌入式固件\My_curtain_robotV2_VSCode"
```

配置并构建：

```powershell
$cmake = "C:\Users\enze\AppData\Local\stm32cube\bundles\cmake\4.2.3+st.1\bin\cmake.exe"
$ninja = "C:\Users\enze\AppData\Local\stm32cube\bundles\ninja\1.13.2+st.1\bin\ninja.exe"
$gnu = "C:\Users\enze\AppData\Local\stm32cube\bundles\gnu-tools-for-stm32\14.3.1+st.2\bin"
$env:PATH = "$(Split-Path $cmake);$(Split-Path $ninja);$gnu;$env:PATH"

& $cmake -S . -B build\vscode -G Ninja -DCMAKE_BUILD_TYPE=Debug "-DCMAKE_MAKE_PROGRAM=$ninja" "-DCMAKE_TOOLCHAIN_FILE=$PWD\cmake\gcc-arm-none-eabi.cmake"
& $cmake --build build\vscode
```

注意：在 PowerShell 中，`-DCMAKE_MAKE_PROGRAM=$ninja` 必须整体加引号，写成 `"-DCMAKE_MAKE_PROGRAM=$ninja"`。否则 CMake 可能收到字面量 `$ninja`，然后报错：

```text
Running '$ninja' '--version' failed with: no such file or directory
```

如果出现这个错误，删除缓存后重新配置：

```powershell
Remove-Item -Recurse -Force build\vscode
```

然后重新运行上面的配置和构建命令。

## 构建成功标志

成功时会看到类似输出：

```text
Build files have been written to: ...\build\vscode
[37/37] Linking C executable My_curtain_robotV2.elf
Memory region         Used Size  Region Size  %age Used
RAM:                  3512 B     8 KB         42.87%
FLASH:                39236 B    64 KB        59.87%
```

生成文件在：

```text
D:\enze\Documents\智能窗帘\01_软件\STM32嵌入式固件\My_curtain_robotV2_VSCode\build\vscode
```

主要产物：

```text
My_curtain_robotV2.elf
My_curtain_robotV2.map
compile_commands.json
```

`build/` 是生成目录，不要提交到 git。

## X 盘问题

VS Code 终端有时会显示在 `X:\>`，这不是 STM32 工程目录。不要在 `X:\>` 直接运行：

```powershell
cmake --build build\vscode
```

正确做法是先进入 VSCode 工程目录，或者直接使用 VS Code 的 `STM32: Build Debug` 任务。

当前已经取消 `X:` 盘符映射。它原本只是 `subst` 映射到 STM32 VSCode 工程目录，不是真实磁盘。取消映射不会删除源码；后续也不要重新依赖 `X:\` 作为工程入口。

## 开发环境维护记录

### 已清理的问题

- 已取消 `X:` 盘符映射，后续直接打开 `01_软件\STM32嵌入式固件\My_curtain_robotV2_VSCode`。
- STM32 构建产物位于 `build/`，该目录已被忽略，不提交到 git。
- 本地备份位于 `04_本地备份/`，该目录已被 `.gitignore` 忽略，不提交到 git。
- 当前仓库只保留 `My_curtain_robotV2_VSCode` 作为 STM32 主开发工程。
- STM32 构建警告已处理，当前 VSCode/CMake Debug 构建可以无 warning 通过。

### 暂时保留的问题

- `My_curtain_robotV2_VSCode/MDK-ARM/` 仍保留在 VSCode 工程内。它不是主开发入口，但可能是 CubeMX/历史工程生成残留，暂不删除。
- `04_本地备份/` 体积较大，但它是本地恢复资料，不参与源码版本管理。

## STM32CubeMX

如果需要改引脚、外设或重新生成代码：

1. 在 VS Code 左侧 STM32Cube 面板中打开 STM32CubeMX。
2. 打开这个 `.ioc`：

```text
D:\enze\Documents\智能窗帘\01_软件\STM32嵌入式固件\My_curtain_robotV2_VSCode\My_curtain_robotV2.ioc
```

3. 保持 Toolchain / IDE 为 CMake。
4. 生成代码后，回到 VS Code 重新执行 `STM32: Build Debug`。

不要用 CubeMX 把这个工程重新生成成 Keil-only 工程。

## 给后续 AI 的规则

1. STM32 开发以 `My_curtain_robotV2_VSCode` 为准。
2. 不要删除 `CMakeLists.txt`、`CMakePresets.json`、`.vscode/tasks.json`、`cmake/`。
3. 不要把 VSCode 工程替换成只支持 Keil 的目录。
4. 构建前先确认当前目录是 `My_curtain_robotV2_VSCode`。
5. 如果构建失败，先看 `build\vscode\CMakeCache.txt` 里的 `CMAKE_MAKE_PROGRAM` 是否是完整 ninja.exe 路径。
6. 修复构建问题时优先改 VSCode/CMake 配置，不要移动整个仓库。
7. 修改源码后，至少运行一次：

```powershell
& "C:\Users\enze\AppData\Local\stm32cube\bundles\cmake\4.2.3+st.1\bin\cmake.exe" --build "D:\enze\Documents\智能窗帘\01_软件\STM32嵌入式固件\My_curtain_robotV2_VSCode\build\vscode"
```

## 当前验证记录

2026-05-15 已恢复并验证 VSCode/CMake 工程。

验证命令使用：

```text
CMake 4.2.3+st.1
Ninja 1.13.2+st.1
GNU Tools for STM32 14.3.1+st.2
```

验证结果：

```text
配置成功
构建成功
生成 My_curtain_robotV2.elf
```
