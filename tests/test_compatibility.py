
import sys
import types

from recommendation.compatibility import check_compatibility


def create_mock_database(monkeypatch, mock_record):
    database = types.ModuleType("database")
    db = types.ModuleType("database.db")

    def mock_lookup(device_id, accessory_id):
        return mock_record

    db.get_compatibility = mock_lookup
    database.db = db

    monkeypatch.setitem(sys.modules, "database", database)
    monkeypatch.setitem(sys.modules, "database.db", db)


def test_compatible_accessory(monkeypatch):
    create_mock_database(monkeypatch, {
        "status": "compatible",
        "notes": "Both devices support the same connection."
    })

    result = check_compatibility("phone1", "charger1")

    assert result["status"] == "compatible"
    assert result["compatible"] is True


def test_incompatible_accessory(monkeypatch):
    create_mock_database(monkeypatch, {
        "status": "incompatible",
        "notes": "The accessory does not support this device."
    })

    result = check_compatibility("phone1", "charger2")

    assert result["status"] == "incompatible"
    assert result["compatible"] is False


def test_unknown_compatibility(monkeypatch):
    create_mock_database(monkeypatch, {
        "status": "unknown",
        "notes": "Compatibility is not verified."
    })

    result = check_compatibility("phone1", "charger3")

    assert result["status"] == "unknown"
    assert result["compatible"] is None


def test_missing_compatibility_record(monkeypatch):
    create_mock_database(monkeypatch, None)

    result = check_compatibility("phone1", "charger4")

    assert result["status"] == "unknown"
    assert result["compatible"] is None
