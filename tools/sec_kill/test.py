#!/usr/bin/env python3
"""
测试脚本 - 验证时间提醒服务功能
"""
import json
import time
import os
import sys
from datetime import datetime

def parse_time_string(time_str):
    """解析时间字符串格式：2025-09-28 17:00:00"""
    try:
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        return int(dt.timestamp())
    except ValueError as e:
        print(f"时间格式解析错误: {e}")
        return None

def test_config():
    """测试配置文件"""
    print("=== 测试配置文件 ===")
    
    config_file = "timer_conf.json"
    if not os.path.exists(config_file):
        print(f"✗ 配置文件 {config_file} 不存在")
        return False
        
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        timers = config.get('timers', [])
        print(f"✓ 找到 {len(timers)} 个定时器配置")
        
        for i, timer in enumerate(timers):
            name = timer.get('name', f'定时器{i+1}')
            time_str = timer.get('time', '')
            
            # 解析时间字符串
            timestamp = parse_time_string(time_str)
            if timestamp is None:
                print(f"  {name}: ✗ 时间格式错误")
                continue
                
            target_time = datetime.fromtimestamp(timestamp)
            current_time = datetime.now()
            time_diff = timestamp - current_time.timestamp()
            
            print(f"  {name}:")
            print(f"    目标时间: {target_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"    当前时间: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"    时间差: {time_diff:.0f} 秒")
            
            if time_diff <= 0:
                print(f"    ⚠️  该定时器已过期")
            elif time_diff <= 60:
                print(f"    ⚠️  该定时器即将触发 ({time_diff:.0f} 秒)")
            else:
                print(f"    ✓ 该定时器正常")
                
        return True
        
    except json.JSONDecodeError as e:
        print(f"✗ 配置文件格式错误: {e}")
        return False
    except Exception as e:
        print(f"✗ 读取配置文件时出错: {e}")
        return False

def test_main_script():
    """测试主脚本导入"""
    print("\n=== 测试主脚本 ===")
    
    try:
        # 尝试导入主模块
        sys.path.insert(0, os.getcwd())
        from main import TimerService, TimerWindow
        print("✓ 主脚本导入成功")
        return True
    except ImportError as e:
        print(f"✗ 主脚本导入失败: {e}")
        return False
    except Exception as e:
        print(f"✗ 主脚本测试失败: {e}")
        return False

def test_gui():
    """测试GUI功能"""
    print("\n=== 测试GUI功能 ===")
    
    try:
        import tkinter as tk
        from tkinter import ttk
        print("✓ tkinter 可用")
        
        # 创建测试窗口
        root = tk.Tk()
        root.title("测试窗口")
        root.geometry("200x100")
        
        label = ttk.Label(root, text="GUI测试成功!")
        label.pack(expand=True)
        
        # 3秒后关闭
        root.after(3000, root.destroy)
        root.mainloop()
        
        print("✓ GUI功能正常")
        return True
        
    except Exception as e:
        print(f"✗ GUI测试失败: {e}")
        return False

def create_test_timer():
    """创建测试定时器"""
    print("\n=== 创建测试定时器 ===")
    
    # 创建30秒后的测试定时器
    test_time = datetime.now().timestamp() + 30  # 30秒后
    time_str = datetime.fromtimestamp(test_time).strftime("%Y-%m-%d %H:%M:%S")
    
    test_config = {
        "timers": [
            {
                "name": "测试提醒 (30秒后)",
                "time": time_str  # 使用字符串格式
            }
        ]
    }
    
    try:
        with open("timer_conf.json", "w", encoding='utf-8') as f:
            json.dump(test_config, f, indent=2, ensure_ascii=False)
        
        print(f"✓ 创建测试定时器: {time_str}")
        print("  30秒后将触发提醒窗口")
        return True
        
    except Exception as e:
        print(f"✗ 创建测试定时器失败: {e}")
        return False

def main():
    """主函数"""
    print("=== 时间提醒服务测试程序 ===")
    
    tests = [
        ("配置文件测试", test_config),
        ("主脚本测试", test_main_script),
        ("GUI功能测试", test_gui),
        ("创建测试定时器", create_test_timer)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"✗ {test_name} 失败")
        except Exception as e:
            print(f"✗ {test_name} 出错: {e}")
    
    print(f"\n=== 测试结果 ===")
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("✓ 所有测试通过!")
        print("\n现在可以运行以下命令启动服务:")
        print("  python main.py")
        return 0
    else:
        print("✗ 部分测试失败，请检查错误信息")
        return 1

if __name__ == "__main__":
    sys.exit(main())