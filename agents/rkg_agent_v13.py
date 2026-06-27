import json
from datetime import datetime


########################################################
# INPUT FILES
########################################################

RKG_V11_FILE = (
    "storage/metadata/rkg_data_v11.json"
)

IMPACT_FILE = (
    "storage/rkg/impact_registry_v11.json"
)

CHANGE_FILE = (
    "storage/rkg/change_registry_v12.json"
)

FAILURE_FILE = (
    "storage/rkg/failure_registry_v10.json"
)


########################################################
# OUTPUT
########################################################

OUTPUT_FILE = (
    "storage/metadata/rkg_data_v13.json"
)


########################################################
# JSON Loader
########################################################

def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


########################################################
# Generator
########################################################

def generate_metadata():

    print("===================================")
    print("GNDO RKG AGENT v13")
    print("===================================")

    rkg_v11 = load_json(
        RKG_V11_FILE
    )

    impacts = load_json(
        IMPACT_FILE
    )

    changes = load_json(
        CHANGE_FILE
    )

    failures = load_json(
        FAILURE_FILE
    )

    print()

    print("Requirements :", len(rkg_v11))
    print("Impacts      :", len(impacts))
    print("Changes      :", len(changes))
    print("Failures     :", len(failures))

    print()

    metadata = []

    print("Loaded Successfully")

    stats = {
        "Requirements": len(rkg_v11),
        "Impacts": len(impacts),
        "Changes": len(changes),
        "Failures": len(failures)
    }

    print(stats)

    return stats


if __name__ == "__main__":

    generate_metadata()
