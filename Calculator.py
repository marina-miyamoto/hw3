def readNumber(line, index): #Separating Numbers
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        keta = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * keta
            keta /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def readPlus(line, index): #Read Plus Sign
    token = {'type': 'PLUS'}
    return token, index + 1


def readMinus(line, index): #Read Minus Sign
    token = {'type': 'MINUS'}
    return token, index + 1

def readMultiply(line, index): #Read Multiply Sign
    token = {'type': 'MULTIPLY'}
    return token, index + 1

def readDivide(line, index): #Read Divide Sign
    token = {'type': 'DIVIDE'}
    return token, index + 1


def tokenize(line): #Change the numbers/signs to tokens
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readMultiply(line, index)
        elif line[index] == '/':
            (token, index) = readDivide(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

def evaluate_multiplication_division(tokens):
    index = 2
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'MULTIPLY':
                new_number = tokens[index - 2]['number'] * tokens[index]['number']
                del tokens[index]
                del tokens[index - 1]
                del tokens[index - 2]
                token = {'type': 'NUMBER', 'number': new_number}
                tokens.insert(index - 2, token)
                index = index - 2
               
                
            elif tokens[index - 1]['type'] == 'DIVIDE':
                new_number = tokens[index - 2]['number'] / tokens[index]['number']
                del tokens[index]
                del tokens[index - 1]
                del tokens[index - 2]
                token = {'type': 'NUMBER', 'number': new_number}
                tokens.insert(index - 2, token)
                index = tokens.index(token)
                
            elif tokens[index - 1]['type'] != 'PLUS' and tokens[index - 1]['type'] != 'MINUS':
                print('Invalid syntax')
                exit(1)
        index += 1
    return tokens

def evaluate_addition_subtraction(tokens):
    answer = 0
    index = 1
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer

def evaluate_answer(line):
    tokens = tokenize(line)
    tokens = evaluate_multiplication_division(tokens)
    return evaluate_addition_subtraction(tokens)

def test(line):
    actualAnswer = evaluate_answer(line)
    expectedAnswer = eval(line)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expectedAnswer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("1.5+8*2")
    test("0.5+8/2")
    test("1-2")
    test("1-5+3")
    test("1-9.8*2")
    test("6-8/2")
    test("7*3")
    test("6*3.3*4")
    test("5*5+3")
    test("1*9.8-2")
    test("6*8/2")
    test("1/2")
    test("1/5+3")
    test("1/9.8-2")
    test("1/8*2")
    test("1/8/2")
    test("44+2.5-3*4")
    test("1+2-3/4")
    test("6+7-8*9/10")
    print("==== Test finished! ====\n")

runTest()

while True:
    print('> ', end="")
    line = input()
    answer = evaluate_answer(line)
    print("answer = %f\n" % answer)   