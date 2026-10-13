from pathlib import Path
import subprocess


def launch_notebooks(notebook_dir=None):
    """Launch JupyterLab with the AIRTUKT tutorials."""

    if notebook_dir is None:
        notebook_dir = Path.cwd()

    notebook_dir = Path(notebook_dir).expanduser().resolve()

    print(f"Launching JupyterLab from: {notebook_dir}")

    subprocess.run(
        ["jupyter", "lab", str(notebook_dir)],
        check=True,
    )
