import json

OUTPUT_FILE = (
    "storage/rkg/impact_registry_v11.json"
)

def generate_impacts():

    impacts = [
        {
            "failure_id":"FAIL-CH07-001",
            "impact_level":"HIGH",
            "impact_type":"Loss of Independence",
            "retest_required":True,
            "safety_significant":True,
            "affected_requirement":"REQ-CH07-001",
            "affected_verification":"VER-CH07-001",
            "affected_test":"TEST-CH07-001"
        },
        {
            "failure_id":"FAIL-CH07-002",
            "impact_level":"MEDIUM",
            "impact_type":"Logic Fault",
            "retest_required":True,
            "safety_significant":True,
            "affected_requirement":"REQ-CH07-002",
            "affected_verification":"VER-CH07-002",
            "affected_test":"TEST-CH07-002"
        },
        {
            "failure_id":"FAIL-CH07-003",
            "impact_level":"LOW",
            "impact_type":"Documentation Mismatch",
            "retest_required":False,
            "safety_significant":False,
            "affected_requirement":"REQ-CH07-003",
            "affected_verification":"VER-CH07-003",
            "affected_test":"TEST-CH07-003"
        }
    ]

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            impacts,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Generated {len(impacts)} Impact records"
    )

if __name__ == "__main__":

    generate_impacts()
