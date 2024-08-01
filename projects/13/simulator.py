from typing import List
from hack_simulator import HackComputer
from file_operations import load_code, parse_file_name, save_ram_to_file

def simulate(file_name: str, cycles: int) -> None:
    machine_code = load_code(file_name)
    hack_simulator = HackComputer.create()
    ram_slots = hack_simulator.execute_instruction_set(machine_code, cycles)
    output_file_name = parse_file_name(file_name)
    save_ram_to_file(ram_slots, output_file_name)