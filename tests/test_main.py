import os
import re
import logging
import requests
from bs4 import BeautifulSoup
from typing import Optional
import typer
from typer import Typer, Argument, Option
from rich.progress import track
import pytest
from online_novel_downloader.main import (
    url_callback,
    save_folder_callback,
    website_callback,
    get_lightnovelcave_info,
    get_next_url,
    download,
)


# Test the URL callback
def test_url_callback():
    valid_url = "https://example.com"
    invalid_url = "htp://invalid-url"

    assert url_callback(valid_url) == valid_url

    with pytest.raises(typer.BadParameter):
        url_callback(invalid_url)


# Test the save folder callback
def test_save_folder_callback():
    valid_folder = "valid_folder"
    invalid_folder = "invalid/folder"

    assert save_folder_callback(valid_folder) == valid_folder

    with pytest.raises(typer.BadParameter):
        save_folder_callback(invalid_folder)


# Test the website callback
def test_website_callback():
    valid_website = "lightnovelcave"
    invalid_website = "unsupportedwebsite"

    assert website_callback(valid_website) == valid_website

    with pytest.raises(typer.BadParameter):
        website_callback(invalid_website)


# Test the get_lightnovelcave_info function
def test_get_lightnovelcave_info():
    html_content = """
    <html>
        <input id="orderno" value="1"/>
        <div id="chapter-container">
            <p>Paragraph 1</p>
            <p>Paragraph 2</p>
        </div>
    </html>
    """
    soup = BeautifulSoup(html_content, "html.parser")
    result = get_lightnovelcave_info(soup)

    assert result["current_chapter"] == "1"
    assert result["chapter_content"] == ["Paragraph 1", "Paragraph 2"]


# Test the get_next_url function
def test_get_next_url():
    html_content = """
    <html>
        <a class="button nextchap" href="/next-chapter"/>
    </html>
    """
    soup = BeautifulSoup(html_content, "html.parser")
    website = "lightnovelcave"

    next_url = get_next_url(website, soup)
    assert next_url == "https://lightnovelcave.com/next-chapter"


# Test the download function
def test_download(requests_mock):
    start_url = "https://lightnovelcave.com/start-chapter"
    next_url = "https://lightnovelcave.com/next-chapter"
    html_content_start = """
    <html>
        <input id="orderno" value="1"/>
        <div id="chapter-container">
            <p>Paragraph 1</p>
        </div>
        <a class="button nextchap" href="/next-chapter"/>
    </html>
    """
    html_content_next = """
    <html>
        <input id="orderno" value="2"/>
        <div id="chapter-container">
            <p>Paragraph 2</p>
        </div>
    </html>
    """

    requests_mock.get(start_url, text=html_content_start)
    requests_mock.get(next_url, text=html_content_next)

    download(
        start_url=start_url,
        website="lightnovelcave",
        total_chapters=2,
        save_folder="test_folder",
        base_file_name="chapter",
        version=None,
        verbose=None,
    )

    assert os.path.exists("test_folder/chapter_1.txt")
    assert os.path.exists("test_folder/chapter_2.txt")

    with open("test_folder/chapter_1.txt", "r") as file:
        content = file.read()
        assert "Paragraph 1" in content

    with open("test_folder/chapter_2.txt", "r") as file:
        content = file.read()
        assert "Paragraph 2" in content

    # Clean up
    os.remove("test_folder/chapter_1.txt")
    os.remove("test_folder/chapter_2.txt")
    os.rmdir("test_folder")


# if __name__ == "__main__":
#     pytest.main()
