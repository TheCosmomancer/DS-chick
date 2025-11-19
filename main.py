class UsolvedRequirementException(Exception):
    pass


class Heap:
    def __init__(self, array=None):
        self.array = array if array is not None else []

    def addItem(self, item):
        self.array.append(item)
        i = len(self.array) - 1
        while i > 0 and self.array[i].priority < self.array[(i - 1) // 2].priority:
            self.array[i], self.array[(i - 1) // 2] = (
                self.array[(i - 1) // 2],
                self.array[i],
            )
            i = (i - 1) // 2
    def extractMin(self):
        if len(self.array) == 0:
            return None
        
        # Store min element (root)
        minItem = self.array[0]
        
        # Move last element to root
        self.array[0] = self.array[-1]
        self.array.pop()
        
        # Heapify down
        i = 0
        while True:
            smallest = i
            left = 2 * i + 1
            right = 2 * i + 2
            
            if left < len(self.array) and self.array[left].priority < self.array[smallest].priority:
                smallest = left
            if right < len(self.array) and self.array[right].priority < self.array[smallest].priority:
                smallest = right
            
            if smallest == i:
                break
                
            self.array[i], self.array[smallest] = self.array[smallest], self.array[i]
            i = smallest
        
        return minItem
    def solve(self):
        solved = Heap()
        last_solved_count = -1
        
        while len(self.array) > 0:
            # Check if we made progress in the last iteration
            if len(solved.array) == last_solved_count:
                return "Cycle detected"
            last_solved_count = len(solved.array)
            
            # Try to solve all remaining expressions
            unsolved_heap = Heap()
            while tosolve := self.extractMin():
                try:
                    tosolve.answer = Expression.solve(tosolve.expression, Heap(solved.array.copy()))[0]
                    solved.addItem(tosolve)
                except UsolvedRequirementException:
                    unsolved_heap.addItem(tosolve)
            
            # Put unsolved items back for next iteration
            self.array = unsolved_heap.array

        ret = ""
        while solveditem := solved.extractMin():
            ret += str(solveditem.id) + ": " + str(solveditem.answer) + "\n"
        return ret


class Stack:
    def __init__(self):
        self.array = []

    def push(self, item):
        self.array.append(item)

    def pop(self):
        ret = self.array[-1]
        self.array.pop()
        return ret
    def isEmpty(self):
        return len(self.array) == 0
class Expression:
    def __init__(self, id, priority, expression, answer=None):
        self.id = id
        self.priority = priority
        self.expression = expression
        self.answer = answer

    @staticmethod
    def solve(expression, heap, i=0):
        outputStack = Stack()
        operatorStack = Stack()
        precedence = {"'": 4, "^": 3, "*": 2, "/": 2, "%": 2, "+": 1, "-": 1}
        while expression[i] != ")":
            # print(f'{expression}, {i}: {expression[i]}\n')
            if expression[i] == "(":
                # print("calling solve")
                answer, i = Expression.solve(expression, heap, i + 1)
                outputStack.push(answer)
            elif expression[i].isdigit():
                outputStack.push(int(expression[i]))
                i += 1
            elif expression[i] == "[":
                temp = ""
                i += 1
                while expression[i] != "]":
                    temp += expression[i]
                    i += 1
                i += 1
                answer = None
                while potentialAnswer := heap.extractMin():
                    if potentialAnswer.id == int(temp):
                        answer = potentialAnswer.answer
                        break
                    else:
                        heap.addItem(potentialAnswer)
                if answer is None:
                    raise UsolvedRequirementException(
                        "Expression requested another expression that is not solved yet"
                    )
                outputStack.push(answer)
            elif expression[i] in "+-*/%^'":
                unaryfixer = 1 if expression[i] == "'" else 0
                while not operatorStack.isEmpty():
                    op = operatorStack.pop()
                    if not (precedence.get(op, 0) >= precedence[expression[i]] + unaryfixer):
                        operatorStack.push(op)
                        break
                    if op == "'":
                        operand = outputStack.pop()
                        outputStack.push(
                            Expression.calculateOperation(operand, None, op)
                        )
                    else:
                        operand2 = outputStack.pop()
                        operand1 = outputStack.pop()
                        outputStack.push(
                            Expression.calculateOperation(operand1, operand2, op)
                        )
                operatorStack.push(expression[i])
                i += 1
        while not operatorStack.isEmpty():
            op = operatorStack.pop()
            if op == "'":
                operand = outputStack.pop()
                outputStack.push(Expression.calculateOperation(operand, None, op))
            else:
                operand2 = outputStack.pop()
                operand1 = outputStack.pop()
                outputStack.push(
                    Expression.calculateOperation(operand1, operand2, op)
                )
        if i+2 < len(expression):
            i += 1
        return outputStack.pop(), i

    @staticmethod
    def calculateOperation(operand1, operand2, opration):
        if opration != "'":
            if opration == "+":
                return operand1 + operand2
            elif opration == "-":
                return operand1 - operand2
            elif opration == "*":
                return operand1 * operand2
            elif opration == "/":
                return operand1 / operand2
            elif opration == "%":
                return operand1 % operand2
            elif opration == "^":
                return operand1**operand2
        else:
            return 0 - operand1


def main():
    heap = Heap()
    while True:
        expression = input("Enter an expression to solve or 's' to solve all:")
        if expression != "s":
            expression = "(" + expression.replace(" ", "").replace("\n", "") + ")"
            priority = input("Enter priority of expression:")
            heap.addItem(Expression(len(heap.array), int(priority), expression))
        else:
            break
    print(heap.solve())


if __name__ == "__main__":
    main()
