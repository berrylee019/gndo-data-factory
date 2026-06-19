import json

OUTPUT_FILE = (
    "storage/rkg/verification_registry_v07.json"
)

def generate():

    data = [
        {
            "verification_id":"VER-CH01-001",
            "chapter":"01",
            "requirement_id":"REQ-CH01-001",
            "verification_method":"Inspection",
            "verification_name":
                "Design Basis Documentation Review",
            "acceptance_criteria":
                "Design basis documented"
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

if __name__ == "__main__":
    generate()
