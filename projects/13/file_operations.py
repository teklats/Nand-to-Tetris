from typing import List, Dict
from assembler import Assembler
import json

def read_file(file_name: str) -> List[str]:
    with open(file_name, 'r') as file:
        return file.readlines()

def write_file(data: Dict[str, Dict[str, int]], file_name: str) -> None:
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def parse_file_name(file_name: str) -> str:
    file = file_name.split("/")[-1]
    real_file_name = file.split(".")[0]
    return f"{real_file_name}.json"

def convert_asm_to_machine_code(lines: List[str]) -> List[str]:
    assembler = Assembler.create()
    return assembler.assemble(lines)

def load_code(file_name: str) -> List[str]:
    lines = read_file(file_name)
    if file_name.endswith(".asm"):
        lines = convert_asm_to_machine_code(lines)
    return lines

def save_ram_to_file(ram_data: List[str], file_name: str) -> None:
    ram_dict = {address: int(content) for entry in ram_data for address, content in [entry.split(":")]}
    data = {"RAM": ram_dict}
    write_file(data, file_name)