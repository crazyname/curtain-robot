# 协作指南

本仓库同时包含 STM32 固件、Python 控制程序、微信小程序、硬件资料和项目文档。协作时请保持改动范围清晰，避免一次 PR 同时修改多个无关子系统。

## 分支流程

从最新 `main` 新建任务分支：

```powershell
git fetch origin
git switch main
git pull --ff-only origin main
git switch -c <type>/<short-task-name>
```

示例：

```powershell
git switch -c docs/update-serial-protocol
```

## PR 范围原则

- 一个 PR 只解决一个明确任务。
- 文档整理、固件功能、Python 控制、小程序页面、硬件资料更新应尽量分开提交。
- 不要把构建产物、缓存、日志、临时文件、个人配置或密钥提交到仓库。
- 修改协议时，应同步检查 STM32、Python、小程序和 `docs/串口协议草案.md` 是否需要一起更新。

## 提交前检查

只修改 README、协作说明、版本记录或 `.gitignore` 时，至少运行：

```powershell
git status
git diff --stat
git diff
```

修改 STM32 固件时，进入主工程后构建：

```powershell
cd "01_软件\STM32嵌入式固件\My_curtain_robotV2_VSCode"
cmake --preset Debug
cmake --build --preset Debug
```

修改 Python 控制程序时，运行：

```powershell
cd "01_软件\Python控制程序"
python -m pip install -r requirements.txt
python test_curtain.py
```

修改微信小程序时，使用微信开发者工具打开：

```text
01_软件/微信小程序/My_Curtain_robot_Wechart/
```

并确认相关页面可以加载，蓝牙或接口调用逻辑按实际设备联调。

## .gitignore 维护

`.gitignore` 必须提交到仓库，因为它是多人协作的统一忽略规则。它用于排除缓存、构建产物、日志、密钥、本地备份和临时文件，不应用来隐藏源码、工程配置、正式文档或硬件源文件。

如果新增工具链或生成目录，请先确认不会误忽略这些内容：

- STM32 工程配置，例如 `.ioc`、`CMakeLists.txt`、`CMakePresets.json`、`.uvprojx`。
- Python 源码和 `requirements.txt`。
- 微信小程序源码和 `project.config.json`。
- `docs/`、`README.md`、`CONTRIBUTING.md`、`CHANGELOG.md`。
- PCB、EDA、CAD 等正式硬件源文件。

## 版本号维护

仓库协作版本记录在 `CHANGELOG.md` 中。该版本号用于描述仓库整体协作状态，不一定等同于 Python 程序内部的 `PROJECT_VERSION`。

建议规则：

- 文档、协作流程、ignore 规则整理可以提升补丁版本。
- 协议、固件命令、Python 控制闭环等功能变化应记录对应影响。
- 不要把计划写成已完成；未验证内容应明确标注为部分实现或待验证。

## PR 描述模板

```markdown
## 变更内容

- 

## 验证

- [ ] STM32 构建通过，或本 PR 不涉及 STM32
- [ ] Python 测试通过，或本 PR 不涉及 Python
- [ ] 小程序已打开检查，或本 PR 不涉及小程序
- [ ] 文档链接和路径已检查

## 风险和后续

- 
```
