def check_same_names(var):
    for key in simbol_table:
        for type in simbol_table[key]:
            if var in simbol_table[key][type]:
                return False
    return True


def table(tree):
    global simbol_table
    for part in tree.parts:
        if type(part) not in [str, int, float]:
            if part.type in ["Var", "parameter_list"]:
                for i in part.parts:
                    if i.type == "Type":
                        type_tmp = i.parts[0]
                    if i.type == "ID":
                        if part.scope not in simbol_table.keys():
                            simbol_table[part.scope] = {type_tmp: []}
                        elif type_tmp not in simbol_table[part.scope].keys():
                            simbol_table[part.scope][type_tmp] = []
                        for j in i.parts:
                            if check_same_names(j):
                                simbol_table[part.scope][type_tmp].append(j)
                            else:
                                print("Same name is used")
            table(part)


def get_table(init_prog):
    global simbol_table
    simbol_table = {}
    with open(init_prog, "r") as f:
        s = f.read()

    result = ps().parse(s)
    print(result)
    table(result)

    return simbol_table
