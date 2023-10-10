import glob
import pandas as pd

files = sorted(glob.glob("./*.csv"))
df = pd.concat([pd.read_csv(x) for x in files], axis=0, ignore_index=True)
summary = f"{len(df)} issues with a total of {df['pages'].sum()} pages\n"

with open("README.md", "r") as f:
    lines = f.readlines()
    lines[3] = summary
with open("README.md", "w") as f:
    f.writelines(lines)