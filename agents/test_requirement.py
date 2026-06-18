import json

with open(
"storage/rkg/requirement_registry_v06.json",
"r",
encoding="utf-8"
) as f:

requirements = json.load(f)

print(
f"Requirements Loaded: {len(requirements)}"
)

print(
requirements[0]
)
