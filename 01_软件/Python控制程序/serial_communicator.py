"""
串口通信模块 - 用于与U60FNQ2单片机通信
"""
import serial
import time
import logging
import threading

logger = logging.getLogger(__name__)


class SerialCommunicator:
    """串口通信类，用于与U60FNQ2单片机通信"""
    
    def __init__(self, port, baudrate=9600, timeout=1.0):
        """
        初始化串口通信
        
        Args:
            port: 串口设备路径（如 '/dev/ttyUSB0' 或 'COM3'）
            baudrate: 波特率
            timeout: 超时时间（秒）
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None
        self.is_connected = False
        self.receive_callback = None
        self.receive_thread = None
        self.running = False
        
    def connect(self):
        """连接串口"""
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
            self.is_connected = True
            self.running = True
            
            # 启动接收线程
            self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
            self.receive_thread.start()
            
            logger.info(f"串口连接成功: {self.port} @ {self.baudrate}bps")
            return True
        except Exception as e:
            logger.error(f"串口连接失败: {e}")
            self.is_connected = False
            return False
    
    def disconnect(self):
        """断开串口连接"""
        self.running = False
        if self.serial and self.serial.is_open:
            self.serial.close()
        self.is_connected = False
        logger.info("串口已断开")
    
    def send_command(self, command):
        """
        发送命令到单片机
        
        Args:
            command: 命令字符串（如 "ON", "OFF", "C"）
        
        Returns:
            bool: 发送是否成功
        """
        if not self.is_connected or not self.serial:
            logger.error("串口未连接")
            return False
        
        try:
            # 添加换行符
            cmd = command + '\r\n'
            self.serial.write(cmd.encode('utf-8'))
            logger.debug(f"发送命令: {command}")
            return True
        except Exception as e:
            logger.error(f"发送命令失败: {e}")
            return False
    
    def set_receive_callback(self, callback):
        """
        设置接收数据回调函数
        
        Args:
            callback: 回调函数，接收一个参数（接收到的数据字符串）
        """
        self.receive_callback = callback
    
    def _receive_loop(self):
        """接收数据循环（在独立线程中运行）"""
        buffer = ""
        while self.running and self.is_connected:
            try:
                if self.serial and self.serial.in_waiting > 0:
                    data = self.serial.read(self.serial.in_waiting).decode('utf-8', errors='ignore')
                    buffer += data
                    
                    # 处理完整的数据行
                    while '\n' in buffer or '\r' in buffer:
                        line_end = buffer.find('\n')
                        if line_end == -1:
                            line_end = buffer.find('\r')
                        if line_end == -1:
                            break
                        
                        line = buffer[:line_end].strip()
                        buffer = buffer[line_end+1:]
                        
                        if line:
                            logger.debug(f"接收到数据: {line}")
                            if self.receive_callback:
                                self.receive_callback(line)
                
                time.sleep(0.01)  # 避免CPU占用过高
            except Exception as e:
                logger.error(f"接收数据错误: {e}")
                time.sleep(0.1)
    
    def send_open_command(self):
        """发送打开窗帘命令"""
        return self.send_command("ON")
    
    def send_close_command(self):
        """发送关闭窗帘命令"""
        return self.send_command("OFF")
    
    def send_calibrate_command(self):
        """发送校准命令"""
        return self.send_command("C")
