#!/bin/sh
crontab ./bbs_comment_crontab
crontab -l
tail -f time.txt
