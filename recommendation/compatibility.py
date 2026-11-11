
def check_compatibility(device_id, accessory_id):
    """
    Check whether an accessory is compatible with a device.
    """

    try:
        from database.db import get_compatibility
    except ImportError:
        return {
            "device_id": device_id,
            "accessory_id": accessory_id,
            "status": "unknown",
            "compatible": None,
            "reason": "Compatibility database is not available."
        }

    record = get_compatibility(device_id, accessory_id)

    if not record:
        return {
            "device_id": device_id,
            "accessory_id": accessory_id,
            "status": "unknown",
            "compatible": None,
            "reason": "No verified compatibility record is available."
        }

    status = record.get("status", "unknown")
    notes = record.get("notes")

    if status == "compatible":
        compatible = True
        reason = notes or "The database confirms compatibility."

    elif status == "incompatible":
        compatible = False
        reason = notes or "The database confirms incompatibility."

    else:
        status = "unknown"
        compatible = None
        reason = notes or "Compatibility has not been verified."

    return {
        "device_id": device_id,
        "accessory_id": accessory_id,
        "status": status,
        "compatible": compatible,
        "reason": reason
    }
