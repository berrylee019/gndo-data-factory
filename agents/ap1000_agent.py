import json
from datetime import datetime

OUTPUT_FILE = "storage/metadata/ap1000_data.json"

def main():

    documents = [
        {
            "reactor": "AP1000",
            "title": "AP1000 Design Control Document",
            "source": "Westinghouse",
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

    print("AP1000 data updated")

if __name__ == "__main__":
    main()
