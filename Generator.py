from StateMachine import *
from Token import *
from Binary import *

symbol_table = []
identifier_table = []
keyword_table = []
regmem_table = []
number_table = []
operator_table = []
punctutation_table = []

keywords=['true','false','int','bool','char','else','while','if']
operators=['=', '+', '-', '/', '*', '||', '&&', '++', '--', '==', '!=', '>', '<', '>=', '<=', '!', '+=', '-=', '*=', '/=', '%=']
punctutations=['(', ')', '{', '}', ',', ';']


def set_to_symbol_table(token):
    if token in keywords:
        x = -1
        for z in range(len(keyword_table)):
            if token == keyword_table[z]:
                x = z
                symbol_table.append(['keyword', z])
        if x == -1:
            keyword_table.append(token)
            symbol_table.append(['keyword', len(keyword_table)-1])
    elif token in operators:
        x = -1
        for z in range(len(operator_table)):
            if token == operator_table[z]:
                x = z
                symbol_table.append(['operator', z])
        if x == -1:
            operator_table.append(token)
            symbol_table.append(['operator', len(operator_table) - 1])
    elif token in punctutations:
        x = -1
        for z in range(len(punctutation_table)):
            if token == punctutation_table[z]:
                x = z
                symbol_table.append(['punctutation', z])
        if x == -1:
            punctutation_table.append(token)
            symbol_table.append(['punctutation', len(punctutation_table) - 1])
    else:
        try:
            int(token)
            number_table.append(['s'+str(len(number_table)),token,None,None])
            symbol_table.append(['number',len(number_table) -1])
        except:
            x = -1
            for z in range(len(identifier_table)):
                if token == identifier_table[z][0]:
                    x = z
                    symbol_table.append(['identifier', z])
            if x == -1:
                identifier_table.append([token,None,None])
                symbol_table.append(['identifier', len(identifier_table) - 1])


def find_end(tokens,start_token,char):
    token_enum = start_token + 0
    if char == ')':
        parentheses_count = 0
        finded = False
        while not finded:
            if tokens[token_enum] == '(':
                parentheses_count += 1
            elif tokens[token_enum] == ')':
                parentheses_count -= 1
            if parentheses_count == 0:
                return token_enum
            token_enum += 1
    else:
        if char == '}':
            brace_count = 0
            finded = False
            while not finded:
                if tokens[token_enum] == '{':
                    brace_count += 1
                elif tokens[token_enum] == '}':
                    brace_count -= 1
                if brace_count == 0:
                    return token_enum
                token_enum += 1
        elif char == ';':
            finded = False
            while not finded and token_enum<len(tokens):
                if tokens[token_enum] == ';':
                    return token_enum + 1
                token_enum += 1


def check_expression(tokens,start=0,end=0):
    current_state = 0
    token_enum = start + 0
    while token_enum < end:
        current_state = expression_automata[current_state][token_expression_num(tokens[token_enum].strip())]
        token_enum += 1
    return [current_state,True,token_enum]


def check_statement(tokens,start=0,end=0):
    current_state = 0
    token_enum = start
    token_end = end
    while token_enum < token_end:
        tmp_token = tokens[token_enum].strip()
        tmp_state = current_state
        current_state = statement_automata[current_state][token_statement_num(tmp_token)]
        if current_state in [2, 6, 9, 12]:
            last_var = tmp_token
        if current_state == 14 and tmp_state == 12:
            start_tmp = token_enum+1
        if current_state == 7:
            if tmp_state == 15:
                exp_end = find_end(tokens,start_tmp,';')
                check_expression(tokens,start=start_tmp,end=exp_end-1)
                current_state = 0
                token_enum = exp_end-1
            else:
                exp_end = find_end(tokens, token_enum+1, ';')
                check_expression(tokens, start=token_enum+1, end=exp_end-1)
                current_state = 0
                token_enum = exp_end-1
        if current_state == 0 and tmp_token == 'if':
            result = check_if(tokens,start=token_enum+1)
            token_enum = result[0] + 1
        elif current_state == 0 and tmp_token == 'while':
            result = check_while(tokens,start=token_enum+1)
            token_enum = result[0] + 1
        token_enum += 1


def check_if(tokens,start):
    token_enum = start + 0
    start_statement = find_end(tokens, token_enum, char=')')
    check_expression(tokens, start=token_enum + 1, end=start_statement)
    if tokens[start_statement + 1] == '{':
        end_statement = find_end(tokens, start_statement + 1, char='}')
        check_statement(tokens=tokens, start=start_statement + 2, end=end_statement)
    else:
        end_statement = find_end(tokens, start_statement + 1, char=';')
        check_statement(tokens=tokens, start=start_statement + 1, end=end_statement)
    if len(tokens) > end_statement+1 and tokens[end_statement+1] == 'else':
        if tokens[end_statement + 2] == '{':
            end_statement_tmp = find_end(tokens, end_statement + 2, char='}')
            check_statement(tokens=tokens, start=end_statement + 3, end=end_statement_tmp)
        else:
            end_statement_tmp = find_end(tokens, end_statement + 2, char=';')
            check_statement(tokens=tokens, start=end_statement + 2, end=end_statement_tmp)
        return [end_statement_tmp , True]
    else:
        return [end_statement , True]


def check_while(tokens,start):
    token_enum = start + 0
    start_statement = find_end(tokens, token_enum, char=')')
    check_expression(tokens, start=token_enum + 1, end=start_statement)
    if tokens[start_statement+1] == '{':
        end_statement = find_end(tokens, start_statement + 1, char='}')
        check_statement(tokens=tokens, start=start_statement + 2, end=end_statement)
    else:
        end_statement = find_end(tokens, start_statement + 1, char=';')
        check_statement(tokens=tokens, start=start_statement + 1, end=end_statement)
    return [end_statement , True]

def generate_binary_code(tokens):
    for token in tokens:
        set_to_symbol_table(token)
    check_statement(tokens,end=len(tokens))
    print(identifier_table)
    print(punctutation_table)