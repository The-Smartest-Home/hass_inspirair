```bash
mamba env create -f environment.yml
mamba activate ha-aldes
poetry install
pre-commit install
pre-commit install --hook-type commit-msg
```

## Languages

```bash
pybabel extract -F babel.cfg --omit-header --input-dirs=ha_aldes  -o ha_aldes/i18n/ha_aldes.pot
pybabel init -i ha_aldes/i18n/ha_aldes.pot -d ha_aldes/i18n -l de -D ha_aldes
pybabel init -i ha_aldes/i18n/ha_aldes.pot -d ha_aldes/i18n -l en -D ha_aldes
```

```bash
pybabel extract -F babel.cfg --omit-header --input-dirs=ha_aldes  -o ha_aldes/i18n/ha_aldes.pot
```

```bash
pybabel update -i ha_aldes/i18n/ha_aldes.pot -d ha_aldes/i18n -l de -D ha_aldes  --omit-header
pybabel update -i ha_aldes/i18n/ha_aldes.pot -d ha_aldes/i18n -l en -D ha_aldes  --omit-header
```

```bash
pybabel compile -f -d ha_aldes/i18n -D ha_aldes
```
