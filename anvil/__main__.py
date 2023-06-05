"""The main entry point for the anvil command line tool."""

from anvil.config import AnvilConfig


def run(config: AnvilConfig) -> None:
    pass


def main():
    """The main entry point for the anvil command line tool."""
    from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

    parser = ArgumentParser(
        description="Anvil: open-source SciML tool for automated design evaluation & optimization",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("config", help="Path to the configuration file")
    args = parser.parse_args()

    conf = AnvilConfig.from_file(args.config)
    run(conf)


if __name__ == "__main__":
    main()
