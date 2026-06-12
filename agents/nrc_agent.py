import json
from pathlib import Path

OUTPUT_FILE = "storage/metadata/nrc_data.json"

def save_documents(documents):
    Path("storage/metadata").mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)

def main():

    documents = [
        {
            "title": "NUREG-0800",
            "source": "NRC",
            "category": "Standard Review Plan"
        },
        {
            "title": "10 CFR Part 50",
            "source": "NRC",
            "category": "Regulation"
        },
        {
            "title": "10 CFR Part 52",
            "source": "NRC",
            "category": "Regulation"
        }
    ]

    save_documents(documents)

    print(f"Saved {len(documents)} NRC records")

if __name__ == "__main__":
    main()
