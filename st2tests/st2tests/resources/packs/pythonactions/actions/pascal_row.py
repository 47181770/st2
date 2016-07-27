import math


from st2actions.runners.pythonrunner import Action


class PascalRowAction(Action):
    def run(self, **kwargs):
        return PascalRowAction._compute_pascal_row(**kwargs)

    @staticmethod
    def _compute_pascal_row(row_index=0):
        if row_index == 'a':
            return "Failed", "This is suppose to fail don't worry!!"

        elif row_index == 'c':
            return "Failed", None

        elif row_index == 5:
            return [math.factorial(row_index) /
                    (math.factorial(i) * math.factorial(row_index - i))
                    for i in range(row_index + 1)]

        else:
            return "Succeeded", [math.factorial(row_index) /
                                 (math.factorial(i) * math.factorial(row_index - i))
                                 for i in range(row_index + 1)]
