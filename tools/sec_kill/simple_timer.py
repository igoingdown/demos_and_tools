#!/usr/bin/env python3
"""
简化版时间提醒服务 - 不依赖GUI库
"""
import json
import time
import threading
import os
import sys
from datetime import datetime
import platform

class SimpleTimerService:
    def __init__(self):
        self.config_file = "timer_conf.json"
        self.timers = []
        self.running = True
        self.active_alerts = {}  # 存储活跃的提醒
        self.load_config()
        
    def load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.timers = config.get('timers', [])
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 加载了 {len(self.timers)} 个定时器配置")
            print(self.timers)
        except FileNotFoundError:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 配置文件 {self.config_file} 不存在，创建默认配置")
            self.create_default_config()
        except json.JSONDecodeError as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 配置文件格式错误: {e}")
            
    def create_default_config(self):
        """创建默认配置文件"""
        # 创建5分钟后的测试定时器
        default_config = {
            "timers": [
                {
                    "name": "测试提醒 (5分钟后)",
                    "timestamp": int(time.time()) + 300
                }
            ]
        }
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        self.timers = default_config['timers']
        
    def show_alert(self, timer_name, time_left):
        """显示提醒（终端版本）"""
        alert_key = f"{timer_name}_{int(time.time())}"
        
        def run_alert():
            print(f"\n{'='*60}")
            print(f"⏰ 提醒: {timer_name}")
            print(f"⏰ 距离目标时间还有: {time_left} 秒")
            print(f"{'='*60}")
            
            # 显示倒计时
            for i in range(time_left, 0, -1):
                now = datetime.now()
                time_str = now.strftime("%Y-%m-%d %H:%M:%S") + f".{now.microsecond // 1000:03d}"
                print(f"\r当前时间: {time_str} | 倒计时: {i:2d} 秒", end='', flush=True)
                time.sleep(1)
            
            print(f"\n{'='*60}")
            print(f"⏰ 时间到: {timer_name}")
            print(f"{'='*60}\n")
            
            # 播放提示音（如果支持）
            try:
                if platform.system() == "Windows":
                    import winsound
                    winsound.Beep(1000, 1000)  # 频率1000Hz，持续1秒
                elif platform.system() == "Darwin":  # macOS
                    os.system('afplay /System/Library/Sounds/Glass.aiff')
                else:  # Linux
                    os.system('beep -f 1000 -l 1000 2>/dev/null || echo -e "\a"')
            except:
                pass  # 如果播放声音失败，忽略
        
        # 在新线程中运行提醒，避免阻塞主循环
        alert_thread = threading.Thread(target=run_alert)
        alert_thread.daemon = True
        alert_thread.start()
        
    def check_timers(self):
        """检查定时器"""
        current_time = int(time.time())
        # print(current_time)
        
        for timer in self.timers:
            target_time = timer['timestamp']
            #print(target_time)
            time_diff = target_time - current_time
            print(time_diff)
            
            # 如果距离目标时间还有1分钟（60秒）
            if 0 < time_diff <= 60:
                # 避免重复提醒同一个定时器
                alert_key = f"{timer['name']}_{target_time}"
                if alert_key not in self.active_alerts:
                    self.active_alerts[alert_key] = True
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] 提醒: {timer['name']} 将在 {time_diff} 秒后到达")
                    self.show_alert(timer['name'], time_diff)
                    
            # 如果定时器已过期，从活跃提醒中移除
            elif time_diff <= 0:
                alert_key = f"{timer['name']}_{target_time}"
                if alert_key in self.active_alerts:
                    del self.active_alerts[alert_key]
                    
    def run(self):
        """运行服务"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 定时器服务启动...")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 配置文件: {self.config_file}")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 按 Ctrl+C 停止服务")
        
        while self.running:
            try:
                self.check_timers()
                time.sleep(1)  # 每秒检查一次
            except KeyboardInterrupt:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 服务停止中...")
                self.running = False
                break
            except Exception as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 发生错误: {e}")
                time.sleep(1)
                
    def stop(self):
        """停止服务"""
        self.running = False

def create_test_config():
    """创建测试配置"""
    # 创建30秒后的测试定时器
    test_config = {
        "timers": [
            {
                "name": "测试提醒 (30秒后)",
                "timestamp": int(time.time()) + 30
            },
            {
                "name": "测试提醒 (45秒后)",
                "timestamp": int(time.time()) + 45
            }
        ]
    }
    
    with open("timer_conf.json", "w", encoding='utf-8') as f:
        json.dump(test_config, f, indent=2, ensure_ascii=False)
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 已创建测试配置")
    for timer in test_config['timers']:
        target_time = datetime.fromtimestamp(timer['timestamp'])
        print(f"  {timer['name']}: {target_time.strftime('%H:%M:%S')}")

def main():
    """主函数"""
    # 如果没有配置文件，创建测试配置
    if not os.path.exists("timer_conf.json"):
        create_test_config()
    
    # 启动服务
    service = SimpleTimerService()
    
    try:
        service.run()
    except KeyboardInterrupt:
        service.stop()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 服务已停止")

if __name__ == "__main__":
    main()
