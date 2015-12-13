# Git 使用规范建议

1. master 作为发布分支，确保 master 上的为当前最稳定的可工作代码，不可进行代码修改操作；master 分支上须打上标签注明版本号。
2. dev 分支为开发分支，所有新功能点的开发代码经确认后合并到该分支；须确保该分支任何时刻均处于代码完整可测试状态；阶段开发完成并测试确认后，merge 到  master 分支发布。
3. 新功能点开发分支命名 fea[功能点编号]，由 dev 分支 fork，功能点完成后，经测试确认，merge 到dev 分支；若新功能点放弃开发，不做 merge，保留该 feature 分支。示范：`git checkout -b fea34`
4. bug 修复分支：重大 bug 需开新分支修复的，首先在 Github 上发布 Issue，简要说明 bug 情况及修改方案，由 bug 所在分支[master 及 dev 之一] fork 出分支 fix+issue 编号，完成修改确认成功后 merge 回原来分支；修改失败，保留修复分支，不做 merge。示范：`git checkout -b fix23`
