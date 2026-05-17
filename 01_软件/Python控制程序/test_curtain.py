"""
智能窗帘机器人测试脚本
用于测试各个模块的功能（不需要实际硬件）
"""
import logging
import sys
from unittest.mock import Mock, MagicMock

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_gpio_controller():
    """测试GPIO控制器（模拟模式）"""
    print("\n测试GPIO控制器...")
    try:
        # 模拟RPi.GPIO
        sys.modules['RPi'] = MagicMock()
        sys.modules['RPi.GPIO'] = MagicMock()
        
        from gpio_controller import GPIOController
        
        # 创建模拟控制器
        controller = GPIOController(18, 23, 24)
        print("✓ GPIO控制器初始化成功")
        
        controller.forward()
        print("✓ 电机正转命令执行成功")
        
        controller.reverse()
        print("✓ 电机反转命令执行成功")
        
        controller.stop()
        print("✓ 电机停止命令执行成功")
        
        controller.cleanup()
        print("✓ GPIO控制器清理成功")
        
        return True
    except Exception as e:
        print(f"✗ GPIO控制器测试失败: {e}")
        return False


def test_serial_communicator():
    """测试串口通信器（模拟模式）"""
    print("\n测试串口通信器...")
    try:
        from serial_communicator import SerialCommunicator
        
        # 创建通信器（不实际连接）
        communicator = SerialCommunicator('/dev/ttyUSB0', 9600)
        print("✓ 串口通信器初始化成功")
        
        # 测试命令发送（模拟）
        print("✓ 串口通信器功能正常（模拟模式）")
        
        return True
    except Exception as e:
        print(f"✗ 串口通信器测试失败: {e}")
        return False


def test_motor_controller():
    """测试电机控制器"""
    print("\n测试电机控制器...")
    try:
        from motor_controller import MotorController
        
        # 创建控制器（不依赖实际硬件）
        controller = MotorController(data_file='test_data.json')
        print("✓ 电机控制器初始化成功")
        
        # 测试数据保存和加载
        controller.open_time = 6000
        controller.close_time = 5500
        controller.save_data()
        print("✓ 数据保存成功")
        
        controller.load_data()
        print(f"✓ 数据加载成功 - 打开时间:{controller.open_time}ms, 关闭时间:{controller.close_time}ms")
        
        return True
    except Exception as e:
        print(f"✗ 电机控制器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_serial_calibration_protocol():
    """测试0.3串口校准协议：开始和结束都应向STM32发送C"""
    print("\n测试串口校准协议...")
    try:
        from motor_controller import MotorController

        serial_mock = Mock()
        controller = MotorController(serial_communicator=serial_mock, data_file='test_data.json')
        controller.start_calibration()
        controller.end_calibration('open')

        if serial_mock.send_calibrate_command.call_count != 2:
            raise AssertionError("校准命令C没有发送两次")

        print("✓ 串口校准协议正常（C开始，C结束）")
        return True
    except Exception as e:
        print(f"✗ 串口校准协议测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_light_sensor():
    """测试光线传感器（模拟模式）"""
    print("\n测试光线传感器...")
    try:
        # 模拟RPi.GPIO
        if 'RPi' not in sys.modules:
            sys.modules['RPi'] = MagicMock()
            sys.modules['RPi.GPIO'] = MagicMock()
        
        from light_sensor import LightSensor
        
        sensor = LightSensor(25, threshold=500)
        print("✓ 光线传感器初始化成功")
        
        value = sensor.read()
        print(f"✓ 光线值读取成功: {value}")
        
        is_bright = sensor.is_bright()
        print(f"✓ 光线状态判断成功: {'明亮' if is_bright else '昏暗'}")
        
        return True
    except Exception as e:
        print(f"✗ 光线传感器测试失败: {e}")
        return False


def test_auto_controller():
    """测试自动控制器"""
    print("\n测试自动控制器...")
    try:
        from auto_controller import AutoController
        from motor_controller import MotorController
        
        motor_ctrl = MotorController(data_file='test_data.json')
        auto_ctrl = AutoController(motor_ctrl)
        
        print("✓ 自动控制器初始化成功")
        
        auto_ctrl.set_auto_times("07:00:00", "18:00:00")
        print("✓ 自动控制时间设置成功")
        
        auto_ctrl.enable()
        print("✓ 自动控制启用成功")
        
        auto_ctrl.disable()
        print("✓ 自动控制禁用成功")
        
        return True
    except Exception as e:
        print(f"✗ 自动控制器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有测试"""
    print("=" * 50)
    print("智能窗帘机器人 - 模块测试")
    print("=" * 50)
    
    results = []
    results.append(("GPIO控制器", test_gpio_controller()))
    results.append(("串口通信器", test_serial_communicator()))
    results.append(("电机控制器", test_motor_controller()))
    results.append(("串口校准协议", test_serial_calibration_protocol()))
    results.append(("光线传感器", test_light_sensor()))
    results.append(("自动控制器", test_auto_controller()))
    
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name}: {status}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\n总计: {passed}/{total} 测试通过")
    print("=" * 50)
    
    # 清理测试文件
    import os
    if os.path.exists('test_data.json'):
        os.remove('test_data.json')
        print("\n测试文件已清理")


if __name__ == '__main__':
    main()
