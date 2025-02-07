-- 获取当前日期
set currentDate to current date
set d to day of currentDate as integer
set m to month of currentDate as integer
set currentYear to year of currentDate as string
set currentWeekday to currentDate's weekday

set currentMonth to text -2 thru -1 of ("00" & m)
set currentDay to text -2 thru -1 of ("00" & d)


set formattedDateString to currentYear & "." & currentMonth  & "." & currentDay & " " & currentWeekday 

-- 设置备忘录标题
set noteTitle to formattedDateString

set noteBody to "最重要的事" & return & "业务"& return & "技术"& return & "管理"& return & "稳定性"


-- 创建备忘录
tell application "Notes"
    activate
    set newNote to make new note with properties {name:noteTitle, body:noteBody}
end tell
