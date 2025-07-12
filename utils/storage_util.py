import shutil
def get_disk_usage_percent(path="/"):
    total, used, free = shutil.disk_usage(path)
    return (used / total) * 100
