# This tests to see if the program is working on the website www.lightnovelcave.com

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
        ],
    )
    assert result.exit_code == 0
