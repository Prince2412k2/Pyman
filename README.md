# Pyman
A tui tool to track all your python environments.
finds all .env and .venv in path given in config.
finda anaconda/miniconda path and tracks all env in tht also

## Fetures
- Analyze -> see  all your pythin env in one place, with how much space they take
- CRUD    -> install, remove,updare,create packages/enviroments
- Offload -> offload envs to free up spaces, and reload them when needed
- snapshots -> snapshot all your envs and save them to github. so you can recreate them without hassle


### Requirements

- **uv is required**

- get yoself some [UV](https://github.com/astral-sh/uv)
- cd into repo

```bash
uv sync
```

```bash
python main.py
```

> note: still working on it,pushing it just for testing
