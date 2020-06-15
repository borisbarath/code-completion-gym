import glob
import os
import numpy as np
import json

from sklearn.utils import shuffle
from tqdm import tqdm

files = glob.glob(
    "tornado_processed_40_tokens/test/*_processed.txt", recursive=True)

all_data = []
all_lines = 0

print(len(files))

for file in tqdm(files):
    with open(file, "r") as f:
        lines = f.readlines()
        # all_lines += len(lines)
        # all_data += lines

        for line in lines:
            obj = json.loads(line)
            for prediction in obj["predictions"]:
                out_obj = {}
                out_obj["token_stream"] = obj["token_stream"]
                out_obj["prediction"] = prediction
                if prediction == obj["real_token"]:
                    out_obj["label"] = 1
                else:
                    out_obj["label"] = 0

                all_data.append(json.dumps(out_obj))
                all_lines += 1


print(len(all_data))
print(all_lines)
all_data_shuffled = shuffle(all_data)
del all_data


print("There will be", all_lines//20, "files")

chunks = [all_data_shuffled[x:x+20]
          for x in range(0, len(all_data_shuffled), 20)]

for idx, chunk in tqdm(enumerate(chunks), total=len(chunks)):
    with open(os.path.join("tornado_split_40_tokens/test", "tornado_{}.txt".format(idx)), "w+") as out:
        for line in chunk:
            out.write(line)
            out.write("\n")
