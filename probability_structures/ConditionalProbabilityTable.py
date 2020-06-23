#                                                       #
#   Causal Graph                                        #
#                                                       #
#   Author: Braden Dubois (braden.dubois@usask.ca)      #
#   Written for: Dr. Eric Neufeld                       #
#                                                       #
#########################################################

# Python libraries
import numpy as np      # Used in table->str formatting
import math             # Used in table->str formatting

# Other modules of project
from probability_structures.IO_Logger import io
from probability_structures.VariableStructures import *         # The Outcome and Variable classes


class ConditionalProbabilityTable:
    """
    A basic conditional probability table that reflects the values of one Variable, and any number of conditional
    values

    :param variable: A Variable object, representing the variable this table computes a probability for
    :param given: A (possibly empty) list of Variables, representing the parents for the variable given
    :param table_rows: A list of rows in the table, each formatted as [<OUTCOME>, ["<GIVEN_1_OUTCOME>, ...], <P>]
    """

    # When outputting information, the number of digits to round to
    digits_of_probability_precision = 2

    # Padding units on the left/right sides of each cell
    padding = 1

    def __init__(self, variable: Variable, given: list, table_rows: list):
        self.variable = variable    # The LHS of the table, single-variable only
        self.given = given          # The RHS/body of the table

        self.table_rows = []

        # Clean up the rows; Each is formatted as: [outcome of variable, list of outcomes of parents, probability]
        for row in table_rows:
            self.table_rows.append([Outcome(variable.name, row[0]), row[1], float(row[2])])

    def __str__(self) -> str:
        """
        String builtin for a ConditionalProbabilityTable
        :return: A string representation of the table.
        """

        # Create a snazzy numpy table
        # Rows: 1 for a header + 1 for each row; Columns: 1 for variable, 1 for each given var, 1 for the probability
        rows = 1 + len(self.table_rows)
        columns = 1 + len(self.given) + 1

        # dtype declaration is better than "str", as str only allows one character in each cell
        table = np.empty((rows, columns), dtype='<U100')

        # Populate the first row: variable, given variables, probability
        table[0][0] = self.variable.name
        for i in range(len(self.given)):
            table[0][i+1] = self.given[i]
        table[0][table.shape[1]-1] = "P()"

        # Populate each row
        for i in range(len(self.table_rows)):
            row = self.table_rows[i]

            # Value of the given variable
            table[i+1][0] = row[0].outcome

            # Each given variable's value
            for given_idx in range(len(row[1])):
                table[i+1][1+given_idx] = row[1][given_idx]

            # The probability, to some modifiable number of digits
            table[i+1][table.shape[1]-1] = "{0:.2f}".format(row[2])

        # Wiggle/Padding, column by column
        for column_index in range(1 + len(self.given) + 1):
            widest_element = max([len(cell) for cell in table[:, column_index]])
            for row_index in range(1 + len(self.table_rows)):
                cell_value = table[row_index][column_index]
                l_padding = math.ceil((widest_element - len(cell_value) / 2)) * " " + " " * self.padding
                r_padding = math.floor((widest_element - len(cell_value) / 2)) * " " + " " * self.padding
                table[row_index][column_index] = l_padding + cell_value + r_padding

        # Convert to fancy string
        string_list = ["|" + "|".join(row) + "|" for row in table]
        top_bottom_wrap = "-" * len("|" + "|".join(table[0]) + "|")
        string_list.insert(1, top_bottom_wrap)

        return top_bottom_wrap + "\n" + "\n".join(string_list) + "\n" + top_bottom_wrap

    def __eq__(self, other) -> bool:
        """
        Equality builtin for a ConditionalProbabilityTable
        :param other: Another ConditionalProbabilityTable to compare to
        :return:
        """
        if isinstance(other, ConditionalProbabilityTable):
            return self.variable == other.variable and set(self.given) == set(other.given)
        else:
            return False

    def probability_lookup(self, outcome: list, given: set) -> float:
        """
        Directly lookup the probability for the row corresponding to the queried outcome and given data
        :param outcome: The specific outcome to lookup
        :param given: A set of [<VARIABLE>, <OUTCOME>] sub-lists of known data
        :return: A probability corresponding to the respective row. Raises an Exception otherwise.
        """
        for row in self.table_rows:
            # If the outcome for this row matches, and each outcome for the given data matches...
            if outcome[0] == row[0] and set(row[1]) == given:
                return row[2]       # We have our answer

        # Iterated over all the rows and didn't find the correct one
        io.write("Couldn't find row:", str([str(item) for item in outcome]), str([str(item) for item in given]))
        raise Exception