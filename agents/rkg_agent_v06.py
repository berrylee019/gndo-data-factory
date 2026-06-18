import json
from datetime import datetime

RKG_V05_FILE = "storage/metadata/rkg_data_v05.json"
REQUIREMENT_FILE = "storage/rkg/requirement_registry_v06.json"

OUTPUT_FILE = "storage/metadata/rkg_data_v06.json"

def load_json(path):

```
with open(
    path,
    "r",
    encoding="utf-8"
) as f:

    return json.load(f)
```

def generate_metadata():

```
rkg_v05 = load_json(
    RKG_V05_FILE
)

requirements = load_json(
    REQUIREMENT_FILE
)

requirement_map = {}

for req in requirements:

    chapter = req["chapter"]

    if chapter not in requirement_map:

        requirement_map[chapter] = []

    requirement_map[chapter].append(req)

metadata = []

for item in rkg_v05:

    chapter = item["chapter"]

    req_list = requirement_map.get(
        chapter,
        []
    )

    if not req_list:

        metadata.append(item)

        continue

    for req in req_list:

        metadata.append({

            "chapter": chapter,

            "topic": item["topic"],

            "system_id":
                item.get("system_id"),

            "system_name":
                item.get("system_name"),

            "domain":
                item.get("domain"),

            "component_id":
                item.get("component_id"),

            "component_name":
                item.get("component_name"),

            "requirement_id":
                req["requirement_id"],

            "requirement":
                req["requirement"],

            "requirement_system":
                req["system"],

            "requirement_component":
                req["component"],

            "cfr":
                item["cfr"],

            "rg":
                item["rg"],

            "nureg":
                item["nureg"],

            "srp":
                item["srp"],

            "ap1000":
                item["ap1000"],

            "apr1400":
                item["apr1400"],

            "status":
                "linked",

            "created_at":
                datetime.utcnow().isoformat()
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
    f"Generated {len(metadata)} RKG v0.6 records"
)
```

if **name** == "**main**":

```
generate_metadata()
```
