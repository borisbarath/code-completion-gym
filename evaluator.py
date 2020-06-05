#!/usr/bin/env python3

from lib import Counter, JediPredictor
from tqdm import tqdm
import argparse
import glob


def evaluate_model_keystrokes(file, path, model, counter, limit):
    try:
        return (0, counter.count_keystrokes(file, limit, model))

    except Exception as e:
        print(e)
        return (-1, file)


def performance_evaluation():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', required=True,
                        help="path to python3 test files")
    parser.add_argument('-l', '--limit', default=None,
                        help="how many completions to return")
    args = parser.parse_args()

    counter = Counter()
    model = JediPredictor()
    print("using jedi predictor")

    files = glob.glob(args.path)

    out = open('evaluation_jedi.txt', "w+")

    print(len(files), "files in path")

    res_names = [(evaluate_model_keystrokes(
        f, path=args.path, model=model, counter=counter, limit=args.limit), f) for f in tqdm(files)]

    results = [res for (res, name) in res_names]
    print(len(results))
    print(results)
    out.write("Model: jedi")
    out.write("\n")

    errors = []
    ratios = []

    for result in results:
        if result[0] == 0:
            ratios.append(result[1])
        else:
            errors.append(result[1])

    out.write("Percent of keystrokes compared to no prediction: {}".format(
        sum(ratios)/len(ratios)))
    out.write("\n")

    for tup in res_names:
        out.write(tup[1])
        out.write(" ")
        out.write(str(tup[0][1]))
        out.write("\n")

    out.close()


if __name__ == "__main__":
    performance_evaluation()
