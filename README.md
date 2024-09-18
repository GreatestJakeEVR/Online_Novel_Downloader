# Online Novel Downloader

## Description

Light novel cave is a website that hosts web novels. This program is made to help with downloading novel chapters.

## Use

For the first version it will only work on <www.lightnovelcave.com>

If you want to run the program in its own dedicated environment where it won't mess with your other python installs you can use pipx

After installing the module in your python environment, you can run it via the terminal
by having python run the package as a script like so:

```
python -m online_novel_downloader
```

or by using its command line tool name like so:

```
online-novel-downloader
```

IMPORTANT: pay attention since the first example uses the importable version of the package
name (with "_" as seprators) while the second uses the command line tool name (with "-" as
seperators).

**Usage**:

```console
$ online-novel-downloader [OPTIONS] START_URL
```

**Arguments**:

* `START_URL`: The URL for the chapter of the novel to start downloading text from.  [required]

**Options**:

* `--website TEXT`: The website to download the novel from. Currently only lightnovelcave is supported.  [default: lightnovelcave]
* `--total-chapters INTEGER RANGE`: The number of chapters to download if you don't want to download as many as possible.  [default: 99999; 1<=x<=99999]
* `--save-folder TEXT`: The folder name to save the downloaded text files to.  [default: downloaded_chapters]
* `--base-file-name TEXT`: The base name for the downloaded text files. For example: 'chapter' will save files as 'chapter_1.txt', 'chapter_2.txt', etc.  [default: chapter]
* `--version`: Display the version of the project and exit.
* `--verbose`: Display the info messages.
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.
