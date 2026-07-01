# Workshop

This Workshop environment is for contributing to the [Ubuntu Robotics documentation](https://canonical-robotics.readthedocs-hosted.com/en/latest/).
It provides a self-contained Sphinx build environment and an opencode AI coding agent,
so you can write, preview,
and validate docs without any local setup.

## Quick start

At the documentation project root, run:

```bash
workshop launch
workshop run docs-run
```

Open your browser at `http://127.0.0.1:8042/`.

## Setup

Mount your local opencode config and credentials:

```bash
workshop stop robotics-docs-dev
workshop remount robotics-docs-dev/opencode:opencode-config ~/.config/opencode
workshop remount robotics-docs-dev/opencode:opencode-data ~/.local/share/opencode
workshop start robotics-docs-dev
```

Import your SSH key from GitHub:

```bash
workshop run import-ssh-key <GH_HANDLE>
```

Connect VS Code to the workshop:

```bash
code --folder-uri vscode-remote://ssh-remote+workshop@$(workshop run -- get-ip)/project
```

> Note
> If VS Code refuses the SSH connection after a workshop refresh,
> clear the stale host key:
> `ssh-keygen -R "$(workshop run -- get-ip)"`

Resume your last opencode session:

```bash
workshop run opencode --continue
```
