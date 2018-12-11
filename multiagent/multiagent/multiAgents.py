#coding=utf-8
# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # create a list of old food  （当前状态的豆子数保存为列表oldFood）
        oldFood = currentGameState.getFood().asList()
        # 可用打印函数打印出oldFood，看看它的值是什么

        # set infinite values for best/worst moves  (初始化两个值：正无穷和负无穷)
        inf = float('inf')
        negInf = float('-inf')

        gPositions = []

        # iterate over ghost states
        for gState in newGhostStates:

            # get the ghost's coordinates
            gPos = gState.getPosition()
            gPositions.append(gPos)

            # if action causes you to safely eat a pellet, that's the best move（判断如果下一个动作能让你吃到豆子，且不被ghost吃掉，则返回正无穷;可用newFood和oldFood这两个列表的长度来判断是否有豆子被吃了，以及用采取吃豆子后的位置和gohost的新位置不一样，按照上面的两种判断，补全如下条件）
            if oldFood.__len__() - newFood.__len__() and newPos != gPos:
                return inf

            # if action causes you to die, that's the worst move（如果吃豆人的下一个动作会引起被幽灵吃掉，则返回一个负无穷；判断是否会被幽灵吃掉可利用吃豆人采取动作之后的位置newPos和幽灵的位置gPos是否一致）
            elif newPos == gPos and gState.scaredTimer == 0:
                return negInf

        values = []

        # iterate over new food coordinates（）
        for food in newFood:
            for gPos in gPositions:
        # get pacman's distance to a pellet and his distance to a ghost, weigh the pellets as more important，请自己定义状态的值：例如用pacman距离豆子距离的远近，越近值越大；以及pacman距离gohost的远近，越远值应该越大，可以综合考虑来定义这样的距离，补全下述函数；例如：manhattanDistance(newPos, food)表示pacman和豆子的距离
                v = manhattanDistance(newPos, gPos)\
                    / manhattanDistance(newPos, food)
                values.append(v)

        # return the optimal move


        return max(values)


        # return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def minValue(self, gameState, currentAgentIndex, curDepth):
        v = ("unknown", float("inf"))
        # 对极小值首先做一个初始化为正无穷
        # 请补全如下语句：如果没有可以再走的招数了就返回评估值，跳出循环；提示：gameState的getLegalAction函数可返回当前Agent可走的合法招数的列表

        actions = gameState.getLegalActions(currentAgentIndex)

        if not actions:  # 跳出循环选项，如果没有可以再采取的行为了就返回评估值
            return self.evaluationFunction(gameState)  # 补全：返回评估值

            # 补全如下代码：对每一个合理的行为进行评估，提示：仍然要获得当前合理的行为招数：
        for action in actions:
            if action == "Stop":
                continue

            retVal = self.value(gameState.generateSuccessor(currentAgentIndex, action),
                                currentAgentIndex + 1,
                                curDepth)  # 加深层数，递归调用
            if type(retVal) == tuple:  # 最底层返回的是评估值，其余层返回下一层的最小值。父层记录action和评估值，最底层没有子，所以没有action
                retVal = retVal[1]

            vNew = min(v[1], retVal)  # 如果存在比之间更佳合适的action，则替换v。
            if vNew != v[1]:
                v = (action, vNew)

        return v

    def maxValue(self, gameState, currentAgentIndex, curDepth):
        v = ("unknown", float("-inf"))
        # 对极小值首先做一个初始化为正无穷
        # 请补全如下语句：如果没有可以再走的招数了就返回评估值，跳出循环；提示：gameState的getLegalAction函数可返回当前Agent可走的合法招数的列表

        actions = gameState.getLegalActions(currentAgentIndex)

        if not actions:  # 跳出循环选项，如果没有可以再采取的行为了就返回评估值
            return self.evaluationFunction(gameState)  # 补全：返回评估值

            # 补全如下代码：对每一个合理的行为进行评估，提示：仍然要获得当前合理的行为招数：
        for action in actions:
            if action in ["Stop"]:
                continue

            retVal = self.value(gameState.generateSuccessor(currentAgentIndex, action),
                                currentAgentIndex + 1,
                                curDepth)  # 加深层数，递归调用
            if type(retVal) == tuple:  # 最底层返回的是评估值，其余层返回下一层的最小值。父层记录action和评估值，最底层没有子，所以没有action
                retVal = retVal[1]

            vNew = max(v[1], retVal)  # 如果存在比之间更佳合适的action，则替换v。
            if vNew != v[1]:
                v = (action, vNew)

        return v

    def value(self, gameState, currentAgentIndex, curDepth):
        if currentAgentIndex >= gameState.getNumAgents():  # 如果所有agent都计算完毕了，则本层遍历完毕，进入下一层。否则开始计算
            currentAgentIndex = 0
            curDepth += 1
        if curDepth == self.depth:  # 如果到达了规定的深度，则运行评估函数返回一个值
            return self.evaluationFunction(gameState)  # 返回值为float类型
        if currentAgentIndex == self.index:  # pacman的索引是0，如果该计算pacman的值了就调用max
            return self.maxValue(gameState, currentAgentIndex, curDepth)  # 返回值为tuple类型
        else:  # 如果是ghost的索引就调用min
            return self.minValue(gameState, currentAgentIndex, curDepth)

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        # 当前玩家为pacman （可用当前Agent的索引值来指定是哪个玩家）
        # 以及当前节点的值
        agentIndex, level = 0, 0

        # 返回当前应采取的行为, 提示：值被存储为一个二元组，第一项为“行为”，第二项为“当前的值”
        return self.value(gameState, agentIndex, level)[0]
        # util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def minValue(self, gameState, currentAgentIndex, curDepth, alpha, beta):
        v = ("unknown", float("inf"))

        actions = gameState.getLegalActions(currentAgentIndex)
        # 补全如下代码：若没有合法的行动招数，则返回当前的值
        if not actions:
            return self.evaluationFunction(gameState)

        # 补全如下代码：对每一个合理的行为进行评估，提示：仍然要获得当前合理的行为招数
        for action in actions:
            if action == "Stop":
                continue

            retVal = self.value(gameState.generateSuccessor(currentAgentIndex, action), currentAgentIndex + 1,
                                curDepth, alpha, beta)
            if type(retVal) is tuple:
                retVal = retVal[1]

            vNew = min(v[1], retVal)

            if vNew is not v[1]:
                v = (action, vNew)

            # 补全如下代码：如果当前节点的值不大于父节点的α值，则不进行继续搜索，返回当前节点
            if vNew < alpha:
                return v

            # 补全如下代码：若当前节点的值比当前的β值还小，则更新β值为当前节点的值
            beta = min(vNew, beta)

        return v

    def maxValue(self, gameState, currentAgentIndex, curDepth, alpha, beta):
        v = ("unknown", float("-inf"))

        actions = gameState.getLegalActions(currentAgentIndex)
        # 补全如下代码：若没有合法的行动招数，则返回当前的值
        if not actions:
            return self.evaluationFunction(gameState)

        # 补全如下代码：对每一个合理的行为进行评估，提示：仍然要获得当前合理的行为招数
        for action in actions:
            if action == "Stop":
                continue

            retVal = self.value(gameState.generateSuccessor(currentAgentIndex, action), currentAgentIndex + 1,
                                curDepth, alpha, beta)
            if type(retVal) is tuple:
                retVal = retVal[1]

            vNew = max(v[1], retVal)

            if vNew is not v[1]:
                v = (action, vNew)

            # 补全如下代码：如果当前节点的值不大于父节点的α值，则不进行继续搜索，返回当前节点
            if vNew > beta:
                return v

            # 补全如下代码：若当前节点的值比当前的β值还小，则更新β值为当前节点的值
            alpha = max(vNew, alpha)

        return v

    def value(self, gameState, currentAgentIndex, curDepth, alpha, beta):
        if currentAgentIndex >= gameState.getNumAgents():  # 如果所有agent都计算完毕了，则本层遍历完毕，进入下一层。否则开始计算
            currentAgentIndex = 0
            curDepth += 1
        if curDepth == self.depth:  # 如果到达了规定的深度，则运行评估函数返回一个值
            return self.evaluationFunction(gameState)  # 返回值为float类型
        if currentAgentIndex == self.index:  # pacman的索引是0，如果该计算pacman的值了就调用max
            return self.maxValue(gameState, currentAgentIndex, curDepth, alpha, beta)  # 返回值为tuple类型
        else:  # 如果是ghost的索引就调用min
            return self.minValue(gameState, currentAgentIndex, curDepth, alpha, beta)

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        agentIndex, level = 0, 0
        return self.value(gameState, agentIndex, level, float('-inf'), float('inf'))[0]
        # util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def expValue(self, gameState, currentAgentIndex, curDepth):
        v = ["unknown", 0]

        if not gameState.getLegalActions(currentAgentIndex):
            return self.evaluationFunction(gameState)

        # 补全如下代码：求执行每个行动的概率，假定当前所有可能行动的概率相等;提示：可用如下函数：len(gameState.getLegalActions(currentAgentIndex)) 获得当前可能行动的个数。

        actions = gameState.getLegalActions(currentAgentIndex)

        prob = 1.0 / len(actions)

    # 补全如下代码：对于所有可能的行动
        for action in actions:
            if action == "Stop":
                continue

            retVal = self.value(gameState.generateSuccessor(currentAgentIndex, action),
                                currentAgentIndex + 1, curDepth)

            if type(retVal) is tuple:
                retVal = retVal[1]

    # 补全如下代码：值为期望，应为值和概率的乘积
            v[1] += retVal * prob
            v[0] = action

        return tuple(v)

    def maxValue(self, gameState, currentAgentIndex, curDepth):
        v = ("unknown", float("-inf"))
        # 对极小值首先做一个初始化为正无穷
        # 请补全如下语句：如果没有可以再走的招数了就返回评估值，跳出循环；提示：gameState的getLegalAction函数可返回当前Agent可走的合法招数的列表

        actions = gameState.getLegalActions(currentAgentIndex)

        if not actions:  # 跳出循环选项，如果没有可以再采取的行为了就返回评估值
            return self.evaluationFunction(gameState)  # 补全：返回评估值

            # 补全如下代码：对每一个合理的行为进行评估，提示：仍然要获得当前合理的行为招数：
        for action in actions:
            if action in ["Stop"]:
                continue

            retVal = self.value(gameState.generateSuccessor(currentAgentIndex, action),
                                currentAgentIndex + 1,
                                curDepth)  # 加深层数，递归调用
            if type(retVal) == tuple:  # 最底层返回的是评估值，其余层返回下一层的最小值。父层记录action和评估值，最底层没有子，所以没有action
                retVal = retVal[1]

            vNew = max(v[1], retVal)  # 如果存在比之间更佳合适的action，则替换v。
            if vNew != v[1]:
                v = (action, vNew)

        return v

    def value(self, gameState, currentAgentIndex, curDepth):
        if currentAgentIndex >= gameState.getNumAgents():  # 如果所有agent都计算完毕了，则本层遍历完毕，进入下一层。否则开始计算
            currentAgentIndex = 0
            curDepth += 1
        if curDepth == self.depth:  # 如果到达了规定的深度，则运行评估函数返回一个值
            return self.evaluationFunction(gameState)  # 返回值为float类型
        if currentAgentIndex == self.index:  # pacman的索引是0，如果该计算pacman的值了就调用max
            return self.maxValue(gameState, currentAgentIndex, curDepth)  # 返回值为tuple类型
        else:  # 如果是ghost的索引就调用min
            return self.expValue(gameState, currentAgentIndex, curDepth)

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        # 当前玩家为pacman （可用当前Agent的索引值来指定是哪个玩家）
        # 以及当前节点的值
        agentIndex, level = 0, 0

        # 返回当前应采取的行为, 提示：值被存储为一个二元组，第一项为“行为”，第二项为“当前的值”
        return self.value(gameState, agentIndex, level)[0]
        # util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood().asList()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    # create a list of old food  （当前状态的豆子数保存为列表oldFood）
    oldFood = currentGameState.getFood().asList()
    # 可用打印函数打印出oldFood，看看它的值是什么

    # set infinite values for best/worst moves  (初始化两个值：正无穷和负无穷)
    inf = float('inf')
    negInf = float('-inf')

    gPositions = []

    # iterate over ghost states
    for gState in newGhostStates:

        # get the ghost's coordinates
        gPos = gState.getPosition()
        gPositions.append(gPos)

        # if action causes you to safely eat a pellet, that's the best move（判断如果下一个动作能让你吃到豆子，且不被ghost吃掉，则返回正无穷;可用newFood和oldFood这两个列表的长度来判断是否有豆子被吃了，以及用采取吃豆子后的位置和gohost的新位置不一样，按照上面的两种判断，补全如下条件）
        if oldFood.__len__() - newFood.__len__() and newPos != gPos:
            return inf

        # if action causes you to die, that's the worst move（如果吃豆人的下一个动作会引起被幽灵吃掉，则返回一个负无穷；判断是否会被幽灵吃掉可利用吃豆人采取动作之后的位置newPos和幽灵的位置gPos是否一致）
        elif newPos == gPos and gState.scaredTimer == 0:
            return negInf

    values = []

    # iterate over new food coordinates（）
    for food in newFood:
        for gPos in gPositions:
            # get pacman's distance to a pellet and his distance to a ghost, weigh the pellets as more important，请自己定义状态的值：例如用pacman距离豆子距离的远近，越近值越大；以及pacman距离gohost的远近，越远值应该越大，可以综合考虑来定义这样的距离，补全下述函数；例如：manhattanDistance(newPos, food)表示pacman和豆子的距离
            v = manhattanDistance(newPos, gPos) \
                / manhattanDistance(newPos, food)
            values.append(v)

    # return the optimal move

    return max(values)
    # util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

