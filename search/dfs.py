    search_struct = util.Stack()
    successors = problem.getSuccessors(problem.getStartState())

    path_actions = []

    for ea in successors:
        search_struct.push(ea)

    find_goal = False

    visited_pos = set()
    visited_pos.add(problem.getStartState())

    # 开始遍历：如果栈不空，且没有到达目标结点(请填充如下两个条件)：
    while (not search_struct.isEmpty()) and (not find_goal):
        choice = search_struct.pop()
        if not problem.isGoalState(choice[0]):
            # 如果该节点没被访问
            if not choice[0] in visited_pos:
                visited_pos.add(choice[0])
                path_actions.append(choice)
            # filter的意思是对sequence中的所有item依次执行 function(item)
            choice_successors = filter(lambda v: v[0] not in visited_pos, problem.getSuccessors(choice[0]))

            if not len(choice_successors):
                path_actions.pop(-1)
                if path_actions:
                    search_struct.push(path_actions[-1])
            else:
                for ea in choice_successors:
                    search_struct.push(ea)
        else:
            path_actions.append(choice)
            visited_pos.add(choice[0])
            find_goal = True

    return [ea[1] for ea in path_actions]