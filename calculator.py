from collections import deque
from math import inf
import logging

logging.basicConfig(level=logging.ERROR, filename='../EnglishTest/logger.txt', filemode='w')
proc = deque()  # main expression operations
variables = {}  # variables that had been introduced to program
digits = set(map(str, range(10)))  # {'0', '1', ..., '9'}
signs = {'-', '+', '*', '(', ')', '/'}


def about():
    """Displays the information about the program"""
    print("The program calculates the results of expressions\n"
          "You can also introduce variables (names should contain only latin symbols)")


def parse(exp):
    exp = exp.replace(' ', '')
    exp = fix_multiple_signs(exp)
    if '=' in exp:
        if exp.count('=') != 1:
            raise ArithmeticError("Invalid assignment")
        make_var(exp)
        return
    to_postfix(exp)
    return get_result()


def fix_multiple_signs(exp):
    loc_signs = {'-', '+', '*', '/'}
    i = 0
    last_sign = ''
    while i < len(exp):
        if exp[i] in loc_signs:
            tmp = exp[i]
            if last_sign:
                if last_sign in {'*', '/'} or tmp in {'*', '/'}:
                    raise ArithmeticError("Invalid expression")
                if last_sign == '-' and exp[i] == '-':
                    exp = exp[:i - 1] + '+' + exp[i + 1:]
                elif last_sign == '-' and exp[i] == '+':
                    exp = exp[:i - 1] + '-' + exp[i + 1:]
                else:
                    exp = exp[:i - 1] + exp[i:]
            else:
                i += 1
            last_sign = tmp
        else:
            last_sign = ''
            i += 1
    return exp


def make_var(buffer):
    global variables
    i = 0
    tmp = ''
    while buffer[i] != '=':
        tmp += buffer[i]
        i += 1
    i += 1
    if not check_var_name(tmp):
        raise ValueError("Invalid identifier")
    try:
        value = parse(buffer[i:])
    except ArithmeticError:
        raise ValueError("Invalid assignment")
    variables[tmp] = value


def check_var_name(tmp):
    letters = set("abcdefghijklmnopqrstuvwxyz")
    for i in tmp.lower():
        if i not in letters:
            return False
    return True


def get_result():
    global proc
    tmp = deque()
    result = inf
    while proc:
        symbol = proc.popleft()
        if symbol in signs:
            a = tmp.pop()
            b = tmp.pop()
            result = count(b, a, symbol)
            tmp.append(result)
        else:
            tmp.append(symbol)
    if result == inf:
        result = tmp.pop()
    return result


def count(a, b, symbol):
    if symbol == '+':
        return a + b
    elif symbol == '-':
        return a - b
    elif symbol == '*':
        return a * b
    elif symbol == '/':
        return a / b
    else:
        raise ArithmeticError("Invalid expression")


def to_postfix(exp):
    global state
    br_lvl = 0
    i = 0
    ops = {0: deque()}  # value - signs found on key br_lvl
    while i < len(exp):
        x, i = get_opd(exp, i)
        if i != 0:
            state = False
        if x:
            proc.append(x)
        if i >= len(exp):
            if ops[br_lvl]:
                tmp_sign = ops[br_lvl].pop()
                proc.append(tmp_sign)
            break
        if exp[i] in {'(', ')'}:
            if exp[i] == '(':
                br_lvl += 1
                state = True
                ops[br_lvl] = deque()
            elif exp[i] == ')':
                tmp_sign = ops[br_lvl].pop()
                proc.append(tmp_sign)
                br_lvl -= 1
                if br_lvl < 0:
                    raise ArithmeticError("Invalid expression")
        if ops[br_lvl]:
            tmp_sign = ops[br_lvl].pop()
            if tmp_sign in {'*', '/'}:
                proc.append(tmp_sign)
            else:
                ops[br_lvl].append(tmp_sign)
        if exp[i] in {'+', '-'}:
            if ops[br_lvl]:
                tmp_sign = ops[br_lvl].pop()
                if tmp_sign:
                    if tmp_sign in {'+', '-'}:
                        proc.append(tmp_sign)
                    else:
                        ops[br_lvl].append(tmp_sign)
            ops[br_lvl].appendleft((exp[i]))
        if exp[i] in {'*', '/'}:
            ops[br_lvl].append(exp[i])
        i += 1
    if ops[br_lvl]:
        proc.append(ops[br_lvl].pop())
    if br_lvl != 0:
        raise ArithmeticError("Invalid expression")


# except Exception as ee:
#     logging.error(f"An error occurred: {ee}\nInput: {exp}\n-----------")
#     raise ArithmeticError("Invalid expression")


def get_opd(exp, start):
    global variables, digits, signs, state
    """Name is short for 'get operand'; gets number or variable from the expression"""
    if exp[start] in signs and exp[start] != '-':
        return None, start
    tmp = ''
    i = start
    if exp[start] == '-' and state:
        tmp += '-'
        i += 1
    num = True
    while exp[i] not in signs:
        tmp += exp[i]
        if exp[i] not in digits:
            num = False
        i += 1
        if i == len(exp):
            break
    if tmp == '-':
        raise ArithmeticError("Invalid expression")
    if num:
        return int(tmp), i
    else:
        if tmp in variables:
            return variables[tmp], i
        else:
            raise ValueError("Unknown variable")


while True:
    state = True
    proc = deque()
    buf = input()
    if buf:
        if buf[0] == '/':
            if buf == '/help':
                about()
                continue
            if buf == '/exit':
                print("Bye!")
                exit(0)
            print("Unknown command")
            continue
        try:
            res = parse(buf)
        except Exception as e:
            print(e)
            continue
        if res is not None:
            if round(res) == res:
                print(round(res))
            else:
                print(res)

# def bracket(exp):
# 3 8 4 3 + 2 * 1 + * + 6 2 1 + / -
#     global signs, digits
#     """ Parsing expression from bracket """
#     out = []
#     for i in range(len(exp)):
#         tmp = ''
#         num = True
#         while exp[i] not in signs:
#             tmp += exp[i]
#             if exp[i] not in digits:
#                 num = False
#             i += 1
#         if num:
#             out.append(int(tmp))
#         else:
#             if tmp in variables:
#                 out.append(variables[tmp])
#             else:
#                 pass  # TODO: deal with the exceptions
# def parse_exp(buffer):
#     signs = {'-', '+', '*', '(', ')', ' ', '/'}
#     digits = set("0123456789")
#     for i in range(len(buffer)):
#         tmp = ''
#         num = True
#         while buffer[i] not in signs:
#             tmp += buffer[i]
#             if buffer[i] not in digits:
#                 num = False
#             i += 1
#         if tmp:
#             if num:
#                 proc.append(int(tmp))
# def parse(buffer):
#     if '=' in buffer:
#         if buffer.count('=') > 1:
#             result = "Invalid assignment"
#         else:
#             result = make_var(buffer)
#         return result
#     result = 0
#     i = 0
#     tmp = ''
#     tmp_var = ''
#     last_proc = 1  # 1 <=> +, 2 <=> -
#     state = 1  # 0 - number, 1 - plus, 2 - minus
#     digits = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}
#     while i < len(buffer):
#         flag = True
#         c = buffer[i]
#         if c == ' ':
#             i += 1
#             continue
#         if c in digits:
#             tmp, last_proc, state = make_number(state, tmp, c, last_proc)
#         else:
#             if c not in {'+', '-'}:
#                 while True:
#                     tmp_var += c
#                     i += 1
#                     if i == len(buffer):
#                         break
#                     c = buffer[i]
#                     if c in {' ', '+', '-'}:
#                         break
#                 c = tmp_var
#                 tmp_var = ''
#                 flag = False
#             tmp, state, result, last_proc, error = proc(tmp, result, last_proc, c, state)
#             if error:
#                 return error
#         if flag:
#             i += 1
#     result += increase_res(tmp, last_proc)
#     return result
#
#
# def make_var(buffer):
#     global variables
#     i = 0
#     tmp = ''
#     while buffer[i] != ' ' and buffer[i] != '=':
#         tmp += buffer[i]
#         i += 1
#     while buffer[i] != '=':
#         i += 1
#     i += 1
#     if not check_var_name(tmp):
#         return "Invalid identifier"
#     value = parse(buffer[i:])
#     if value in ("Unknown variable", "Invalid assignment"):
#         return value
#     variables[tmp] = value
#     return None
#
#
# def check_var_name(tmp):
#     letters = set("abcdefghijklmnopqrstuvwxyz")
#     for i in tmp.lower():
#         if i not in letters:
#             return False
#     return True
#
#
# def make_number(state, tmp, c, last_proc):
#     if not tmp:
#         last_proc = state
#         if last_proc == 0:
#             raise ValueError("Two numbers in a row")
#     tmp += c
#     return tmp, last_proc, 0
#
#
# def proc(tmp, result, last_proc, c, state):
#     error = None
#     if tmp:
#         result += increase_res(tmp, last_proc)
#         tmp = ''
#     if c == '+':
#         if state != 2:
#             state = 1
#     elif c == '-':
#         if state == 2:
#             state = 1
#         else:
#             state = 2
#     else:
#         if c in variables:
#             tmp = str(variables[c])
#             last_proc = state
#             state = 0
#         else:
#             if not check_var_name(c):
#                 error = "Invalid assignment"
#             else:
#                 error = "Unknown variable"
#     return tmp, state, result, last_proc, error
#
#
# def increase_res(tmp, last_proc):
#     return int(tmp) * ((-1) ** (last_proc - 1))
#
#
# def about():
#     """Displays the information about the program"""
#     print("The program calculates expressions contains only integers, '+' and '-'\n"
#           "You can also introduce variables (names should contain only latin symbols)")
#
#
# variables = {}
# while True:
#     buf = input()
#     if buf:
#         if buf[0] == '/':
#             if buf == '/help':
#                 about()
#                 continue
#             if buf == '/exit':
#                 print("Bye!")
#                 exit(0)
#             print("Unknown command")
#             continue
#         else:
#             try:
#                 res = parse(buf)
#                 if res is not None:
#                     print(parse(buf))
#             except ValueError:
#                 print("Invalid expression")
