# Git

## Setup
- `git init` — create a new repo in the current directory
- `git clone <url>` — copy a remote repo down locally
- `git remote add origin <url>` — attach a remote to a local repo
- `git remote -v` — confirm remotes

## Everyday
- `git status` — show what's changed
- `git add <file>` — stage one file
- `git add -A` — stage everything
- `git commit -m "message"` — commit staged changes
- `git push` — push to the tracked upstream branch
- `git push -u origin <branch>` — push and set upstream so plain `git push` works after
- `git pull` — fetch and merge from the tracked upstream branch
- `git log --oneline --graph --decorate --all` — the log view actually worth reading

## Branching
- `git branch` — list local branches
- `git switch -c <name>` — create + switch in one step
- `git switch <name>` — switch to existing branch
- `git merge <branch>` — merge into current branch
- `git rebase <branch>` — replay current branch's commits on top of another
- `git branch -d <name>` — delete (blocks if unmerged)
- `git branch -D <name>` — delete regardless

## Undoing things
- `git restore <file>` — discard unstaged changes to a file
- `git restore --staged <file>` — unstage, keep the edits
- `git reset --soft HEAD~1` — undo last commit, keep changes staged
- `git reset --hard HEAD~1` — undo last commit, discard changes entirely (careful)
- `git revert <commit>` — new commit that undoes an old one; safe on shared/pushed history
- `git stash` — shelve work-in-progress without committing
- `git stash pop` — reapply the most recently stashed changes
- `git stash list` — see all stashed work

## Inspecting
- `git diff` — unstaged changes
- `git diff --staged` — staged changes
- `git show <commit>` — full diff of one commit
- `git blame <file>` — who last touched each line

## Rule of thumb
`reset --hard` and `push --force` rewrite history — fine on a private branch,
dangerous on anything shared. `revert` is the safe default once something's pushed.
