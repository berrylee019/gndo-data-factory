import json

VERIFICATION_FILE = (
"storage/rkg/verification_registry_v07.json"
)
OUTPUT_FILE = (
    "storage/rkg/verification_registry_v08.json"
)


def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def generate():

    verifications = load_json(
        VERIFICATION_FILE
    )

    data = []

    for ver in verifications:

        test_id = ver[
            "verification_id"
        ].replace(
            "VER",
            "TEST"
        )

        data.append({

            "test_id":
                test_id,

            "chapter":
                ver["chapter"],

            "verification_id":
                ver["verification_id"],

            "test_name":
                f"Test for {ver['verification_id']}",

            "test_type":
                "Analysis",

            "acceptance_criteria":
                "Requirement satisfied"

        })

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
        f"Generated {len(data)} test records"
    )

if __name__ == "__main__":
    
    generate()
