set currentDate to current date
set d to day of currentDate as integer
set m to month of currentDate as integer
set currentYear to year of currentDate as string

set currentMonth to text -2 thru -1 of ("00" & m)
set currentDay to text -2 thru -1 of ("00" & d)

set formattedDateString to currentYear & "." & currentMonth & "." & currentDay

-- 获取当前用户的主目录路径
set homeFolder to POSIX path of (path to home folder as string)

-- 定义目录路径
set folderPath to homeFolder & "/Desktop/" & formattedDateString




tell application "Photos"
    activate -- 激活照片应用
    
    delay 2 -- 等待一段时间以确保应用程序完全打开
    
    tell application "System Events"
        tell process "Photos"
            set allMenuItems to menu items of menu "编辑" of menu bar 1
            set foundMenuItem to missing value
            repeat with menuItem in allMenuItems
                if name of menuItem contains "全选" then
                    log name of menuItem 
                    set foundMenuItem to menuItem
                    exit repeat
                end if
            end repeat
            
            if foundMenuItem is not missing value then
                log "aaa"
                click foundMenuItem -- 选中所有照片
            else
                display alert "无法找到菜单项“选择所有”" message "请确保Photos应用程序处于活动状态，并且菜单项名称正确。"
            end if
        end tell
    end tell
    

    log "bbb"
    -- 在此添加导出到指定目录的代码
    set exportFolder to folderPath 

    log "ccc"
    delay 1 -- 等待一段时间以确保导出菜单项可用

    tell application "System Events"
        tell process "Photos"
            set allMenuItems to menu items of menu "文件" of menu bar 1
            set foundMenuItem to missing value
            repeat with menuItem in allMenuItems
                if name of menuItem contains "导出" then
                    log name of menuItem 
                    set foundMenuItem to menuItem
                    exit repeat
                end if
            end repeat
            
            if foundMenuItem is not missing value then
                log "aaa"
                click foundMenuItem -- 选中所有照片
            else
                display alert "无法找到菜单项“导出”" message "请确保Photos应用程序处于活动状态，并且菜单项名称正确。"
            end if

            log "ddd"
            delay 1 -- 等待导出窗口打开

            -- 模拟按下向右箭头键
            --keystroke (ASCII character 29)
            delay 1 -- 等待窗口打开

            -- 模拟按下向下箭头键
            --keystroke (ASCII character 31)
            --keystroke (ASCII character 31)

            --keystroke return -- 确认前往文件夹对话框
        end tell
    end tell

end tell

