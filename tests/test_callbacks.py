import os
from typer.testing import CliRunner

from online_novel_downloader.main import app


runner = CliRunner()


def test_version_callback():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "ln_cave_downloader Version:" in result.stdout


def test_total_chapters_callback():
    # Callback checks for negative numbers
    result = runner.invoke(app, ["http://www.google.com", "--total-chapters", "-10"])
    assert result.exit_code != 0


def test_url_callback():
    # Invalid URLS
    result = runner.invoke(app, ["not_a_url"])
    assert result.exit_code != 0

    result = runner.invoke(app, ["htps://google.com/"])
    assert result.exit_code != 0


def test_save_folder_callback():
    if os.name == "nt":  # OS is Windows
        result = runner.invoke(
            app, ["https://google.com/", "--save-folder", "Invalid<FolderName"]
        )
        assert result.exit_code != 0

        result = runner.invoke(app, ["https://google.com/", "--save-folder", "CON"])
        assert result.exit_code != 0

    else:  # OS is POSIX (Linux, Unix, macOS)
        result = runner.invoke(
            app, ["https://google.com/", "--save-folder", "Invalid/FolderName"]
        )
        assert result.exit_code != 0


def test_website_callback():
    result = runner.invoke(app, ["https://google.com/", "--website", "not_a_website"])
    assert result.exit_code != 0
