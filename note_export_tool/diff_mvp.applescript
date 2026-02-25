-- ==========================================
-- MVP：查找“隐藏”在其他文件夹的笔记（无任何配置能力）
-- 核心能力：在 Notes 指定账户中，找出不在“主文件夹”的笔记并生成报告
-- 用法：osascript diff_mvp.applescript
-- ==========================================

on run
	set reportPath to (POSIX path of (path to desktop folder)) & "Folder_Mismatch_Report_MVP.txt"
	set mismatchCount to 0
	set faultCount to 0
	set mismatchLines to {}
	set faultLines to {}

	tell application "Notes"
		try
			set targetAccount to my pickTargetAccount()
			set mainFolder to my pickMainFolder(targetAccount)

			log "[MVP] 账户: " & (name of targetAccount)
			log "[MVP] 主文件夹: " & (name of mainFolder)

			-- 更快的做法：枚举账户下所有 folder，跳过主文件夹，仅处理其余文件夹中的笔记
			set allFolders to every folder of targetAccount
			set totalFolders to count of allFolders
			log "[MVP] 扫描文件夹数: " & totalFolders

			repeat with fIdx from 1 to totalFolders
			set aFolder to item fIdx of allFolders
			if aFolder is not mainFolder then
				try
					set folderName to name of aFolder

					-- 优先批量拉取属性（通常更快）；失败则回退到逐条处理
					try
						set noteTitles to name of every note of aFolder
						set noteIDs to id of every note of aFolder
						set folderNoteCount to count of noteIDs

						if folderNoteCount > 0 then
							log "[MVP] 处理文件夹: " & folderName & " (" & folderNoteCount & ")"
						end if

						repeat with nIdx from 1 to folderNoteCount
							set nTitle to item nIdx of noteTitles
							set nID to item nIdx of noteIDs
							set mismatchCount to mismatchCount + 1
							set end of mismatchLines to "[" & folderName & "] | 标题: " & nTitle & " | id: " & nID
						end repeat
					on error errMsg number errNum
						-- 回退：逐条处理，尽量不要让单个笔记阻塞整个文件夹
						set folderNotes to every note of aFolder
						set folderNoteCount to count of folderNotes
						if folderNoteCount > 0 then log "[MVP] 逐条处理文件夹: " & folderName & " (" & folderNoteCount & ")"
						repeat with nIdx from 1 to folderNoteCount
							set aNote to item nIdx of folderNotes
							try
								set nTitle to name of aNote
								set nID to id of aNote
								set mismatchCount to mismatchCount + 1
								set end of mismatchLines to "[" & folderName & "] | 标题: " & nTitle & " | id: " & nID
							on error noteErrMsg number noteErrNum
								set faultCount to faultCount + 1
								set end of faultLines to "(" & noteErrNum & ") " & noteErrMsg
							end try
						end repeat
				end try
				on error errMsg number errNum
					set faultCount to faultCount + 1
					set end of faultLines to "(" & errNum & ") " & errMsg
				end try
			end if
		end repeat
		on error errMsg number errNum
			-- Notes 访问级别错误（例如权限/脚本字典变化）
			my writeReport(reportPath, "[MVP] 运行失败: (" & errNum & ") " & errMsg & return, {}, 0, {}, 0)
			return reportPath
		end try
	end tell

	set reportText to "--- 异常笔记查找报告（MVP）---" & return
	set reportText to reportText & "报告路径: " & reportPath & return
	set reportText to reportText & "----------------------------" & return
	set reportText to reportText & "发现不在主文件夹的笔记数: " & mismatchCount & return
	set reportText to reportText & "无法访问的笔记数: " & faultCount & return & return

	if mismatchCount > 0 then
		set reportText to reportText & "--- 明细 ---" & return
		set reportText to reportText & (my joinLines(mismatchLines)) & return
		set reportText to reportText & return
	end if

	if faultCount > 0 then
		set reportText to reportText & "--- 错误 ---" & return
		set reportText to reportText & (my joinLines(faultLines)) & return
	end if

	my writeReport(reportPath, reportText, mismatchLines, mismatchCount, faultLines, faultCount)
	return reportPath
end run

-- 用换行拼接列表（避免循环在不同编译器/环境下的兼容性问题）
on joinLines(theList)
	if theList is {} then return ""
	set oldTIDs to AppleScript's text item delimiters
	set AppleScript's text item delimiters to return
	set joinedText to theList as text
	set AppleScript's text item delimiters to oldTIDs
	return joinedText
end joinLines

-- 选择目标账户：优先 iCloud，否则回退到第一个账户
on pickTargetAccount()
	tell application "Notes"
		try
			return first account whose name is "iCloud"
		on error
			return first account
		end try
	end tell
end pickTargetAccount

-- 选择主文件夹：优先“备忘录”，否则尝试常见名称
on pickMainFolder(targetAccount)
	tell application "Notes"
		try
			return first folder of targetAccount whose name is "备忘录"
		on error
			set possibleNames to {"备忘录", "Notes", "我的备忘录", "My Notes"}
			repeat with folderName in possibleNames
				try
					return first folder of targetAccount whose name is folderName
				on error
					-- 继续尝试
				end try
			end repeat
			-- 最后兜底：直接取第一个 folder
			return first folder of targetAccount
		end try
	end tell
end pickMainFolder

-- 写入报告文件（纯文件输出，不弹窗）
on writeReport(reportPath, reportText, mismatchLines, mismatchCount, faultLines, faultCount)
	try
		set fileRef to open for access (POSIX file reportPath) with write permission
		set eof fileRef to 0
		write reportText to fileRef as «class utf8»
		close access fileRef
		log "[MVP] 报告已写入: " & reportPath
	on error errMsg number errNum
		try
			close access (POSIX file reportPath)
		end try
		log "[MVP] 写入报告失败: (" & errNum & ") " & errMsg
	end try
end writeReport
