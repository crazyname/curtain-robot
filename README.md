# 智能窗帘机器人 - Python实现

基于3D打印与Python的智能窗帘机器人设计与实现

## 项目简介

这是一个基于树莓派和Python开发的智能窗帘机器人系统，支持：
- GPIO直接控制电机（正反转、启停）
- 串口通信控制（与U60FNQ2单片机通信）
- 光线传感器自动控制
- 时间定时自动控制
- 窗帘位置校准功能

## 功能特性

### 基础控制功能
- ✅ Python编写GPIO控制程序，直接驱动电机
- ✅ 实现对电机的精准启停与正反转
- ✅ 支持串口模块收发数据
- ✅ 支持环境感知（光线、时间）的自动触发

### 智能联动功能
- ✅ 基于时间的自动控制（定时打开/关闭）
- ✅ 基于光线传感器的自动控制
- ✅ 窗帘位置记忆功能（校准后保存）
- ✅ 低功耗设计支持

## 硬件要求

### 必需硬件
- 树莓派（Raspberry Pi）或其他支持GPIO的单板计算机
- 电机驱动模块（如DRV8833或类似）
- N20减速电机
- 电源模块

### 可选硬件
- U60FNQ2单片机（如果使用串口控制模式）
- 光线传感器（如光敏电阻+ADC模块MCP3008）
- 蓝牙模块（用于远程控制）

### GPIO引脚连接
根据 `config.py` 中的配置：
- `MOTOR_NSLEEP_PIN`: 电机使能引脚（默认GPIO 18）
- `MOTOR_IN1_PIN`: 电机方向控制1（默认GPIO 23）
- `MOTOR_IN2_PIN`: 电机方向控制2（默认GPIO 24）
- `LIGHT_SENSOR_PIN`: 光线传感器引脚（默认GPIO 25）

## 安装步骤

### 1. 克隆或下载项目

```bash
cd 智能窗帘
```

### 2. 安装Python依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制示例配置文件并修改：

```bash
cp .env.example .env
```

编辑 `.env` 文件，根据你的硬件连接修改相应的配置。

### 4. 配置GPIO权限（Linux）

如果使用GPIO，需要将用户添加到gpio组：

```bash
sudo usermod -a -G gpio $USER
```

或者使用sudo运行程序。

## 使用方法

### 基本使用

运行主程序：

```bash
python curtain_robot.py
```

程序会启动交互式命令行界面，你可以使用以下命令：

- `1` 或 `open` - 打开窗帘
- `2` 或 `close` - 关闭窗帘
- `3` 或 `cal_open` - 校准打开时间
- `4` 或 `cal_close` - 校准关闭时间
- `5` 或 `status` - 查看状态
- `6` 或 `enable_auto` - 启用自动控制
- `7` 或 `disable_auto` - 禁用自动控制
- `q` 或 `quit` - 退出程序

### 首次使用 - 校准窗帘位置

1. 运行程序后，选择 `3` 或 `cal_open` 校准打开时间
2. 按照提示手动将窗帘完全打开，然后按回车
3. 选择 `4` 或 `cal_close` 校准关闭时间
4. 按照提示手动将窗帘完全关闭，然后按回车
5. 校准数据会自动保存到 `curtain_data.json`

### 自动控制配置

在 `.env` 文件中配置：

```env
AUTO_CONTROL_ENABLED=True
AUTO_OPEN_TIME=07:00:00
AUTO_CLOSE_TIME=18:00:00
LIGHT_THRESHOLD=500
```

或者在程序中启用：

```python
robot.auto_controller.enable()
```

## 项目结构

```
智能窗帘/
├── curtain_robot.py          # 主程序
├── config.py                 # 配置文件
├── gpio_controller.py        # GPIO控制模块
├── serial_communicator.py    # 串口通信模块
├── motor_controller.py       # 电机控制模块
├── light_sensor.py           # 光线传感器模块
├── auto_controller.py        # 自动控制模块
├── requirements.txt          # Python依赖
├── .env.example              # 配置示例文件
├── README.md                 # 项目说明
└── curtain_data.json         # 数据存储文件（自动生成）
```

## 模块说明

### GPIOController
GPIO控制器，直接控制电机驱动模块：
- `forward()` - 电机正转（打开窗帘）
- `reverse()` - 电机反转（关闭窗帘）
- `stop()` - 停止电机
- `run_for_time()` - 运行指定时间

### SerialCommunicator
串口通信器，用于与U60FNQ2单片机通信：
- `send_open_command()` - 发送打开命令
- `send_close_command()` - 发送关闭命令
- `send_calibrate_command()` - 发送校准命令

### MotorController
电机控制器，封装电机控制逻辑：
- `open_curtain()` - 打开窗帘
- `close_curtain()` - 关闭窗帘
- `start_calibration()` - 开始校准
- `end_calibration()` - 结束校准

### LightSensor
光线传感器模块：
- `read()` - 读取光线值
- `is_bright()` - 判断是否光线充足
- `start_monitoring()` - 开始监控光线变化

### AutoController
自动控制器，实现定时和光线自动控制：
- `enable()` - 启用自动控制
- `disable()` - 禁用自动控制
- `set_auto_times()` - 设置自动控制时间

## 开发说明

### 控制模式

系统支持两种控制模式：

1. **GPIO直接控制模式**：树莓派直接通过GPIO控制电机驱动模块
2. **串口控制模式**：通过串口与U60FNQ2单片机通信，由单片机控制电机

如果两种模式都配置了，优先使用串口控制模式。

### 扩展开发

#### 添加新的传感器

在 `light_sensor.py` 中添加新的传感器类，然后在 `curtain_robot.py` 中初始化并使用。

#### 添加Web界面

可以集成Flask或FastAPI创建Web控制界面：

```python
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/api/open', methods=['POST'])
def api_open():
    robot.open_curtain()
    return jsonify({'status': 'success'})
```

#### 添加MQTT支持

可以添加MQTT客户端，实现远程控制：

```python
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    if msg.topic == 'curtain/control':
        command = msg.payload.decode()
        if command == 'open':
            robot.open_curtain()
```

## 故障排除

### GPIO权限错误
```bash
sudo usermod -a -G gpio $USER
# 然后重新登录
```

### 串口权限错误
```bash
sudo usermod -a -G dialout $USER
# 然后重新登录
```

### 找不到串口设备
检查串口设备：
```bash
ls -l /dev/ttyUSB* /dev/ttyACM*
```

### 电机不转动
1. 检查GPIO引脚连接是否正确
2. 检查电源是否正常
3. 检查电机驱动模块是否正常工作
4. 查看日志文件 `curtain_robot.log`

## 注意事项

1. **首次使用必须校准**：不同窗帘的长度不同，必须进行校准才能准确控制
2. **电源要求**：确保电机驱动模块有足够的电源供应
3. **安全注意**：电机运行时注意安全，避免夹手
4. **数据备份**：`curtain_data.json` 文件保存了校准数据，建议备份

## 许可证

本项目仅供学习和研究使用。

## 作者

基于广东工业大学树莓派与Python课程项目开发

## 更新日志

### v1.0.0
- 初始版本
- 实现基础GPIO控制
- 实现串口通信
- 实现光线传感器支持
- 实现定时自动控制
- 实现校准功能
