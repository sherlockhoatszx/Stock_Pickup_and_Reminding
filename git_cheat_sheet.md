# Git Cheat Sheet

## 基本操作

`git status` 查看当前状态

`git add` 将修改后的文件加入暂存区

`git commit -m <msg>` 提交更改

`git commit -am <msg>` 自动将 index 中的修改后的文件加入暂存区


## 版本回退或前进


`git log` 查看 git 历史版本, 显示 commit id, author, date, updated file 等信息

`git log --pretty=oneline` 查看 git 历史版本简单信息, 包括 commit id, 文件变动两个信息

`git log --graph` 可以看到分支合并图, `--graph` 可以和 `--pretty-oneline` 同时使用

`git reset --hard <commit_id>` 回退(或前进)版本, commit id 仅需输入前几位(不可过少, 须使 git 系统可唯一确定版本)

`git reflog` 显示 git 命令历史及对应的 commit id

## 查看和管理修改

`git diff <file>` 查看文件修改(commit 之前)

`git diff HEAD -- <file>` 查看工作区和版本库中文件的区别

`git checkout -- <file>` 丢弃**工作区**中对 file 的修改

`git reset HEAD <file>` 撤销(unstage)**暂存区**中对 file 的修改

## 文件删除

`git rm <file>` 将 file 从 git 跟踪文件列表中删除

## 远程仓库

`git remote add <remote-name> <url>` 添加远程仓库

`git remote remove <remote-name>` 从本地删除远程仓库信息

`git push -u origin master` 将本地 master 分支推送到名为 origin 的远程仓库, -u 表示将本地 master 分支和远程的 master 分支关联, 以后推送或拉取时可简化命令

`git clone <url>` 从远程仓库克隆

`git remote -v` 查看所有远程仓库(all remote repositories)

## 分支管理

`git branch <branch>` 创建分支

`git checkout <branch>` 切换到 branch 分支

`git checkout -b <branch>` 创建分支并切换到新建分支

`git branch` 查看当前所有分支

`git merge <branch>` 将 branch 分支合并到当前分支. 可使用 `--no-ff` 选项禁用 `FastForward`模式

`git branch -d <branch>` 删除分支

`git pull` 从远程仓库拉取分支, 如果已经设置本地和远程的分支联接

`git pull <remote> <branch>` 从远程拉取指定分支, 完整命令

`git branch --set-upstream dev orgin/dev` 指定本地 dev 分支和远程 dev 分支的联接

`冲突` 当两个分支对同一文件进行了不同修改的时候, 产生冲突. 合并时, Git 系统会在该文件中对所有修改进行标记, 需进入该文件, 手动解决冲突

## 参考资料

1. [Pro Git](https://git-scm.com/book/zh/v2)
2. [廖雪峰: Git 教程](http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)
3. [多人协作](http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/0013760174128707b935b0be6fc4fc6ace66c4f15618f8d000)
