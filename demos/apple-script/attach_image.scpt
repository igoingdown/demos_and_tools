-- 指定要插入的图片路径
set imagePath to (path to desktop as text) & "s.png" -- 请替换为您的图片文件名
set posixPath to POSIX path of imagePath 
display dialog posixPath

if (do shell script "test -e " & quoted form of POSIX path of imagePath & " && echo true || echo false") is "true" then
    -- 插入附件
else
    display dialog "图片未找到！"
end if


-- 告诉“备忘录”应用程序执行以下操作
tell application "Notes"
    -- 创建一个新的备忘录
    set newNote to make new note with properties {name:"新备忘录", body:"这是我的新备忘录，包含一张图片。"}
    set theFile to posixPath as POSIX file
    -- 将图片添加为附件
    tell newNote to make new attachment with data theFile
end tell
-- 显示完成提示
display dialog "备忘录已创建，并插入了图片。"

