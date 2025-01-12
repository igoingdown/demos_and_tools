-- 获取当前日期
set currentDate to current date
set dateString to (currentDate as string)
set currentWeekday to currentDate's weekday
display dialog "Today is " & currentWeekday

-- 获取天气信息（请替换为您的 API 密钥）
--set weatherInfo to do shell script "curl -s 'https://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q=Beijing' | jq -r '.current.condition.text'"

-- 生成备忘录标题
set memoTitle to dateString & " " & currentWeekday

-- 打开 Safari 并抓取网页
tell application "Safari"
    activate
    open location "https://m.bj.bendibao.com/news/251071.html"
    delay 5 -- 等待页面加载
end tell

-- 截图并保存
set screenshotPath to (path to desktop as text) & "screenshot.png"
do shell script "screencapture -x " & quoted form of POSIX path of screenshotPath

-- 创建备忘录并插入截图
tell application "Notes"
    set newNote to make new note with properties {name:memoTitle, body:""}
    tell newNote
        -- 使用 POSIX 路径创建附件
        make new attachment with properties {file:POSIX file (POSIX path of screenshotPath)}
    end tell
end tell

-- 关闭 Safari
tell application "Safari" to quit

