import json

OUTPUT_FILE = (
    "storage/rkg/verification_registry_v07.json"
)


def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def generate():

    requirements = load_json(
        "storage/rkg/requirement_registry_v06.json"
    )

    data = []

    for req in requirements:

        verification_id = req[
            "requirement_id"
        ].replace(
            "REQ",
            "VER"
        )

        data.append({

            "verification_id":
                verification_id,

            "chapter":
                req["chapter"],

            "requirement_id":
                req["requirement_id"],

            "verification_method":
                "Analysis",

            "verification_name":
                f"Verification for {req['requirement_id']}",

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
        f"Generated {len(data)} Verification records"
    )

if __name__ == "__main__":
    
    generate()
