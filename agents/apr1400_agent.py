import json
from datetime import datetime

REGISTRY_FILE = "storage/registry/apr1400_registry.json"
OUTPUT_FILE = "storage/metadata/apr1400_data.json"

def main():

    documents = [
        {
            "reactor": "APR1400",
            "title": "APR1400 Standard Design Description",
            "source": "KHNP",
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

    print("APR1400 data updated")

if __name__ == "__main__":
    main()
