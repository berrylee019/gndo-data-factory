import json

INPUT_FILE = (
    "storage/rkg/design_artifact_registry_v09.json"
)

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:

    artifacts = json.load(f)

print(
    f"Generated {len(artifacts)} Design Artifacts"
)
