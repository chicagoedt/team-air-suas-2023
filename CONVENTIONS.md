# Conventions

## Git

### Branching

Branch from main to contribute. Branch names should have an appropriate prefix (usually test/, feat/ or fix/) and under 4 words and 20 characters. They should be all lowercase with dashes '-' in between words.

- test/branch-name
- feat/branch-name
- fix/branch-name

### Commits

Commits in the branch can be whatever you want, but when you merge to main, you should squash your commits to just the prefix and a short description (the branch name works). Add more detail on what you did in the body of the commit.

For example:

branch: `feat/add-new-objects`
commit: `feat: add new objects`

If there was extra detail I needed to add to the commit, the whole commit would look like this:

```
feat: add objects to winch

- change servo speeds
- created new class Winch
- code structure improvements
```

### Merging

On your branch, run `git rebase main` to pull the most recent changes to main into your branch (do this periodically, not just when you are finished). Resolve any merge conflicts as you go. When you're finished, squash your commits with `git rebase -i <commit-hash-before-your-first>` and change `pick` to `squash` or `s`.

Now your `git log --oneline` should have only commits with commit prefixes and you should be caught up with the main branch. You can now make a pull request from your branch to main and Advik or Adam can approve it.

## Files

File and directory names should be all lowercase with dashes '-' in between words; i.e. `my-python-script.py` and `/my-directory`. Organize files in appropriate directories.

## Programming Style

Pick a standard and stick to it. If you are writing a new file, choose a commonly-used convention for variable names, spaces, and indentation, and use it throughout your file. If you are editing an existing file, maintain the already chosen conventions.

