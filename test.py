import unittest
from main import SpreadSheetCalc

# Create the SpreadSheet Calculator Object
ss_calc_obj = SpreadSheetCalc()

class TestSpreadSheetCalc(unittest.TestCase):

    def test_process_rpn_expression(self):

        self.cell_expressions = {
            "A1": "4 5 *",
            "A2": "A1"
        }

        expression = self.cell_expressions["A1"].split()
        self.computed_values = {}
        self.visited_cells = set()

        # Test Case
        self.assertEqual(ss_calc_obj.process_rpn_expression(expression, self.computed_values, self.visited_cells), 20)

if __name__ == '__main__':
    unittest.main()