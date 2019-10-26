# Documentation
* [API doc](https://docs.google.com/spreadsheets/d/1B6I-gnoz-LEUB3Nxu2pnc9xj-iwYfOphf2pOYdGjRVQ/edit?usp=sharing) 

# Clone repository
`git clone https://github.com/sduoase/STAR_DICES.git`

# Working on a new story/issue
1. Create a new branch for that story/issue `git checkout -b branch_name`
2. Fix issue/story...
3. Commit your work `git commit -a`. You'll need to write a commit message: explain how you have resolved the issue/story
4. Update your local code with changes made by others `git pull --rebase origin master`
    * You might encounter merge issues during this step if somebody else has modified the same file
    * If that's the case you must resolve them and then execute `git pull --rebase origin master` again
    * Ask for help if you don't know how to resolve merge issues
5. Upload your branch to the GitHub repository `git push -u origin branch_name`
6. Create a pull request selecting the branch you have just created (as compare) `https://github.com/sduoase/STAR_DICES/compare`
7. Wait for code review and approval

