# ha-aldes

A python library that connects to a ventilation system from `InspirAir® Home` from `Aldes` via Modus and exposes it as a device or home-assistant.

Only the ventilation mode is currently writable. However, it takes a **significant** time before the value changes after a write command.
Since the register will stay at its previous setting while switching between states.

## Supported Models

In theory this lib should work with any `InspirAir® Home` Ventilation system.

Currently, only the following was actually tested:

- InspirAIR Home SC 370

## Configuration

See [env_config.py](./hass_inspirair/env_config.py) for configuration options which can be set via environment variables.

## Simulator/Testing

The compose stack includes a simulator that exposes the relevante registers via Modbus-TCP. The presented values are a pure mock.
However, this stack can be used to try out the behavior of the MQTT discovery.

1. Run `docker-compose up`
2. Add the MQTT Integration (`host=mqtt`)
3. A device should show up
