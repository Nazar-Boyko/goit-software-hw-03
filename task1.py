
from pathlib import Path
import argparse

from concurrent.futures import ThreadPoolExecutor
import shutil

import os

def scan_directory(path):

    files = []

    for item in path.iterdir():

        if item.is_file():
            files.append(item)

        elif item.is_dir():
            files.extend(scan_directory(item))

    return files


def get_files(path):

    files = []

    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:

        futures = []

        for item in path.iterdir():

            if item.is_dir():
                futures.append(
                    executor.submit(scan_directory, item)
                )

            else:
                files.append(item)


        for future in futures:
            files.extend(future.result())

    return files


def copy_file(files: list, main_dir):

    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:

        futures = []

        for path in files:
            futures.append(
                executor.submit(copy_one_file, path, main_dir)
            )

        for future in futures:
            future.result()


def copy_one_file(path,main_dir):

    source = Path(path)
    extension = source.suffix[1:] if source.suffix else "no_extension"
    target_dir = Path(main_dir) / extension

    target_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(
        source, 
        target_dir / source.name)




def create_directory(path: Path) -> None:
    try:
        path.mkdir(parents=True, exist_ok=True)
    except (PermissionError, OSError) as e:
        print(f"Помилка при створенні деректорії {path}: {e}")


def main():

    parser = argparse.ArgumentParser(description="Опис програми")

    parser.add_argument("nameDir", help="Введіть назву деректорія яка потербує сорутвання")
    parser.add_argument("nameNewDir",nargs="?",help="Введіть назву для нової деректорії", default="dist")

    args = parser.parse_args()

    original_dir = Path(args.nameDir)
    new_dir = Path(args.nameNewDir)

    create_directory(new_dir)

    files = get_files(original_dir)

    copy_file(files, new_dir)





if __name__ == "__main__":
    main()