import argparse

from .environments import setup_environments
from .kernel import install_kernels
from .launcher import launch_notebooks


def main():
    parser = argparse.ArgumentParser(
        description="AIRTUKT: ML tutorials for turbulence research"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Install command
    install_parser = subparsers.add_parser(
        "install",
        help="Install the AIRTUKT environments and Jupyter kernels",
    )

    # Notebook command
    notebook_parser = subparsers.add_parser(
        "notebook",
        help="Launch the AIRTUKT tutorials in JupyterLab",
    )

    args = parser.parse_args()

    if args.command == "install":

        print("\n===================================")
        print("       Installing AIRTUKT")
        print("===================================\n")

        # Create environments and install requirements
        python_executables = setup_environments()

        AIRTUKT_python = python_executables["AIRTUKT"]
        AIRTUKT2_python = python_executables["AIRTUKT2"]

        # Install both Jupyter kernels
        install_kernels(
            AIRTUKT_python,
            AIRTUKT2_python,
        )

        print("\n===================================")
        print("       AIRTUKT installation complete")
        print("===================================\n")

    elif args.command == "notebook":

        launch_notebooks()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
