
import json
from datetime import datetime

RKG_V11_FILE = (
    "storage/metadata/rkg_data_v11.json"
)

IMPACT_FILE = (
    "storage/rkg/impact_registry_v11.json"
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

    rkg_v11 = load_json(
        RKG_V11_FILE
    )

    impacts = load_json(
        IMPACT_FILE
    )

    changes = load_json(
        CHANGE_FILE
    )

    impact_map = {}
    change_map = {}

    for impact in impacts:

        impact_map[
            impact["failure_id"]
        ] = impact

    for change in changes:

        change_map[
            change["target_id"]
        ] = change


    metadata = []

    for item in rkg_v11:

        failure_id = item.get(
            "failure_id"
        )

        impact = impact_map.get(
            failure_id,
            {}
        )

        artifact_id = item.get(
            "artifact_id"
        )

        
        change = change_map.get(
            artifact_id,
            {}
        )

        print(
            "ARTIFACT:",
            artifact_id
        )
        
        print(
            "CHANGE:",
            change
        )
        
        metadata.append({

            **item,

            # v1.1 Impact
            
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

            # v1.2 Change

            "change_id":
                change.get(
                    "change_id"
                ),
        
            "change_type":
                change.get(
                    "change_type"
                ),
        
            "impact_scope":
                change.get(
                    "impact_scope"
                ),
        
            "requires_reverification":
                change.get(
                    "requires_reverification"
                ),
        
            "requires_retest":
                change.get(
                    "requires_retest"
                ),

            "affected_requirement":
                change.get(
                    "affected_requirement"
                ),
            
            "affected_verification":
                change.get(
                    "affected_verification"
                ),
            
            "affected_test":
                change.get(
                    "affected_test"
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
        f"Generated {len(metadata)} RKG v1.2 records"
    )

if __name__ == "__main__":

    generate_metadata()
