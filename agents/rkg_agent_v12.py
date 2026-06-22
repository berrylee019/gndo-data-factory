
import json
from datetime import datetime

RKG_V11_FILE = (
    "storage/metadata/rkg_data_v11.json"
)

CHANGE_FILE = (
    "storage/rkg/change_registry_v12.json"
)

OUTPUT_FILE = (
    "storage/metadata/rkg_data_v12.json"
)

def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)

def generate_metadata():

    rkg_v10 = load_json(
        RKG_V10_FILE
    )

    impacts = load_json(
        IMPACT_FILE
    )

    impact_map = {}

    for impact in impacts:

        impact_map[
            impact["failure_id"]
        ] = impact

    metadata = []

    for item in rkg_v10:

        failure_id = item.get(
            "failure_id"
        )

        impact = impact_map.get(
            failure_id,
            {}
        )

        metadata.append({

            **item,

            "impact_level":
                impact.get(
                    "impact_level"
                ),

            "impact_type":
                impact.get(
                    "impact_type"
                ),

            "retest_required":
                impact.get(
                    "retest_required"
                ),

            "safety_significant":
                impact.get(
                    "safety_significant"
                ),

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
        f"Generated {len(metadata)} RKG v1.1 records"
    )

if __name__ == "__main__":

    generate_metadata()
