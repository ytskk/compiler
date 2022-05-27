import struct

registers = {
    "t0": 0,
    "t1": 0,
    "t2": 0,
    "t3": 0,
    "t4": 0,
    "t5": 0,
    "t6": 0,
    "t7": 0,
    "s0": 0,
    "s1": 0,
    "s2": 0,
    "s3": 0,
    "s4": 0,
    "s5": 0,
    "s6": 0,
    "s7": 0,
    "t8": 0,
    "t9": 0,
    "k0": 0,
    "k1": 0,
    "lbl1": 0,
}

all_registers = {
    "at": 0,
    "v0": 0,
    "v1": 0,
    "a0": 0,
    "a1": 0,
    "a2": 0,
    "a3": 0,
    "t0": 0,
    "t1": 0,
    "t2": 0,
    "t3": 0,
    "t4": 0,
    "t5": 0,
    "t6": 0,
    "t7": 0,
    "s0": 0,
    "s1": 0,
    "s2": 0,
    "s3": 0,
    "s4": 0,
    "s5": 0,
    "s6": 0,
    "s7": 0,
    "t8": 0,
    "t9": 0,
    "k0": 0,
    "k1": 0,
    "gp": 0,
    "sp": 0,
    "fp": 0,
    "ra": 0,
    "f4": 0,
    "f6": 0,
    "f8": 0,
    "f10": 0,
    "f16": 0,
    "f18": 0,
    "lbl1": 0,
}

float_registers = {
    "f4": 0,
    "f6": 0,
    "f8": 0,
    "f10": 0,
    "f16": 0,
    "f18": 0,
}


get_bina = lambda x: x > 0 and bin(x)[2:] or f"-{bin(x)[3:]}"


def float_to_binary(value):
    val = struct.unpack("I", struct.pack("f", value))[0]
    val = get_bina(val)
    while len(val) < 32:
        val = f"0{val}"
    return int(val[:16], 2)


def alloc_reg_float():
    for reg in float_registers:
        if float_registers[reg] == 0:
            float_registers[reg] = 1
            return reg
    raise Exception("Not enough register")


def dealloc_reg_float(r):
    if r in float_registers:
        float_registers[r] = 0

    elif r not in all_registers:
        raise Exception(f"{r} is not register!")


def alloc_reg():
    for reg in registers:
        if registers[reg] == 0:
            registers[reg] = 1
            return reg
    raise Exception("Not enough register")


def dealloc_reg(r):
    if r in registers:
        registers[r] = 0

    elif r not in all_registers:
        raise Exception(f"{r} is not register!")


def dealloc_reg_tuple(r):
    if r is None:
        return
    if type(r) is str and is_reg(r):
        dealloc_reg(r)
        return
    reg_list = (
        str(r)
        .replace("'", "")
        .replace(" ", "")
        .replace("(", "")
        .replace(")", "")
        .split(",")
    )
    for reg in reg_list:
        if is_reg(reg):
            dealloc_reg(reg)


def is_reg(r):
    return r in all_registers


lbl_cnt = 0


def gen_lbl():
    global lbl_cnt
    lbl_cnt += 1
    return f"lbl{lbl_cnt}"


def gen_condop(op, p1, p2):
    lbl_exit = gen_lbl()
    instructions = []
    if is_reg(p1):
        r2 = p1
    else:
        r2 = alloc_reg()
        instructions.append(f"li ${r2},{str(p1)}")

    if is_reg(p2):
        r3 = p2
    else:
        r3 = alloc_reg()
        instructions.append(f"li ${r3},{str(p2)}")

    if op == "!=":
        instructions.append(f"beq ${r2}, ${r3}, {lbl_exit}")
    elif op == "<":
        instructions.append(f"bge ${r2}, ${r3}, {lbl_exit}")
    elif op == "<=":
        instructions.append(f"bgt ${r2}, ${r3}, {lbl_exit}")
    elif op == "==":
        instructions.append(f"bne ${r2}, ${r3}, {lbl_exit}")
    elif op == ">":
        instructions.append(f"ble ${r2}, ${r3}, {lbl_exit}")
    elif op == ">=":
        instructions.append(f"blt ${r2}, ${r3}, {lbl_exit}")

    dealloc_reg(r2)
    dealloc_reg(r3)
    return lbl_exit, instructions


def gen_binop(op, p1, p2):
    instructions = []
    if op not in ["*", "/"]:

        if is_reg(p1) and not is_reg(p2):
            if op == "&":
                instructions.append(f"andi ${p1}, ${p1}, {str(p2)}")
            elif op == "+":
                instructions.append(f"addi ${p1}, ${p1}, {str(p2)}")
            elif op == "-":
                instructions.append(f"subi ${p1}, ${p1}, {str(p2)}")
            return p1, instructions

        if not is_reg(p1) and is_reg(p2):
            if op == "&":
                instructions.append(f"andi ${p2}, ${p2}, {str(p1)}")
            elif op == "+":
                instructions.append(f"addi ${p2}, ${p2}, {str(p1)}")
            elif op == "-":
                instructions.append(f"subi ${p2}, ${p2}, -{str(p1)}")
            return p2, instructions

    r1 = alloc_reg()
    if is_reg(p1):
        r2 = p1
    else:
        r2 = alloc_reg()
        instructions.append(f"li ${r2},{str(p1)}")

    if is_reg(p2):
        r3 = p2
    else:
        r3 = alloc_reg()
        instructions.append(f"li ${r3},{str(p2)}")

    if op == "&":
        instructions.append(f"and ${r1}, ${r2}, ${r3}")
    elif op == "*":
        instructions.append(f"mul ${r1}, ${r2}, ${r3}")
    elif op == "+":
        instructions.append(f"add ${r1}, ${r2}, ${r3}")
    elif op == "-":
        instructions.append(f"sub ${r1}, ${r2}, ${r3}")
    elif op == "/":
        instructions.append(f"div ${r1}, ${r2}, ${r3}")

    dealloc_reg(r2)
    dealloc_reg(r3)

    return r1, instructions


functions = {}
g_variables = {}
l_variables = {}
s_variables = {}

global_var = True
global_fun_name = ""


def get_stack_num(f_name, v_name):
    stack = 0
    for var in l_variables[f_name]:
        if v_name == var:
            break
        stack += l_variables[f_name][var][1]
    return (stack + 1) * 4


def parse_ast(ast):
    global global_var
    global global_fun_name
    print("_______________________ast______________________")
    print("ast ", ast)
    print("ast[0] ", ast[0])

    """print("_______________________ast______________________")
    print(ast)
    print(type(ast[0]))
    print(ast[0])
    print('_____')
    print(global_var)
    print(global_fun_name)"""

    if type(ast) == int:
        return ast, []

    elif type(ast) == str:
        if ast == "continue":
            return None, ["j START"]

        if ast == "break":
            return None, ["j END"]

        if ast == "ret":
            instructions = ["lw $ra, 0($sp)", "addi $sp, $sp, STACK"]
            if global_fun_name != "main":
                instructions.append("jr $ra")
            return None, instructions

    if type(ast[0]) == int:
        r, instructions = parse_ast(ast[1])
        return (ast[0], r), instructions

    elif type(ast[0]) == tuple:
        r = None
        instructions = []
        for inst in ast:
            ri, insi = parse_ast(inst)
            if ri is not None:
                if r is None:
                    r = ri
                else:
                    r = (r, ri)
            instructions = instructions + insi
        return r, instructions

    if ast[0] == "unit":
        global_var = True
        v_e1 = ast[1]
        v_e2 = ast[2]
        ins1 = []
        ins2 = []
        if type(v_e1) == tuple:
            v_e1, ins1 = parse_ast(v_e1)
            dealloc_reg_tuple(v_e1)
        if type(v_e2) == tuple:
            v_e2, ins2 = parse_ast(v_e2)
            dealloc_reg_tuple(v_e2)
        return None, ins1 + ins2

    # max 2 parameters. Clean Code :)
    if ast[0] == "fun":
        global_var = False
        f_name = ast[2].strip()
        global_fun_name = f_name
        has_arg = False
        if len(ast) > 4:
            has_arg = True
            f_arg = ast[3]
            f_stm = ast[4]
        else:
            f_stm = ast[3]

        instructions = [f"{f_name}:"]
        insa = []
        arg_cnt = 0
        if has_arg:
            r, insa = parse_ast(f_arg)
            dealloc_reg_tuple(r)
            if f_name in l_variables:
                for var in l_variables[f_name]:
                    arg_cnt += l_variables[f_name][var][1]
            print(f"parameters in use: {arg_cnt}")
            if arg_cnt > 4:
                print("To many argumnets in function: " + f_name)
        r, insf = parse_ast(f_stm)
        dealloc_reg_tuple(r)

        # compute total stack area needed
        tot_var = 1
        if f_name in l_variables:
            for var in l_variables[f_name]:
                tot_var += l_variables[f_name][var][1]

        for index, item in enumerate(insf):
            insf[index] = item.replace("STACK", str(tot_var * 4))
        instructions.append("addi $sp, $sp, -" + str(tot_var * 4))
        # save ra
        instructions.append("sw $ra, 0($sp)")
        # load arguments
        if has_arg:
            for i in range(arg_cnt):
                insa.append("sw $a" + str(i) + ", " + str(4 + i * 4) + "($sp)")
        # load ra
        insf.append("lw $ra, 0($sp)")
        # deallocate ra
        insf.append("addi $sp, $sp, " + str(tot_var * 4))
        if f_name != "main":
            insf.append("jr $ra")
        else:
            insf.append("li $v0 10 #program finished call terminate")
            insf.append("syscall")
        functions[f_name] = r, instructions + insa + insf
        return None, []

    if ast[0] == "call":
        f_name = ast[1]
        instructions = []

        if len(ast) > 2:
            f_arg = ast[2]
            r, instructions = parse_ast(f_arg)

            arg_list = (
                str(r)
                .replace("'", "")
                .replace(" ", "")
                .replace("(", "")
                .replace(")", "")
                .split(",")
            )
            arg_cnt = 0
            for a in arg_list:
                if is_reg(a):
                    instructions.append("add $a" + str(arg_cnt) + " $zero, $" + a)
                    dealloc_reg(a)
                else:
                    instructions.append("li $a" + str(arg_cnt) + " " + a)
                arg_cnt += 1

        instructions.append("jal " + f_name)
        return "v0", instructions

    if ast[0] == "cond":
        v_op = ast[1]
        v_e1 = ast[2]
        v_e2 = ast[3]
        ins1 = []
        ins2 = []
        if type(v_e1) == tuple:
            v_e1, ins1 = parse_ast(v_e1)
        if type(v_e2) == tuple:
            v_e2, ins2 = parse_ast(v_e2)

        lbl, instructions = gen_condop(v_op, v_e1, v_e2)
        return lbl, ins1 + ins2 + instructions

    if ast[0] == "if":
        if_exp = ast[1]
        if_stmt = ast[2]

        ins_e = []
        if type(if_exp) == tuple:
            lbl, ins_e = parse_ast(if_exp)
        r, ins_s = parse_ast(if_stmt)
        dealloc_reg_tuple(r)

        instructions = ins_e + ins_s
        instructions.append(lbl + ":")
        return None, instructions

    if ast[0] == "ifelse":
        if_exp = ast[1]
        if_stmt = ast[2]
        else_stmt = ast[3]

        ins_e = []
        lbl_e = gen_lbl()
        if type(if_exp) == tuple:
            lbl, ins_e = parse_ast(if_exp)

        r, ins_s = parse_ast(if_stmt)
        dealloc_reg_tuple(r)
        ins_s.append("j " + lbl_e)
        r, ins_else = parse_ast(else_stmt)
        dealloc_reg_tuple(r)

        instructions = ins_e + ins_s
        instructions.append(lbl + ":")
        instructions.extend(ins_else)
        instructions.append(lbl_e + ":")
        return None, instructions

    if ast[0] == "while":
        w_exp = ast[1]
        w_stmt = ast[2]

        instructions = []
        ins_e = []
        ins_s = []
        if type(w_exp) == tuple:
            lbl_exit, ins_e = parse_ast(w_exp)
        if type(w_stmt) == tuple:
            r, ins_s = parse_ast(w_stmt)
            dealloc_reg_tuple(r)

        lbl_start = gen_lbl()
        instructions.append(lbl_start + ":")
        for index, item in enumerate(ins_s):
            ins_s[index] = ins_s[index].replace("START", lbl_start)
            ins_s[index] = ins_s[index].replace("END", lbl_exit)
        instructions = instructions + ins_e + ins_s
        instructions.append("j " + lbl_start)
        instructions.append(lbl_exit + ":")
        return None, instructions

    elif ast[0] == "decli":
        inse = []
        v_type = ast[1]
        v_name = ast[2]
        stack = 0
        if global_var:
            g_variables[v_name] = (v_type, "0")
        else:
            if global_fun_name not in l_variables:
                l_variables[global_fun_name] = {v_name: (v_type, 1)}
            else:
                l_variables[global_fun_name][v_name] = (v_type, 1)
            stack = get_stack_num(global_fun_name, v_name)
        if len(ast) > 3:
            v_exp = ast[3]
            if type(v_exp) == tuple:
                re, inse = parse_ast(v_exp)
                v_exp = re
            if is_reg(v_exp):
                if global_var:
                    inse.append("sw $" + v_exp + "," + v_name)
                else:
                    inse.append("sw $" + v_exp + ", " + str(stack) + "($sp)")
                dealloc_reg(re)
            else:
                if v_type == "int":
                    r1 = alloc_reg()
                    # print('r1  ', r1)
                    if global_var:
                        inse.append("li $" + r1 + "," + str(v_exp))
                        inse.append("sw $" + r1 + "," + v_name)
                    else:
                        inse.append("li $" + r1 + "," + str(v_exp))
                        inse.append("sw $" + r1 + ", " + str(stack) + "($sp)")
                    dealloc_reg(r1)
                elif v_type == "float":
                    r1 = alloc_reg_float()
                    v_exp = float_to_binary(v_exp)
                    if global_var:
                        inse.append("lui $1, " + str(v_exp))
                        inse.append("mtc1 $1, " + "$" + r1)
                    else:
                        inse.append("lui $1, " + str(v_exp))
                        inse.append("mtc1 $1, " + "$" + r1)
                    dealloc_reg_float(r1)

        else:
            if not global_var:
                inse.append("sw $zero, " + str(stack) + "($sp)")
        return None, inse

    elif ast[0] == "arrdeciz":
        inse = []
        v_type = ast[1]
        v_name = ast[2]
        v_num = ast[3]
        stack = 0
        if global_var:
            dec = "0"
            for i in range(int(v_num) - 1):
                dec += ", 0"
            g_variables[v_name] = (v_type, dec)
        else:
            if global_fun_name not in l_variables:
                l_variables[global_fun_name] = {v_name: (v_type, v_num)}
            else:
                l_variables[global_fun_name][v_name] = (v_type, v_num)
            stack = get_stack_num(global_fun_name, v_name)
        if not global_var:
            for i in range(int(v_num)):
                inse.append("sw $zero, " + str(stack + i * 4) + "($sp)")
        return None, inse

    elif ast[0] == "arrdeci":
        inse = []
        v_type = ast[1]
        v_name = ast[2]
        v_num = ast[3]
        v_list = ast[4]
        stack = 0
        if global_var:
            g_variables[v_name] = (
                v_type,
                str(v_list).replace("(", "").replace(")", ""),
            )
        else:
            if global_fun_name not in l_variables:
                l_variables[global_fun_name] = {v_name: (v_type, v_num)}
            else:
                l_variables[global_fun_name][v_name] = (v_type, v_num)
            stack = get_stack_num(global_fun_name, v_name)
        if not global_var:
            i = 0
            r, instructions = parse_ast(v_list)
            exp_list = (
                str(r)
                .replace("'", "")
                .replace(" ", "")
                .replace("(", "")
                .replace(")", "")
                .split(",")
            )
            for exp in exp_list:
                try:
                    e = int(exp)
                    r1 = alloc_reg()
                    instructions.append("li $" + r1 + "," + str(e))
                    instructions.append(
                        "sw $" + r1 + ", " + str(stack + i * 4) + "($sp)"
                    )
                    dealloc_reg(r1)
                except ValueError:
                    r = exp
                    instructions.append(
                        "sw $" + r + ", " + str(stack + i * 4) + "($sp)"
                    )
                    dealloc_reg(r)
                i += 1
            inse += instructions
        return None, inse

    elif ast[0] == "assign":
        v_name = ast[1]
        v_exp = ast[2]
        instructions = []
        stack = 0
        if v_name not in g_variables:
            stack = get_stack_num(global_fun_name, v_name)
        if type(v_exp) == tuple:
            v_exp, instructions = parse_ast(v_exp)
            if type(v_exp) == int:
                r1 = alloc_reg()
                instructions.append("li $" + r1 + "," + str(v_exp))
                v_exp = r1
            if v_name in g_variables:
                instructions.append("sw $" + v_exp + ", " + v_name)
            else:
                instructions.append("sw $" + v_exp + ", " + str(stack) + "($sp)")
            dealloc_reg(v_exp)
        else:
            r1 = alloc_reg()
            if v_name in g_variables:
                instructions.append("li $" + r1 + "," + str(v_exp))
                instructions.append("sw $" + r1 + "," + v_name)
            else:
                instructions.append("li $" + r1 + "," + str(v_exp))
                instructions.append("sw $" + r1 + ", " + str(stack) + "($sp)")
            dealloc_reg(r1)
        return None, instructions

    elif ast[0] == "ret":
        v_exp = ast[1]
        instructions = []
        if type(v_exp) == tuple:
            v_exp, instructions = parse_ast(v_exp)
        if type(v_exp) == str:
            instructions.append("add $v0, $zero, $" + v_exp)
            dealloc_reg(v_exp)
        elif type(v_exp) == int:
            instructions.append("li $v0, " + str(v_exp))
        instructions.append("lw $ra, 0($sp)")
        instructions.append("addi $sp, $sp, STACK")
        if global_fun_name != "main":
            instructions.append("jr $ra")
        return "v0", instructions

    elif ast[0] == "id":
        v_name = ast[1]
        instructions = []
        r1 = alloc_reg()
        if v_name in g_variables:
            instructions.append("lw $" + r1 + "," + v_name)
        else:
            stack = get_stack_num(global_fun_name, v_name)
            instructions.append("lw $" + r1 + ", " + str(stack) + "($sp)")
        return r1, instructions

    elif ast[0] == "char":
        if "'" not in ast[1]:
            raise Exception("char type error:" + ast[1])
        return ord(ast[1].replace("'", "")), []

    elif ast[0] == "binop":
        v_op = ast[1]
        v_e1 = ast[2]
        v_e2 = ast[3]
        ins1 = []
        ins2 = []
        if type(v_e1) == tuple:
            v_e1, ins1 = parse_ast(v_e1)
        if type(v_e2) == tuple:
            v_e2, ins2 = parse_ast(v_e2)

        r, instructions = gen_binop(v_op, v_e1, v_e2)
        return r, ins1 + ins2 + instructions

    elif ast[0] == "id":
        v_name = ast[1]
        r1 = alloc_reg()
        instructions = []
        if v_name in g_variables:
            instructions.append("lw $" + r1 + "," + v_name)
        else:
            stack = get_stack_num(global_fun_name, v_name)
            instructions.append("lw $" + r1 + ", " + str(stack) + "($sp)")
        return r1, instructions

    elif ast[0] == "asm":
        return None, [ast[1].replace('"', "")]

    elif ast[0] == "printstr":
        lbl = gen_lbl()
        s_variables[lbl] = ast[1]

        return None, [f"la $a0, {lbl}", "li $v0, 4", "syscall"]

    elif ast[0] == "not":
        v_exp = ast[1]
        instructions = []
        if type(v_exp) == tuple:
            v_exp, instructions = parse_ast(v_exp)
        if type(v_exp) == int:
            v_exp = ~v_exp
        elif is_reg(v_exp):
            instructions.append("not $" + v_exp + ", $" + v_exp)
        return v_exp, instructions

    elif ast[0] == "address":
        v_name = ast[1]
        instructions = []
        r1 = alloc_reg()
        if v_name in g_variables:
            instructions.append("la $" + r1 + "," + v_name)
        else:
            stack = get_stack_num(global_fun_name, v_name)
            instructions.append("addi $" + r1 + ", $sp, " + str(stack))
        return r1, instructions

    elif ast[0] == "paccess":
        v_name = ast[1]
        instructions = []
        r1 = alloc_reg()
        if v_name in g_variables:
            instructions.append("lw $" + r1 + "," + v_name)
            instructions.append("lw $" + r1 + ", ($" + r1 + ")")
        else:
            stack = get_stack_num(global_fun_name, v_name)
            instructions.append("lw $" + r1 + ", " + str(stack) + "($sp)")
            instructions.append("lw $" + r1 + ", ($" + r1 + ")")
        return r1, instructions

    elif ast[0] == "passign":
        v_name = ast[1]
        v_exp = ast[2]
        instructions = []
        stack = 0
        if v_name not in g_variables:
            stack = get_stack_num(global_fun_name, v_name)
        if type(v_exp) == tuple:
            v_exp, instructions = parse_ast(v_exp)
            if type(v_exp) == int:
                r1 = alloc_reg()
                instructions.append("li $" + r1 + "," + str(v_exp))
                v_exp = r1
            if v_name in g_variables:
                r2 = alloc_reg()
                instructions.append("lw $" + r2 + "," + v_name)
                instructions.append("sw $" + v_exp + ", ($" + r2 + ")")
                dealloc_reg(r2)
            else:
                r2 = alloc_reg()
                instructions.append("lw $" + r2 + ", " + str(stack) + "($sp)")
                instructions.append("sw $" + v_exp + ", ($" + r2 + ")")
                dealloc_reg(r2)
            dealloc_reg(v_exp)
        else:
            r1 = alloc_reg()
            if v_name in g_variables:
                r2 = alloc_reg()
                instructions.append("li $" + r1 + "," + str(v_exp))
                instructions.append("lw $" + r2 + "," + v_name)
                instructions.append("sw $" + r1 + ", ($" + r2 + ")")
                dealloc_reg(r2)
            else:
                r2 = alloc_reg()
                instructions.append("li $" + r1 + "," + str(v_exp))
                instructions.append("lw $" + r2 + ", " + str(stack) + "($sp)")
                instructions.append("sw $" + r1 + ", ($" + r2 + ")")
                dealloc_reg(r2)
            dealloc_reg(r1)
        return None, instructions

    raise Exception("Unknown AST:", ast)


def parse(ast, asm):
    _, instructions = parse_ast(ast)

    instructions.append(".data")

    for var in s_variables:
        instructions.append(var + ": .asciiz " + s_variables[var])

    for var in g_variables:
        instructions.append(var + ": .word " + g_variables[var][1])

    instructions.append(".text")
    instructions.append("")

    if "main" in functions:
        for line in functions["main"][1]:
            instructions.append(line)
        instructions.append("")
    else:
        raise Exception("No main found!")

    for f in functions:
        if f == "main":
            continue
        for line in functions[f][1]:
            instructions.append(line)
        instructions.append("")

    for line in instructions:
        asm.write(line + "\n")
