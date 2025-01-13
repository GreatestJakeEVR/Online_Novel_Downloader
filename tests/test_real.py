import os
from typer.testing import CliRunner

from online_novel_downloader.main import app


runner = CliRunner()


def test_lightnovelcave():
    result = runner.invoke(
        app,
        [
            "https://www.lightnovelcave.com/novel/shadow-slave-1365/chapter-1763",
            "--total-chapters",
            "3",
            "--save-folder",
            "test_folder",
        ],
    )
    assert result.exit_code == 0

    # Clean up
    os.remove("test_folder/chapter_1763.txt")
    os.remove("test_folder/chapter_1764.txt")
    os.remove("test_folder/chapter_1765.txt")
    os.rmdir("test_folder")


def test_royalroad():
    result = runner.invoke(
        app,
        [
            "https://www.royalroad.com/fiction/21220/mother-of-learning/chapter/305052/19-tangled-webs",
            "--total-chapters",
            "3",
            "--save-folder",
            "test_folder",
        ],
    )
    assert result.exit_code == 0

    # Clean up
    os.remove("test_folder/chapter_1763.txt")
    os.remove("test_folder/chapter_1764.txt")
    os.remove("test_folder/chapter_1765.txt")
    os.rmdir("test_folder")
