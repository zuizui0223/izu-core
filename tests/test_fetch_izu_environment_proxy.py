import importlib.util
from pathlib import Path

import pytest


def load_module():
    path = Path(__file__).parents[1] / "scripts" / "fetch_izu_environment_proxy.py"
    spec = importlib.util.spec_from_file_location("fetch_izu_environment_proxy", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def point() -> dict[str, object]:
    return {"island_id": "Oshima", "latitude": 34.7384790, "longitude": 139.4023682}


def test_climate_url_retains_declared_proxy_and_period():
    module = load_module()
    url = module.climate_url(34.7384790, 139.4023682, "1981-01-01", "2010-12-31")

    assert "latitude=34.7384790" in url
    assert "longitude=139.4023682" in url
    assert "start_date=1981-01-01" in url
    assert "end_date=2010-12-31" in url
    assert "temperature_2m_mean%2Cprecipitation_sum" in url


def test_transient_transport_error_retries_only_the_declared_query(monkeypatch):
    module = load_module()
    attempts = []
    responses = [OSError("temporary TLS timeout"), OSError("temporary TLS timeout"), {"daily": {}}]

    def fake_fetch(url):
        attempts.append(url)
        value = responses.pop(0)
        if isinstance(value, Exception):
            raise value
        return value

    monkeypatch.setattr(module, "fetch_json", fake_fetch)
    monkeypatch.setattr(module.time, "sleep", lambda seconds: None)

    payload, used = module.fetch_json_with_retry("https://example.org/query", max_attempts=5, retry_delay_seconds=1.0)

    assert payload == {"daily": {}}
    assert used == 3
    assert attempts == ["https://example.org/query"] * 3


def test_climate_summary_uses_actual_daily_rows_and_keeps_proxy_boundary():
    module = load_module()
    payload = {
        "daily": {
            "time": ["1981-01-01", "1981-01-02", "1982-01-01", "1982-02-01"],
            "temperature_2m_mean": [10.0, 14.0, 12.0, None],
            "precipitation_sum": [1.0, 3.0, 10.0, 6.0],
        }
    }
    summary = module.summarize_climate(payload, point(), "1981-01-01", "1982-02-01", "https://example.org", attempts_used=2)

    assert summary["mean_daily_temperature_c"] == "12.000000"
    assert summary["mean_annual_precipitation_mm"] == "10.000000"
    assert summary["days_with_temperature"] == "3"
    assert summary["days_with_precipitation"] == "4"
    assert summary["attempts_used"] == "2"
    assert "Island proxy point" in summary["proxy_boundary"]


def test_distance_rows_use_symmetric_great_circle_proxies_without_self_rows():
    module = load_module()
    rows = module.distance_rows(
        [
            {"island_id": "A", "latitude": 34.0, "longitude": 139.0},
            {"island_id": "B", "latitude": 35.0, "longitude": 139.0},
            {"island_id": "C", "latitude": 35.0, "longitude": 140.0},
        ]
    )

    assert len(rows) == 3
    assert {(row["from_island"], row["to_island"]) for row in rows} == {("A", "B"), ("A", "C"), ("B", "C")}
    assert all(float(row["great_circle_proxy_km"]) > 0.0 for row in rows)
    assert all("not least-cost dispersal" in row["distance_interpretation"] for row in rows)


def test_climate_summary_rejects_misaligned_arrays():
    module = load_module()
    payload = {
        "daily": {
            "time": ["1981-01-01"],
            "temperature_2m_mean": [10.0, 11.0],
            "precipitation_sum": [1.0],
        }
    }

    with pytest.raises(ValueError, match="different lengths"):
        module.summarize_climate(payload, point(), "1981-01-01", "1981-01-01", "https://example.org", attempts_used=1)
