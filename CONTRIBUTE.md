```bash
mamba env create -f environment.yml
mamba activate ha-aldes
poetry install
pre-commit install
pre-commit install --hook-type commit-msg
```
