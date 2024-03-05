-- 选择要导出的图片文件
set imageFiles to choose file with prompt "选择要导出的图片文件：" with multiple selections allowed

-- 设置导出目标文件夹
set exportFolder to choose folder with prompt "选择要导出到的文件夹："



-- 声明一个整型变量并初始化为0
set myInteger to 0

-- 循环使整型变量自增
repeat with i from 1 to 10
    -- 输出当前值
    display dialog "当前值为：" & myInteger
    
    -- 自增
    set myInteger to myInteger + 1
end repeat


-- 导出图片为JPEG格式
repeat with imageFile in imageFiles
    tell application "Preview"
        activate
        open imageFile
--        set fileName to name of imageFile
        --set exportName to exportFolder & "/" & (text 1 thru -5 of fileName) & ".jpg"
        --save document 1 in file exportName as "JPEG" with compression level maximum
        close document 1 without saving
    end tell
end repeat

display dialog "导出完成！"

