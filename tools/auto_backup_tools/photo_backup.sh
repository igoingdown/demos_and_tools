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

# 备份照片
backup_dir="$HOME/Desktop/iPhone_Photos_Backup"
mkdir -p "$backup_dir"
idevicebackup2 backup "$backup_dir" --include "CameraRoll"

echo "照片已备份至 $backup_dir"
