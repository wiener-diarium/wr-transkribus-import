import os
from transkribus_utils.transkribus_utils import ACDHTranskribusUtils


tr_user = os.environ.get("TRANSKRIBUS_USER")
tr_pw = os.environ.get("TRANSKRIBUS_PASSWORD")
new_user = os.environ.get("NEW_USER")
client = ACDHTranskribusUtils(user=tr_user, password=tr_pw)
filter_string = "wrz__176"
new_user = new_user

print(f"adding new user {new_user} to collections with name containing {filter_string}")
col_ids = [x["colId"] for x in client.filter_collections_by_name(filter_string)]
for col_id in col_ids:
    status = client.add_user_to_collection(new_user, col_id=col_id, send_mail=True)
    print(status)
