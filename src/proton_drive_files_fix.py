import argparse
import os
import re

CLASH_PATTERN = ' \\(# Name [Cc]lash [^#)]+ #\\)'


def main(target_dir: str, dry_run: bool = True) -> int:
    if dry_run:
        print("Running script as a dry run.")

    groups = group_clashing_files(target_dir)
    if len(groups) == 0:
        print("No clashing files found!")
        return 0

    for (base_path, group) in groups.items():
        if len(group) != 1:
            print("WARN: The following group of files has differing file sizes:")
            print(f"    Base path: `{base_path}`")
            for (size, paths) in group.items():
                print(f"    {size} bytes:")
                for path in paths:
                    print(f"        - `{path}`")
        else:
            for (size, paths) in group.items():
                print(f"File grouping located. Base path: `{base_path}`; file size: {size} bytes; files in group:")
                for path in paths:
                    print(f"    - `{path}`")
                if os.path.exists(base_path):
                    base_size = os.path.getsize(base_path)
                    if base_size == size:
                        print("A file with the base name already exists; deleting all other files in the group...")
                        if base_path in paths:
                            paths.remove(base_path)  # Just to be safe.
                        for path in paths:
                            delete_file(path, dry_run)
                    else:
                        print(f"WARN: A file with the base name already exists, but its size ({base_size} bytes) "
                              "doesn't match that of the rest of the group.")
                else:
                    rename_file(paths[0], base_path, dry_run)
                    if base_path in paths:
                        paths.remove(base_path)  # Just to be safe.
                    for path in paths[1:]:
                        delete_file(path, dry_run)
        print()

    if dry_run:
        print("This was a dry run; no files have been changed!")

    return 0


def group_clashing_files(target: str) -> dict[str, dict[int, list[str]]]:
    """
    Groups clashing files into a map like so: {base_path: {file_size: [original_path1, original_path2, ...]}}.
    """
    groups = {}
    for root, dirs, files in os.walk(target):
        for file in files:
            path = os.path.join(root, file)
            if re.search(CLASH_PATTERN, file):
                base_file = re.sub(CLASH_PATTERN, '', file)
                base_path = os.path.join(root, base_file)
                size = os.path.getsize(path)
                if base_path in groups:
                    if size in groups[base_path]:
                        groups[base_path][size].append(path)
                    else:
                        groups[base_path][size] = [path]
                else:
                    groups[base_path] = {size: [path]}
    return groups


def delete_file(path: str, dry_run: bool) -> None:
    if dry_run:
        print(f"Would delete `{path}`, but this is a dry run.")
    else:
        print(f"Deleting `{path}`")
        os.remove(path)


def rename_file(src: str, dst: str, dry_run: bool) -> None:
    if dry_run:
        print(f"Would rename `{src}` to `{dst}` and delete all other files in the group, but this is a dry run.")
    else:
        print(f"Renaming `{src}` to `{dst}` and deleting all other files in the group.")
        os.rename(src, dst)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="proton_drive_files_fix",
                                     description="Script to resolve clashing files in a Proton Drive library")
    parser.add_argument("proton_drive_library_path")
    parser.add_argument("-d", "--dry-run", action="store_true")
    args = parser.parse_args()
    exit(main(args.proton_drive_library_path, args.dry_run))
