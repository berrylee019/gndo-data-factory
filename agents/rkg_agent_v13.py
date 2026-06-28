import json
from datetime import datetime


RKG_V11_FILE = "storage/metadata/rkg_data_v11.json"

VERIFICATION_FILE = "storage/rkg/verification_registry_v07.json"

TEST_FILE = "storage/rkg/test_registry_v08.json"

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
    
    verifications = load_json(
        VERIFICATION_FILE
    )
    
    tests = load_json(
        TEST_FILE
    )
    
    failures = load_json(
        FAILURE_FILE
    )
    
    impacts = load_json(
        IMPACT_FILE
    )
    
    changes = load_json(
        CHANGE_FILE
    )

    print()
    
    print("Requirements :", len(rkg_v11))
    print("Impacts      :", len(impacts))
    print("Changes      :", len(changes))
    print("Failures     :", len(failures))
    
    print()
    
    # ===============================
    # 여기부터 Map 생성
    # ===============================
    
    verification_map = {
        r["requirement_id"]: r
        for r in verifications
    }
    
    test_map = {
        r["verification_id"]: r
        for r in tests
    }
    
    failure_map = {
        r["requirement_id"]: r
        for r in failures
    }
    
    impact_map = {
        r["failure_id"]: r
        for r in impacts
    }
    
    change_map = {
        r["target_id"]: r
        for r in changes
    }
    
    print("Verification Map :", len(verification_map))
    print("Test Map         :", len(test_map))
    print("Failure Map      :", len(failure_map))
    print("Impact Map       :", len(impact_map))
    print("Change Map       :", len(change_map))
    
    print()
    
    # ===============================
    # 여기까지 Map 생성
    # ===============================
    
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
