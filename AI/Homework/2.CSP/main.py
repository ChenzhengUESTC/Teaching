# 请加入注释...
class Variable:
    # 请加入注释...
    def __init__(self, name, range):
        self.name = name
        self.range = range


# 请加入注释...
class Constraint:
    # 请加入注释...
    def __init__(self, constraint):
        self.constraint = constraint

    # 请加入注释...
    def __eq__(self, other):
        if not isinstance(other, Constraint):
            # don't attempt to compare against unrelated types
            return NotImplemented

        if self.constraint[0] == other.constraint[0] and self.constraint[1] == other.constraint[1]:
            return True
        if self.constraint[0] == other.constraint[1] and self.constraint[1] == other.constraint[0]:
            return True
        return False


# 请加入注释...
class Assignment:
    # 请加入注释...
    def __init__(self):
        self.assignments = dict()

    # 请加入注释...
    def assign(self, var, value):
        self.assignments[var] = value

    # 请加入注释...
    def remove(self, var, value):
        self.assignments.pop(var)

    # 请加入注释...
    def get_assigned_value(self, var):
        return self.assignments[var]

    # 请加入注释...
    def __str__(self):
        str = ""
        for key in self.assignments.keys():
            str += key.name + ": [" + ' '.join(self.assignments[key]) + "]\n"
        return str


# 请加入注释...
class Csp_Problem:
    # 请加入注释...
    def __init__(self, variables, constraints):
        self.variables = variables
        self.constraints = constraints

    # 请加入注释...
    def is_complete(self, assignment):
        for var in self.variables:
            if var not in assignment.assignments.keys():
                return False
        return True

    # 请加入注释...
    def select_unassigned_variable(self, assignment):
        for var in self.variables:
            if var not in assignment.assignments.keys():
                return var

    # 请加入注释...
    def is_consistent(self, var, value, assignment):
        for assigned_var in assignment.assignments:
            if Constraint((assigned_var, var)) in self.constraints and value == assignment.get_assigned_value(
                    assigned_var):
                return False
        return True


# 请加入注释...
def backtracking_search(csp_problem):
    return recursive_backtracking(Assignment(), csp_problem)


# 请加入注释...
def recursive_backtracking(assignment, csp_problem):
    # 请加入注释...
    if csp_problem.is_complete(assignment):
        return assignment
    # 请加入注释...
    var = csp_problem.select_unassigned_variable(assignment)
    # 请加入注释...
    for value in var.range:
        # 请加入注释...
        if csp_problem.is_consistent(var, value, assignment):
            # 请加入注释...
            assignment.assign(var, value)
            # 请加入注释...
            result = recursive_backtracking(assignment, csp_problem)
            # 请加入注释...
            if result != "failure":
                return result
            # 请加入注释...
            assignment.remove(var, value)
    return "failure"


if __name__ == '__main__':
    # 请加入注释...
    variables = list()
    # 请加入注释...
    class_计算机编程简介 = Variable("计算机编程简介",
                             [["教师A", "周一"], ["教师A", "周三"], ["教师A", "周五"], ["教师C", "周一"], ["教师C", "周三"], ["教师C", "周五"]])
    class_人工智能导论 = Variable("人工智能导论", [["教师A", "周一"], ["教师A", "周三"], ["教师A", "周五"]])
    class_软件工程 = Variable("软件工程",
                          [["教师B", "周一"], ["教师B", "周三"], ["教师B", "周五"], ["教师C", "周一"], ["教师C", "周三"], ["教师C", "周五"]])
    class_计算机视觉 = Variable("计算机视觉",
                           [["教师B", "周一"], ["教师B", "周三"], ["教师B", "周五"], ["教师C", "周一"], ["教师C", "周三"], ["教师C", "周五"]])
    class_机器学习 = Variable("机器学习",
                          [["教师A", "周一"], ["教师A", "周三"], ["教师A", "周五"], ["教师B", "周一"], ["教师B", "周三"], ["教师B", "周五"]])

    # 请加入注释...
    variables.append(class_计算机编程简介)
    variables.append(class_人工智能导论)
    variables.append(class_软件工程)
    variables.append(class_计算机视觉)
    variables.append(class_机器学习)

    # 请加入注释...
    constraints = list()
    # 请加入注释...
    constraints.append(Constraint((class_计算机编程简介, class_人工智能导论)))
    constraints.append(Constraint((class_人工智能导论, class_软件工程)))
    constraints.append(Constraint((class_人工智能导论, class_计算机视觉)))
    constraints.append(Constraint((class_软件工程, class_计算机视觉)))

    # 请加入注释...
    csp_problem = Csp_Problem(variables, constraints)

    # 请加入注释...
    print(backtracking_search(csp_problem))
