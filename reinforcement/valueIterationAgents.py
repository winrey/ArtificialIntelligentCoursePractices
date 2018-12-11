# coding=utf-8
# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent


class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        currIterations = 0

        # 利用循环语句实施值迭代：请补全如下代码：当currIterations的值小于最大迭代值时
        while currIterations < iterations:
            # 初始化一个计数器来跟踪每次迭代时的值，注意可利用util.Counter()函数
            allVals = util.Counter()

            # 请补全如下代码：获得状态：提示可采用mdp中的函数
            possStates = mdp.getStates()

            for state in possStates:
                # 补全如下代码：如果当前状态是非终止状态(可用mdp相关函数来判断)，则不要迭代，否则计算
                if not mdp.isTerminal(state):
                    # initialize counter for getting values from the current state
                    vals = util.Counter()
                    # 补全如下代码：获得当前状态下可能的行为 （可用mdp相关函数来判断）
                    possActions = mdp.getPossibleActions(state)
                    # iterate over actions and get their qvalues
                    for action in possActions:
                        vals[action] = self.computeQValueFromValues(state, action)
                    # 为该状态和行为获得最佳看见的值
                    allVals[state] = max(vals.values())

            currIterations += 1
            # 补全如下代码：使用最好的值更新策略
            self.values = allVals

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # 补全代码：获得由当前状态可能转移到的状态和转移概率（可利用mdp的相关函数）
        stateProbPairs = self.mdp.getTransitionStatesAndProbs(state, action)
        # 初始化值为0
        actVal = 0
        # 计算Q值（用到mdp获得回报的函数）
        for pair in stateProbPairs:
            # compute q-value
            actVal += pair[1] * (self.mdp.getReward(state, action, pair[0]) + self.discount * self.values[pair[0]])

        # 补全代码：返回值
        return actVal
        # util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # 提示：首先判断是否是终止状态，若是则返回None
        if self.mdp.isTerminal(state):
            return None
        # 补全代码：获得当前状态所有合法的行为（提示：可用mdp的相关函数实现），若无合法行为则返回None

        actions = self.mdp.getPossibleActions(state)
        if len(actions) == 0:
            return None

        # initialize a counter to hold our values
        values = util.Counter()

        # 补全代码：遍历每个可能的动作并计算q-value （提示：可利用上述计算Q值的函数）
        for action in actions:
            values[action] = self.getQValue(state, action)

        # return the best action
        return values.argMax()
        # util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
