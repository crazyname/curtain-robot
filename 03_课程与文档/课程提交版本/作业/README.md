# 智能窗帘机器人 - Python实现

基于3D打印与Python的智能窗帘机器人设计与实现

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境

```bash
cp .env.example .env
# 编辑 .env 文件，根据你的硬件连接修改配置
```

### 3. 运行程序

```bash
python3 curtain_robot.py
```

## 项目结构

```
作业/
├── curtain_robot.py          # 主程序
├── config.py                 # 配置文件
├── gpio_controller.py        # GPIO控制模块
├── serial_communicator.py    # 串口通信模块
├── motor_controller.py       # 电机控制模块
├── light_sensor.py           # 光线传感器模块
├── auto_controller.py         # 自动控制模块
├── test_curtain.py           # 测试脚本
├── requirements.txt          # Python依赖
├── .env.example              # 配置示例
├── README.md                 # 本文件
└── 项目说明文档.md           # 详细文档
```

## 主要功能

- ✅ GPIO直接控制电机
- ✅ 串口通信控制（与U60FNQ2单片机）
- ✅ 光线传感器自动控制
- ✅ 定时自动控制
- ✅ 窗帘位置校准和记忆

## 详细文档

请查看 [项目说明文档.md](项目说明文档.md) 获取完整的使用说明、API文档和开发指南。

## 许可证

本项目仅供学习和研究使用。
