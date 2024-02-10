```bash
mamba env create -f environment.yml
mamba activate ha-aldes
poetry install
pre-commit install
pre-commit install --hook-type commit-msg
```

## Languages

```bash
pybabel extract -F babel.cfg --omit-header --input-dirs=hass_inspirair  -o hass_inspirair/i18n/hass_inspirair.pot
pybabel init -i hass_inspirair/i18n/hass_inspirair.pot -d hass_inspirair/i18n -l de -D hass_inspirair
pybabel init -i hass_inspirair/i18n/hass_inspirair.pot -d hass_inspirair/i18n -l en -D hass_inspirair
```

```bash
pybabel extract -F babel.cfg --omit-header --input-dirs=hass_inspirair  -o hass_inspirair/i18n/hass_inspirair.pot
```

```bash
pybabel update -i hass_inspirair/i18n/hass_inspirair.pot -d hass_inspirair/i18n -l de -D hass_inspirair  --omit-header
pybabel update -i hass_inspirair/i18n/hass_inspirair.pot -d hass_inspirair/i18n -l en -D hass_inspirair  --omit-header
```

```bash
pybabel compile -f -d hass_inspirair/i18n -D hass_inspirair
```
