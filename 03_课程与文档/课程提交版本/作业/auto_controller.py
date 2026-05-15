"""
自动控制模块 - 基于时间和光线传感器的自动控制
"""
import schedule
import time
import logging
import threading
from datetime import datetime

logger = logging.getLogger(__name__)


class AutoController:
    """自动控制器类，实现基于时间和光线的自动控制"""
    
    def __init__(self, motor_controller, light_sensor=None):
        """
        初始化自动控制器
        
        Args:
            motor_controller: 电机控制器实例
            light_sensor: 光线传感器实例（可选）
        """
        self.motor_controller = motor_controller
        self.light_sensor = light_sensor
        self.enabled = False
        self.schedule_thread = None
        self.running = False
        
        # 自动控制时间
        self.auto_open_time = "07:00:00"
        self.auto_close_time = "18:00:00"
        
        logger.info("自动控制器初始化完成")
    
    def set_auto_times(self, open_time, close_time):
        """
        设置自动控制时间
        
        Args:
            open_time: 自动打开时间（格式: "HH:MM:SS"）
            close_time: 自动关闭时间（格式: "HH:MM:SS"）
        """
        self.auto_open_time = open_time
        self.auto_close_time = close_time
        
        # 清除旧的任务
        schedule.clear()
        
        # 添加新的定时任务
        schedule.every().day.at(open_time).do(self._auto_open)
        schedule.every().day.at(close_time).do(self._auto_close)
        
        logger.info(f"自动控制时间已设置 - 打开:{open_time}, 关闭:{close_time}")
    
    def enable(self):
        """启用自动控制"""
        if self.enabled:
            return
        
        self.enabled = True
        self.running = True
        
        # 设置定时任务
        schedule.clear()
        schedule.every().day.at(self.auto_open_time).do(self._auto_open)
        schedule.every().day.at(self.auto_close_time).do(self._auto_close)
        
        # 启动调度线程
        self.schedule_thread = threading.Thread(target=self._schedule_loop, daemon=True)
        self.schedule_thread.start()
        
        # 如果启用了光线传感器，启动光线监控
        if self.light_sensor:
            self.light_sensor.start_monitoring(callback=self._on_light_change)
        
        logger.info("自动控制已启用")
    
    def disable(self):
        """禁用自动控制"""
        self.enabled = False
        self.running = False
        schedule.clear()
        
        if self.light_sensor:
            self.light_sensor.stop_monitoring()
        
        logger.info("自动控制已禁用")
    
    def _schedule_loop(self):
        """定时任务循环"""
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def _auto_open(self):
        """自动打开窗帘"""
        if not self.enabled:
            return
        
        logger.info(f"定时任务触发 - 自动打开窗帘 ({datetime.now().strftime('%H:%M:%S')})")
        self.motor_controller.open_curtain()
    
    def _auto_close(self):
        """自动关闭窗帘"""
        if not self.enabled:
            return
        
        logger.info(f"定时任务触发 - 自动关闭窗帘 ({datetime.now().strftime('%H:%M:%S')})")
        self.motor_controller.close_curtain()
    
    def _on_light_change(self, is_bright):
        """
        光线变化回调
        
        Args:
            is_bright: True表示光线充足，False表示光线不足
        """
        if not self.enabled:
            return
        
        # 可以根据光线变化自动控制窗帘
        # 例如：光线充足时打开窗帘，光线不足时关闭窗帘
        if is_bright:
            logger.info("光线充足 - 自动打开窗帘")
            self.motor_controller.open_curtain()
        else:
            logger.info("光线不足 - 自动关闭窗帘")
            self.motor_controller.close_curtain()
