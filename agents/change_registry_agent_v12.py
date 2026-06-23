import json

OUTPUT_FILE = (
    "storage/rkg/change_registry_v12.json"
)

changes = [

    {
        "change_id": "CHG-CH07-001",
        "target_type": "ARTIFACT",
        "target_id": "DOC-CH07-001",
        "change_type": "Design Update",
        "change_description": "PPS logic modification",
        "impact_scope": "FULL",
        "affected_requirement":
            "REQ-CH07-001",

        "affected_verification":
            "VER-CH07-001",
    
        "affected_test":
            "TEST-CH07-001",
        
        "requires_reverification": True,
        "requires_retest": True
    },

    {
        "change_id": "CHG-CH07-002",
        "target_type": "SYSTEM",
        "target_id": "SYS-CH07",
        "change_type": "Software Revision",
        "change_description": "Trip setpoint update",
        "impact_scope": "PARTIAL",
        "affected_requirement":
            "REQ-CH07-001",

        "affected_verification":
            "VER-CH07-001",
    
        "affected_test":
            "TEST-CH07-001",
        
        "requires_reverification": True,
        "requires_retest": False
    }

]

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        changes,
        f,
        indent=2,
        ensure_ascii=False
    )

print(
    f"Generated {len(changes)} Change records"
)
