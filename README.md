# proton_drive_files_fix

Simple Python script that resolves clashing files in a Proton Drive library (i.e., files with `(# Name Clash ... #)` in
them.)

## Motivation

I use [Syncthing](https://syncthing.net/) to sync my personal files between all of my machines, and I also use Proton
Drive to sync those files to the cloud. However, I found that if I run the Proton Drive client on more than one of these
machines, then it doesn't recognize the files created by Syncthing as the same files that already exist on Proton Drive.
So, it creates multiple copies of the same files, and it adds a suffix like `(# Name Clash 823da3ff #)`. This is
annoying, so now I only run the Proton Drive client on one of my machines.

This script cleans up all of these clashing files. It looks for files with the `(# Name Clash ... #)` suffix and puts
them into groups based on their base file path (without the `(# Name Clash ... #)` part) and their file sizes. If a
group of clashing files shares the same file size, the script will delete all but one file and remove the suffix.
Otherwise, it will report the group of files and leave it up to you to resolve the conflict.

## Usage

**Back up your files**! To execute the script as a dry run (files will not be modified), run the following command:

```shell
python proton_drive_files_fix.py -d <proton_drive_library_path>
```

or

```shell
python proton_drive_files_fix.py --dry-run <proton_drive_library_path>
```

To execute the script as a real run (files will be modified), run the following command:

```shell
python proton_drive_files_fix.py <proton_drive_library_path>
```