# Git Basics

## What is Git?
Git is a distributed version control system created by Linus Torvalds in 2005. It tracks changes in source code during software development, allowing multiple developers to collaborate efficiently. Unlike centralized systems, every developer has a full copy of the repository history on their local machine.

## Essential Git Commands
- `git init` — Initialize a new Git repository in the current directory.
- `git clone <url>` — Create a local copy of a remote repository.
- `git add <file>` — Stage changes for the next commit. Use `git add .` to stage all changes.
- `git commit -m "message"` — Save staged changes with a descriptive message.
- `git push` — Upload local commits to the remote repository.
- `git pull` — Download and merge changes from the remote repository.
- `git status` — Show the current state of the working directory and staging area.
- `git log` — View commit history.

## Branching and Merging
Branches allow you to work on features or fixes in isolation. Create a branch with `git branch feature-name` and switch to it with `git checkout feature-name` (or `git checkout -b feature-name` to do both). When the feature is complete, merge it back with `git merge feature-name` from the main branch.

## What is a Pull Request?
A Pull Request (PR) is a method of submitting contributions to a project. It lets you notify team members that you have completed a feature. The team can then review the code, discuss changes, and merge the branch into the main codebase. PRs are central to collaborative workflows on platforms like GitHub, GitLab, and Bitbucket.

## .gitignore File
The `.gitignore` file tells Git which files or directories to ignore. Common entries include `node_modules/`, `__pycache__/`, `.env`, `*.pyc`, and IDE-specific folders like `.vscode/` or `.idea/`. This keeps the repository clean by excluding generated files, dependencies, and sensitive configuration.
