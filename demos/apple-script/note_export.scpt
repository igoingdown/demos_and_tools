on removeHTMLTags(inputString)
    set cleanedString to ""
    set inTag to false
    repeat with i from 1 to length of inputString
        set currentChar to character i of inputString
        if currentChar is "<" then
            set inTag to true
        else if currentChar is ">" then
            set inTag to false
        else if not inTag then
            if currentChar is not "" then
                set cleanedString to cleanedString & currentChar
            end if
        end if
    end repeat
    return cleanedString
end removeHTMLTags

tell application "Notes"
    set allNotes to every note
    repeat with currentNote in allNotes
        set noteTitle to the name of currentNote
        set noteContent to the body of currentNote
        set cleanContent to my removeHTMLTags(noteContent)
        log "正文：" & cleanContent 
    end repeat
end tell

