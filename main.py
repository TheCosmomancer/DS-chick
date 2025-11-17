class UsolvedRequirementException(Exception):
    pass
class Heap:
    def __init__(self):
        self.array = []
    def findAnswerByID(self,id):
        for i in range(len(self.array)):
            if self.array[i].id == id:
                if self.array[i].answer is None:
                    raise UsolvedRequirementException(
                        "Expression requested another expression that is not solved yet"
                    )
                return self.array[i].answer
    def addItem(self,item):
        self.array.append(item)
        i = len(self.array) - 1
        while i > 0 and self.array[i].priority < self.array[(i-1)//2].priority:
            self.array[i], self.array[(i-1)//2] = self.array[(i-1)//2], self.array[i]
            i = (i-1)//2
    def solve(self):
        lastunsolved = {}
        unsolved = {self.array[x].id:False for x in range(len(self.array))}
        while False in unsolved.values():
            for i in range(len(self.array)):
                if self.array[i].answer is None:
                    try:
                        self.array[i].answer = Expression.solve(self.array[i].expression,self)[0]
                        unsolved[self.array[i].id] = True
                    except:
                        pass
            if unsolved == lastunsolved:
                return "Cycle detected"
            lastunsolved = unsolved.copy()
        ret = ""
        for i in range(len(self.array)):
            ret += str(self.array[i].id) + ": " + str(self.array[i].answer) + "\n"
        return ret

class Expression:
    def __init__(self,id,priority,expression,answer = None):
        self.id = id
        self.priority = priority
        self.expression = expression
        self.answer = answer
    @staticmethod
    def solve(expression, heap, i=0):
        expStack = []
        operate = False
        while expression[i]!=')':
            if not operate:
                if expression[i]=='(':
                    answer, i = Expression.solve(expression, i + 1)
                    expStack.append(answer)
                elif expression[i].isdigit():
                    expStack.append(int(expression[i]))
                    i += 1
                elif expression[i]=='[':
                    temp = ''
                    i += 1
                    while expression[i]!=']':
                        temp += expression[i]
                        i += 1
                    i += 1
                    temp = int(temp)
                    answer = heap.findAnswerByID(temp)#TODO
                    expStack.append(answer)
                else:
                    expStack.append(expression[i])
                    operate = True
                    i += 1
            else:
                operand2 = expStack[-1]
                expStack.pop()
                opration = expStack[-1]
                expStack.pop()
                operand1 = expStack[-1]
                expStack.pop()
                if opration == "'":
                    expStack.append(operand1)
                expStack.append(Expression.calculateOperation(operand1, operand2, opration))
                operate = False
        i += 1
        return expStack[-1], i
    @staticmethod
    def calculateOperation(operand1, operand2, opration):
        if opration != "'":
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
        else:
            return 0 - operand1
def main():
    heap = Heap()
    while True:
        expression = input("Enter an expression to solve or 's' to solve all:")
        if expression != "s":
            expression = '(' + expression.replace(' ','').replace('\n','') + ')'
            priority = input("Enter priority of expression:")
            heap.addItem(Expression(len(heap.array), int(priority), expression))
        else:
            break
    print(heap.solve())
if __name__ == "__main__":
    main()