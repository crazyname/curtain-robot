"""
智能窗帘机器人配置文件
"""
import os
from dotenv import load_dotenv

load_dotenv()

# GPIO引脚配置（树莓派）
# 电机控制引脚 - 根据实际硬件连接修改
MOTOR_NSLEEP_PIN = int(os.getenv('MOTOR_NSLEEP_PIN', '18'))  # 电机使能引脚
MOTOR_IN1_PIN = int(os.getenv('MOTOR_IN1_PIN', '23'))        # 电机方向控制1
MOTOR_IN2_PIN = int(os.getenv('MOTOR_IN2_PIN', '24'))        # 电机方向控制2

# 光线传感器引脚
LIGHT_SENSOR_PIN = int(os.getenv('LIGHT_SENSOR_PIN', '25'))  # 光线传感器ADC引脚

# 串口配置（用于与U60FNQ2单片机通信）
SERIAL_PORT = os.getenv('SERIAL_PORT', '/dev/ttyUSB0')       # 串口设备
SERIAL_BAUDRATE = int(os.getenv('SERIAL_BAUDRATE', '9600'))   # 波特率
SERIAL_TIMEOUT = float(os.getenv('SERIAL_TIMEOUT', '1.0'))    # 超时时间

# 电机运行时间配置（毫秒）
# 这些值需要在首次使用时通过校准功能设置
MOTOR_OPEN_TIME = int(os.getenv('MOTOR_OPEN_TIME', '5000'))   # 打开窗帘时间
MOTOR_CLOSE_TIME = int(os.getenv('MOTOR_CLOSE_TIME', '5000')) # 关闭窗帘时间

# 自动控制配置
AUTO_CONTROL_ENABLED = os.getenv('AUTO_CONTROL_ENABLED', 'True').lower() == 'true'
LIGHT_THRESHOLD = int(os.getenv('LIGHT_THRESHOLD', '500'))    # 光线阈值（0-1023）
AUTO_OPEN_TIME = os.getenv('AUTO_OPEN_TIME', '07:00:00')      # 自动打开时间
AUTO_CLOSE_TIME = os.getenv('AUTO_CLOSE_TIME', '18:00:00')    # 自动关闭时间

# 日志配置
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'curtain_robot.log')

# 数据存储文件
DATA_FILE = os.getenv('DATA_FILE', 'curtain_data.json')
