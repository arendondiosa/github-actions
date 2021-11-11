import argparse
import sys

from os import path, listdir
from os.path import isfile, join

def get_all_files(file_path):
    """

    """
    all_files = []
    if path.isfile(file_path):
        with open(file_path) as file:
            lines = file.readlines()
            all_files = [line.rstrip() for line in lines]

    return all_files

def get_file_extension(file_path):
    """

    """
    filename, file_extension = path.splitext(file_path)
    return file_extension

def search_files_by_type(type, all_files):
    """

    """
    files_filtered = [file_item for file_item in all_files if get_file_extension(file_item) == type]
    return files_filtered

def format_output(files_filtered):
    """

    """
    return " ".join(files_filtered)

def check_migrations(migrations_path):
    """

    """
    migrations_files = get_all_files(migrations_path)
    return " ".join(migrations_files)

def main():
    desc = "Search inside a path for files that contains migrations duplicated, using the down revision id as criteria"

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "--input-file-path",
        dest="input_file_path",
        default="out.txt",
        type=str,
        help="path where the migration validation are going to run",
    )
    parser.add_argument(
        "--extension",
        dest="extension",
        default=".py",
        type=str,
        help="path where the migration validation are going to run",
    )
    parser.add_argument(
        "--migrations-path",
        dest="migrations_path",
        default="",
        type=str,
        help="path where the migration validation are going to run",
    )

    args, remaining_args = parser.parse_known_args()

    print("INFO: Processing detected migrations inside {}".format(args.input_file_path))

    all_files = get_all_files(args.input_file_path)
    files_filtered = search_files_by_type(args.extension, all_files)

    if args.migrations_path:
        print(check_migrations(args.migrations_path))
    else:
        print(format_output(files_filtered))

    print("INFO: No problems were found in migrations")
    sys.exit(0)


if __name__ == "__main__":
    main()
