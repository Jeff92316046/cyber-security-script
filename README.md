# cyber-security-script

### usage
install uv
```sh
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

install python3.11
```sh
uv python install 3.11
```

install dependency
```sh
uv venv --python 3.11
uv sync
```