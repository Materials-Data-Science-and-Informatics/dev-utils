from pathlib import Path
from shutil import copyfile, move

from typer.testing import CliRunner

from dev_utils.update_codemeta import app

runner = CliRunner()


def test_update_codemeta(tmp_path):
    # use own pyproject.toml for testing
    # NOTE: make path absolute, because isolated_filesystem changes cwd
    pyproject_copy = (tmp_path / "pyproject.toml").absolute()
    copyfile("pyproject.toml", pyproject_copy)
    assert pyproject_copy.is_file()

    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        td = Path(td)
        move(pyproject_copy, td / "pyproject.toml")
        assert (td / "pyproject.toml").is_file()

        # run without codemeta.json existing -> should create
        result = runner.invoke(app, ["codemeta.json", "pyproject.toml"])
        assert result.exit_code == 0
        assert (td / "codemeta.json").is_file()

        # run with existing codemeta.json and no changes -> same file
        expected = (td / "codemeta.json").read_bytes()
        result = runner.invoke(app, ["codemeta.json", "pyproject.toml"])
        assert result.exit_code == 0
        observed = (td / "codemeta.json").read_bytes()
        assert expected == observed

        # run with existing codemeta.json not matching pyproject toml
        # -> should update codemeta.json
        with open("codemeta.json", "w") as f:
            f.write("{}")  # make codemeta empty
        result = runner.invoke(app, ["codemeta.json", "pyproject.toml"])
        assert result.exit_code == 0
        observed = (td / "codemeta.json").read_bytes()
        assert expected == observed
