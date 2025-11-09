class Expression:
    def __init__(self,id,priority,expression,answer = None):
        self.id:int = id
        self.priority:int = priority
        self.expression:str = expression
        self.__answer:int | None = answer
    @property
    def answer(self,visited = None):
        if self.__answer is None:
            self.__answer = Expression.solve(self.expression,[self.id] + visited if visited is not None else [self.id])[0]
        return self.__answer
    @staticmethod
    def solve(expression,visited,i=0,heap = None):
        expStack = []
        operate = False
        while expression[i]!=')':
            if not operate:
                if expression[i]=='(':
                    answer, i = Expression.solve(expression, visited, i + 1)
                    expStack.append(answer)
                elif expression[i].isdigit():
                    expStack.append(int(expression[i]))
                    i += 1
                elif expression[i]=='[':
                    temp = ''
                    while expression[i]!=']':
                        temp += expression[i]
                        i += 1
                    i += 1
                    temp = int(temp)
                    if temp not in visited:
                        answer = heap.findAnswerByID(temp, visited)#TODO
                        expStack.append(answer)
                    else:
                        raise Exception("Cyclic expression")
                else:
                    expStack.append(expression[i])
                    operate = True
                    i += 1
            else:
                operand1 = expStack.pop()
                opration = expStack.pop()
                if opration != "'":
                    operand2 = expStack.pop()
                else:
                    operand2 = None
                expStack.append(Expression.calculateOperation(operand1, operand2, opration))
                operate = False
        i += 1
        return expression, i
    @staticmethod
    def calculateOperation(operand1, operand2, opration):
        if operand2 is not None:
            if opration == '+':
                return operand1 + operand2
            elif opration == '-':
                return operand1 - operand2
            elif opration == '*':
                return operand1 * operand2
            elif opration == '/':
                return operand1 / operand2
            elif opration == '%':
                return operand1 % operand2
            elif opration == '^':
                return operand1 ** operand2
        elif opration == "'":
            return 0 - operand1