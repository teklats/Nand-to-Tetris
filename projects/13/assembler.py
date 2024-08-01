from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass
class Assembler:
    comp_table = {
        "0": "0101010",
        "1": "0111111",
        "-1": "0111010",
        "D": "0001100",
        "A": "0110000",
        "!D": "0001101",
        "!A": "0110001",
        "-D": "0001111",
        "-A": "0110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "D+A": "0000010",
        "D-A": "0010011",
        "A-D": "0000111",
        "D&A": "0000000",
        "D|A": "0010101",
        "M": "1110000",
        "!M": "1110001",
        "-M": "1110011",
        "M+1": "1110111",
        "M-1": "1110010",
        "D+M": "1000010",
        "D-M": "1010011",
        "M-D": "1000111",
        "D&M": "1000000",
        "D|M": "1010101"
    }

    jump_table = {
        '': '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111',
    }

    dest_table = {
        '': '000',
        'M': '001',
        'D': '010',
        'MD': '011',
        'A': '100',
        'AM': '101',
        'AD': '110',
        'AMD': '111',
    }

    symbols = {
        'R0': '0',
        'R1': '1',
        'R2': '2',
        'R3': '3',
        'R4': '4',
        'R5': '5',
        'R6': '6',
        'R7': '7',
        'R8': '8',
        'R9': '9',
        'R10': '10',
        'R11': '11',
        'R12': '12',
        'R13': '13',
        'R14': '14',
        'R15': '15',
        'SCREEN': '16384',
        'KBD': '24576',
        'SP': '0',
        'LCL': '1',
        'ARG': '2',
        'THIS': '3',
        'THAT': '4'
    }

    def __init__(self) -> None:
        self.code_line = 0
        self.unique = 16

    @classmethod
    def create(cls) -> Assembler:
        return cls()

    def assemble(self, assembly: Iterable[str]) -> Iterable[str]:
        hack = []

        self.first_pass(assembly)

        for line in assembly:
            line = line.strip()

            if line.startswith("//") or not line or line.startswith('('):
                continue
            if line.startswith("@"):
                hack.append(self.a_instruction(line))
            else:
                hack.append(self.c_instruction(line))

        return hack

    def a_instruction(self, line: str) -> str:
        if line[1].isdigit():
            binary = bin(int(line[1:]))[2:]
            ans = '0' * (16 - len(binary)) + binary
            return ans
        if line[1:] in self.symbols:
            binary = bin(int(self.symbols[line[1:]]))[2:]
            ans = '0' * (16 - len(binary)) + binary
            return ans

        self.symbols[line[1:]] = str(self.unique)
        binary = bin(int(self.symbols[line[1:]]))[2:]
        ans = '0' * (16 - len(binary)) + binary
        self.unique += 1
        return ans

    def c_instruction(self, line: str) -> str:
        line = line.split("/")[0].strip()

        half = line.split(";")
        if len(half) > 1:
            jmp = half[1]
        else:
            jmp = ""

        dest_pos = half[0]
        dest = dest_pos.split("=")

        if len(dest) > 1:
            comp = dest[1]
            dest1 = dest[0]
        else:
            comp = dest[0]
            dest1 = ""

        ans = "111" + self.comp_table[comp] + self.dest_table[dest1]
        ans += self.jump_table[jmp]
        return ans

    def first_pass(self, assembly: Iterable[str]) -> None:
        for line in assembly:
            line = line.strip()
            if line.startswith('('):
                self.symbols[line.split(")")[0][1:]] = str(self.code_line + 1)
            else:
                self.code_line += 1
        return None
