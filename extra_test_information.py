import javalang
from javalang.ast import Node

class varibale:
    pass

def process_node(node):
    if isinstance(node, Node):
        # 检查是否是本地变量声明
        if node.__class__.__name__ == 'LocalVariableDeclaration':
            # 处理变量声明的内容
            for variable_declarator in node.declarators:
                variable_name = variable_declarator.name
                # 在这里进行你想要的操作
                print("Variable Name: ", variable_name)

        # 递归处理子节点
        for child_node in node.children:
            process_node(child_node)


# 处理方法调用
def process_method_invocation(tem):
    pass


# 被调用功能数加一
def addFunctionNumber(fun, funs, variable_set_con):
    if fun not in variable_set_con:
        if fun not in funs:
            funs[fun] = 1
        else:
            funs[fun] = funs[fun] + 1
    return funs

#method diaoyong
#yanzheng
def extra_javafile_information(path, no_list, production):
    variable_set = {}  # bianliang
    method_invocation_set = {}
    sps_funs = []
    fd = open(path, "r", encoding="utf-8")  #读取Java源代码
    tree = javalang.parse.parse(fd.read())               # 根据源代码解析出一颗抽象语法树
    # 遍历AST中的节点
    process_node(tree)
    classes = []
    # types以class为分割一个class一个type
    # 成员变量
    i = 0

    ver_set = ["assertTrue", "assertFalse", "assertEquals", "assertSame", "assertNotSame", "assertNotNull", "assertNull"]
    variable_set_con = ['int', 'boolean', 'float', 'complex', 'String', 'long']

    for f in tree.types[0].methods:
        if f.name in no_list:
            funs_in_ver_set = {}
            funs_not_in_ver_set = {}
            # 记录局部变量与函数间的关系
            variable_about_fun = {}
            #variable_type = {}
            # 记录变量作为参数被调用在函数中的情况

            for child in f.body:
                # if production == "_MultipleBugs_.NOB_1.ID_323":
                #     print(child)
                if child.__class__.__name__ == 'LocalVariableDeclaration':   #局部变量声明
                    # 处理变量声明的内容
                    for variable_declarator in child.declarators:
                        variable_name = variable_declarator.name
                        variable_member = variable_declarator.initializer
                        variable_type = child.type.name
                        # print("局部变量声明:", variable_name, variable_member, variable_type)
                        variable_about_fun[variable_name] = set()   #连接局部变量与函数
                        variable_about_fun[variable_name].add(variable_type)
                        if variable_type not in variable_set_con:
                            if variable_type not in funs_in_ver_set:
                                funs_in_ver_set[variable_type] = 1
                                funs_not_in_ver_set[variable_type] = 1
                            else:
                                funs_in_ver_set[variable_type] = funs_in_ver_set[variable_type] + 1
                                funs_not_in_ver_set[variable_type] = funs_not_in_ver_set[variable_type] + 1
                        variable_member_name = ""
                        if variable_member.__class__.__name__ == 'MethodInvocation':  #方法调用
                            variable_member_name = variable_member.member
                            reference_members = []
                            # print("方法调用: ", variable_member)
                            variable_about_fun[variable_name].add(variable_member_name)
                            for mr in variable_member.arguments:
                                if mr.__class__.__name__ == 'MemberReference':
                                    if mr.qualifier is not "" and mr.qualifier in variable_about_fun:
                                        variable_about_fun[mr.qualifier].add(variable_member_name)
                                    else:
                                        if mr.member not in variable_about_fun:
                                            variable_about_fun[mr.member] = set()
                                        variable_about_fun[mr.member].add(variable_member_name)
                                    reference_members.append(mr.member)
                                elif mr.__class__.__name__ == 'Cast':
                                    expression = mr.expression
                            if variable_member_name not in method_invocation_set:
                                if variable_set.get(variable_member.qualifier) is "":
                                    method_invocation_set[variable_name] = str(variable_member.qualifier) + "." + str(variable_member_name)
                                    if variable_member_name not in variable_set_con:
                                        if variable_member_name not in funs_not_in_ver_set:
                                            funs_not_in_ver_set[variable_member_name] = 1
                                        else:
                                            funs_not_in_ver_set[variable_member_name] = funs_not_in_ver_set[variable_member_name] + 1
                                else:
                                    method_invocation_set[variable_name] = str(
                                        variable_set.get(variable_member.qualifier)) + "." + str(variable_member_name)
                                    if variable_member_name not in variable_set_con:
                                        if variable_member_name not in funs_not_in_ver_set:
                                            funs_not_in_ver_set[variable_member_name] = 1
                                        else:
                                            funs_not_in_ver_set[variable_member_name] = funs_not_in_ver_set[variable_member_name]  + 1
                                        # funs.append(str(variable_member_name))  #str(variable_set.get(variable_member.qualifier)) + "." +
                                variable_set[variable_name] = variable_type
                                if str(variable_set.get(variable_member.qualifier)) not in classes:
                                    classes.append(str(variable_set.get(variable_member.qualifier)))
                        elif variable_member.__class__.__name__ == 'ClassCreator':

                            if variable_name not in variable_set.keys():
                                variable_set[variable_name] = variable_type
                                #print("New Class: ", variable_type, variable_name)
                        elif variable_member.__class__.__name__ == 'ArrayCreator':
                            if variable_member.dimensions[0].value not in variable_set.keys():
                                variable_set[variable_member.dimensions[0].value] = variable_member.type.name
                        elif variable_member.__class__.__name__ == 'MemberReference':
                                reference_members = []
                                reference_members.append(variable_member.member)
                        else:
                            # print("aaaaaa:", variable_member.__class__.__name__, child)
                            pass

                elif child.__class__.__name__ == 'StatementExpression':   #语句表达
                    expression = child.expression
                    # print("语句表达:", child)
                    if expression.__class__.__name__ == 'MethodInvocation':
                        state_fun = expression.member
                        state_class = expression.qualifier
                        reference_members = []
                        reference_methods = []
                        if state_class not in variable_about_fun:
                            variable_about_fun[state_class] = set()
                        variable_about_fun[state_class].add(state_fun)
                        if state_fun in ver_set:
                            for mr in expression.arguments:
                                # 如果传入的是函数，直接添加；若为变量，添加其对应函数

                                #方法调用
                                if mr.__class__.__name__ == 'MethodInvocation':
                                    # 可疑函数
                                    # print("可疑函数:", mr.member, state_fun)
                                    funs_in_ver_set = addFunctionNumber(mr.member, funs_in_ver_set, variable_set_con)
                                elif mr.__class__.__name__ == 'Literal':
                                    pass
                                elif mr.__class__.__name__ == 'MemberReference':
                                    # 调用参数，参数相关的所有函数
                                    if mr.qualifier is not "" and mr.qualifier in variable_about_fun:
                                        for fun in variable_about_fun[mr.qualifier]:
                                            # print("fun是11:", fun)
                                            funs_in_ver_set = addFunctionNumber(fun, funs_in_ver_set, variable_set_con)
                                    else:
                                        # print("2222:", mr.member, mr.qualifier)
                                        if mr.member not in variable_about_fun:
                                            variable_about_fun[mr.member] = set()
                                        else:
                                            if len(variable_about_fun[mr.member]) != 0:
                                                for fun in variable_about_fun[mr.member]:
                                                    funs_in_ver_set = addFunctionNumber(fun, funs_in_ver_set, variable_set_con)
                        else:
                            # print("fansile", expression)
                            for mr in expression.arguments:
                                if mr.__class__.__name__ == 'MemberReference':
                                    reference_members.append(mr.member)
                                    if mr.qualifier is not "" and mr.qualifier in variable_about_fun:
                                        variable_about_fun[mr.qualifier].add(mr.member)
                                    else:
                                        if mr.member not in variable_about_fun:
                                            variable_about_fun[mr.member] = set()
                                        variable_about_fun[mr.member].add(mr.member)
                                elif mr.__class__.__name__ == 'MethodInvocation':
                                    if variable_set.get(mr.qualifier) != None:
                                        reference_methods.append(str(mr.member))
                                        variable_about_fun[mr.qualifier].add(mr.member)
                                elif mr.__class__.__name__ == 'Cast':
                                    new_expression = mr.expression
                                elif mr.__class__.__name__ == 'Literal':
                                    if expression.qualifier is not "" and expression.qualifier in variable_about_fun:
                                        variable_about_fun[expression.qualifier].add(expression.member)
                                    elif expression.qualifier not in variable_about_fun:
                                        variable_about_fun[expression.qualifier] = set()
                                        variable_about_fun[expression.qualifier].add(expression.member)
                            if variable_set.get(expression.qualifier) == None:
                                if expression.qualifier != None:
                                    if state_fun not in variable_set_con:
                                        if state_fun not in funs_not_in_ver_set:
                                            funs_not_in_ver_set[state_fun] = 1
                                        else:
                                            funs_not_in_ver_set[state_fun] = funs_not_in_ver_set[state_fun] + 1
                                        # funs.append(str(state_fun)) #str(expression.qualifier) + "." +
                                    # print("haliduya:", str(expression.qualifier) + "." + str(state_fun), expression)

                            else:
                                method_invocation_set[expression.qualifier] = str(
                                    variable_set.get(expression.qualifier)) + "." + str(state_fun)
                                if state_fun not in variable_set_con:
                                    if state_fun not in funs_not_in_ver_set:
                                        funs_not_in_ver_set[state_fun] = 1
                                    else:
                                        funs_not_in_ver_set[state_fun] = funs_not_in_ver_set[state_fun] + 1
                            if len(reference_methods) > 0:
                                for rm in reference_methods:
                                    if rm not in variable_set_con:
                                        if rm not in funs_not_in_ver_set and rm not in variable_set.keys() and rm not in method_invocation_set.keys():
                                            funs_not_in_ver_set[rm] = 1
                                        else:
                                            funs_not_in_ver_set[rm] = funs_not_in_ver_set[rm] + 1
                    elif expression.__class__.__name__ == 'Assignment':
                        if expression.value.__class__.__name__ == 'Literal':
                            pass
                        elif expression.value.__class__.__name__ == 'MemberReference':
                            pass
                    else:
                        print("bbbbbbb:", expression.__class__.__name__)
                elif child.__class__.__name__ == 'TryStatement':
                    # 如果是验证异常
                    for statement in child.block:
                        expression = statement.expression
                        # print("语句表达:", child)
                        if expression.__class__.__name__ == 'MethodInvocation':
                            state_fun = expression.member
                            funs_in_ver_set = addFunctionNumber(state_fun, funs_in_ver_set, variable_set_con)
                            if state_fun in ver_set:
                                for mr in expression.arguments:
                                    # 如果传入的是函数，直接添加；若为变量，添加其对应函数
                                    if state_fun is not "assertEquals":
                                        # 方法调用
                                        if mr.__class__.__name__ == 'MethodInvocation':
                                            # 可疑函数
                                            pass
                                        elif mr.__class__.__name__ == 'Literal':
                                            funs_in_ver_set = addFunctionNumber(state_fun, funs_in_ver_set, variable_set_con)
                                        elif mr.__class__.__name__ == 'MemberReference':
                                            # 调用参数，参数相关的所有函数
                                            if mr.qualifier is not "" and mr.qualifier in variable_about_fun:
                                                for fun in variable_about_fun[mr.qualifier]:
                                                    print("fun是333:", fun)
                                                    funs_in_ver_set = addFunctionNumber(fun, funs_in_ver_set, variable_set_con)
                                            else:
                                                if mr.member not in variable_about_fun:
                                                    variable_about_fun[mr.member] = set()
                                                for fun in variable_about_fun[mr.member]:
                                                    print("fun是444:", fun)
                                                    funs_in_ver_set = addFunctionNumber(fun, funs_in_ver_set, variable_set_con)
                            else:
                                for mr in expression.arguments:
                                    if mr.__class__.__name__ == 'MemberReference':
                                        if mr.qualifier is not "" and mr.qualifier in variable_about_fun:
                                            variable_about_fun[mr.qualifier].add(expression.member)
                                            for fun in variable_about_fun[mr.qualifier]:
                                                print("fun是555:", fun)
                                                funs_in_ver_set = addFunctionNumber(fun, funs_in_ver_set, variable_set_con)
                                        else:
                                            variable_about_fun[mr.member].add(expression.member)
                                            for fun in variable_about_fun[mr.member]:
                                                # print("fun是666:", fun)
                                                funs_in_ver_set = addFunctionNumber(fun, funs_in_ver_set, variable_set_con)
                                    elif mr.__class__.__name__ == 'Cast':
                                        new_expression = mr.expression

                        elif expression.__class__.__name__ == 'Assignment':
                            if expression.value.__class__.__name__ == 'Literal':
                                pass
                            elif expression.value.__class__.__name__ == 'MemberReference':
                                pass
                        else:
                            print("bbbbbbb:", expression.__class__.__name__)

                    for statement in child.catches:
                        for statement in statement.block:
                            if statement.__class__.__name__ == 'StatementExpression':
                                expression = statement.expression
                                if expression.__class__.__name__ == 'MethodInvocation':
                                    state_fun = expression.member
                                    state_class = expression.qualifier
                                    reference_members = []
                                    for mr in expression.arguments:
                                        if mr.__class__.__name__ == 'MemberReference':
                                            reference_members.append(mr.member)
                                    if state_fun == "verifyException":
                                        state_class = expression.arguments[0].value
                                    pass
                                elif expression.__class__.__name__ == 'Assignment':
                                    if expression.value.__class__.__name__ == 'Literal':
                                        pass
                                    elif expression.value.__class__.__name__ == 'MemberReference':
                                        pass
                                else:
                                    print("bbbbbbb:", expression.__class__.__name__)
                else:
                    print("dddddd", child.__class__.__name__)
            # print("mmmmmmmmmmmm:", variable_about_fun)
            # if len(funs_in_ver_set) == 0:
            sps_funs.append(funs_not_in_ver_set)
            # else:
            #     sps_funs.append(funs_in_ver_set)

        #i = i + 1
    return variable_set, method_invocation_set, sps_funs