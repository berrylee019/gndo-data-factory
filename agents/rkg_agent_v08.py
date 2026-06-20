import json
from datetime import datetime

RKG_V07_FILE = (
"storage/metadata/rkg_data_v07.json"
)

TEST_FILE = (
"storage/rkg/test_registry_v08.json"
)

OUTPUT_FILE = (
"storage/metadata/rkg_data_v08.json"
)

def load_json(path):

```
with open(
    path,
    "r",
    encoding="utf-8"
) as f:

    return json.load(f)
```

def generate_metadata():

```
rkg_v07 = load_json(
    RKG_V07_FILE
)

tests = load_json(
    TEST_FILE
)

test_map = {}

for test in tests:

    verification_id = test[
        "verification_id"
    ]

    test_map[
        verification_id
    ] = test

metadata = []

for item in rkg_v07:

    verification_id = item.get(
        "verification_id"
    )

    test_info = test_map.get(
        verification_id,
        {}
    )

    metadata.append({

        **item,

        "test_id":
            test_info.get(
                "test_id"
            ),

        "test_name":
            test_info.get(
                "test_name"
            ),

        "test_type":
            test_info.get(
                "test_type"
            ),

        "acceptance_criteria":
            test_info.get(
                "acceptance_criteria"
            ),

        "created_at":
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
    f"Generated {len(metadata)} RKG v0.8 records"
)
```

if **name** == "**main**":

```
generate_metadata()
```
