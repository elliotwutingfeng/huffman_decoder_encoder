import unittest

from huffman import Huffman
from collections import Counter


class TestHello(unittest.TestCase):
    def setUp(self):
        self.sample_frequency_table = {
            "c": 32,
            "d": 42,
            "e": 120,
            "k": 7,
            "l": 42,
            "m": 24,
            "u": 37,
            "z": 2,
        }

        self.sample_prefix_code_table = {
            "c": "1110",
            "d": "101",
            "e": "0",
            "k": "111101",
            "l": "110",
            "m": "11111",
            "u": "100",
            "z": "111100",
        }

        self.sample_body = "The Quick Brown Fox Jumps Over The Lazy Dog"

    def test_unit_make_prefix_code_table(self):
        tree = Huffman._create_tree(self.sample_frequency_table)
        table = Huffman._create_prefix_code_table(tree)
        assert table == self.sample_prefix_code_table

    def test_unit_make_tree(self):
        tree = Huffman._create_tree(self.sample_frequency_table)
        assert tree.weight == 306
        assert tree.left.weight == 120
        assert tree.right.weight == 186
        assert tree.right.left.weight == 79
        assert tree.right.right.weight == 107
        assert tree.right.left.left.weight == 37
        assert tree.right.left.right.weight == 42
        assert tree.right.right.left.weight == 42
        assert tree.right.right.right.weight == 65
        assert tree.right.right.right.left.weight == 32
        assert tree.right.right.right.right.weight == 33
        assert tree.right.right.right.right.left.weight == 9
        assert tree.right.right.right.right.right.weight == 24
        assert tree.right.right.right.right.left.left.weight == 2
        assert tree.right.right.right.right.left.right.weight == 7

        tree = Huffman._create_tree(Counter(self.sample_body))
        assert tree.left.left.char == " "

    def test_unit_compress(self):
        compressed = Huffman.compress(self.sample_body)
        assert compressed == (
            b'{"T":2,"h":2,"e":3," ":8,"Q":1,"u":2,"i":1,"c":1,"k":1,"B":1,"r":2,"o":3,"w"'
            b':1,"n":1,"F":1,"x":1,"J":1,"m":1,"p":1,"s":1,"O":1,"v":1,"L":1,"a":1,"z":1,"'
            b'y":1,"D":1,"g":1}\x00\xe3\xa9\x9e\xa3\xc6\xae\xa3\x9f\xd6\xf7\xc4\xab'
            b"\xd0\xcc\x9c\xd2\xe5\xfd\xd3\xf9\xc6\xd2\xae\xfb\xb7\xb1\xdas"
        )

    def test_unit_decompress(self):
        compressed = Huffman.compress(self.sample_body)
        decompressed = Huffman.decompress(compressed)
        assert decompressed == self.sample_body

    def test_integration(self):
        with open("135-0.txt", "r", encoding="utf-8") as f:
            body = f.read()
        compressed = Huffman.compress(body)
        decompressed = Huffman.decompress(compressed)
        assert decompressed == body
