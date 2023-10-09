import pandas as pd
import time
import requests
from config import IIIF_COLLECTION_URL
from tqdm import tqdm


START_YEAR = 1703
END_YEAR = 1704

data = []
for i in tqdm(range(START_YEAR, END_YEAR)):
    iiif_col_url = IIIF_COLLECTION_URL.format(str(i))
    print(iiif_col_url)
    r = requests.get(iiif_col_url)
    issues = r.json()
    for x in issues["manifests"]:
        # time.sleep(1)
        issue = requests.get(x["@id"]).json()
        page_count = len(issue["sequences"][0]["canvases"])
        item = {"id": issue["@id"], "title": issue["label"], "pages": page_count}
        data.append(item)

df = pd.DataFrame(data)

df.to_csv("data.csv", index=False)
