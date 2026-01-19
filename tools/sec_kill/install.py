#!/usr/bin/env python3
"""
安装脚本 - 设置时间提醒服务
"""
import os
import sys
import platform
import subprocess

def install_requirements():
    """安装依赖"""
    print("正在检查依赖...")
    try:
        import tkinter
        print("✓ tkinter 已安装")
    except ImportError:
        print("✗ tkinter 未安装")
        print("请手动安装 tkinter:")
        if platform.system() == "Windows":
            print("  Windows: tkinter 通常随Python一起安装")
        elif platform.system() == "Darwin":
            print("  macOS: brew install python-tk")
        elif platform.system() == "Linux":
            print("  Linux: sudo apt-get install python3-tk")
        return False
    return True

def setup_service():
    """设置系统服务"""
    system = platform.system()
    
    if system == "Windows":
        print("\nWindows 系统设置:")
        print("1. 使用任务计划程序创建定时任务")
        print("2. 运行以下命令创建任务:")
        print(f"   schtasks /create /xml \"{os.path.join(os.getcwd(), 'timer_service.xml')}\" /tn \"TimerService\"")
        print("\n或者手动运行 start_service.bat 启动服务")
        
    elif system == "Darwin":  # macOS
        print("\nmacOS 系统设置:")
        plist_path = os.path.expanduser("~/Library/LaunchAgents/com.timer.service.plist")
        
        try:
            # 复制plist文件到LaunchAgents目录
            subprocess.run(["cp", "com.timer.service.plist", plist_path], check=True)
            print(f"✓ 已复制服务文件到 {plist_path}")
            
            # 加载服务
            subprocess.run(["launchctl", "load", plist_path], check=True)
            print("✓ 服务已加载并设置为开机自启")
            
        except subprocess.CalledProcessError as e:
            print(f"✗ 设置服务时出错: {e}")
            print("请手动运行以下命令:")
            print(f"  cp com.timer.service.plist ~/Library/LaunchAgents/")
            print("  launchctl load ~/Library/LaunchAgents/com.timer.service.plist")
            
    else:
        print(f"不支持的操作系统: {system}")
        return False
        
    return True

def main():
    """主函数"""
    print("=== 时间提醒服务安装程序 ===")
    
    # 检查依赖
    if not install_requirements():
        print("依赖检查失败，请手动安装缺失的依赖")
        return 1
    
    # 设置服务
    if not setup_service():
        print("服务设置失败")
        return 1
    
    print("\n✓ 安装完成!")
    print("\n使用方法:")
    print("1. 编辑 timer_conf.json 文件添加你的定时器")
    print("2. 服务将在系统启动时自动运行")
    print("3. 也可以手动运行: python main.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())