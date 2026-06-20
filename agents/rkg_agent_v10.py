import json
from datetime import datetime

RKG_V09_FILE = (
"storage/metadata/rkg_data_v09.json"
)

ARTIFACT_FILE = (
"storage/rkg/design_artifact_registry_v09.json"
)

OUTPUT_FILE = (
"storage/metadata/rkg_data_v10.json"
)

def load_json(path):


    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:
    
        return json.load(f)


def generate_metadata():


    rkg_v09 = load_json(
        RKG_V09_FILE
    )
    
    artifacts = load_json(
        ARTIFACT_FILE
    )
    
    artifact_map = {}

    for artifact in artifacts:
    
        chapter = artifact["chapter"]

        if chapter not in artifact_map:
          
            artifact_map[chapter] = []
            
        artifact_map[chapter].append(
            artifact
        )
      
    metadata = []
    
    for item in rkg_v09:
    
        chapter = item["chapter"]
    
        artifact_list = artifact_map.get(
            chapter,
            []
        )

        if not artifact_list:

            metadata.append(item)

            continue

        for artifact in artifact_list:
        
            metadata.append({
    
                **item,
    
                "artifact_id":
                    artifact["artifact_id"],
    
                "artifact_type":
                    artifact["artifact_type"],
    
                "artifact_name":
                    artifact["artifact_name"],
    
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
        f"Generated {len(metadata)} RKG v1.0 records"
    )
    
    
if __name__ == "__main__":


    generate_metadata()
