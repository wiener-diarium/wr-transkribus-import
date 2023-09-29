import os
import requests
import time
from tqdm import tqdm
from transkribus_utils.transkribus_utils import ACDHTranskribusUtils

from config import IIIF_COLLECTION_URL, IIIF_COL_DIR, START_YEAR, END_YEAR

tr_user = os.environ.get("TRANSKRIBUS_USER")
tr_pw = os.environ.get("TRANSKRIBUS_PASSWORD")
client = ACDHTranskribusUtils(user=tr_user, password=tr_pw)

os.makedirs(IIIF_COL_DIR, exist_ok=True)
for i in range(START_YEAR, END_YEAR):
    year = f"{i}"
    iiif_col_file = f"{os.path.join(IIIF_COL_DIR, str(year).lower())}.json"
    iiif_col_url = IIIF_COLLECTION_URL.format(year)
    manifests = {}
    col_name = f"wrz__{year}"
    col_id = client.get_or_create_collection(col_name)
    print(col_id, col_name)
    time.sleep(20)
    r = requests.get(iiif_col_url)
    data = r.json()
    for x in tqdm(data["manifests"]):
        label = x["label"]
        date = label.split()[-1]
        id = f"wrz{date.replace('-', '')}"
        manifests[id] = {"url": x["@id"], "label": label, "id": id, "date": date}
        client.upload_iiif_from_url(x["@id"], col_id)
        time.sleep(1)
print("done")
