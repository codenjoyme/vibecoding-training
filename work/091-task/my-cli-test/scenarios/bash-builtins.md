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

> `echo "hello snapshot testing" > /workspace/test.txt`
```
```
> `cat /workspace/test.txt`
```
hello snapshot testing
```
> `wc -c /workspace/test.txt`
```
23 /workspace/test.txt
```
