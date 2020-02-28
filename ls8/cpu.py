"""CPU functionality."""

import sys

PRN = 0b01000111
LDI = 0b10000010
HLT = 0b00000001
MUL = 0b10100010
CMP = 0b10100111
JMP = 0b01010100
JNE = 0b01010110
JEQ = 0b01010101


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 255
        self.reg = [0] * 8
        self.pc = 0
        self.E = 0
        self.L = 0
        self.G = 0

    def ram_read(self, read_address):
        return self.ram[read_address]

    def ram_write(self, write_value, write_address):
        self.ram[write_address] = write_value

    def load(self, file):
        """Load a program into memory."""

        address = 0
        program = []
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
        
        try:
            with open(file) as f:
                for line in f:
                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    if num == '':
                        continue
                    val = int(num, 2)
                    program.append(f"{val:08b}")

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

        print(program)

        for instruction in program:
            instruction = '0b' + instruction
            # self.ram[address] = instruction
            self.ram[address] = int(instruction, 2)
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            # Equal: during a CMP, set to 1 if registerA is equal to registerB, zero otherwise.
            if self.reg[reg_a] == self.reg[reg_b]:
                self.E = 1
            # Less-than: during a CMP, set to 1 if registerA is less than registerB, zero otherwise.
            elif self.reg[reg_a] <= self.reg[reg_b]:
                self.L = 1
            else:
                #  Greater-than: during a CMP, set to 1 if registerA is greater than registerB, zero otherwise.
                self.G = 1
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
        while True:
            ir = self.ram[self.pc]
            op_A = self.ram_read(self.pc + 1)
            op_B = self.ram_read(self.pc + 2)

            if ir == LDI:
                self.reg[op_A] = op_B
                self.pc += 3
            elif ir == PRN:
                print(self.reg[op_A])
                self.pc += 2
            elif ir == HLT:
                break
                sys.exit(1)
            elif ir == MUL:
                self.alu("MUL", op_A, op_B)
                self.pc += 3
            
            
            elif ir == JMP:
            #    Set the PC to the address stored in the given register. 
                self.pc = self.reg[op_A]

            elif ir == CMP:
                
                self.alu("CMP", op_A, op_B)
                self.pc += 3

            elif ir == JEQ:
                # If equal flag is set (true), jump to the address stored in the given register.
                if self.E == 1:
                    self.pc = self.reg[op_A]
                else:
                    self.pc += 2

            elif ir == JNE:
                # If E flag is clear (false, 0), jump to the address stored in the given register.
                if self.E == 0:
                    self.pc = self.reg[op_A]
                else:
                    self.pc += 2
            