"""
智能窗帘机器人主程序
"""
import logging
import signal
import sys
import time
from config import *
from serial_communicator import SerialCommunicator
from motor_controller import MotorController
from auto_controller import AutoController

# 配置日志
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class CurtainRobot:
    """智能窗帘机器人类"""
    
    def __init__(self):
        """初始化智能窗帘机器人"""
        logger.info("=" * 50)
        logger.info(f"智能窗帘机器人 v{PROJECT_VERSION} 启动中...")
        logger.info(f"控制模式: {CONTROL_MODE}")
        logger.info("=" * 50)
        
        # 初始化组件
        self.gpio_controller = None
        self.serial_communicator = None
        self.motor_controller = None
        self.light_sensor = None
        self.auto_controller = None
        
        self._init_control_backend()
        
        # 初始化电机控制器
        self.motor_controller = MotorController(
            gpio_controller=self.gpio_controller,
            serial_communicator=self.serial_communicator,
            data_file=DATA_FILE
        )
        
        if LIGHT_SENSOR_ENABLED:
            self._init_light_sensor()
        else:
            logger.info("光线传感器未启用，0.3默认由STM32侧负责传感器/低功耗硬件逻辑")
        
        # 初始化自动控制器
        self.auto_controller = AutoController(
            self.motor_controller,
            self.light_sensor
        )
        
        # 设置自动控制时间
        self.auto_controller.set_auto_times(AUTO_OPEN_TIME, AUTO_CLOSE_TIME)
        
        # 如果启用自动控制
        if AUTO_CONTROL_ENABLED:
            self.auto_controller.enable()
            logger.info("自动控制已启用")
        
        # 注册信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("=" * 50)
        logger.info("智能窗帘机器人初始化完成")
        logger.info("=" * 50)

    def _init_control_backend(self):
        """按0.3主线初始化控制后端。"""
        if CONTROL_MODE not in {"serial", "gpio", "auto"}:
            raise ValueError("CONTROL_MODE 只能是 serial、gpio 或 auto")

        if CONTROL_MODE in {"serial", "auto"}:
            self._init_serial_controller()

        if CONTROL_MODE == "gpio" or (CONTROL_MODE == "auto" and self.serial_communicator is None):
            self._init_gpio_controller()

        if self.serial_communicator is None and self.gpio_controller is None:
            raise RuntimeError("未找到可用控制后端：请检查串口配置，或设置 CONTROL_MODE=gpio 并在树莓派上运行")

    def _init_serial_controller(self):
        """初始化串口控制模式：Python发命令，STM32执行硬件动作。"""
        try:
            self.serial_communicator = SerialCommunicator(
                SERIAL_PORT,
                SERIAL_BAUDRATE,
                SERIAL_TIMEOUT
            )
            if self.serial_communicator.connect():
                logger.info("串口通信器初始化成功（STM32主控模式）")
                self.serial_communicator.set_receive_callback(self._on_serial_receive)
            else:
                logger.warning("串口连接失败")
                self.serial_communicator = None
        except Exception as e:
            logger.warning(f"串口通信器初始化失败: {e}")
            self.serial_communicator = None

    def _init_gpio_controller(self):
        """初始化GPIO直控模式：仅作为树莓派原型备用。"""
        try:
            from gpio_controller import GPIOController

            self.gpio_controller = GPIOController(
                MOTOR_NSLEEP_PIN,
                MOTOR_IN1_PIN,
                MOTOR_IN2_PIN
            )
            logger.info("GPIO控制器初始化成功（树莓派直控备用模式）")
        except Exception as e:
            logger.warning(f"GPIO控制器初始化失败: {e}")
            self.gpio_controller = None

    def _init_light_sensor(self):
        """初始化树莓派光线传感器备用路径。"""
        try:
            from light_sensor import LightSensor

            self.light_sensor = LightSensor(
                LIGHT_SENSOR_PIN,
                LIGHT_THRESHOLD
            )
            logger.info("光线传感器初始化成功")
        except Exception as e:
            logger.warning(f"光线传感器初始化失败: {e}")
            self.light_sensor = None
    
    def _on_serial_receive(self, data):
        """
        串口接收数据回调
        
        Args:
            data: 接收到的数据字符串
        """
        logger.debug(f"串口接收: {data}")
        
        # 处理来自单片机的响应
        # 例如：工作时间的反馈等
        if "worktime:" in data:
            try:
                worktime = int(data.split(":")[1])
                logger.info(f"接收到工作时间: {worktime}ms")
            except:
                pass
        elif data.startswith("STATE:") and self.serial_communicator.last_device_status:
            status = self.serial_communicator.last_device_status
            logger.info(
                f"接收到设备状态: {status['state']}, "
                f"校准状态: {'已校准' if status['calibrated'] else '未校准/占位'}"
            )
    
    def open_curtain(self):
        """打开窗帘"""
        logger.info("用户命令: 打开窗帘")
        self.motor_controller.open_curtain()
    
    def close_curtain(self):
        """关闭窗帘"""
        logger.info("用户命令: 关闭窗帘")
        self.motor_controller.close_curtain()

    def stop_curtain(self):
        """立即停止窗帘运动。"""
        logger.info("用户命令: 停止窗帘")
        self.motor_controller.stop()
    
    def calibrate_open(self):
        """校准打开时间"""
        logger.info("用户命令: 校准打开时间")
        self.motor_controller.start_calibration()
        input("请手动将窗帘完全打开，然后按回车键...")
        self.motor_controller.end_calibration('open')
    
    def calibrate_close(self):
        """校准关闭时间"""
        logger.info("用户命令: 校准关闭时间")
        self.motor_controller.start_calibration()
        input("请手动将窗帘完全关闭，然后按回车键...")
        self.motor_controller.end_calibration('close')
    
    def get_status(self):
        """获取状态信息"""
        status = {
            'version': PROJECT_VERSION,
            'control_mode': CONTROL_MODE,
            'gpio_controller': self.gpio_controller is not None,
            'serial_communicator': self.serial_communicator is not None and self.serial_communicator.is_connected,
            'light_sensor': self.light_sensor is not None,
            'auto_control_enabled': self.auto_controller.enabled,
            'open_time': self.motor_controller.open_time,
            'close_time': self.motor_controller.close_time,
            'device_status': (
                self.serial_communicator.last_device_status
                if self.serial_communicator else None
            ),
        }
        
        if self.light_sensor:
            status['light_value'] = self.light_sensor.read()
            status['is_bright'] = self.light_sensor.is_bright()
        
        return status
    
    def print_status(self):
        """打印状态信息"""
        status_query = None
        if self.serial_communicator:
            status_query = self.serial_communicator.query_status()
        status = self.get_status()
        print("\n" + "=" * 50)
        print(f"智能窗帘机器人状态 v{status['version']}")
        print("=" * 50)
        print(f"控制模式: {status['control_mode']}")
        print(f"GPIO控制器: {'已连接' if status['gpio_controller'] else '未连接'}")
        print(f"串口通信器: {'已连接' if status['serial_communicator'] else '未连接'}")
        print(f"光线传感器: {'已连接' if status['light_sensor'] else '未连接'}")
        if status['light_sensor']:
            print(f"  当前光线值: {status['light_value']}")
            print(f"  光线状态: {'明亮' if status['is_bright'] else '昏暗'}")
        print(f"自动控制: {'已启用' if status['auto_control_enabled'] else '已禁用'}")
        print(f"打开时间: {status['open_time']}ms")
        print(f"关闭时间: {status['close_time']}ms")
        if status_query and status_query['success']:
            device_status = status_query['status']
            print("STM32状态查询: 已收到本次 STATUS 响应")
            print(f"STM32运行状态: {device_status['state']}")
            print(f"STM32校准标志: {'1' if device_status['calibrated'] else '0'}")
        elif status_query and status_query['error'] == 'timeout':
            print("STM32状态查询: 超时，未收到本次 STATUS 响应")
        elif status_query and status_query['error'] == 'send_failed':
            print("STM32状态查询: STATUS 发送失败")
        print("=" * 50 + "\n")
    
    def _signal_handler(self, signum, frame):
        """信号处理函数"""
        logger.info("接收到退出信号，正在清理资源...")
        self.cleanup()
        sys.exit(0)
    
    def cleanup(self):
        """清理资源"""
        logger.info("正在清理资源...")
        
        if self.auto_controller:
            self.auto_controller.disable()
        
        if self.motor_controller:
            self.motor_controller.cleanup()
        
        if self.serial_communicator:
            self.serial_communicator.disconnect()
        
        logger.info("资源清理完成")
    
    def run_interactive(self):
        """运行交互式命令行界面"""
        print("\n" + "=" * 50)
        print(f"智能窗帘机器人 v{PROJECT_VERSION} - STM32主控调试台")
        print("=" * 50)
        print("命令列表:")
        print("  1 或 open    - 打开窗帘")
        print("  2 或 close   - 关闭窗帘")
        print("  0 或 stop    - 立即停止窗帘")
        print("  3 或 cal_open  - 校准打开时间")
        print("  4 或 cal_close - 校准关闭时间")
        print("  5 或 status  - 查看状态")
        print("  6 或 enable_auto  - 启用自动控制")
        print("  7 或 disable_auto - 禁用自动控制")
        print("  q 或 quit    - 退出程序")
        print("=" * 50 + "\n")
        
        while True:
            try:
                cmd = input("请输入命令: ").strip().lower()
                
                if cmd in ['1', 'open']:
                    self.open_curtain()
                elif cmd in ['2', 'close']:
                    self.close_curtain()
                elif cmd in ['0', 'stop']:
                    self.stop_curtain()
                elif cmd in ['3', 'cal_open']:
                    self.calibrate_open()
                elif cmd in ['4', 'cal_close']:
                    self.calibrate_close()
                elif cmd in ['5', 'status']:
                    self.print_status()
                elif cmd in ['6', 'enable_auto']:
                    self.auto_controller.enable()
                    print("自动控制已启用")
                elif cmd in ['7', 'disable_auto']:
                    self.auto_controller.disable()
                    print("自动控制已禁用")
                elif cmd in ['q', 'quit', 'exit']:
                    break
                else:
                    print("未知命令，请重新输入")
                
                time.sleep(0.5)
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"执行命令时出错: {e}")
        
        self.cleanup()


def main():
    """主函数"""
    try:
        robot = CurtainRobot()
        robot.run_interactive()
    except Exception as e:
        logger.error(f"程序运行出错: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
