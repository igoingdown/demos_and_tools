display dialog "导出完成！"


tell application "Voice Memos"
    activate -- 激活语音备忘录应用

    delay 2 -- 等待一段时间以确保应用程序完全打开

    tell application "System Events"
        tell process "Voice Memos"
            -- 选择所有语音备忘录
            click menu item "选择所有" of menu "编辑" of menu bar 1

            -- 等待一段时间以确保选择完成
            delay 2

            -- 获取选中的语音备忘录
            set selectedMemos to selected of list 1 of scroll area 1 of window 1
        end tell
    end tell

    -- 导出选中的语音备忘录
    repeat with aMemo in selectedMemos
        set memoName to name of aMemo
        set exportPath to "Macintosh HD:Users:YourUsername:Desktop:" & memoName & ".mp3" -- 修改为你的目标文件夹路径
        export aMemo to POSIX file exportPath as "MP3"
    end repeat
end tell

