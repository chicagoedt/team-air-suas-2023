# Conventions

## Git

### Branching

Branch from main to contribute. Branch names should have an appropriate prefix (usually test/, feat/ or fix/) and under 4 words and 20 characters. They should be all lowercase with dashes '-' in between words.

For example:

- `test/branch-name`
- `feat/branch-name`
- `fix/branch-name`

### Commits

Commits in the branch can be whatever you want, but when you merge to main, you should squash your commits to just the prefix and a short description (like the branch name).

For example:

`git branch feat/add-new-objects`

`git commit -m "feat: add new objects"`

If you have changed a lot in one commit that you want to detail, you can just type `git commit` and git will open up a file for you to edit. The first line of the file should be the short commit message with the prefix. The second line should be blank. And the remaining lines can be whatever you need to explain what you changed.

For example:

`git commit`

...

```
feat: add objects to winch

- change servo speeds
- created new class Winch
- code structure improvements
```

See [here](https://www.conventionalcommits.org/en/v1.0.0-beta.2/) for more information.

### Merging

On your branch, run `git rebase main` to pull the most recent changes to main into your branch (do this periodically, not just when you are finished). Resolve any merge conflicts as you go. When you're finished, squash your commits with `git rebase -i <commit-hash-before-your-first>` and change `pick` to `squash` or `s`.

Now your `git log --oneline` should have only commits with commit prefixes and you should be caught up with the main branch. You can now make a pull request from your branch to main and Advik or Adam can approve it.

## Files

File and directory names should be all lowercase with dashes '-' in between words; i.e. `my-python-script.py` and `/my-directory`. Organize files in appropriate directories.

## Programming Style

Pick a standard and stick to it. If you are writing a new file, choose a commonly-used convention for variable names, spaces, and indentation, and use it throughout your file. If you are editing an existing file, maintain the already chosen conventions.

