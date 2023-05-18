class MyLanguageInterpreter:
    def __init__(self):
        self.variables = {}

    def run(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if line:
                if line.startswith('if'):
                    self.interpret_conditional(line)
                elif line.startswith('while'):
                    self.interpret_loop(line)
                else:
                    self.interpret_line(line)

    def interpret_line(self, line):
        tokens = line.split('=')
        if len(tokens) != 2:
            print("Invalid statement:", line)
            return

        variable = tokens[0].strip()
        expression = tokens[1].strip()

        if variable not in self.variables:
            self.variables[variable] = 0

        value = self.evaluate_expression(expression)
        self.variables[variable] = value

    # This function is to evaluate expressions
    def evaluate_expression(self, expression):
        if '(' in expression and ')' in expression:
            start_index = expression.index('(')
            end_index = expression.index(')')

            if start_index > end_index:
                print("Invalid expression:", expression)
                return 0

            inner_expression = expression[start_index + 1: end_index]
            inner_value = self.evaluate_expression(inner_expression)

            expression = expression[:start_index] + str(inner_value) + expression[end_index + 1:]

            return self.evaluate_expression(expression)

        if '+' in expression:
            parts = expression.split('+')
            return self.evaluate_expression(parts[0].strip()) + self.evaluate_expression(parts[1].strip())
        elif '-' in expression:
            parts = expression.split('-')
            return self.evaluate_expression(parts[0].strip()) - self.evaluate_expression(parts[1].strip())
        elif '*' in expression:
            parts = expression.split('*')
            return self.evaluate_expression(parts[0].strip()) * self.evaluate_expression(parts[1].strip())
        elif '/' in expression:
            parts = expression.split('/')
            return self.evaluate_expression(parts[0].strip()) / self.evaluate_expression(parts[1].strip())
        elif expression.isdigit():
            return int(expression)
        else:
            return self.variables.get(expression, 0)

    # This function is to evaluate if statements
    def interpret_conditional(self, line):
        line = line[2:]  # Remove the 'if' keyword
        parts = line.split(';')
        if_condition = parts[0].strip()
        else_block = None
        if len(parts) > 1:
            else_block = parts[1].strip()

        parts = if_condition.split(':')
        if len(parts) != 2:
            print("Invalid conditional statement:", line)
            return

        condition = parts[0].strip()
        block = parts[1].strip()

        if condition:
            if '==' in condition:
                variable, value = condition.split('==')
            elif '<' in condition:
                variable, value = condition.split('<')
            elif '>' in condition:
                variable, value = condition.split('>')
            elif '<=' in condition:
                variable, value = condition.split('<=')
            elif '>=' in condition:
                variable, value = condition.split('>=')
            else:
                print("Invalid condition:", condition)
                return

            variable = variable.strip()
            value = self.evaluate_expression(value.strip())

            if variable in self.variables:
                if '==' in condition and self.variables[variable] == value:
                    self.interpret_line(block)
                elif '<' in condition and self.variables[variable] < value:
                    self.interpret_line(block)
                elif '>' in condition and self.variables[variable] > value:
                    self.interpret_line(block)
                elif '<=' in condition and self.variables[variable] <= value:
                    self.interpret_line(block)
                elif '>=' in condition and self.variables[variable] >= value:
                    self.interpret_line(block)
                elif else_block:
                    self.interpret_line(else_block)
    
    # The two preceding function is for loop evaluation               
    def evaluate_condition(self, condition):
        if '==' in condition:
            variable, value = condition.split('==')
        elif '<' in condition:
            variable, value = condition.split('<')
        elif '>' in condition:
            variable, value = condition.split('>')
        elif '<=' in condition:
            variable, value = condition.split('<=')
        elif '>=' in condition:
            variable, value = condition.split('>=')
        else:
            print("Invalid condition:", condition)
            return False

        variable = variable.strip()
        value = self.evaluate_expression(value.strip())

        if variable in self.variables:
            if '==' in condition:
                return self.variables[variable] == value
            elif '<' in condition:
                return self.variables[variable] < value
            elif '>' in condition:
                return self.variables[variable] > value
            elif '<=' in condition:
                return self.variables[variable] <= value
            elif '>=' in condition:
                return self.variables[variable] >= value
        else:
            print("Undefined variable:", variable)
            return False
            
    def interpret_loop(self, line):
        line = line[5:]  # Remove the 'while' keyword
        condition, loop_body = line.split(':', 1)

        condition = condition.strip()
        loop_body = loop_body.strip()

        while True:
            # Check if the condition is true
            if self.evaluate_condition(condition):
                # Execute the loop body
                for command in loop_body.split(';'):
                    command = command.strip()
                    if command:
                        self.interpret_line(command)
            else:
                break

    def print_variables(self):
        for variable, value in self.variables.items():
            print(variable, '=', value)


# Example usage
interpreter = MyLanguageInterpreter()
interpreter.run('c:/Users/kirkp/OneDrive/Documents/BSCS(3)/2nd sem/PL/input.txt')
interpreter.print_variables()
