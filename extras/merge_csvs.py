import argparse
import csv
import os
from pathlib import Path


def parse_arguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Positional mandatory arguments
    parser.add_argument("root_dir", help="Root directory of data to be merged", type=str)

    # Optional arguments
    parser.add_argument("-o", "--out_path", help="Name of created dataset.", type=str, default="data.csv")

    # Print version
    parser.add_argument("--version", action="version", version='%(prog)s - Version 1.0')

    # Parse arguments
    return parser.parse_args()


def process_csvs(file_list, writer):
    for i, file in file_list:
        with open(file, 'rt', newline="") as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            if i > 0:
                next(reader)  # skip the header row
            for row in reader:
                writer.writerow(row)


def get_files(root_dir):
    print("Gathering file paths...")
    file_list = list(Path(root_dir).rglob("*.[cC][sS][vV]"))
    print("Done. {} files have been located.\n".format(len(file_list)))
    return file_list


def main():
    csv.field_size_limit(1000000000)  # up the field size because stories are long
    # Parse the arguments
    args = parse_arguments()

    # Raw print arguments
    print("You are running the script with arguments: ")
    for a in args.__dict__:
        print(str(a) + ": " + str(args.__dict__[a]))

    root_dir = args.root_dir
    out_path = args.out_path

    # Run function
    file_list = get_files(root_dir)

    with open(out_path, "w", newline="") as out_csv:
        writer = csv.writer(out_csv, delimiter=',')
        process_csvs(file_list, writer)


if __name__ == '__main__':
    main()
