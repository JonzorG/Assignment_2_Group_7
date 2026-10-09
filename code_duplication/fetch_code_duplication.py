# AI generated code

# Requires a user defined SONAR_PROJECT_KEY
# Requires a user defined SONAR_TOKEN


import csv
import getpass
import json
import os
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

SONAR_URL = os.getenv("SONAR_URL", "https://sonarcloud.io")


def get_project_key():
    project_key = os.getenv("SONAR_PROJECT_KEY")
    if project_key:
        return project_key

    report_task = os.path.join(os.path.dirname(__file__), ".scannerwork", "report-task.txt")
    if os.path.isfile(report_task):
        with open(report_task, encoding="utf-8") as report:
            for line in report:
                if line.startswith("projectKey="):
                    return line.partition("=")[2].strip()

    return input("SonarQube project key: ").strip()


PROJECT_KEY = get_project_key()
TOKEN = os.getenv("SONAR_TOKEN") or getpass.getpass("SonarQube token: ")

# Set to "" if the Sonar project is analyzed from inside the blender folder
# and its component paths do not start with "blender/".
FOLDER_PREFIX = "blender"

folders = []
page = 1
page_size = 500

while True:
    query = urlencode({
            "component": PROJECT_KEY,
            "metricKeys": "duplicated_lines,duplicated_lines_density",
            "qualifiers": "DIR",
            "strategy": "all",
            "p": page,
            "ps": page_size,
        })
    request = Request(
        f"{SONAR_URL}/api/measures/component_tree?{query}",
        headers={"Authorization": f"Bearer {TOKEN}"},
    )
    try:
        with urlopen(request, timeout=30) as response:
            data = json.load(response)
    except HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise SystemExit(f"SonarQube API returned HTTP {error.code}: {details}") from error

    for component in data.get("components", []):
        path = component.get("path")
        if not path:
            # Directory component keys are typically PROJECT_KEY:relative/path.
            prefix = f"{PROJECT_KEY}:"
            key = component["key"]
            path = key[len(prefix):] if key.startswith(prefix) else component["name"]

        path = path.replace("\\", "/").strip("/")
        if FOLDER_PREFIX and path != FOLDER_PREFIX and not path.startswith(FOLDER_PREFIX + "/"):
            continue

        measures = {
            measure["metric"]: measure.get("value", "")
            for measure in component.get("measures", [])
        }
        folders.append({
            "folder": path,
            "duplicated_lines": measures.get("duplicated_lines", ""),
            "duplicated_lines_density_percent": measures.get(
                "duplicated_lines_density", ""
            ),
        })

    total = data.get("paging", {}).get("total", 0)
    if page * page_size >= total or not data.get("components"):
        break
    page += 1

folders.sort(key=lambda folder: folder["folder"])

with open("duplication_by_folder.csv", "w", newline="", encoding="utf-8") as output:
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "folder",
            "duplicated_lines",
            "duplicated_lines_density_percent",
        ],
    )
    writer.writeheader()
    writer.writerows(folders)

print(f"Wrote {len(folders)} folders to duplication_by_folder.csv")