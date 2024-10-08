# using powershell

1. Get large files path 

git rev-list --objects --all | git cat-file --batch-check='%(objectsize:disk) %(rest)' | Where-Object { $_ -match '^[0-9]+\s' -and [int]$_.Split(' ')[0] -gt 100MB } | Sort-Object

2. add trackin 

git lfs install
git lfs track "models/models.pkl"

3. Git attribute 

git add .gitattributes

4. Add path 

git add models/  

5.  Commit and push 

 git commit -m "Add large files with Git LFS"
 git push
 


