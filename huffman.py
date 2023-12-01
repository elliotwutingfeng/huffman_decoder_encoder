from __future__ import annotations
import json

from heapq import heapify, heappop, heappush
from collections import Counter
from typing import Generator


class Node:
    def __init__(
        self,
        weight: int,
        left: Node | None = None,
        right: Node | None = None,
        char: str | None = None,
    ) -> None:
        if not isinstance(weight, int) or weight < 1:
            raise ValueError("weight must be a positive integer.")
        self.weight = weight
        self.left = left
        self.right = right
        self.char = char

    def __eq__(self, other):
        return self.weight == other.weight

    def __lt__(self, other):
        if self.__eq__(other) and self.char is not None and other.char is not None:
            return self.char < other.char
        return self.weight < other.weight


class Huffman:
    @staticmethod
    def _create_tree(frequency_table: Counter[str]) -> Node:
        queue = [Node(weight, char=char) for char, weight in frequency_table.items()]
        heapify(queue)

        while len(queue) > 1:
            child_1 = heappop(queue)
            child_2 = heappop(queue)
            parent = Node(child_1.weight + child_2.weight)
            parent.left = child_1 if child_1 < child_2 else child_2
            parent.right = child_2 if parent.left is child_1 else child_1
            heappush(queue, parent)

        return heappop(queue)

    @staticmethod
    def _create_prefix_code_table(tree: Node) -> dict[str, str]:
        table: dict[str, str] = {}

        def aux(node: Node, bit_code: str = ""):
            if node.char is not None:
                table[node.char] = bit_code
            if node.left:
                aux(node.left, bit_code + "0")
            if node.right:
                aux(node.right, bit_code + "1")

        aux(tree)
        return table

    @staticmethod
    def _text_to_bit_strings(
        text: str, prefix_code_table: dict[str, str]
    ) -> Generator[str]:
        for char in text:
            bit_code: str | None = prefix_code_table.get(char, None)
            if bit_code is None:
                raise ValueError(
                    "text contains character not found in prefix_code_table."
                )
            yield bit_code

    @staticmethod
    def compress(text: str) -> bytes:
        character_frequency_table = Counter(text)
        tree = Huffman._create_tree(character_frequency_table)
        prefix_code_table = Huffman._create_prefix_code_table(tree)
        output = bytearray(
            json.dumps(character_frequency_table, separators=(",", ":")).encode()
        )
        output.append(
            0
        )  # delimiter between character_frequency_table and compressed body
        acc = 1
        for idx, bit in enumerate(
            bit
            for bit_string in Huffman._text_to_bit_strings(text, prefix_code_table)
            for bit in bit_string
        ):
            acc <<= 1
            acc |= int(bit)
            if (idx + 1) % 7 == 0:
                output.append(acc)
                acc = 1

        if (idx + 1) % 7 != 0:
            output.append(acc)

        return bytes(output)

    @staticmethod
    def decompress(body: bytes) -> str:
        partitions = body.split(b"\x00", 1)
        if len(partitions) != 2:
            raise ValueError("No delimiter found.")
        try:
            preamble = json.loads(partitions[0])
            character_frequency_table = Counter(preamble)
        except Exception as e:
            raise ValueError("Invalid preamble: " + e)

        compressed_body = partitions[1]
        tree = Huffman._create_tree(character_frequency_table)
        node = tree
        res = ""

        for byte in compressed_body:
            byte_str = format(byte, "b")[1:]
            for char in byte_str:
                node = node.left if char == "0" else node.right
                if node is None:
                    raise ValueError("Undefined character found in body.")
                if node.char is not None:
                    res += node.char
                    node = tree

        return res
