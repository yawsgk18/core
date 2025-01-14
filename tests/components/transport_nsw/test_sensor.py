"""The tests for the Transport NSW (AU) sensor platform."""
from unittest.mock import patch

from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component

VALID_CONFIG = {
    "sensor": {
        "platform": "transport_nsw",
        "stop_id": "209516",
        "route": "199",
        "destination": "",
        "api_key": "YOUR_API_KEY",
    }
}


def get_departuresMock(_stop_id, route, destination, api_key):
    """Mock TransportNSW departures loading."""
    data = {
        "stop_id": "209516",
        "route": "199",
        "due": 16,
        "delay": 6,
        "real_time": "y",
        "destination": "Palm Beach",
        "mode": "Bus",
    }
    return data


@patch("TransportNSW.TransportNSW.get_departures", side_effect=get_departuresMock)
async def test_transportnsw_config(mocked_get_departures, hass: HomeAssistant) -> None:
    """Test minimal TransportNSW configuration."""
    assert await async_setup_component(hass, "sensor", VALID_CONFIG)
    await hass.async_block_till_done()
    state = hass.states.get("sensor.next_bus")
    assert state.state == "16"
    assert state.attributes["stop_id"] == "209516"
    assert state.attributes["route"] == "199"
    assert state.attributes["delay"] == 6
    assert state.attributes["real_time"] == "y"
    assert state.attributes["destination"] == "Palm Beach"
    assert state.attributes["mode"] == "Bus"


def get_departuresMock_notFound(_stop_id, route, destination, api_key):
    """Mock TransportNSW departures loading."""
    data = {
        "stop_id": "n/a",
        "route": "n/a",
        "due": "n/a",
        "delay": "n/a",
        "real_time": "n/a",
        "destination": "n/a",
        "mode": "n/a",
    }
    return data


@patch(
    "TransportNSW.TransportNSW.get_departures", side_effect=get_departuresMock_notFound
)
async def test_transportnsw_config_not_found(
    mocked_get_departures_not_found, hass: HomeAssistant
) -> None:
    """Test minimal TransportNSW configuration."""
    assert await async_setup_component(hass, "sensor", VALID_CONFIG)
    await hass.async_block_till_done()
    state = hass.states.get("sensor.next_bus")
    assert state.state == "unknown"
    assert state.attributes["stop_id"] == "209516"
    assert state.attributes["route"] is None
    assert state.attributes["delay"] is None
    assert state.attributes["real_time"] is None
    assert state.attributes["destination"] is None
    assert state.attributes["mode"] is None
