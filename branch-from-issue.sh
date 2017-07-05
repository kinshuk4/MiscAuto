git checkout master
git pull origin master
issueNum=150
issueString=""
branchName="ISSUE-"$issueNum
git checkout -b $branchName

git add --all
git commit -m $issueString
git push origin $branchName


git checkout my-feature-branch
git pull origin my-feature-branch
git pull origin master

 $ git checkout master
 $ git pull origin master
 $ git merge --no-ff my-feature-branch

 git branch -d my-feature-branch