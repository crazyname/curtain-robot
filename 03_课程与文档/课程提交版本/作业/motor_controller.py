"""
电机控制模块 - 封装电机控制逻辑
"""
import time
import logging
import json
import os
from gpio_controller import GPIOController
from serial_communicator import SerialCommunicator

logger = logging.getLogger(__name__)


class MotorController:
    """电机控制器类，封装电机控制逻辑"""
    
    def __init__(self, gpio_controller=None, serial_communicator=None, data_file='curtain_data.json'):
        """
        初始化电机控制器
        
        Args:
            gpio_controller: GPIO控制器实例（直接控制模式）
            serial_communicator: 串口通信实例（通过单片机控制模式）
            data_file: 数据存储文件路径
        """
        self.gpio_controller = gpio_controller
        self.serial_communicator = serial_communicator
        self.data_file = data_file
        
        # 电机运行时间（毫秒）
        self.open_time = 5000   # 默认打开时间
        self.close_time = 5000  # 默认关闭时间
        
        # 当前状态
        self.is_calibrating = False
        self.calibration_start_time = None
        
        # 加载保存的数据
        self.load_data()
        
        logger.info(f"电机控制器初始化完成 - 打开时间:{self.open_time}ms, 关闭时间:{self.close_time}ms")
    
    def load_data(self):
        """从文件加载保存的数据"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.open_time = data.get('open_time', self.open_time)
                    self.close_time = data.get('close_time', self.close_time)
                    logger.info(f"已加载保存的数据 - 打开:{self.open_time}ms, 关闭:{self.close_time}ms")
        except Exception as e:
            logger.error(f"加载数据失败: {e}")
    
    def save_data(self):
        """保存数据到文件"""
        try:
            data = {
                'open_time': self.open_time,
                'close_time': self.close_time
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            logger.info("数据已保存")
        except Exception as e:
            logger.error(f"保存数据失败: {e}")
    
    def open_curtain(self, duration_ms=None):
        """
        打开窗帘
        
        Args:
            duration_ms: 运行时间（毫秒），如果为None则使用保存的时间
        """
        if duration_ms is None:
            duration_ms = self.open_time
        
        logger.info(f"打开窗帘 - 运行时间: {duration_ms}ms")
        
        if self.serial_communicator:
            # 通过串口控制
            self.serial_communicator.send_open_command()
        elif self.gpio_controller:
            # 直接GPIO控制
            self.gpio_controller.run_for_time('forward', duration_ms)
        else:
            logger.error("未配置GPIO控制器或串口通信器")
    
    def close_curtain(self, duration_ms=None):
        """
        关闭窗帘
        
        Args:
            duration_ms: 运行时间（毫秒），如果为None则使用保存的时间
        """
        if duration_ms is None:
            duration_ms = self.close_time
        
        logger.info(f"关闭窗帘 - 运行时间: {duration_ms}ms")
        
        if self.serial_communicator:
            # 通过串口控制
            self.serial_communicator.send_close_command()
        elif self.gpio_controller:
            # 直接GPIO控制
            self.gpio_controller.run_for_time('reverse', duration_ms)
        else:
            logger.error("未配置GPIO控制器或串口通信器")
    
    def start_calibration(self):
        """开始校准模式"""
        if self.is_calibrating:
            logger.warning("校准已在进行中")
            return
        
        self.is_calibrating = True
        self.calibration_start_time = time.time() * 1000  # 转换为毫秒
        
        logger.info("开始校准模式 - 发送开始命令")
        
        if self.serial_communicator:
            self.serial_communicator.send_calibrate_command()
        elif self.gpio_controller:
            # 直接控制模式下的校准
            self.gpio_controller.forward()
        else:
            logger.error("未配置GPIO控制器或串口通信器")
    
    def end_calibration(self, direction='open'):
        """
        结束校准模式
        
        Args:
            direction: 'open' 或 'close'，表示校准的是打开还是关闭
        """
        if not self.is_calibrating:
            logger.warning("未在校准模式中")
            return
        
        end_time = time.time() * 1000  # 转换为毫秒
        duration = int(end_time - self.calibration_start_time)
        
        if direction == 'open':
            self.open_time = duration
            logger.info(f"校准完成 - 打开时间: {duration}ms")
        elif direction == 'close':
            self.close_time = duration
            logger.info(f"校准完成 - 关闭时间: {duration}ms")
        
        self.is_calibrating = False
        self.calibration_start_time = None
        
        # 停止电机
        if self.gpio_controller:
            self.gpio_controller.stop()
        
        # 保存数据
        self.save_data()
    
    def stop(self):
        """立即停止电机"""
        logger.info("停止电机")
        if self.gpio_controller:
            self.gpio_controller.stop()
    
    def cleanup(self):
        """清理资源"""
        self.stop()
        if self.gpio_controller:
            self.gpio_controller.cleanup()
        logger.info("电机控制器资源已清理")
