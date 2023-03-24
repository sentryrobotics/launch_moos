"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """launch.moos."""


if __name__ == "__main__":
    main(prog_name="launch_moos")  # pragma: no cover
