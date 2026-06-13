import json
from datetime import datetime

REGISTRY_FILE = "storage/registry/ap1000_registry.json"
OUTPUT_FILE = "storage/metadata/ap1000_data.json"

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
                doc.get("doc_id",""),

            "title":
                doc.get("title",""),

            "source":
                "Westinghouse",

            "category":
                "AP1000",

            "url":
                doc.get("url",""),

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
        f"Generated {len(metadata)} AP1000 records"
    )

if __name__ == "__main__":
    generate_metadata()
