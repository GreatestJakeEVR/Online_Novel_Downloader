from typing import Optional

import typer
from typing_extensions import Annotated
from rich import print

__version__ = "0.1.0"

app = typer.Typer()


def version_callback(value: bool):
    if value:
        print(f"ln_cave_downloader Version: {__version__}")
        raise typer.Exit()


def total_chapters_callback(value: int):
    if value <= 0:
        raise typer.BadParameter("total-chapters must be a positive integer")
    return value


@app.command()
def main(
    start_url: Annotated[
        str,
        typer.Argument(
            help="The URL for the chapter of the novel to start downloading text from."
        ),
    ],
    version: Annotated[
        Optional[bool], typer.Option("--version", callback=version_callback)
    ] = None,
    total_chapters: Annotated[
        int,
        typer.Option(
            callback=total_chapters_callback,
            help="The number of chapters to download if you don't want to download as many as possible.",
        ),
    ] = 999999,
    save_folder: Annotated[
        str,
        typer.Option(
            help="The folder name to save the downloaded text files to.",
        ),
    ] = "downloaded_chapters",
    base_file_name: Annotated[
        str,
        typer.Option(
            help="The base name for the downloaded text files. For example: 'chapter' will save files as 'chapter_1.txt', 'chapter_2.txt', etc.",
        ),
    ] = "chapter",
):
    """
    The main function of the script. It will download the chapter text starting
    with the start_url and continue until it either hits the end of the novel
    or until it hits the number of chapters specified by total_chapters.
    """
    print("hey")


if __name__ == "__main__":
    app()
