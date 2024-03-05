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




-- 检查目录是否存在
set folderExists to (do shell script "[ -d " & quoted form of folderPath & " ] && echo 'true' || echo 'false'")

-- 如果目录不存在，则创建目录
if folderExists is "false" then
    do shell script "mkdir -p " & quoted form of folderPath
    display dialog "目录已创建！"
else
    display dialog "目录已存在！"
end if

-- 设置导出目录
set exportFolder to folderPath


tell application "Photos"
    activate
    delay 2 -- 等待一会儿以确保照片应用已经完全打开

    set allPhotos to get every media item of folder "Photos"

    
     -- 导出所有照片
    repeat with aPhoto in allPhotos
        export aPhoto to POSIX file (exportFolder & "/" & name of aPhoto & ".jpg") as alias
    end repeat
end tell
