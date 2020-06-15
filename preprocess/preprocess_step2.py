from tqdm import tqdm
import glob
import re
import os
import jedi
import tokenize
import json


def filename_from_path(path):
    return os.path.splitext(path)[0].replace("/", "_")


def prepare_function(input_file, output_folder, jedi_limit=5):

    out_file_name = filename_from_path(input_file)
    output_file = output_folder + "/" + out_file_name + "_processed.txt"
    jedi_file = open(input_file, 'r').read()

    with open(output_file, "w+") as out:
        prefix = []
        token_stream = []
        token_string = ""
        alt = ''
        # out.write("[")
        with open(input_file, 'rb') as f:
            tokens = tokenize.tokenize(f.readline)

            print("Processing {}".format(input_file))

            end_line, end_col = 0, 0
            for token in tokens:
                # skip certain tokens like encoding
                if token.type in {57, 59}:
                    continue
                if token.type in {0, 4, 5, 53, 56, 58}:
                    (start_line, start_col) = token.start
                    if end_line == start_line and start_col != end_col:
                        prefix.append(" ")
                    (end_line, end_col) = token.end
                    prefix.append(token.string)
                    token_stream.append(token.string)
                    continue

                # get string of the token
                token_string = token.string

                # determine whether there is a space or tab between two tokens
                (start_line, start_col) = token.start
                if end_line != start_line and start_col != 0:
                    for _ in range(start_col):
                        prefix.append(" ")
                if end_line == start_line and start_col != end_col:
                    prefix.append(" ")

                # iterate through current token, calling jedi
                last_token_prefix = []
                for ch in token_string:
                    # prefix of last token to be fed to jedi
                    last_token_prefix.append(ch)
                    token_prefix = "".join(last_token_prefix)

                    # get predictions from jedi
                    script = jedi.Script(jedi_file, sys_path="tornado")
                    try:
                        completions = list(map(lambda completion: completion.name, script.complete(
                            start_line, start_col + len(last_token_prefix))))
                    except:
                        continue

                    alt = ''.join(prefix)
                    obj = {}
                    obj["prefix"] = alt
                    obj["token_stream"] = token_stream[-20:]
                    obj["token_prefix"] = token_prefix
                    obj["real_token"] = token.string
                    obj["predictions"] = completions[:jedi_limit]

                    out.write(json.dumps(obj))
                    out.write("\n")

                # build prefix and token stream
                (end_line, end_col) = token.end
                prefix.append(token_string)
                token_stream.append(token_string)

        alt = ''.join(prefix)

        obj = {}
        obj["prefix"] = alt
        obj["token_stream"] = token_stream[-40:]
        obj["token_prefix"] = token_prefix
        obj["real_token"] = token_prefix
        obj["predictions"] = completions[:jedi_limit]
        out.write(json.dumps(obj))
        out.write("\n")

    out.close()


output_folder = "thesis_data/tornado_processed_40_tokens"

files = glob.glob("tornado/**/*.py", recursive=True)


out_files = [name for name in os.listdir(output_folder)]

print(len(files), "files in path")

for f in tqdm(files):
    out_file_name = filename_from_path(f)
    if out_file_name + "_processed.txt" in out_files:
        continue

    prepare_function(f, output_folder, jedi_limit=10)
