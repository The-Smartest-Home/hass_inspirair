# hass-inspirair

A python library that connects to a ventilation system `InspirAir® Home` from `Aldes` via ModBus and exposes it as a device for home-assistant.

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
