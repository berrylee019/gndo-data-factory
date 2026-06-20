import json

INPUT_FILE = (
    "storage/rkg/failure_registry_v10.json"
)

def main():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    print(
        f"Generated {len(data)} Failure Mode records"
    )

if __name__ == "__main__":

    main()
