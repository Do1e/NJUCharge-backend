import json
import time
import re

with open("status.json", "r", encoding="utf-8") as f:
    status = json.load(f)

# sort by restmin
outlets = []
for station in status:
    for outlet in station["outlets"]:
        outlet["station"] = {"id": station["id"], "name": station["name"]}
        outlet["update_time"] = time.strftime(
            "%m-%d %H:%M:%S", time.localtime(outlet["update_time"])
        )
        outlet_name = outlet["name"].split(" ")[1]
        station_name = station["name"]
        outlet["name"] = (
            re.search(r"(\d+号机(?:-\d+)?)", station_name).group(1) + " " + outlet_name
        )
        outlet["station"] = station_name[: -len(outlet["name"].split(" ")[0])]
        outlets.append(outlet)

outlets.sort(key=lambda x: (x["restmin"], x["msg"]))
with open("outlets.json", "w", encoding="utf-8") as f:
    json.dump(outlets, f, ensure_ascii=False, indent=2)
