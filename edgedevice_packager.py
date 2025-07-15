import os
import zipfile

PROJECT_ROOT = "./edgedevice_final"
OUTPUT_ZIP = "RePlay_EdgeDevice_v13.zip"

with zipfile.ZipFile(OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(PROJECT_ROOT):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, PROJECT_ROOT)
            zipf.write(full_path, arcname)

print(f"✅ Packaged: {OUTPUT_ZIP}")
