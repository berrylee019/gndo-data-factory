import json
from datetime import datetime

SYSTEM_FILE = "storage/rkg/system_registry_v05.json"
COMPONENT_FILE = "storage/rkg/component_registry_v05.json"
REGISTRY_FILE = "storage/rkg/rkg_registry_v05.json"

OUTPUT_FILE = "storage/metadata/rkg_data_v05.json"

def load_json(path):


with open(
    path,
    "r",
    encoding="utf-8"
) as f:

    return json.load(f)


def generate_metadata():


systems = load_json(
    SYSTEM_FILE
)

components = load_json(
    COMPONENT_FILE
)

registry = load_json(
    REGISTRY_FILE
)

system_map = {
    item["chapter"]: item
    for item in systems
}

component_map = {}

for item in components:

    chapter = item["chapter"]

    if chapter not in component_map:

        component_map[chapter] = []

    component_map[chapter].append(item)

metadata = []

for item in registry:

    chapter = item["chapter"]

    system_info = system_map.get(
        chapter,
        {}
    )

    component_list = component_map.get(
        chapter,
        []
    )

    if not component_list:

        metadata.append({

            "chapter": chapter,

            "topic": item["topic"],

            "system_id":
                system_info.get(
                    "system_id"
                ),

            "system_name":
                system_info.get(
                    "system_name"
                ),

            "domain":
                system_info.get(
                    "domain"
                ),

            "component_id": None,

            "component_name": None,

            "cfr": item["cfr"],

            "rg": item["rg"],

            "nureg": item["nureg"],

            "srp": item["srp"],

            "ap1000": item["ap1000"],

            "apr1400": item["apr1400"],

            "status": "linked",

            "created_at":
                datetime.utcnow().isoformat()
        })

    else:

        for comp in component_list:

            metadata.append({

                "chapter": chapter,

                "topic": item["topic"],

                "system_id":
                    system_info.get(
                        "system_id"
                    ),

                "system_name":
                    system_info.get(
                        "system_name"
                    ),

                "domain":
                    system_info.get(
                        "domain"
                    ),

                "component_id":
                    comp["component_id"],

                "component_name":
                    comp["component_name"],

                "cfr": item["cfr"],

                "rg": item["rg"],

                "nureg": item["nureg"],

                "srp": item["srp"],

                "ap1000": item["ap1000"],

                "apr1400": item["apr1400"],

                "status": "linked",

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
    f"Generated {len(metadata)} RKG v0.5 records"
)


if __name__ == "__main__":


generate_metadata()

