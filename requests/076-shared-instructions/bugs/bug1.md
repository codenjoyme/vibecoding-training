эта логика групп непонятная, я хочу init сделать а меня группу просят, я хз что писать там. Можешь сам из pacakge.json взять имя проекта? падает если не указать группу
```
> skills init --repo https://github.com/merck-gen/cex-cic-skills-dev              

Error: specify at least one group (use --groups flag or positional args)

Initialize skills workspace from a central repository.
 
Clones the skills repository, resolves skills for the specified groups,

and applies sparse checkout so only the needed skills are present.
 
Usage:

  skills init --repo <url-or-path> [--groups <group1>[,<group2>...]] [group...]
 
Flags:

  --repo    URL or local path to the central skills repository (required)

  --groups  Groups to initialize (comma-separated or repeated flag; positional args also accepted)
 
Examples:

  skills init --repo https://github.com/org/skills --groups backend

  skills init --repo ../skills-repo --groups backend,security

  skills init --repo ../skills-repo backend security
```
