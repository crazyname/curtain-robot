"""
GPIO控制模块 - 用于控制电机
"""
import RPi.GPIO as GPIO
import time
import logging

logger = logging.getLogger(__name__)


class GPIOController:
    """GPIO控制器类，用于控制电机"""
    
    def __init__(self, nsleep_pin, in1_pin, in2_pin):
        """
        初始化GPIO控制器
        
        Args:
            nsleep_pin: 电机使能引脚
            in1_pin: 电机方向控制引脚1
            in2_pin: 电机方向控制引脚2
        """
        self.nsleep_pin = nsleep_pin
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin
        
        # 设置GPIO模式
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # 配置引脚为输出模式
        GPIO.setup(self.nsleep_pin, GPIO.OUT)
        GPIO.setup(self.in1_pin, GPIO.OUT)
        GPIO.setup(self.in2_pin, GPIO.OUT)
        
        # 初始化引脚状态（电机停止）
        self.stop()
        
        logger.info(f"GPIO控制器初始化完成 - NSLEEP:{nsleep_pin}, IN1:{in1_pin}, IN2:{in2_pin}")
    
    def enable(self):
        """使能电机"""
        GPIO.output(self.nsleep_pin, GPIO.HIGH)
        logger.debug("电机已使能")
    
    def disable(self):
        """禁用电机（进入低功耗模式）"""
        GPIO.output(self.nsleep_pin, GPIO.LOW)
        logger.debug("电机已禁用")
    
    def forward(self):
        """电机正转（打开窗帘）"""
        self.enable()
        GPIO.output(self.in1_pin, GPIO.HIGH)
        GPIO.output(self.in2_pin, GPIO.LOW)
        logger.debug("电机正转（打开窗帘）")
    
    def reverse(self):
        """电机反转（关闭窗帘）"""
        self.enable()
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.HIGH)
        logger.debug("电机反转（关闭窗帘）")
    
    def brake(self):
        """电机刹车（停止但不禁用）"""
        GPIO.output(self.in1_pin, GPIO.HIGH)
        GPIO.output(self.in2_pin, GPIO.HIGH)
        logger.debug("电机刹车")
    
    def stop(self):
        """电机停止并禁用"""
        self.brake()
        time.sleep(0.1)  # 短暂延时确保刹车完成
        self.disable()
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.LOW)
        logger.debug("电机停止")
    
    def run_for_time(self, direction, duration_ms):
        """
        运行电机指定时间
        
        Args:
            direction: 'forward' 或 'reverse'
            duration_ms: 运行时间（毫秒）
        """
        if direction == 'forward':
            self.forward()
        elif direction == 'reverse':
            self.reverse()
        else:
            logger.error(f"未知方向: {direction}")
            return
        
        # 运行指定时间
        time.sleep(duration_ms / 1000.0)
        
        # 停止电机
        self.stop()
        logger.info(f"电机运行 {duration_ms}ms ({direction})")
    
    def cleanup(self):
        """清理GPIO资源"""
        self.stop()
        GPIO.cleanup()
        logger.info("GPIO资源已清理")
