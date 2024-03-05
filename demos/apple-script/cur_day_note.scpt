-- 获取当前日期
set currentDate to current date
set d to day of currentDate as integer
set m to month of currentDate as integer
set currentYear to year of currentDate as string

set currentMonth to text -2 thru -1 of ("00" & m)
set currentDay to text -2 thru -1 of ("00" & d)


set formattedDateString to currentYear & "." & currentMonth  & "." & currentDay

-- 设置备忘录标题
set noteTitle to formattedDateString

-- 创建备忘录
tell application "Notes"
    activate
    set newNote to make new note with properties {name:noteTitle, body:""}
end tell


