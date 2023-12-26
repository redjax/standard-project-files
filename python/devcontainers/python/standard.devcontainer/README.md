# My standard Python VSCode Devcontainer

## Usage

- Create a directory in the root of your project called `.devcontainer`
- Create a file `Dockerfile`, either in the root of your project or inside `.devcontainer`
- Create `.devcontainer/devcontainer.json`
  - Edit `.devcontainer/devcontainer.json`, changing `"build": { "context": }` and `"build": { "dockerFile": }` to match where you put your `Dockerfile`
