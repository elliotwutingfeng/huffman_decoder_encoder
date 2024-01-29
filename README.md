# huffman_decoder_encoder

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
[![Coveralls](https://img.shields.io/coverallsCoverage/github/elliotwutingfeng/huffman_decoder_encoder?logo=coveralls&style=for-the-badge)](https://coveralls.io/github/elliotwutingfeng/huffman_decoder_encoder?branch=main)
[![GitHub license](https://img.shields.io/badge/LICENSE-BSD--3--CLAUSE-GREEN?style=for-the-badge)](LICENSE)

Toy implementation of a [Huffman Decoder/Encoder](https://en.wikipedia.org/wiki/Huffman_coding) for lossless data compression. Works on UTF-8 text files. For serious work, use a production-grade utility like [xz](https://en.wikipedia.org/wiki/XZ_Utils) instead.

## Requirements

Python 3.10+

## Setup

```shell
python3 -m venv venv
venv/bin/python3 -m pip install --upgrade pip
venv/bin/python3 -m pip install -r requirements.txt
```

## Testing

```shell
venv/bin/python3 -m pytest --cov --timeout 30 -k test_unit
```

## Usage

```shell
venv/bin/python3 main.py --input-file content_to_compress.txt --output-file output
```

## How does this compare to xz?

File: [135-0.txt](135-0.txt)

```markdown
   Algorithm ▏ Size (B)
------------ ▏---------
Uncompressed ▏ 3369045 🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦
     Huffman ▏ 2120395 🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦
          xz ▏  971928 🟦🟦🟦🟦🟦🟦🟦
```

## References

- <https://codingchallenges.fyi/challenges/challenge-huffman>
- <https://opendsa-server.cs.vt.edu/ODSA/Books/CS3/html/Huffman.html>
