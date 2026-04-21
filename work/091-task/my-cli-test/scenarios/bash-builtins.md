# Bash Builtins — Snapshot Test

## Phase 1: Environment

Check the current user.

> `whoami`

Show the current working directory.

> `pwd`

## Phase 2: File Operations

Create a file and verify its content.

> `echo "hello world" > /workspace/test.txt`
> `cat /workspace/test.txt`
> `wc -c /workspace/test.txt`
