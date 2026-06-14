import json
from datetime import datetime

REGISTRY_FILE = "storage/registry/rg_registry.json"
OUTPUT_FILE = "storage/metadata/rg_data.json"

def generate_metadata():

    with open(
        REGISTRY_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        registry = json.load(f)

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
                "",

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

if __name__ == "__main__":
    generate_metadata()

print(
    f"Generated {len(metadata)} RG records"
)
