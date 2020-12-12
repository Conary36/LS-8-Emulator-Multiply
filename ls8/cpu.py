"""CPU functionality."""

import sys

ADD = 0b10100000
AND = 0b10101000
CALL = 0b01010000
CMP = 0b10100111
DEC = 0b01100110
DIV = 0b10100011
HLT = 0b00000001
INC = 0b01100101
INT = 0b01010010
IRET = 0b00010011
JEQ = 0b01010101
JGE = 0b01011010
JGT = 0b01010111
JLE = 0b01011001
JLT = 0b01011000
JMP = 0b01010100
JNE = 0b01010110
LD = 0b10000011
LDI = 0b10000010
MOD = 0b10100100
MUL = 0b10100010
NOP = 0b00000000
NOT = 0b01101001
OR = 0b10101010
POP = 0b01000110
PRA = 0b01001000
PRN = 0b01000111
PUSH = 0b01000101
RET = 0b00010001
SHL = 0b10101100
SHR = 0b10101101
ST = 0b10000100
SUB = 0b10100001
XOR = 0b10101011

OPERANDS_OFFSET = 6


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # register 8 bits
        self.executable = {}
        # ram is 256 bits
        # max writable ram
        self.reg = [0] * 8
        # SP points at the value at the top of the stack (most recently pushed), or at address F4 if empty.
        self.reg[7] = 0xF4  # 244 # int('F4', 16)
        self.ir = 0  # instruction register
        self.ram = [0] * 256
        self.mar = 0
        self.mdr = 0
        self.fl = 0
        self.pc = 0
        self.running = True
        self.ex_table()

    def ex_table(self):
        self.executable[LDI] = self.ldi
        self.executable[PRN] = self.prn

    def ldi(self, reg_num, mdr):
        self.reg[reg_num] = mdr

    def prn(self, reg_num):
        print(self.reg[reg_num])

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        program = []
        with open(filename) as f:
            for line in f:
                split_line = line.split("#")[0]
                stripped_split_line = split_line.strip()

                if stripped_split_line != "":
                    command = int(stripped_split_line, 2)
                    program.append(command)
                    print(command)

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    @property
    def sp(self):
        return self.reg[7]

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        while not HLT:
            # Determine how many bytes in this instruction

            # IR (Instruction Register) = value at memory address in PC (Program Counter)
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.execute_instruction(ir, operand_a, operand_b)

    def execute_instruction(self, instruction, operand_a, operand_b):
        if instruction == self.HLT:
            self.HLT = True
            self.pc += 1
        elif instruction == PRN:
            print(self.reg[operand_a])
            self.pc += 2
        elif instruction == LDI:
            self.reg[operand_a] = operand_b
            self.pc += 3

        elif instruction == MUL:
            self.reg[operand_a] *= operand_b
            self.pc += 3


        elif instruction == PUSH:
            chosen_register = self.ram[self.pc + 1]
            current_reg_value = self.reg[chosen_register]
            # Decrement pointer
            self.reg[self.sp] -= 1
            self.ram[self.reg[self.sp]] = current_reg_value
            self.pc += 2

        elif instruction == POP:
            chosen_register = self.ram[self.pc + 1]
            current_mem_val = self.ram[self.reg[self.sp]]
            self.reg[chosen_register] = current_mem_val
            # Increment pointer
            self.reg[self.sp] += 1
            self.pc += 2

        elif instruction == CALL:
            # PUSH the return address onto the stack
            ## Find address/index of the command after call
            next_command_address = self.pc + 2
            # Push the address onto the stack
            ## Decrement the pointer
            self.reg[self.sp] -= 1
            # add next command address into stack pointer memory
            self.ram[self.reg[self.sp]] = next_command_address
            # Jump and set the PC to address directed to by register
            reg_number = self.ram[self.pc + 1]
            # Get address of Subroutine out of register
            address_to_jump_to: int = self.reg[reg_number]
            # set the PC
            self.pc = address_to_jump_to



        elif instruction == RET:
            self.pc = self.ram[self.reg[self.sp]]
            # pop from stack
            self.reg[self.sp] += 1

        else:
            print("INVALID INSTRUCTION.")
