import json
from datetime import datetime


RKG_V11_FILE = "storage/metadata/rkg_data_v11.json"

VERIFICATION_FILE = "storage/rkg/verification_registry_v07.json"

TEST_FILE = "storage/rkg/test_registry_v08.json"

FAILURE_FILE = "storage/rkg/failure_registry_v10.json"

IMPACT_FILE = "storage/rkg/impact_registry_v11.json"

CHANGE_FILE = "storage/rkg/change_registry_v12.json"

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
    
        ####################################################
        # 기본 키
        ####################################################
    
        requirement_id = item.get("requirement_id")
        artifact_id = item.get("artifact_id")
    
        ####################################################
        # Verification
        ####################################################
    
        verification = verification_map.get(
            requirement_id,
            {}
        )
    
        verification_id = verification.get(
            "verification_id"
        )
    
        ####################################################
        # Test
        ####################################################
    
        test = test_map.get(
            verification_id,
            {}
        )
    
        ####################################################
        # Failure
        ####################################################
    
        failure = failure_map.get(
            requirement_id,
            {}
        )
    
        failure_id = failure.get(
            "failure_id"
        )
    
        ####################################################
        # Impact
        ####################################################
    
        impact = impact_map.get(
            failure_id,
            {}
        )
    
        ####################################################
        # Change
        ####################################################
    
        change = change_map.get(
            artifact_id,
            {}
        )
    
        ####################################################
        # Verification Merge
        ####################################################
    
        item["verification_id"] = verification.get(
            "verification_id"
        )
    
        item["verification_method"] = verification.get(
            "verification_method"
        )
    
        item["verification_name"] = verification.get(
            "verification_name"
        )
    
        item["acceptance_criteria"] = verification.get(
            "acceptance_criteria"
        )
    
        ####################################################
        # Test Merge
        ####################################################
    
        item["test_id"] = test.get(
            "test_id"
        )
    
        item["test_name"] = test.get(
            "test_name"
        )
    
        item["test_type"] = test.get(
            "test_type"
        )
    
        ####################################################
        # Failure Merge
        ####################################################
    
        item["failure_id"] = failure.get(
            "failure_id"
        )
    
        item["failure_mode"] = failure.get(
            "failure_mode"
        )
    
        item["affected_system"] = failure.get(
            "affected_system"
        )
    
        item["failure_severity"] = failure.get(
            "severity"
        )
    
        item["failure_consequence"] = failure.get(
            "consequence"
        )
    
        item["mitigation"] = failure.get(
            "mitigation"
        )
    
        ####################################################
        # Impact Merge
        ####################################################
    
        item["impact_level"] = impact.get(
            "impact_level"
        )
    
        item["impact_type"] = impact.get(
            "impact_type"
        )
    
        item["retest_required"] = impact.get(
            "retest_required"
        )
    
        item["safety_significant"] = impact.get(
            "safety_significant"
        )
    
        ####################################################
        # Change Merge
        ####################################################
    
        item["change_id"] = change.get(
            "change_id"
        )
    
        item["change_type"] = change.get(
            "change_type"
        )
    
        item["impact_scope"] = change.get(
            "impact_scope"
        )
    
        item["requires_reverification"] = change.get(
            "requires_reverification"
        )
    
        item["requires_retest"] = change.get(
            "requires_retest"
        )
    
        item["affected_requirement"] = change.get(
            "affected_requirement"
        )
    
        item["affected_verification"] = change.get(
            "affected_verification"
        )
    
        item["affected_test"] = change.get(
            "affected_test"
        )
    
        ####################################################
        # Timestamp
        ####################################################
    
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
