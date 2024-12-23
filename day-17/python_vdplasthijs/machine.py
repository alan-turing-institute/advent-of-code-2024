import numpy as np

class Machine:
    '''Initial code'''
    def __init__(self, a, b, c): 
        self.a = a
        self.b = b
        self.c = c
        self.output = []
    
    def bit_xor(self, x, y):
        bin_x = bin(x)[2:]
        bin_y = bin(y)[2:]
        while len(bin_x) > len(bin_y):
            bin_y = '0' + bin_y
        while len(bin_x) < len(bin_y):
            bin_x = '0' + bin_x 

        new = []
        for ii, x_ in enumerate(bin_x):
            y_ = bin_y[ii]
            if int(x_) + int(y_) == 1:
                new.append('1')
            else:
                new.append('0')
        return int(''.join(new), 2)
    
    def call(self, code, op):  
        if code == 0:
            return self.adv(code, op)
        if code == 1:
            return self.bxl(code, op)
        if code == 2:
            return self.bst(code, op)
        if code == 3:
            return self.jnz(code, op)
        if code == 4:
            return self.bxc(code, op)
        if code == 5:
            return self.out(code, op)
        if code == 6:
            assert False
        if code == 7:
            return self.cdv(code, op)
        
    def combo(self, op):
        if op < 4:
            return int(op)
        elif op == 4:
            return self.a 
        elif op == 5:
            return self.b

    def adv(self, code, op):  # 0
        div = self.a / (2 ** self.combo(op))
        self.a = int(np.floor(div)) 
        return None

    def bxl(self, code, op):   # 1
        self.b = self.bit_xor(self.b, op)
        return None

    def bst(self, code, op):  # 2
        self.b = self.combo(op) % 8 
        return None

    def jnz(self, code, op):  # 3
        if self.a != 0:
            return op 
        return None
            
    def bxc(self, code, op): # 4
        self.b = self.bit_xor(self.b, self.c)
        return None

    def out(self, code, op):  # 5
        self.output.append(self.combo(op) % 8)
        return None

    def cdv(self, code, op):  # 7
        div = self.a / (2 ** self.combo(op))
        self.c  = int(np.floor(div))
        return None

class MachineOpt:
    '''Using bit operations'''
    def __init__(self, a, b, c): 
        self.a = a
        self.b = b
        self.c = c
        self.output = []
    
    def call(self, code, op):
        if code == 0:
            self.a = self.a >> self.combo(op)
        elif code == 1:
            self.b = self.b ^ op
        elif code == 2:
            self.b = self.combo(op) % 8
        elif code == 3:
            if self.a != 0:
                return op
        elif code == 4:
            self.b = self.b ^ self.c
        elif code == 5:
            self.output.append(self.combo(op) % 8)
        elif code == 7:
            self.c  = self.a >> op
        
        return None 
    
    def combo(self, op):
        if op < 4:
            return op
        elif op == 4:
            return self.a 
        elif op == 5:
            return self.b

def solve_machine(a_init, b, c, programme):
    m = MachineOpt(a_init, b, c)
    len_programme = len(programme)
    instruct = 0
    while instruct < len_programme:
        tmp = m.call(programme[instruct], programme[instruct + 1])
        if tmp is None:
            instruct += 2
        else:
            instruct = tmp 

    return m.output 

def combo_opt(op, a, b):
    if op < 4:
        return op
    elif op == 4:
        return a 
    elif op == 5:
        return b
        
def solve_machine_opt(a, b, c, programme): 
    '''Same but without class, bit quicker.'''
    len_programme = len(programme)
    instruct = 0
    output = []
    while instruct < len_programme:
        code = programme[instruct]
        op = programme[instruct + 1]
        if code == 0:
            a = a >> combo_opt(op, a, b)
        elif code == 1:
            b = b ^ op
        elif code == 2:
            b = combo_opt(op, a, b) % 8
        elif code == 3 and a != 0:
            instruct = op
            continue
        elif code == 4:
            b = b ^ c
        elif code == 5:
            output.append(combo_opt(op, a, b) % 8)
        elif code == 7:
            c  = a >> combo_opt(op, a, b)
        
        instruct += 2
        
    return output 

def calc_n_match(a_init, b, c, programme):
    output = solve_machine_opt(a_init, b, c, programme)
    if len(programme) != len(output):
        return None
    return sum([x == y for x, y in zip(output, programme)])
