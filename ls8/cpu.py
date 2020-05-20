"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUS = 0b01000101
POP = 0b01000110
# Assign stack pointer to index 7 of register
SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8  # Stack pointer at R7
        self.PC = 0
        self.reg[SP] = 0xf4 # Set initial value of where stack pointer is pointing (F4 if it's empty)

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

        if op == 'ADD':
            self.reg[reg_a] += self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
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
                sys.exit()
            elif Instruction_reg == LDI:
                self.reg[operand_a] = operand_b
                self.PC += 3
            elif Instruction_reg == PRN:
                register_num = self.ram[self.PC + 1]
                print(self.reg[register_num])
                self.PC += 2
            elif Instruction_reg == MUL:
                self.alu(MUL, operand_a, operand_b)
                self.PC += 3
            elif Instruction_reg == PUS:
                # Decrement the stack pointer
                self.reg[SP] -= 1
                # Get the reg number we're pushing to
                reg_key = self.ram[self.PC + 1]
                # Grab the value out of that register
                reg_value = self.reg[reg_key]
                # Store that value at the current stack pointer
                most_recent_stack_address = self.reg[SP]
                self.ram[most_recent_stack_address] = reg_value
                # Increment the PC
                self.PC += 2
            elif Instruction_reg == POP:
               # 1. Copy the value from the address pointed to by `SP` to the given register.
               pop_reg_key = self.ram[self.PC + 1]
               pop_reg_val = self.ram[self.reg[SP]]
               self.reg[pop_reg_key] = pop_reg_val
               # 2. Increment `SP`.
               self.reg[SP] += 1
               self.PC += 2








