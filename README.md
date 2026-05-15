# 智能窗帘 STM32 VSCode 工程

当前说明版本：0.3.3-vscode

本仓库当前以 VS Code + STM32Cube 扩展 + CMake + Ninja + GCC 作为 STM32 固件开发方式。后续 AI 或开发者优先维护 VSCode 工程，不要把它删除成只剩 Keil 工程。

旧版 Keil/CubeMX 工程 `My_curtain_robotV2` 已压缩备份到本地目录 `本地备份_不提交git\固件工程备份\`，该备份目录不提交到 git。仓库内只保留 `My_curtain_robotV2_VSCode` 作为 STM32 固件开发工程。

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
