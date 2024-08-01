from __future__ import annotations
from typing import List

class HackComputer:
    sp: int = 0
    a_reg: int = 0
    d_reg: int = 0
    RAM: List[int] = []
    checked: List[bool] = []
    end_check: int = 0

    def __init__(self):
        self.initialize_ram_and_registers()

    def initialize_ram_and_registers(self) -> None:
        self.RAM = [0] * 24576
        self.RAM[0] = 256  # SP 
        self.RAM[1] = 300  # LCL
        self.RAM[2] = 400  # ARG
        self.RAM[3] = 3000 # THIS
        self.RAM[4] = 3010 # THAT
        self.checked = [False] * 24576

    @classmethod
    def create(cls) -> HackComputer:
        return cls()

    def execute_instruction_set(self, instruction_set: List[str], cycles: int) -> List[str]:
        ret: List[str] = []
        num_cycle: int = 0
        while self.sp < len(instruction_set) and num_cycle < cycles:
            self._execute_instruction(instruction_set[self.sp])
            
            if self.sp == len(instruction_set) - 1:
                self.end_check += 1

            if self.end_check == 3:
                break

            num_cycle += 1

        for i in range(0, 16384):
            if self.checked[i]:
                ret.append(f"{i}:{self.RAM[i]}")
        return ret

    def _collect_checked_ram(self) -> List[str]:
        return [f"{i}:{self.RAM[i]}" for i in range(0, 16384) if self.checked[i]]

    def _execute_instruction(self, instruction: str) -> None:
        op_code: str = instruction[0]

        if op_code == "0":
            address: int = int(instruction[-15:], 2)
            self.a_reg = address
            self.sp += 1
        else: 
            j: str = instruction[-3:]
            d: str = instruction[-6:-3]
            c: str = instruction[4:10]
            a: str = instruction[3]

            comp: int = self._compute(a, c)
            if d != "000":
                if d[0] == "1":
                    self.a_reg = comp
                if d[1] == "1":
                    self.d_reg = comp
                if d[2] == "1":
                    self.RAM[self.a_reg] = comp
                    self.checked[self.a_reg] = True
            if j != "000":
                self._jump(comp, j)
            else:
                self.sp += 1

    def _execute_a_instruction(self, instruction: str) -> None:
        address = int(instruction[-15:], 2)
        self.a_reg = address
        self.sp += 1

    def _execute_c_instruction(self, instruction: str) -> None:
        j, d, c, a = self._parse_c_instruction(instruction)
        comp = self._compute(a, c)
        self._handle_destination(d, comp)
        if j != "000":
            self._jump(comp, j)
        else:
            self.sp += 1

    def _parse_c_instruction(self, instruction: str) -> tuple:
        j = instruction[-3:]
        d = instruction[-6:-3]
        c = instruction[4:10]
        a = instruction[3]
        return j, d, c, a

    def _handle_destination(self, d: str, comp: int) -> None:
        if d != "000":
            if d[0] == "1":
                self.a_reg = comp
            if d[1] == "1":
                self.d_reg = comp
            if d[2] == "1":
                self._update_ram(comp)

    def _update_ram(self, value: int) -> None:
        self.RAM[self.a_reg] = value
        self.checked[self.a_reg] = True

    def _compute(self, a: str, c: str) -> int:
        if a == "0":
            return self._compute_a_is_zero(c)
        else:
            return self._compute_a_is_one(c)

    def _compute_a_is_zero(self, c: str) -> int:
        computations = {
            "101010": 0,         # 0
            "111111": 1,         # 1
            "111010": -1,        # -1
            "001100": self.d_reg, # D
            "110000": self.a_reg, # A
            "001101": ~self.d_reg,# !D
            "110001": ~self.a_reg,# !A
            "001111": -self.d_reg,# -D
            "110011": -self.a_reg,# -A
            "011111": self.d_reg + 1, # D+1
            "110111": self.a_reg + 1, # A+1
            "001110": self.d_reg - 1, # D-1
            "110010": self.a_reg - 1, # A-1
            "000010": self.d_reg + self.a_reg, # D+A
            "010011": self.d_reg - self.a_reg, # D-A
            "000111": self.a_reg - self.d_reg, # A-D
            "000000": self.d_reg & self.a_reg, # D&A
            "010101": self.d_reg | self.a_reg  # D|A
        }
        return computations.get(c, 0)

    def _compute_a_is_one(self, c: str) -> int:
        computations = {
            "110000": self.RAM[self.a_reg], # M
            "110001": ~self.RAM[self.a_reg],# !M
            "110011": -self.RAM[self.a_reg],# -M
            "110111": self.RAM[self.a_reg] + 1, # M+1
            "110010": self.RAM[self.a_reg] - 1, # M-1
            "000010": self.d_reg + self.RAM[self.a_reg], # D+M
            "010011": self.d_reg - self.RAM[self.a_reg], # D-M
            "000111": self.RAM[self.a_reg] - self.d_reg, # M-D
            "000000": self.d_reg & self.RAM[self.a_reg], # D&M
            "010101": self.d_reg | self.RAM[self.a_reg]  # D|M
        }
        return computations.get(c, 0)

    def _jump(self, comp: int, j: str) -> None:
        jump_conditions = {
            "001": comp > 0,  # JGT
            "010": comp == 0, # JEQ
            "011": comp >= 0, # JGE
            "100": comp < 0,  # JLT
            "101": comp != 0, # JNE
            "110": comp <= 0  # JLE
        }
        if jump_conditions.get(j, True): 
            self.sp = self.a_reg
        else:
            self.sp += 1