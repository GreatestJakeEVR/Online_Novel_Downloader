import os
import logging
import re
import json

from pathlib import Path
from typing import Optional

import typer
import requests
from bs4 import BeautifulSoup
from typing_extensions import Annotated
from rich import print
from rich.progress import track


__version__ = "0.1.0"


app = typer.Typer()

logger = logging.getLogger(__name__)


def version_callback(value: bool):
    """
    This function is called when the --version flag is used. It will print the current version.
    """
    if value:
        print(f"ln_cave_downloader Version: {__version__}")
        raise typer.Exit()


def url_callback(url: str):
    """
    Checks to make sure that the URL is valid.

    Parameters
    ----------
    url : str
        The URL to check.
    """
    # Regular expression for a valid URL
    regex = re.compile(
        r"^(https?):\/\/"  # http:// or https://
        r"((([A-Za-z]{1,3})+\.)+([A-Za-z]{2,3})){1,2}"  # Domain name
        r"(\:[0-9]{1,5})?"  # Optional port number
        r"(\/[A-Za-z0-9\-._~:/?#[\]@!$&\'()*+,;=]*)*$",  # Path and query string
        re.IGNORECASE,
    )

    # Matches the URL against the regular expression
    if re.match(regex, url) is not None:
        return url
    else:
        raise typer.BadParameter(f"{url} is not a valid URL.")


def save_folder_callback(name: str):
    """
    Checks to make sure that the folder name is valid.

    Parameters
    ----------
    name : str
        The name for the folder to save the downloaded text files to.
    """
    # Define invalid characters for Windows and reserved names
    windows_invalid_chars = r'[<>:"/\\|?*]'
    windows_reserved_names = [
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
    ]

    # Check for empty or whitespace-only names
    if not name or name.isspace():
        raise typer.BadParameter(f"{name} is not a valid folder name.")

    # Check for length (most file systems have a limit of 255 characters for filenames)
    if len(name) > 255:
        raise typer.BadParameter(f"{name} is not a valid folder name.")

    # Check for invalid characters based on the OS
    if os.name == "nt":  # Windows
        if (
            re.search(windows_invalid_chars, name)
            or name.upper() in windows_reserved_names
        ):
            raise typer.BadParameter(f"{name} is not a valid folder name.")
    else:  # POSIX (Linux, Unix, macOS)
        if "/" in name:
            raise typer.BadParameter(f"{name} is not a valid folder name.")

    return name


def website_callback(website: str):
    """
    Checks to make sure that the website is supported by this program.
    Supported websites:
    - lightnovelcave

    Parameters
    ----------
    website : str
        The website to download the novel from. Currently only lightnovelcave is supported.
    """
    if website == "lightnovelcave":
        return website
    else:
        raise typer.BadParameter(f"{website} is not a valid website.")


def get_lightnovelcave_info(soup: BeautifulSoup) -> dict[str, list]:
    """
    Gets the chapter number and content from the page of a lightnovelcave novel.

    Parameters
    ----------
    r : requests.Response
        A requests.Response object from targeting a lightnovelcave url.

    Returns
    -------
    dict
        A dictionary containing the current chapter number and the chapter content.
        has form: {current_chapter: str, chapter_content: list}
    """
    results_dict = {}

    current_chapter = soup.find("input", id="orderno")
    current_chapter = current_chapter["value"]  # type: ignore #pylance mistaking this as None
    results_dict["current_chapter"] = current_chapter

    chapter_content = soup.find("div", id="chapter-container")
    chapter_content = chapter_content.find_all("p")  # type: ignore
    chapter_content = [x.string for x in chapter_content]
    results_dict["chapter_content"] = chapter_content

    return results_dict


def get_next_url(website: str, soup: BeautifulSoup) -> str:
    """
    Gets the URL for the next chapter of the novel.
    Currently supports these websites:
    - lightnovelcave

    Parameters
    ----------
    website : str
        The name of the website the novel is hosted on. Currently only works for lightnovelcave.
    soup : BeautifulSoup
        The soup object from the current chapter page.

    Returns
    -------
    str
        The URL for the next chapter of the novel.
    """
    if website == "lightnovelcave":
        if soup.find(class_="button nextchap isDisabled") is not None:
            logger.info(
                "End of novel reached before reaching total_chapters downloaded. Exiting."
            )
            raise ValueError("End of novel reached. Exiting.")
        else:
            next_chapter_url = "https://lightnovelcave.com" + soup.find(class_="button nextchap")["href"]  # type: ignore
    else:
        raise ValueError(f"{website} is not a website supported by this program.")
    logging.info(f"Next URL acquired: {next_chapter_url}")
    return next_chapter_url


@app.command()
def download(
    start_url: Annotated[
        str,
        typer.Argument(
            help="The URL for the chapter of the novel to start downloading text from.",
            callback=url_callback,
        ),
    ],
    website: Annotated[
        str,
        typer.Option(
            help="The website to download the novel from. Currently only lightnovelcave is supported.",
            callback=website_callback,
        ),
    ] = "lightnovelcave",
    total_chapters: Annotated[
        int,
        typer.Option(
            min=1,
            max=99999,
            help="The number of chapters to download if you don't want to download as many as possible.",
        ),
    ] = 99999,
    save_folder: Annotated[
        str,
        typer.Option(
            help="The folder name to save the downloaded text files to.",
            callback=save_folder_callback,
        ),
    ] = "downloaded_chapters",
    base_file_name: Annotated[
        str,
        typer.Option(
            help="The base name for the downloaded text files. For example: 'chapter' will save files as 'chapter_1.txt', 'chapter_2.txt', etc.",
        ),
    ] = "chapter",
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            help="Display the version of the project and exit.",
            callback=version_callback,
            is_eager=True,
        ),
    ] = None,
    verbose: Annotated[
        Optional[bool],
        typer.Option(
            "--verbose",
            help="Display the info messages.",
        ),
    ] = None,
):
    """
    The main function of the script. It will download the chapter text starting
    with the start_url and continue until it either hits the end of the novel
    or until it hits the number of chapters specified by total_chapters.
    """
    # Setting the log level
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s -- %(levelname)s %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )
    logging.basicConfig(level=logging.WARNING)

    if verbose:
        logging.getLogger().setLevel(level=logging.INFO)

    # Accessing the provided starting URL.
    print("Beginning chapter downloads.")
    logging.info(f"Requesting chapter 1 out of {total_chapters}: {start_url}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    r = requests.get(start_url, headers=headers)

    status_code = r.status_code
    if status_code != 200:
        logging.info(f"Status Code from request: {r.status_code}")
        print("There was an error accessing the provided URL. Exiting.")
        return

    # Creating the soup object from the request
    soup = BeautifulSoup(r.text, "html.parser")

    # Extracting data from the soup.
    # Right now only works on lightnovelcave. Later this will be customizable.
    results_dict = get_lightnovelcave_info(soup)

    # Checking for existing save folder. Will create it if it doesn't exist.
    current_chapter = results_dict["current_chapter"]

    result_folder = os.path.normpath(os.getcwd() + "/" + save_folder)

    if not os.path.exists(result_folder):
        logging.info(
            "Chapter download folder {result_folder} does not exist. Creating it."
        )
        os.mkdir(result_folder)

    # Writing the chapter to a file
    working_file = os.path.normpath(
        result_folder + "/" + "chapter_" + str(results_dict["current_chapter"]) + ".txt"
    )
    logging.info(f"Writing chapter {current_chapter} to file: {working_file}")

    indent = "    "
    with open(working_file, "w") as file:
        for para in results_dict["chapter_content"]:
            indented_paragraph = f"{indent}{para}\n\n"
            file.write(indented_paragraph)

    # Looping through the rest of the chapters
    for i in track(range(1, total_chapters), description="Downloading Chapters"):
        # Getting the next chapter URL
        tmp_url = get_next_url(website, soup)

        logging.info(f"Requesting chapter URL {i} out of {total_chapters}: {tmp_url}")

        r = requests.get(tmp_url, headers=headers)

        status_code = r.status_code
        logging.info(f"Status Code from request: {r.status_code}")
        if status_code != 200:
            print("There was an error accessing a the url {current_url}. Exiting.")
            return

        # Creating the soup object from the request
        soup = BeautifulSoup(r.text, "html.parser")

        # Getting data from the page
        results_dict = get_lightnovelcave_info(soup)

        # Writing the chapter to a file
        working_file = os.path.normpath(
            result_folder
            + "/"
            + "chapter_"
            + str(results_dict["current_chapter"])
            + ".txt"
        )
        logging.info(f"Writing chapter {current_chapter} to file: {working_file}")

        with open(working_file, "w") as file:
            for para in results_dict["chapter_content"]:
                indented_paragraph = f"{indent}{para}\n\n"
                file.write(indented_paragraph)

    logger.info("Finished downloading all chapters. Exited successfully")
    print("Finished downloading all chapters.")
    return
