import json
from datetime import datetime


########################################################
# INPUT FILES
########################################################

RKG_V11_FILE = "storage/metadata/rkg_data_v11.json"

IMPACT_FILE = "storage/rkg/impact_registry_v11.json"

CHANGE_FILE = "storage/rkg/change_registry_v12.json"

FAILURE_FILE = "storage/rkg/failure_registry_v10.json"


########################################################
# OUTPUT
########################################################

OUTPUT_FILE = "storage/metadata/rkg_data_v13.json"


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
# Registry Maps
########################################################

def build_failure_map(failures):

    failure_map = {}

    for row in failures:

        req = row.get("requirement_id")

        if req:

            failure_map[req] = row

    return failure_map


def build_impact_map(impacts):

    impact_map = {}

    for row in impacts:

        fid = row.get("failure_id")

        if fid:

            impact_map[fid] = row

    return impact_map


def build_change_map(changes):

    change_map = {}

    for row in changes:

        target = row.get("target_id")

        if target:

            change_map[target] = row

    return change_map
