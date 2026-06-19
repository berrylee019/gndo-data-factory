import json

OUTPUT_FILE = (
    "storage/rkg/verification_registry_v07.json"
)

data = [

    {
        "verification_id":"VER-CH07-001",
        "chapter":"07",
        "requirement_id":"REQ-CH07-001",
        "verification_method":"Analysis",
        "verification_name":
            "Protection System Independence Analysis",
        "acceptance_criteria":
            "No common mode failure path"
    },

    {
        "verification_id":"VER-CH07-002",
        "chapter":"07",
        "requirement_id":"REQ-CH07-002",
        "verification_method":"Test",
        "verification_name":
            "ESFAS Reliability Test",
        "acceptance_criteria":
            "Actuation success rate > 99.9%"
    }
]

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        data,
        f,
        indent=2,
        ensure_ascii=False
    )

print(
    f"Generated {len(data)} Verification records"
)
