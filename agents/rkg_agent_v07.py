import json
from datetime import datetime

RKG_V06_FILE = (
    "storage/metadata/rkg_data_v06.json"
)

VERIFICATION_FILE = (
    "storage/rkg/verification_registry_v07.json"
)

OUTPUT_FILE = (
    "storage/metadata/rkg_data_v07.json"
)

def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)

def generate_metadata():

    rkg_v06 = load_json(
        RKG_V06_FILE
    )

    verifications = load_json(
        VERIFICATION_FILE
    )

    verification_map = {}

    for ver in verifications:

        req_id = ver[
            "requirement_id"
        ]

        verification_map[
            req_id
        ] = ver

      
        metadata = []

    for item in rkg_v06:

        req_id = item.get(
            "requirement_id"
        )

        verification = (
            verification_map.get(
                req_id,
                {}
            )
        )

        metadata.append({

            **item,

            "verification_id":
                verification.get(
                    "verification_id"
                ),

            "verification_method":
                verification.get(
                    "verification_method"
                ),

            "verification_name":
                verification.get(
                    "verification_name"
                ),

            "acceptance_criteria":
                verification.get(
                    "acceptance_criteria"
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
        f"Generated {len(metadata)} RKG v0.7 records"
    )

if __name__ == "__main__":

    generate_metadata()
