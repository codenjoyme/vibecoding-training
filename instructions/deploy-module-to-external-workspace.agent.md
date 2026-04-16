# Deploy Training Module to External Workspace

Deploy any training module into an external project folder so a user can run the training there in a separate IDE window.

## When to Use

- User wants to practice a module inside their own project (not the course workspace)
- User specifies an external folder path (e.g., `C:\Java\qwe`, `~/projects/my-app`)
- Module needs to run outside the course workspace for any reason

## Input

1. **Module ID** — e.g., `056`, `120`, `400`
2. **Target folder** — absolute path to the external workspace

## Procedure

### 1. Resolve module path

```
modules/{module-id}-{module-name}/
```

Read `about.md` and `walkthrough.md` from the module folder. Confirm both exist.

### 2. Create `.training/` in target folder

```
{target-folder}/
  .training/
    about.md              ← from module
    walkthrough.md        ← from module
    training-mode.agent.md ← from instructions/
```

- Create `{target-folder}/.training/` directory
- Copy module's `about.md` → `.training/about.md`
- Copy module's `walkthrough.md` → `.training/walkthrough.md`
- Copy `instructions/training-mode.agent.md` → `.training/training-mode.agent.md`

### 3. Confirm and give launch prompt

Tell the user:

1. Open `{target-folder}` in a new IDE window
2. Start a new AI chat and paste:

```
Use the instructions in the .training/ folder to start the training module.
```

## Rules

- Do NOT copy `instructions/`, `modules/`, or any other course structure — only `.training/`
- Do NOT modify original files in the course workspace
- If the target folder does not exist — create it
- If `.training/` already exists in the target — overwrite files (module update)
- If the module has `external_workspace: true` in walkthrough frontmatter — the walkthrough itself may create additional structure (clones, installers); `.training/` setup still applies the same way
