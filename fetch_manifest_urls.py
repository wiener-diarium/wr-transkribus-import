import os
import requests
import json
import time
from tqdm import tqdm
from transkribus_utils.transkribus_utils import ACDHTranskribusUtils

from config import IIIF_COLLECTION_URL, START_YEAR, IIIF_COL_DIR

os.makedirs(IIIF_COL_DIR, exist_ok=True)
year = os.environ.get("YEAR", START_YEAR)
iiif_col_file = f"{os.path.join(IIIF_COL_DIR, str(year).lower())}.json"
iiif_col_url = IIIF_COLLECTION_URL.format(year)
tr_user = os.environ.get("TRANSKRIBUS_USER")
tr_pw = os.environ.get("TRANSKRIBUS_PASSWORD")

manifests = {}
client = ACDHTranskribusUtils(user=tr_user, password=tr_pw)

col_name = f"wrz__{year}"
col_id = client.get_or_create_collection(col_name)
print(col_id, col_name)

r = requests.get(iiif_col_url)
data = r.json()
for x in tqdm(data["manifests"]):
    label = x["label"]
    date = label.split()[-1]
    id = f"wrz{date.replace('-', '')}"
    manifests[id] = {
        "url": x["@id"],
        "label": label,
        "id": id,
        "date": date
    }
    client.upload_iiif_from_url(x["@id"], col_id)
    time.sleep(2)
print("done")

with open(iiif_col_file, "w") as f:
    json.dump(manifests, f, ensure_ascii=True)