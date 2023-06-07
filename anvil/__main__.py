"""The main entry point for the anvil command line tool."""

from anvil.config import AnvilConfig


def run(config: AnvilConfig, seed_design_path: str) -> None:
    pass


def main():
    """The main entry point for the anvil command line tool."""
    from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

    parser = ArgumentParser(
        description="Anvil: open-source SciML tool for automated design evaluation & optimization",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--config",
        "-c",
        help="Path to the configuration file",
        required=True,
        type=str,
    )
    parser.add_argument(
        "--seed-design",
        "-d",
        help="Path to the seed design file",
        required=True,
        type=str,
    )

    args = parser.parse_args()

    conf = AnvilConfig.from_file(args.config)
    run(conf, args.seed_design)


if __name__ == "__main__":
    main()
