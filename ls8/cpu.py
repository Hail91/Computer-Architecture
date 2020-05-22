"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUS = 0b01000101
POP = 0b01000110
ADD = 0b10100000
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
# Assign stack pointer to index 7 of register
SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8  # Stack pointer at R7
        self.PC = 0
        self.reg[SP] = 0XF4 # Set initial value of where stack pointer is pointing (F4 if it's empty)
        self.L = 0 # Flag for "Less than", set to 0 or 1 boolean
        self.G = 0 # Flag for "Greater than" set to 0 or 1 boolean
        self.E = 0 # Flag for "Equal to" set to 0 or 1 boolean

    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        with open(sys.argv[1]) as f:
            for line in f:
                program_value = line.split('#')[0].strip()
                if program_value == '':
                    continue
                value = int(program_value, 2)
                self.ram[address] = value
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == CMP:
            # Set flags to true based on the following conditions
            if self.reg[reg_a] == self.reg[reg_b]:
                self.E = 1
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.G = 1
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.L = 1
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()


    def run(self):
        """Run the CPU."""
        while True:
            # Get instruction from memory
            Instruction_reg = self.ram_read(self.PC)
            # Read from memory at specified address and store
            operand_a = self.ram_read(self.PC + 1)
            # Read from memory at specified address and store
            operand_b = self.ram_read(self.PC + 2)

            if Instruction_reg == HLT:
                print('Anddddd, we\'re done!')
                break
            elif Instruction_reg == LDI:
                self.reg[operand_a] = operand_b
                self.PC += 3
            elif Instruction_reg == ADD:
                self.alu(ADD, operand_a, operand_b)
                self.PC += 3
            elif Instruction_reg == PRN:
                register_num = operand_a
                print(self.reg[register_num])
                self.PC += 2
            elif Instruction_reg == MUL:
                self.alu(MUL, operand_a, operand_b)
                self.PC += 3
            elif Instruction_reg == PUS:
                v = self.reg[operand_a]
                self.reg[SP] -= 1
                self.ram_write(v, self.reg[SP])
                self.PC += 2
            elif Instruction_reg == POP:
                v = self.ram_read(self.reg[SP])
                self.reg[SP] += 1
                self.reg[operand_a] = v
                self.PC += 2
            elif Instruction_reg == CALL:
                self.reg[SP] -= 1
                self.ram[self.reg[SP]] = self.PC + 2
                self.PC = self.reg[operand_a]
            elif Instruction_reg == RET:
                self.PC = self.ram[self.reg[SP]]
                self.reg[SP] += 1
            elif Instruction_reg == CMP:
                self.alu(CMP, operand_a, operand_b)
                self.PC += 3
            elif Instruction_reg == JMP:
                # Need to jump to address at the given reg
                self.PC = self.reg[operand_a]
            elif Instruction_reg == JEQ:
                if self.E == 1:
                    self.PC = self.reg[operand_a]
                else:
                    # Increment the program counter by 2 to move to next instruction (2 bit instr)
                    self.PC += 2
            elif Instruction_reg == JNE:
                if self.E == 0:
                    self.PC = self.reg[operand_a]
                else:
                    self.PC += 2









