import json
from datetime import datetime


RKG_V11_FILE = "storage/metadata/rkg_data_v11.json"

OUTPUT_FILE = "storage/metadata/rkg_data_v13.json"


def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def save_json(path, data):

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


def generate_metadata():

    print("===================================")
    print("GNDO RKG AGENT v13")
    print("===================================")

    rkg_v11 = load_json(
        RKG_V11_FILE
    )

    metadata = []

    for row in rkg_v11:

        item = dict(row)

        item["created_at"] = (
            datetime.utcnow().isoformat()
        )

        metadata.append(item)

    save_json(
        OUTPUT_FILE,
        metadata
    )

    print()

    print(
        "Generated",
        len(metadata),
        "records"
    )

    print()

    print(
        "Output :",
        OUTPUT_FILE
    )


if __name__ == "__main__":

    generate_metadata()
