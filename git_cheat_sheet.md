# Git Cheat Sheet

## 基本操作

`git status` 查看当前状态

`git diff <filename>` 查看文件修改(commit 之前)

`git add` 将修改后的文件加入暂存区

`git commit -m <msg>` 提交更改

`git commit -am <msg>` 自动将 index 中的修改后的文件加入暂存区


## 版本回退或前进


`git log` 查看 git 历史版本, 显示 commit id, author, date, updated file 等信息

`git log --pretty=oneline` 查看 git 历史版本简单信息, 包括 commit id, 文件变动两个信息

`git reset --hard <commit_id>` 回退(或前进)版本, commit id 仅需输入前几位(不可过少, 须使 git 系统可唯一确定版本)

`git reflog` 显示 git 命令历史及对应的 commit id

