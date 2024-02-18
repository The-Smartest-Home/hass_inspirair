# hass-inspirair

![GitHub CI](https://github.com/The-Smartest-Home/hass_inspirair/actions/workflows/test.yaml/badge.svg)

[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

A python library that connects to the ventilation system `InspirAir® Home` from `Aldes` via ModBus and exposes it as a device for Home Assistant.

Only the ventilation mode is currently writable. However, it takes a **significant** time before the value changes after a write command.
Since the register will stay at its previous value until the target state is reached.

## Supported Models

In theory this lib should work with any `InspirAir® Home` Ventilation system.

Currently, only the following was actually tested:

- InspirAIR Home SC 370

## Usage

Configure a `config.ini` file based on your requirements.

```bash
pip intall hass-inspirair
ha-inspirair -c ./config.ini
```

## Configuration

See [config.ini](./config.ini) for configuration options which can also be set via environment variables [(see env_config.py)](./hass_inspirair/env_config.py).

## Simulator/Testing

The compose stack includes a simulator that exposes the relevante registers via Modbus-TCP. The presented values are a pure mock.
However, this stack can be used to try out the behavior of the MQTT discovery.

1. Run `docker-compose up`
2. goto [http://localhost:8123](http://localhost:8123)
3. Setup a user
4. Add the MQTT Integration (`host=mqtt`, no further credentials)
5. A device should show up
