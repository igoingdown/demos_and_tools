#!/usr/bin/env python3
"""
快速测试脚本 - 验证时间提醒服务功能
"""
import json
import time
import os
import sys
from datetime import datetime

def test_basic_functionality():
    """测试基本功能"""
    print("=== 时间提醒服务快速测试 ===")
    
    # 创建测试配置
    test_time = int(time.time()) + 10  # 10秒后
    test_config = {
        "timers": [
            {
                "name": "快速测试 (10秒后)",
                "timestamp": test_time
            }
        ]
    }
    
    try:
        with open("timer_conf.json", "w", encoding='utf-8') as f:
            json.dump(test_config, f, indent=2, ensure_ascii=False)
        
        target_time = datetime.fromtimestamp(test_time)
        current_time = datetime.now()
        time_diff = test_time - current_time.timestamp()
        
        print(f"✓ 创建测试定时器")
        print(f"  目标时间: {target_time.strftime('%H:%M:%S')}")
        print(f"  当前时间: {current_time.strftime('%H:%M:%S')}")
        print(f"  时间差: {time_diff:.0f} 秒")
        
        print(f"\n等待 {time_diff:.0f} 秒进行测试...")
        
        # 模拟定时器检查
        for i in range(int(time_diff) + 5):
            now = int(time.time())
            remaining = test_time - now
            
            if remaining == 60:
                print("⏰ 距离目标时间还有1分钟!")
            elif remaining == 30:
                print("⏰ 距离目标时间还有30秒!")
            elif remaining == 10:
                print("⏰ 距离目标时间还有10秒!")
            elif remaining == 5:
                print("⏰ 距离目标时间还有5秒!")
            elif remaining == 0:
                print("⏰ 时间到! 测试成功!")
                break
            elif remaining < 0:
                print(f"⏰ 测试完成，时间已过 {abs(remaining)} 秒")
                break
                
            time.sleep(1)
        
        print("\n✓ 基本功能测试通过!")
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def parse_time_string(time_str):
    """解析时间字符串格式：2025-09-28 17:00:00"""
    try:
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        return int(dt.timestamp())
    except ValueError as e:
        print(f"时间格式解析错误: {e}")
        return None

def test_config_format():
    """测试配置文件格式"""
    print("\n=== 配置文件格式测试 ===")
    
    try:
        with open("timer_conf.json", "r", encoding='utf-8') as f:
            config = json.load(f)
        
        if 'timers' not in config:
            print("✗ 配置文件缺少 'timers' 字段")
            return False
            
        timers = config['timers']
        if not isinstance(timers, list):
            print("✗ 'timers' 必须是数组")
            return False
            
        for i, timer in enumerate(timers):
            if 'name' not in timer:
                print(f"✗ 定时器 {i+1} 缺少 'name' 字段")
                return False
            if 'time' not in timer:
                print(f"✗ 定时器 {i+1} 缺少 'time' 字段")
                return False
            if not isinstance(timer['time'], str):
                print(f"✗ 定时器 {i+1} 的 'time' 必须是字符串")
                return False
            # 验证时间格式
            timestamp = parse_time_string(timer['time'])
            if timestamp is None:
                print(f"✗ 定时器 {i+1} 的时间格式不正确")
                return False
        
        print(f"✓ 配置文件格式正确，包含 {len(timers)} 个定时器")
        return True
        
    except Exception as e:
        print(f"✗ 配置文件测试失败: {e}")
        return False

def main():
    """主函数"""
    print("开始时间提醒服务功能测试...\n")
    
    # 运行测试
    tests = [
        test_config_format,
        test_basic_functionality
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== 测试结果 ===")
    print(f"通过: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("\n✓ 所有测试通过!")
        print("\n现在可以运行以下命令启动服务:")
        print("  python3 simple_timer.py")
        print("\n或者使用完整版本:")
        print("  python3 main.py")
        return 0
    else:
        print("\n✗ 部分测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())