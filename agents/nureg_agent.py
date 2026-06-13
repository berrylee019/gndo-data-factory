import json
from datetime import datetime

REGISTRY_FILE = "storage/registry/nureg_registry.json"

OUTPUT_FILE = "storage/metadata/nureg_data.json"


def load_registry():

    with open(
        REGISTRY_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def generate_metadata():

    registry = load_registry()

    metadata = []

    for doc in registry:

        metadata.append({

            "doc_id":
                doc["doc_id"],

            "title":
                doc["title"],

            "source":
                "NRC",

            "category":
                doc["category"],

            "url":
                doc.get["url", ""],

            "status":
                "active",

            "collected_at":
                datetime.utcnow().isoformat()
        })

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Generated {len(metadata)} NUREG records"
    )


if __name__ == "__main__":
    generate_metadata()
