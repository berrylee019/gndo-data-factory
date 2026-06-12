import json
from datetime import datetime

OUTPUT_FILE = "storage/metadata/nrc_data.json"


def main():

    documents = [
        {
            "title": "NUREG-0800",
            "source": "NRC",
            "updated_at": datetime.utcnow().isoformat()
        }
    ]

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            documents,
            f,
            indent=2,
            ensure_ascii=False
        )

    print("NRC data updated")


if __name__ == "__main__":
    main()
