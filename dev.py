import csv
import json
import zipfile
from argparse import ArgumentParser
from os import mkdir, path, rename, walk
from secrets import token_hex
from shutil import copyfile, rmtree
from urllib.parse import quote_plus


def preprocess_latex_csv(input_file: str, output_file: str):
    with open(input_file, 'r') as in_file, open(output_file, 'w', newline='') as out_file:
        csv_reader = csv.reader(in_file)
        csv_writer = csv.writer(out_file)

        # Skip the first row (header) of csv_reader
        next(csv_reader)

        for row in csv_reader:
            row.insert(1, row[0])
            row.insert(0, row.pop(1))

            csv_writer.writerow(row)


def build_json_files(source: str, destination: str):
    fieldnames = ["name", "keyword", "content"]

    with open(f"{source}-alfred.csv", newline='', encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=fieldnames)
        for row in reader:
            uid = token_hex(15)
            output = json.dumps(
                {
                    "alfredsnippet": {
                        "snippet": row["content"],
                        "uid": uid,
                        "keyword": row["keyword"],
                        "name": row["name"],
                    },
                },
                sort_keys=False,
                indent=4,
                separators=(',', ': '),
            )
            output_file = destination + "/" + quote_plus(row["name"] + " [" + uid + "].json")
            with open(output_file, "w") as f:
                f.write(output)


def zip_files(destination: str):
    with zipfile.ZipFile(destination + ".zip", "w") as zf:
        for root, _, files in walk(destination):
            for f in files:
                zf.write(
                    path.join(root, f),
                    f,
                    compress_type=zipfile.ZIP_DEFLATED,
                )


def change_zip_extension(destination: str):
    renamee = destination + ".zip"
    pre, _ = path.splitext(renamee)
    rename(renamee, pre + ".alfredsnippets")


def main(source: str, destination: str):
    mkdir(destination)
    copyfile("./info.plist", "./" + destination + "/info.plist")
    build_json_files(source, destination)
    zip_files(destination)
    change_zip_extension(destination)
    rmtree(destination)


if __name__ == "__main__":
    parser = ArgumentParser(description="CSV to Alfred Snippets")
    parser.add_argument("-s", "--source", help="Relative path of csv file", required=True)
    parser.add_argument("-d", "--destination", help="Relative path of output file", required=True)
    args = parser.parse_args()
    source, destination = args.source, args.destination

    # Preprocess the 'latex.csv' file to match the required format
    preprocess_latex_csv('latex.csv', 'latex-alfred.csv')

    main(source, destination)
