# chk

Highly experimental. Note this is my first python code in 5 years ;)

git submodules but better, git subtree but dumber.

Right now this looks like

- the `cp FROM TO` command, but you pass the folder once.
- the `ln -s` command, but you explicitly retrieve newer versions

Dangerous, version everything before running the command, you might lose data.


## Commands

### Operations

```
chk clone
chk push
chk pull
```

### Aliases

Aliases are one very important concept:

```
chk alias add
chk alias rm
chk alias ls
```

This lets you attach a name `my-app:shared-frontend` to a local path. Which might be different for every user.
