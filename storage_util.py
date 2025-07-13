import shutil

def get_storage_status(path="/recordings"):
    usage = shutil.disk_usage(path)
    return {
        "total_gb": round(usage.total / (1024 ** 3), 2),
        "used_gb": round(usage.used / (1024 ** 3), 2),
        "free_gb": round(usage.free / (1024 ** 3), 2),
        "percent_used": round(usage.used / usage.total * 100, 2)
    }
