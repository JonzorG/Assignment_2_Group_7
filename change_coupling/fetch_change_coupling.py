# AI generated code 

import argparse
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

API_URL = (
	"https://codescene.io/projects/85487/jobs/7824863/results/architecture/"
	"temporal-coupling/by-commits/couplings.json"
)


def main():
	parser = argparse.ArgumentParser(
		description="Download CodeScene temporal coupling data by commit."
	)
	parser.add_argument(
		"--minimum-coupling",
		type=int,
		default=21,
		help="Minimum coupling degree to include (default: 21).",
	)
	parser.add_argument(
		"--output",
		type=Path,
		default=Path(__file__).with_name("couplings.json"),
		help="Output JSON path (default: change_coupling/couplings.json).",
	)
	args = parser.parse_args()

	url = f"{API_URL}?{urlencode({'minimum-coupling': args.minimum_coupling})}"
	try:
		with urlopen(url, timeout=30) as response:
			payload = response.read()
	except HTTPError as error:
		details = error.read().decode("utf-8", errors="replace")
		raise SystemExit(f"CodeScene returned HTTP {error.code}: {details}") from error
	except URLError as error:
		raise SystemExit(f"Could not reach CodeScene: {error.reason}") from error

	try:
		couplings = json.loads(payload)
	except json.JSONDecodeError as error:
		raise SystemExit(f"CodeScene returned invalid JSON: {error}") from error

	if not isinstance(couplings, list):
		raise SystemExit("CodeScene returned JSON in an unexpected format (expected a list).")

	args.output.parent.mkdir(parents=True, exist_ok=True)
	args.output.write_bytes(payload)
	print(f"Wrote {len(couplings)} couplings to {args.output}")


if __name__ == "__main__":
	main()