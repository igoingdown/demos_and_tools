#!/bin/bash

# 检查是否已连接iPhone
if ! system_profiler SPUSBDataType | grep "iPhone"; then
    echo "未检测到连接的iPhone设备"
    exit 1
fi

# 检查是否安装了iMobileDevice工具
if ! command -v idevicebackup2 >/dev/null; then
    echo "请先安装iMobileDevice工具"
    echo "可以使用Homebrew运行以下命令进行安装："
    echo "brew install --HEAD usbmuxd"
    echo "brew unlink usbmuxd"
    echo "brew link usbmuxd"
    echo "brew install --HEAD libimobiledevice"
    echo "brew install --HEAD ifuse"
    exit 1
fi

# 备份iPhone
backup_dir="$HOME/Desktop/iPhone_Backup"
mkdir -p "$backup_dir"
idevicebackup2 backup "$backup_dir"

# 导出语音备忘录
voice_memos_dir="$HOME/Desktop/iPhone_VoiceMemos"
mkdir -p "$voice_memos_dir"
ideviceinstaller -u -l -o export "$backup_dir" | grep -i "voice memo" | awk '{print $4}' | xargs -I{} cp -r "{}" "$voice_memos_dir"

echo "语音备忘录已导出至 $voice_memos_dir"
