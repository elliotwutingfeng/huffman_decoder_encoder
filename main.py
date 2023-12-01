import sys
from huffman import Huffman

from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentParser,
    RawDescriptionHelpFormatter,
    RawTextHelpFormatter,
)


class CustomFormatter(
    RawTextHelpFormatter,
    RawDescriptionHelpFormatter,
    ArgumentDefaultsHelpFormatter,
):
    """Custom Help text formatter for argparse."""


def parse_args(args):
    parser = ArgumentParser(
        description="""
    Toy implementation of a Huffman Decoder/Encoder for lossless data compression. Works on UTF-8 text files.
    For serious work, use a production-grade utility like xz instead.
    """,
        formatter_class=CustomFormatter,
        # Disallows long options to be abbreviated
        # if the abbreviation is unambiguous
        allow_abbrev=False,
    )

    parser.add_argument(
        "-i",
        "--input-file",
        required=True,
        help="""
        Path to text file to compress.
        """,
        type=str,
    )

    parser.add_argument(
        "-o",
        "--output-file",
        required=True,
        help="""
        Path to output compressed file.
        """,
        type=str,
    )

    return parser.parse_args(args)


if __name__ == "__main__":
    parser = parse_args(sys.argv[1:])
    try:
        with open(parser.input_file, "r") as f:
            compressed = Huffman.compress(f.read())
    except OSError as e:
        raise e

    try:
        with open(parser.output_file, "wb") as f:
            f.write(compressed)
    except OSError as e:
        raise e
