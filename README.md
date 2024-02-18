# hass-inspirair

![GitHub CI](https://github.com/The-Smartest-Home/hass_inspirair/actions/workflows/test.yaml/badge.svg)

[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

![img.png](docs/tutorial/mqtt_device.png | width=300)

A python application that connects to the ventilation system `InspirAir® Home` from `Aldes` via ModBus and exposes it as a device for [Home Assistant](https://www.home-assistant.io/) .

<details>
<summary>Schematics of dataflow</summary>

```mermaid
graph LR
    P(hass-inspirair) <-- MQTT --> M(MQTT Broker)
    I[InspirAir® Home] <-- ModBus --> P
    HM(Home Assistant \n MQTT Integration) <--MQTT--> M
    H[Home Assistant] <----> HM
```

</details>

Only the ventilation mode is currently writable. However, it takes some time before the value changes after a write command.
Since the register will stay at its previous value until the target state is reached.

Following features are implemented:

<details>
  <summary>1. Register after starting up</summary>
  
```mermaid
sequenceDiagram
    participant H as Home Assistant(MQTT)
    participant L as hass-inspirair
    participant I as InspirAir
    
    
    L->>+I: read_holding_registers
    activate L
    L-->>L: creat config
    
    L->>-H: register <prefix>/<sensor_type>/<object_id>/<device_serial>/config
```
</details>

<details>
<summary>2. Continues updates</summary>

```mermaid
sequenceDiagram

    participant H as Home Assistant(MQTT)
    participant L as hass-inspirair
    participant I as InspirAir


    L->>I: read_holding_registers
    activate L
    L->>L: parse result
    L->>H: publish <prefix>/climate/<device_serial>/state
    L->>L: sleep for <polling interval>
    deactivate L


```

</details>

<details>
<summary>3. React on Home Assistant Inputs</summary>

```mermaid
sequenceDiagram
    participant H as Home Assistant(MQTT)
    participant L as hass-inspirair
    participant I as InspirAir

    H->>L: publish "<prefix>/select/<object_id>/<device_serial>/set"
     activate L
    L->>I: write_registers
    L->>I: read_holding_registers

    L->>L: parse result
    L->>H: publish <prefix>/climate/<device_serial>/state
    deactivate L

```

</details>

<details>
<summary>4. React on Home Assistant MQTT lifecycle events</summary>

```mermaid
sequenceDiagram

    participant H as Home Assistant(MQTT)
    participant L as hass-inspirair
    participant I as InspirAir

    H->>L: publish "<prefix>/status" payload: "online"
    activate L
    L->>+I: read_holding_registers

    L-->>L: creat config

    L->>-H: register <prefix>/<sensor_type>/<object_id>/<device_serial>/config

```

</details>

## Supported Models

In theory this application should work with any `InspirAir® Home` Ventilation system.

Currently, only the following was actually tested:

- InspirAIR Home SC 370

## Usage

Configure a `config.ini` file based on your requirements.
See [config.ini](./config.ini) for configuration options which can also be set via environment variables [(see env_config.py)](./hass_inspirair/env_config.py).

```bash
pip intall hass-inspirair
ha-inspirair -c ./config.ini
```

For are more exhaustive usage tutorial see [docs/tutorial/README.md](docs/tutorial/README.md).

## Simulator/Testing

The compose stack includes a simulator that exposes the relevante registers via Modbus-TCP. The presented values are a pure mock.
However, this stack can be used to try out the behavior of the MQTT discovery.

1. Run `docker-compose up`
2. goto [http://localhost:8123](http://localhost:8123)
3. Setup a user
4. Add the MQTT Integration (`host=mqtt`, no further credentials)
5. A device should show up
