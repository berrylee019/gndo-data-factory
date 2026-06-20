import json
from datetime import datetime

RKG_V09_FILE = (
"storage/metadata/rkg_data_v09.json"
)

FAILURE_FILE = (
"storage/rkg/failure_registry_v10.json"
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
    
    failures = load_json(
        FAILURE_FILE
    )
    
    failure_map = {}

    for failure in failures:
    
        requirement_id = failure["requirement_id"]

        if requirement_id not in failure_map:
          
            failure_map[requirement_id] = []
            
        failure_map[requirement_id].append(
            failure
        )
      
    metadata = []
    
    for item in rkg_v09:
    
        requirement_id = item.get("requirement_id")
    
        failure_list = failure_map.get(
            requirement_id,
            []
        )

        if not failure_list:

            metadata.append(item)

            continue

        for failure in failure_list:
        
            metadata.append({
    
                **item,
    
                "failure_id":
                    failure.get("failure_id")
    
                "failure_mode":
                    failure.get("failure_mode"),
    
                "severity":
                    failure.get("severity"),
    
                "consequence":
                    failure.get("consequence"),
                
                "mitigation":
                    failure.get("mitigation"),

                "affected_system":
                    failure.get("affected_system"),

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
