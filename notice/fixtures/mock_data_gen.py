import json
from datetime import datetime, timedelta

# Initialize the data
data = []

# Generate new items
for i in range(1, 26):
    new_item = {
        "model": "notice.notice",
        "pk": i,
        "fields": {
            "id": str(i),
            "title": f"Notice {i}",
            "content": f"This is the content for Notice {i}",
            "created_at": (datetime(2022, 1, 1) + timedelta(days=i - 1)).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            "updated_at": (datetime(2022, 1, 1) + timedelta(days=i - 1)).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
        },
    }
    data.append(new_item)

# Save the expanded data
with open("expanded_data.json", "w") as f:
    json.dump(data, f, indent=2)
