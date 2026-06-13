import json

def merge():

    all_docs = []

    files = [
        "storage/metadata/nureg_data.json",
        "storage/metadata/rg_data.json",
        "storage/metadata/srp_data.json",
        "storage/metadata/cfr_data.json"
    ]

    for file in files:

        with open(file, "r", encoding="utf-8") as f:

            all_docs.extend(
                json.load(f)
            )

    with open(
        "storage/master/nrc_master.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            all_docs,
            f,
            indent=2,
            ensure_ascii=False
        )
