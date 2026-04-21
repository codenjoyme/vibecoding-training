# Bash Builtins — Snapshot Test

## Phase 1: Environment

Check the current user.

> `whoami`
```
root
```

Show the current working directory.

> `pwd`
```
/workspace
```

## Phase 2: File Operations

Create a file and verify its content.

> `echo "hello world" > /workspace/test.txt`
```
```
> `cat /workspace/test.txt`
```
hello world
```
> `wc -c /workspace/test.txt`
```
12 /workspace/test.txt
```
