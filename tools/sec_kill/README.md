# 时间提醒服务

一个跨平台的时间提醒服务，支持Windows和macOS系统。

## 功能特点

- ⏰ 每秒检查配置文件中的定时器
- 🔔 距离目标时间1分钟时弹出提醒窗口
- 🖥️ 窗口实时显示当前时间（精确到微秒）
- 🔄 支持异步执行和系统启动自动运行
- 💻 跨平台支持（Windows、macOS）

## 文件结构

```
├── timer_conf.json      # 配置文件（定时器列表）
├── main.py             # 主服务脚本
├── install.py          # 安装脚本
├── test.py             # 测试脚本
├── start_service.bat   # Windows启动脚本
├── timer_service.xml   # Windows任务计划配置
├── com.timer.service.plist  # macOS LaunchAgent配置
├── start_service.sh    # macOS启动脚本
└── stop_service.sh     # macOS停止脚本
```

## 快速开始

### 1. 测试服务
```bash
python test.py
```

### 2. 运行服务
```bash
python main.py
```

### 3. 安装为系统服务
```bash
python install.py
```

## 配置文件格式

编辑 `timer_conf.json` 文件添加定时器：

```json
{
  "timers": [
    {
      "name": "会议提醒",
      "timestamp": 1738003200
    },
    {
      "name": "休息提醒", 
      "timestamp": 1738003260
    }
  ]
}
```

时间戳获取方法：
```python
import time
# 获取当前时间戳
print(int(time.time()))
# 获取10分钟后的时间戳
print(int(time.time()) + 600)
```

## 系统要求

- Python 3.6+
- tkinter（通常随Python一起安装）

## 平台特定说明

### Windows
- 使用任务计划程序实现开机自启
- 支持通过 `start_service.bat` 手动启动

### macOS
- 使用 LaunchAgent 实现开机自启
- 支持通过 `start_service.sh` 和 `stop_service.sh` 控制服务

## 使用说明

1. 编辑 `timer_conf.json` 添加你的定时器
2. 运行 `python main.py` 启动服务
3. 服务会在后台运行，每秒检查定时器
4. 当距离目标时间1分钟时，会弹出提醒窗口
5. 窗口显示实时时间，精确到微秒

## 注意事项

- 时间戳使用Unix时间戳（秒）
- 窗口弹出后需要手动关闭
- 服务支持异步执行，不会阻塞系统
- 配置文件修改后无需重启服务，会自动重新加载