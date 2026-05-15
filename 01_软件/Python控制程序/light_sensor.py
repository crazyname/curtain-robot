"""
光线传感器模块
"""
import RPi.GPIO as GPIO
import time
import logging
import threading

logger = logging.getLogger(__name__)


class LightSensor:
    """光线传感器类"""
    
    def __init__(self, pin, threshold=500):
        """
        初始化光线传感器
        
        Args:
            pin: ADC引脚（如果使用模拟传感器）或数字引脚
            threshold: 光线阈值（0-1023），低于此值认为光线不足
        """
        self.pin = pin
        self.threshold = threshold
        self.current_value = 0
        self.monitoring = False
        self.monitor_thread = None
        self.callback = None
        
        # 如果使用模拟传感器，需要ADC（树莓派需要外接ADC模块如MCP3008）
        # 这里使用简化版本，假设使用数字传感器或通过ADC读取
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        
        logger.info(f"光线传感器初始化完成 - 引脚:{pin}, 阈值:{threshold}")
    
    def read(self):
        """
        读取光线传感器值
        
        Returns:
            int: 光线值（0-1023），值越大光线越强
        """
        try:
            # 简化版本：使用数字引脚模拟
            # 实际应用中需要使用ADC读取模拟值
            # 这里返回一个模拟值（实际应该从ADC读取）
            value = GPIO.input(self.pin)
            
            # 模拟ADC读取（实际项目中需要替换为真实的ADC读取代码）
            # 例如使用MCP3008: value = adc.read(channel)
            # 这里使用简单的模拟值
            if value:
                self.current_value = 800  # 光线充足
            else:
                self.current_value = 200  # 光线不足
            
            return self.current_value
        except Exception as e:
            logger.error(f"读取光线传感器失败: {e}")
            return 0
    
    def is_bright(self):
        """判断是否光线充足"""
        value = self.read()
        return value >= self.threshold
    
    def is_dark(self):
        """判断是否光线不足"""
        return not self.is_bright()
    
    def start_monitoring(self, interval=1.0, callback=None):
        """
        开始监控光线变化
        
        Args:
            interval: 检查间隔（秒）
            callback: 回调函数，当光线状态改变时调用
        """
        self.callback = callback
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, args=(interval,), daemon=True)
        self.monitor_thread.start()
        logger.info("光线监控已启动")
    
    def stop_monitoring(self):
        """停止监控"""
        self.monitoring = False
        logger.info("光线监控已停止")
    
    def _monitor_loop(self, interval):
        """监控循环"""
        last_state = None
        while self.monitoring:
            try:
                current_state = self.is_bright()
                if last_state is not None and current_state != last_state:
                    logger.info(f"光线状态改变: {'明亮' if current_state else '昏暗'}")
                    if self.callback:
                        self.callback(current_state)
                last_state = current_state
                time.sleep(interval)
            except Exception as e:
                logger.error(f"光线监控错误: {e}")
                time.sleep(interval)


class MCP3008ADC:
    """
    MCP3008 ADC读取类（可选，如果需要使用模拟光线传感器）
    需要安装spidev库: pip install spidev
    """
    
    def __init__(self, spi_channel=0, spi_device=0):
        """
        初始化MCP3008 ADC
        
        Args:
            spi_channel: SPI通道（通常是0）
            spi_device: SPI设备（通常是0）
        """
        try:
            import spidev
            self.spi = spidev.SpiDev()
            self.spi.open(spi_channel, spi_device)
            self.spi.max_speed_hz = 1000000  # 1MHz
            logger.info("MCP3008 ADC初始化成功")
        except ImportError:
            logger.warning("spidev库未安装，无法使用MCP3008 ADC")
            self.spi = None
        except Exception as e:
            logger.error(f"MCP3008 ADC初始化失败: {e}")
            self.spi = None
    
    def read(self, channel):
        """
        读取ADC通道值
        
        Args:
            channel: ADC通道（0-7）
        
        Returns:
            int: ADC值（0-1023）
        """
        if not self.spi:
            return 0
        
        try:
            # MCP3008读取命令
            adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
            data = ((adc[1] & 3) << 8) + adc[2]
            return data
        except Exception as e:
            logger.error(f"读取ADC失败: {e}")
            return 0
