-- 每天生成一篇当天的备忘录；周日/月末/年末额外生成对应的总结备忘录。
-- 内容均为空，模板后续迭代。

-- 幂等：已存在同名备忘录则跳过。重复执行（含 cron 失败后重试）不会产生重复条目，
-- 周日/月末这种一次多篇的情况下，也只补齐缺失的那几篇。
set noteBody to ""

tell application "Notes"
	activate
	repeat with noteTitle in my titlesFor(current date)
		set t to noteTitle as string
		if (count (every note whose name is t)) is 0 then
			make new note with properties {name:t, body:noteBody}
		end if
	end repeat
end tell


-- 计算指定日期需要创建的所有备忘录标题
on titlesFor(d)
	-- 默认只有当天这一篇
	set titles to {my formatDate(d) & " " & ((weekday of d) as string)}

	-- 周日：补一篇周总结，标题为本周起始日期到结束日期（周一 ~ 周日）
	if weekday of d is Sunday then
		set end of titles to my formatDate(d - 6 * days) & "-" & my formatDate(d) & " 周总结"
	end if

	-- 次日为 1 号，说明今天是月末
	if day of (d + 1 * days) is 1 then
		set end of titles to my formatYearMonth(d) & " 月度总结"

		-- 12 月的月末即年末，再补一篇年度总结
		if month of d is December then
			set end of titles to ((year of d) as string) & " 年度总结"
		end if
	end if

	return titles
end titlesFor

-- YYYY.MM.DD
on formatDate(d)
	return my formatYearMonth(d) & "." & my pad2(day of d)
end formatDate

-- YYYY.MM
on formatYearMonth(d)
	return ((year of d) as string) & "." & my pad2((month of d) as integer)
end formatYearMonth

on pad2(n)
	return text -2 thru -1 of ("00" & n)
end pad2
