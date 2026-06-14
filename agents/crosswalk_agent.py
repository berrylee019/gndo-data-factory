import json
from datetime import datetime

REGISTRY_FILE = "storage/crosswalk/crosswalk_registry.json"
OUTPUT_FILE = "storage/metadata/crosswalk_data.json"

def generate_metadata():

with open(
    REGISTRY_FILE,
    "r",
    encoding="utf-8"
) as f:

    registry = json.load(f)

metadata = []

for item in registry:

    metadata.append({

        "chapter": item["chapter"],
        "topic": item["topic"],
        "srp": item["srp"],
        "ap1000": item["ap1000"],
        "apr1400": item["apr1400"],
        "status": "linked",
        "created_at": datetime.utcnow().isoformat()

    })

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        metadata,
        f,
        indent=2,
        ensure_ascii=False
    )

print(
    f"Generated {len(metadata)} Crosswalk records"
)

if **name** == "**main**":
generate_metadata()
