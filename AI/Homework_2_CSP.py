import copy


# 课程
class Course:
    def __init__(self, name="", avaiable_teachers={}, time={}):
        self.name = name
        self.avaiable_teachers = avaiable_teachers
        self.time = time
        self.avaiable_assignments = set()
        for t in avaiable_teachers:
            for d in Course.avaiable_days:
                self.avaiable_assignments.add((t, d))
        self.assignment = None

    avaiable_days = {"monday", "wednesday", "friday"}

    def assign(self, assignment):
        self.assignment = assignment
        self.avaiable_assignments = None

    def __str__(self):
        return self.name + " assignment:" + str(self.assignment)


# 把上课时间拆分成每半个小时，方便后续计算约束
course_1 = Course("计算机编程简介", {"A", "C"}, {"8:00-8:30AM", "8:30-9:00AM"})
course_2 = Course("人工智能导论", {"A"}, {"8:30-9:00AM", "9:00-9:30AM"})
course_3 = Course("软件工程", {"B", "C"}, {"9:00-9:30AM", "9:30-10:00AM"})
course_4 = Course("计算机视觉", {"B", "C"}, {"9:00-9:30AM", "9:30-10:00AM"})
course_5 = Course("机器学习", {"A"}, {"10:30-11:00AM", "11:00-11:30AM"})

courses = [course_1, course_2, course_3, course_4, course_5]


# 课程安排的状态，方便进行回溯搜索
class AssignmentState:

    def __init__(self, courses={}):
        self.courses = courses

    # 是否已经成功排课了
    def all_assigned(self):
        all_assigned = True
        for course in self.courses:
            if course.assignment is None:
                all_assigned = False
                break
        return all_assigned

    # 找到课程安排对象中的课程对象。注意：，因为有很多个课程安排对象，所以每个课程会有很多个对象，它们的assignment和avaiable_assignments都不一样
    def find_course_by_name(self, course_name):
        for course in self.courses:
            if course.name == course_name:
                return course

    # 按照rv排序，从而实现mrv
    def list_courses_by_rv(self):
        courses_list = dict()
        for course in self.courses:
            if course.assignment != None:
                continue
            rv = len(course.avaiable_assignments)
            courses_list[course] = rv
        return sorted(courses_list.items(), key=lambda x: x[1])

    # 按照cv排序从而实现lcv
    def list_value_by_cv(self, course):
        value_list = dict()
        for value in course.avaiable_assignments:
            cv = 0
            for another_course in self.courses:
                if course == another_course:
                    continue
                if another_course.assignment is not None:
                    continue
                if value in another_course.avaiable_assignments and len(course.time & another_course.time) > 0:
                    # 这里就是在判断约束
                    cv += 1
            value_list[value] = cv
        return sorted(value_list.items(), key=lambda x: x[1])

    # 最简单的前向检查
    def forword_checking(self, course, assignment):
        for another_course in self.courses:
            if course == another_course:
                continue
            if another_course.assignment is not None:
                continue
            if assignment in another_course.avaiable_assignments and len(course.time & another_course.time) > 0:
                # 移除违反约束的值
                another_course.avaiable_assignments.remove(assignment)
                if len(another_course.avaiable_assignments) == 0:
                    return False
        return True

    def print(self):
        print("-------------------------------")
        for c in curr_state.courses:
            print(c)
        print("-------------------------------")


# 搜索前沿。
frige = list()

# 搜索的当前状态
curr_state = AssignmentState(courses)

while curr_state.all_assigned() == False:
    courses_list = curr_state.list_courses_by_rv()
    for course, rv in courses_list:
        value_list = curr_state.list_value_by_cv(course)
        assigned_succ = False
        # 当前搜索节点入栈，接下来就要对这个节点进行扩展了
        frige.append(curr_state)
        for value, cv in value_list:
            # 当前搜索节点入栈，接下来就要对这个节点进行扩展了
            frige.append(curr_state)
            # 这个deepcopy很重要，请参阅面向对象相关文章
            curr_state = copy.deepcopy(curr_state)
            course = curr_state.find_course_by_name(course.name)
            course.assign(value)
            still_possiable = curr_state.forword_checking(course, value)
            if still_possiable:
                # 赋值成功，跳出双重循环
                assigned_succ = True
                break
            else:
                # 赋值失败，回溯
                curr_state = frige.pop()
        if assigned_succ:
            # 赋值成功，跳出循环
            break
        else:
            # 赋值失败，回溯
            curr_state = frige.pop()
if curr_state.all_assigned() == True:
    print("Find csp solution!")
    curr_state.print()
