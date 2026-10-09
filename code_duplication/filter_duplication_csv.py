# AI generated code

import argparse
import csv


def is_blender_root_or_child(folder):
    normalized = folder.replace("\\", "/").strip("/")
    if normalized == "blender":
        return True
    return normalized.startswith("blender/") and "/" not in normalized[len("blender/"):]


parser = argparse.ArgumentParser(
    description="Keep the blender folder and its immediate subfolders from a duplication CSV."
)
parser.add_argument("input", nargs="?", default="duplication_by_folder.csv")
parser.add_argument("output", nargs="?", default="duplication_by_folder_one_level.csv")
args = parser.parse_args()

with open(args.input, newline="", encoding="utf-8-sig") as source:
    reader = csv.DictReader(source)
    if not reader.fieldnames or "folder" not in reader.fieldnames:
        raise SystemExit("Input CSV must contain a 'folder' column.")

    rows = [row for row in reader if is_blender_root_or_child(row["folder"])]

with open(args.output, "w", newline="", encoding="utf-8") as destination:
    writer = csv.DictWriter(destination, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to {args.output}")