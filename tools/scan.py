#!/usr/bin/env python3
import os
import json
import time
from pathlib import Path
from datetime import datetime

BASE_DIR = Path.home() / "cleanclaw-agent"
CONFIG_FILE = BASE_DIR / "CONFIG/settings.json"
REPORT_DIR = Path.home() / "PARKING/reports"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def is_excluded(path, excludes):
    for ex in excludes:
        if ex in path.parts:
            return True
    return False

def scan_files():
    config = load_config()
    scan_path = Path(config["scan_path"])
    excludes = config["exclude_folders"]
    threshold = config["large_file_threshold_mb"] * 1024 * 1024
    old_days = config["old_file_days"]

    results = []
    now = time.time()

    for root, dirs, files in os.walk(scan_path):
        root_path = Path(root)

        if is_excluded(root_path, excludes):
            continue

        for file in files:
            file_path = root_path / file
            try:
                size = file_path.stat().st_size
                modified = file_path.stat().st_mtime
                age_days = (now - modified) / 86400

                info = {
                    "path": str(file_path),
                    "size_mb": round(size / (1024*1024), 2),
                    "age_days": round(age_days, 1)
                }

                if size > threshold:
                    info["flag"] = "LARGE_FILE"

                if age_days > old_days:
                    info["flag"] = info.get("flag", "") + " OLD_FILE"

                results.append(info)

            except:
                continue

    return results

def generate_report(data):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_file = REPORT_DIR / f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    with open(report_file, "w") as f:
        f.write("# CleanClaw Scan Report\n\n")
        for item in data:
            f.write(f"- {item['path']} | {item['size_mb']}MB | {item['age_days']} days | {item.get('flag','')}\n")

    print(f"\n✅ Report generated: {report_file}\n")

if __name__ == "__main__":
    data = scan_files()
    generate_report(data)
