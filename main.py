import sys

class CycleDetectedError(Exception):
    pass

class SpreadSheetCalc:
    def __init__(self):
        # dictionary to map cell names to their raw expressions
        self.cell_expressions = {}

    # Process Reverse Polish Notation (RPN) expression
    def process_rpn_expression(self, expression_parts, computed_values, visited_cells):
        stack = []
        for part in expression_parts:
            # Numbers and negative numbers
            if part.isdigit() or (part[0] == '-' and part[1:].isdigit()):
                stack.append(float(part))
            elif part in computed_values:  # Already computed cell
                stack.append(computed_values[part])
            elif part[0].isalpha() and part[1:].isdigit():  # Cell reference for A1, A2, .... B1, B2...
                if part in visited_cells:  # Check for cycles
                    raise CycleDetectedError(f"Cycle detected at cell {part}")
                stack.append(self.evaluate_single_cell(part, computed_values, visited_cells))
            elif part in ['+', '-', '*', '/']:  # Binary Operators so pop two operands
                b = stack.pop()
                a = stack.pop()
                if part == '+':
                    stack.append(a + b)
                elif part == '-':
                    stack.append(a - b)
                elif part == '*':
                    stack.append(a * b)
                elif part == '/':
                    stack.append(a / b)
            elif part == '++':  # Increment operator
                value = stack.pop()
                stack.append(value + 1)
            elif part == '--':  # Decrement operator
                value = stack.pop()
                stack.append(value - 1)
            else:
                raise ValueError(f"Unknown operator or value: {part}")
        
        return stack.pop()

    # Function to evaluate a single cell
    def evaluate_single_cell(self, cell_name, computed_values, visited_cells):
        visited_cells.add(cell_name)  # Mark this cell as being evaluated
        expression = self.cell_expressions[cell_name].split()
        result = self.process_rpn_expression(expression, computed_values, visited_cells)
        computed_values[cell_name] = result
        visited_cells.remove(cell_name)  # Done evaluating
        return result

    # Function to compute all cell values, with cycle detection
    def compute_all_cell_values(self, width, height):
        computed_values = {}
        # To track cells being evaluated/visited
        visited_cells = set()

        for row in range(height):
            for col in range(width):
                # A1, B2, etc...
                cell_name = f'{chr(65 + row)}{col + 1}'
                if cell_name not in computed_values:
                    try:
                        self.evaluate_single_cell(cell_name, computed_values, visited_cells)
                    except CycleDetectedError as e:
                        print(f"Error: {str(e)}")
                        # Non-zero exit code for cyclic dependency
                        sys.exit(1)
        
        return computed_values

def main():
    input_data = sys.stdin.read().splitlines()

    # Read the first line to get width and height
    width_height = input_data[0].split()
    no_of_cols = int(width_height[0])
    no_of_rows = int(width_height[1])

    # Sanity checks for input values of number of rows and cols
    if no_of_cols < 0 or no_of_rows < 0:
        print(f"Error: Number of rows or columns cannot be negative.")
        sys.exit(2)

    # Create the SpreadSheet Calculator Object
    ss_calc_obj = SpreadSheetCalc()

    # Read each cells expression
    input_idx = 1
    for row in range(no_of_rows):
        for col in range(no_of_cols):
            # A1, B2, etc.. [row computed using ASCII computation]
            cell_name = f'{chr(65 + row)}{col + 1}' 
            ss_calc_obj.cell_expressions[cell_name] = input_data[input_idx]
            input_idx += 1
        
        '''
        cell_expressions = {
                "A1": "A2"
                "A2": "4 5 *"
                "A3": "A1"
                "B1": "A1 B2 / 2 +"
                "B2": "3"/ "B2"
                "B3": "39 B1 B2 * /"
        }
        '''

    # Compute all the cell values
    evaluated_values = ss_calc_obj.compute_all_cell_values(no_of_cols, no_of_rows)

    # Output the result in the required format
    print(f"{no_of_cols} {no_of_rows}")
    for row in range(no_of_rows):
        for col in range(no_of_cols):
            cell_name = f'{chr(65 + row)}{col + 1}'
            print(f"{evaluated_values[cell_name]:.5f}")

if __name__ == "__main__":
    main()


'''
Time Complexity:
Avg Length of Cell Expression: L_Avg
Total cells = N*M 
Time to evaluate single cell using RPN = O(L_Avg)

O(N*M * O(1))
O(N*M * O(L_Avg))

Space Complexity:
Size of expression -> O(L_Avg)
O(N*M) => cell_expressions -> to store all cell data

Worst case: O(N*M*<L_Avg>)
'''