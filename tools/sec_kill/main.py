#!/usr/bin/env python3
import json
import time
import threading
import os
import sys
from datetime import datetime
import platform

# GUI库
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    print("请安装tkinter: pip install tk")
    sys.exit(1)

class TimerWindow:
    def __init__(self, timer_name, service=None):
        self.root = tk.Tk()
        self.service = service
        self.root.title(f"时间提醒 - {timer_name}")
        self.root.geometry("500x200")
        
        # 设置窗口在最前面
        self.root.attributes('-topmost', True)
        
        # 创建标签显示时间
        self.time_label = ttk.Label(
            self.root, 
            text="", 
            font=('Arial', 24),
            anchor='center'
        )
        self.time_label.pack(expand=True, fill='both', padx=20, pady=20)
        
        # 创建提示信息
        self.info_label = ttk.Label(
            self.root,
            text=f"提醒: {timer_name}",
            font=('Arial', 14),
            anchor='center'
        )
        self.info_label.pack(pady=10)
        
        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # 更新时间的标志
        self.running = True
        
        # 开始更新时间
        self.update_time()
        
    def update_time(self):
        if self.running:
            # 获取当前时间，精确到微秒
            now = datetime.now()
            time_str = now.strftime("%Y-%m-%d %H:%M:%S") + f".{now.microsecond // 1000:03d}"
            self.time_label.config(text=time_str)
            # 每100毫秒更新一次
            self.root.after(20, self.update_time)
    
    def on_close(self):
        self.running = False
        self.root.destroy()
        # 通知服务窗口已关闭
        if hasattr(self, 'service'):
            self.service.current_window = None
    
    def show(self):
        self.root.mainloop()

class TimerService:
    def __init__(self):
        self.config_file = "timer_conf.json"
        self.timers = []
        self.running = True
        self.current_window = None  # 当前显示的窗口
        self.load_config()
        
    def load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.timers = config.get('timers', [])
            print(f"加载了 {len(self.timers)} 个定时器配置")
            print(self.timers)
        except FileNotFoundError:
            print(f"配置文件 {self.config_file} 不存在，创建默认配置")
            self.create_default_config()
        except json.JSONDecodeError as e:
            print(f"配置文件格式错误: {e}")
            
    def create_default_config(self):
        """创建默认配置文件"""
        # 获取当前时间并格式化为字符串
        now = datetime.now()
        future_time = now.replace(second=0) + 300  # 5分钟后，秒数设为0
        time_str = future_time.strftime("%Y-%m-%d %H:%M:%S")
        
        default_config = {
            "timers": [
                {
                    "name": "示例提醒",
                    "time": time_str  # 使用字符串格式
                }
            ]
        }
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        self.timers = default_config['timers']
        
    def parse_time_string(self, time_str):
        """解析时间字符串格式：2025-09-28 17:00:00"""
        try:
            dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            return int(dt.timestamp())
        except ValueError as e:
            print(f"时间格式解析错误: {e}")
            return None
            
    def check_timers(self):
        """检查定时器"""
        current_time = int(time.time())
        
        for timer in self.timers:
            # 获取时间字符串并解析为时间戳
            time_str = timer.get('time', '')
            target_time = self.parse_time_string(time_str)
            
            if target_time is None:
                continue
                
            time_diff = target_time - current_time
            
            print(f"定时器 {timer['name']}: 距离目标时间还有 {time_diff} 秒")

            # 如果距离目标时间还有1分钟（60秒）
            if 0 < time_diff <= 60:
                print(f"提醒: {timer['name']} 将在 {time_diff} 秒后到达")
                self.show_timer_window(timer['name'])
                
    def show_timer_window(self, timer_name):
        """显示定时器窗口"""
        # macOS要求GUI必须在主线程，使用非阻塞方式显示窗口
        if self.current_window is None:
            self.current_window = TimerWindow(timer_name, service=self)
            # 不调用mainloop，让主循环处理GUI事件
        
    def run(self):
        """运行服务"""
        print("定时器服务启动...")
        
        while self.running:
            try:
                self.check_timers()
                
                # 处理GUI事件（必须在主线程）
                if self.current_window:
                    try:
                        self.current_window.root.update()
                    except:
                        self.current_window = None
                        
                time.sleep(0.02)  # 每100毫秒检查一次，提高GUI响应性
                
            except KeyboardInterrupt:
                print("\n服务停止中...")
                self.running = False
                break
            except Exception as e:
                print(f"发生错误: {e}")
                time.sleep(1)
                
    def stop(self):
        """停止服务"""
        self.running = False

def create_service_script():
    """创建系统服务脚本"""
    system = platform.system()
    
    if system == "Windows":
        # Windows服务脚本
        service_script = '''@echo off
cd /d "%~dp0"
python main.py
pause'''
        
        with open("start_service.bat", "w") as f:
            f.write(service_script)
            
        # Windows任务计划程序XML配置
        task_xml = f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}</Date>
    <Author>TimerService</Author>
    <Description>时间提醒服务</Description>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
    </LogonTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>false</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>6</Priority>
  </Settings>
  <Actions>
    <Exec>
      <Command>{sys.executable}</Command>
      <Arguments>main.py</Arguments>
      <WorkingDirectory>{os.getcwd()}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>'''
        
        with open("timer_service.xml", "w", encoding='utf-8') as f:
            f.write(task_xml)
            
    elif system == "Darwin":  # macOS
        # macOS LaunchAgent plist
        plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.timer.service</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{os.path.join(os.getcwd(), "main.py")}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>{os.path.join(os.getcwd(), "timer_service.log")}</string>
    <key>StandardErrorPath</key>
    <string>{os.path.join(os.getcwd(), "timer_service_error.log")}</string>
</dict>
</plist>'''
        
        with open("com.timer.service.plist", "w") as f:
            f.write(plist_content)
            
        # macOS启动脚本
        start_script = f'''#!/bin/bash
cd "{os.getcwd()}"
launchctl load com.timer.service.plist
'''
        
        with open("start_service.sh", "w") as f:
            f.write(start_script)
        os.chmod("start_service.sh", 0o755)
        
        # macOS停止脚本
        stop_script = f'''#!/bin/bash
launchctl unload com.timer.service.plist
'''
        
        with open("stop_service.sh", "w") as f:
            f.write(stop_script)
        os.chmod("stop_service.sh", 0o755)

def main():
    """主函数"""
    # 创建服务脚本
    print("aaa")
    create_service_script()
    
    # 启动服务
    service = TimerService()
    
    try:
        service.run()
    except KeyboardInterrupt:
        service.stop()
        print("服务已停止")

if __name__ == "__main__":
    main()
