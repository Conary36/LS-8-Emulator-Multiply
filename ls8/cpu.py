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
        self.reg = [0] * 8
        # ram is 256 bits
        # max writable ram
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.running = True
        self.ex_table()

    def ex_table(self):
        self.executable[LDI] = self.ldi
        self.executable[PRN] = self.prn

    def ldi(self, reg_num, value):
        self.reg[reg_num] = value

    def prn(self, reg_num):
        print(self.reg[reg_num])

    def load(self, program):
        """Load a program into memory."""

        address = 0


        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        # elif op == "CMP":
        #     if self.reg[reg_a] == self.reg[reg_b]:
        #         self.flag = 0b00000001
        #     elif self.reg[reg_a] < self.reg[reg_b]:
        #         self.flag = 0b00000100
        #     elif self.reg[reg_a] > self.reg[reg_b]:
        #         self.flag = 0b00000010
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

        instruction_reg = self.ram_read(self.pc)

        while instruction_reg != HLT:

            # Determine how many bytes in this instruction
            num_operands = instruction_reg >> OPERANDS_OFFSET
            print(f"instruction_reg: {bin(instruction_reg)}")
            print(f"num_operands: {num_operands}")

            # Call appropriate function from dispatch table with proper number of operands
            if num_operands == 0:
                self.executable[instruction_reg]()
                self.pc += 1
            elif num_operands == 1:
                self.executable[instruction_reg](self.ram_read(self.pc + 1))
                self.pc += 2
            elif num_operands == 2:
                self.executable[instruction_reg](self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
                self.pc += 3
            else:
                print("Bad instruction")

            # Read next instruction
            instruction_reg = self.ram_read(self.pc)
