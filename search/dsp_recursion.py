visited_pos = []

    def search(point):
        if problem.isGoalState(point):
            return True, []
        if point in visited_pos:
            return False, []
        visited_pos.append(point)
        successors = problem.getSuccessors(point)
        for s in successors:
            r, a = search(s[0])
            if r:
                return True, [s[1]] + a
        return False, []

    r, p = search(problem.getStartState())
    return p