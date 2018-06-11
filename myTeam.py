# myTeam.py
# ---------
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


from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util, sys
from game import Directions
import game
from util import nearestPoint
import pickle
import sys
sys.path.append('teams/Ace/')

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first= 'MonteCarloAggressiveAgent', second= 'MonteCarloProtectingAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Active Agents
# Monte Carlo Offensive
# Monte CArlo Defensive
# Inactive Agents - Commented
# Qlearning Offensive
# Expectimax Defensive #
##########


##########
# Implementers
# Manoj Kumar Reddy Lingala ,886517
# Mark Wilson, 797899
# Tanvi Bali ,838130 #
##########
class MonteCarloAggressiveAgent(CaptureAgent):

    """
        This will Find the next successor (next_succ) which is a grid position . We take some help from the baseline
        Team to implement the getSuccessor , getFeatures and weights
    """

    def getSuccessor(self, gameState, action):
        next_succ = gameState.generateSuccessor(self.index, action)
        my_position = next_succ.getAgentState(self.index).getPosition()
        if my_position == nearestPoint(my_position):
            return next_succ
        else:
            return next_succ.generateSuccessor(self.index, action)

    def getFeatures(self, gameState, action):
        f = util.Counter()  # Where f is our features
        next_succ = self.getSuccessor(gameState, action)  # next_succ is the successor
        """
        next_succ is obtained from the getSuccessor and find my position with respect to the Ghost


         One sample layout for the position of Ghost and the Pacman
         %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
         %.   %.%..          %.%.%  %  %  %
         %    %.%%%%% %%%% % ..  .     %  %
         %  %   %.%       %% %%%%%%%%     %
         %  % % %.   %% %%      %  .%% %  %
         % %% % % %%    %     %   %.%..%%.%
         %  %  .%    %% % %%.%%%%%%%%%%%  %
         %  %% %% %% %  %     %..% > %.% %%
         % %%   % %. % %%  %  % %% %   %  %
         %  %   % %% %  %  %% % .% %  .%% %
         %% %.%   %..%     %  % %% %% %%  %
         %  %%%%%%%%%%% %% % %%    %.  %  %
         % %%..%.%   %     %    %% % % %% %
         %  % %%.  %      %% %%    % % %. %
         %     %%%%%%%% %%      .%.%   %  %
         %  %           % %%%% %%%%%.%G   %
         %  %  %  %.%.%G <       ..%.%   .%
         %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        """
        # DETERMINE FEATURE 1
        # From getFeatures our task is to just obtain 4 features which are
        # nextsuccScore , foodDistance, isPacman, ghostDistance
        f['nextsuccScore'] = self.getScore(next_succ)
        # In Monte Carlo Implementation Everything depends on the next_succ obtained here. All
        # our features (remaining features) are obtained with respect to the next_succ obtained .
        # Our next task is to find the foodDistance

        # DETERMINE FEATURE 2
        List_of_Food = self.getFood(next_succ).asList()
        # We first determine the List of Food options for us based on the Next_succ obtained above.
        if len(List_of_Food) > 0:
            my_Position = next_succ.getAgentState(self.index).getPosition()
            # Now that we have the list of food options we now need to determine what is my exact position
            # in the lay out and we need to determine the minimum distance for me to reach the food from the list of the
            # food options obtained above.
            min_Distance = min([self.getMazeDistance(my_Position, food) for food in List_of_Food])
            # once I obtain the min distance to the food I will use that as one of my features called foodDistance
            f['foodDistance'] = min_Distance

        # DETERMINE FEATURE 3
        my_Position = next_succ.getAgentState(self.index).getPosition()
        # Now that I have the next succ score and where my food is . I also need to be aware of where my enemy is ?
        # I need to be safe from my enemy and eat as much food as I can from the other side .
        my_enemy = [next_succ.getAgentState(i) for i in self.getOpponents(next_succ)]
        # Again from the range values for my_enemy locations our task to find which one
        # is closest to me and most likely to attack me and end my game .
        range = filter(lambda x: not x.isPacman and x.getPosition() != None, my_enemy)
        # print("my enemy range", range)
        if len(range) > 0:
            pos = [agent.getPosition() for agent in range]
            # We get the position from the range and will determine the closest position with respect to my position
            closest_pos = min(pos, key=lambda x: self.getMazeDistance(my_Position, x))
            # Now it becomes easier to calculate the exact value of the closest distance
            my_closest_Dist = self.getMazeDistance(my_Position, closest_pos)
            # We choose a random value for the closest distance and will use that value to determine the ghostDistance .
            if my_closest_Dist <= 5:
                # If equal or below my random number I will set the ghost ditance to be myclosest distance .
                f['ghostDistance'] = my_closest_Dist

        # DETERMINE FEATURE 4
        f['isPacman'] = 1 if next_succ.getAgentState(self.index).isPacman else 0

        # We have now obtained all our 4 features
        return f

    def getWeights(self, gameState, action):
        # Activity time is very Important here . It is initialed as 0 and increases till the time I am alive.
        # Once I am dead the activity time counter resets itself .
        if self.activityTime > 70:
            # for the purpose of getting weights we use our intitution and select random values for the below.
            return {'nextsuccScore': 200, 'foodDistance': -5, 'ghostDistance': 2, 'isPacman': 1000}
        # Again I will first get the next_succ and my current position for the gamestate and the action
        next_succ = self.getSuccessor(gameState, action)
        my_Position = next_succ.getAgentState(self.index).getPosition()
        # Based on the next_succ value I also check where my enemies are ???
        my_enemy = [next_succ.getAgentState(i) for i in self.getOpponents(next_succ)]

        range = filter(lambda x: not x.isPacman and x.getPosition() != None, my_enemy)

        if len(range) > 0:
            pos = [agent.getPosition() for agent in range]
            # just like features we get the position
            closest_pos = min(pos, key=lambda x: self.getMazeDistance(my_Position, x))
            # just like features we get the closest position
            closest_Dist = self.getMazeDistance(my_Position, closest_pos)
            # just like features we get the closest distance and the closest enemies
            closest_enemies = filter(lambda x: x[0] == closest_pos, zip(pos, range))

            for agent in closest_enemies:
                if agent[1].scaredTimer > 0:
                    # if scared timer is greater than 0 we will set up different random values again.
                    return {'nextsuccScore': 200, 'foodDistance': -5, 'ghostDistance': 0, 'isPacman': 0}
        # Our weights returned !!!
        return {'nextsuccScore': 200, 'foodDistance': -5, 'ghostDistance': 2, 'isPacman': 0}

    def evaluate(self, gameState, action):
        f = self.getFeatures(gameState, action)
        w = self.getWeights(gameState, action)
        # Evalute is called everytime we clone/Simulate the grid and our position.
        # We have taken some help from the baseline team to understand and implement evaluate function
        # But it returns the features and weights for the gamestate and action at 1 particular time
        # for 1 complete run of our cloning process. See below to understand what happens further .
        return f * w

    def __init__(self, index):
        CaptureAgent.__init__(self, index)
        self.enemyfoodcount = "+inf"
        self.activityTime = 0

    def checkifnoPacmanDots(self,gameState, action, d):
        if d == 0:
            return False
        previousScore = self.getScore(gameState)
        # print("my previous score ", previousScore)
        # I now get the recent state and my score for that and check what was my last score ?
        recentState = gameState.generateSuccessor(self.index, action)
        recentScore = self.getScore(recentState)
        if previousScore < recentScore:
            return False
        # Again I set the set of my actions
        actions = recentState.getLegalActions(self.index)
        actions.remove(Directions.STOP)
        reversed_direction = Directions.REVERSE[recentState.getAgentState(self.index).configuration.direction]
        if reversed_direction in actions:
            actions.remove(reversed_direction)
        if len(actions) == 0:
            return True
        for a in actions:
            if not self.checkifnoPacmanDots(recentState, a, d - 1):
                return False
        return True



    def chooseAction(self, gameState):
        # This is where all our processing for our agent happens
        # We first determine the intial state of the game state .
        CaptureAgent.registerInitialState(self, gameState)
        self.distancer.getMazeDistances()
        # Activity time of the pacman plays an important role here . When alive counter / activity
        # time keeps on increasing
        # But we need to make sure that the counter is reset when our pacman dies and we need to start all over again!!
        recentEnemyFood = len(self.getFood(gameState).asList())
        if self.enemyfoodcount != recentEnemyFood:
            self.enemyfoodcount = recentEnemyFood
            self.activityTime = 0
        else:
            self.activityTime += 1
        # If our agent dies , we will set the activity time to 0 again.
        if gameState.getInitialAgentPosition(self.index) == gameState.getAgentState(self.index).getPosition():
            self.activityTime = 0

        # We first determine all the legal actions that we can take ???
        complete_actions = gameState.getLegalActions(self.index)
        complete_actions.remove(Directions.STOP)

        actions = []
        for a in complete_actions:
            if not self.checkifnoPacmanDots(gameState, a, 5):
                # I get the action for every value of D where we have set it randomly to be 5
                actions.append(a)
        if len(actions) == 0:
            actions = complete_actions

        def randomAction(d, gameState):
            # random action is the main function for how our pacman finally chooses an action.
            recentState = gameState.deepCopy()
            # This is the most recent game state. The below layout of the TinyCapture.py
            """
            %%%%%%%%%%%%%%%%%%%%
            %.    .      .    .%
            %.%%.%.%%%%%%.%.%%.%
            %......      ......%
            % %%%%%%%%%%%%%%%% %
            %      G G%%GG     %
            %%%%%%%%%%%%%%%%%%%%
            """
            while d > 0:
                # for every iteration we will get my_action that is a set of legal actions that pacman can take
                my_action = recentState.getLegalActions(self.index)
                # In the set of Actions if there is an Action Stop, We will remove that from the list.
                my_action.remove(Directions.STOP)
                current = recentState.getAgentState(self.index).configuration.direction
                # Is this Current Even Required? Yes it tells us about which direction we have now
                reversed_direction = Directions.REVERSE[recentState.getAgentState(self.index).configuration.direction]
                # Now what do I mean by the reversed direction?
                # Our task is to remove the reversed direction if it  is in the list of my_action.
                # Why should we do that?
                # Removing reversed_direction, STOP from our actions helps us choose the random action for my agent.
                if reversed_direction in my_action and len(my_action) > 1:
                    # If there is reversed direction we dont need that too
                    my_action.remove(reversed_direction)
                acc = random.choice(my_action)
                # Finally it becomes so easy for me to choose my action
                # Acc is a random choice for my Action, I choose this as my new action
                recentState = recentState.generateSuccessor(self.index, acc)
                # We will run the random simulation every time to choose the best action for every new_succ
                d -= 1
            return self.evaluate(recentState, Directions.STOP)


        calulatedValue = []

        for a in actions:
            # This is what was taken from simulation
            new_state = gameState.generateSuccessor(self.index, a)
            # This is my new state
            value = 0
            for i in range(1, 31):
                value += randomAction(10, new_state)
                # my new_state changes and I can now take a new action and move next .
                # print("see how I find my new state", new_state)
            calulatedValue.append(value)

        b = max(calulatedValue)
        # I select the best value from the set of calculated values
        t = filter(lambda x: x[0] ==  b, zip(calulatedValue, actions))
        # print("When Does my game result in a Tie?", t)
        pacplaying = random.choice(t)[1]
        # print("This is what pac playing is ?", pacplaying)

        return pacplaying


class MonteCarloProtectingAgent(CaptureAgent):
    """
     We first take some help from BaselineTeam.py already implemented and design a base class for
     reflex agents that will choose score-maximizing actions.
     We first Find the next successor (next_succ) which is a grid position .
     """

    def getSuccessor(self, gameState, action):
        next_succ = gameState.generateSuccessor(self.index, action)
        my_position = next_succ.getAgentState(self.index).getPosition()
        if my_position != nearestPoint(my_position):
            return next_succ.generateSuccessor(self.index, action)
        else:
            return next_succ

    """
    this will evaluate that is we will compute a linear combination of features and weights (f *w)
    """

    def evaluate(self, gameState, action):
        f = self.getFeatures(gameState, action)
        w = self.getWeights(gameState, action)
        return f * w

    """
    Returns a counter of features for the state
    """

    def getFeatures(self, gameState, action):
        f = util.Counter()
        next_succ = self.getSuccessor(gameState, action)
        f['nextsuccScore'] = self.getScore(next_succ)
        return f

    """
    This function gets the weights 
    """

    def getWeights(self, gameState, action):
        return {'nextsuccScore': 1.0}

    def __init__(self, index):
        CaptureAgent.__init__(self, index)
        self.selectedT = None  # These are our selected Targets which will be selected Randomly
        self.previousFoodPatrolled = None
        self.guarding = {}

    def chooseAction(self, gameState):
        myposition = gameState.getAgentPosition(self.index)

        if myposition == self.selectedT:
            self.selectedT = None
        CaptureAgent.registerInitialState(self, gameState)
        self.distancer.getMazeDistances()
        # We use this for some pre-processing .
        # Now we determine the middle or the central patrolling points.
        # Patrolling center points consists of choosing a point on the edge of the territories
        # of the two teams and move to that point. These points are called patrol points.
        # Compute central positions without walls from map layout.
        # The protective agent will walk among these positions to protect
        # its territory.
        edgeWidth = gameState.data.layout.width - 2
        edgeHeight = gameState.data.layout.height
        if self.red:
            centralpatrollingpoint = edgeWidth / 2
        else:
            centralpatrollingpoint = (edgeWidth / 2) + 1

        self.noneWallAreas = []
        # For our defending agents it is very necessary that it understands/Calculates the Edges and the no wall spots
        for i in range(1, edgeHeight - 1):
            if not gameState.hasWall(centralpatrollingpoint, i):
                self.noneWallAreas.append((centralpatrollingpoint, i))
        while len(self.noneWallAreas) > (edgeHeight - 2) / 2:
            self.noneWallAreas.pop(0)
            # We also need to remove some spots as we are already patrolling the central area
            # Our agent does not have to analyze the entire are . We need not perform
            # un neccesary computations.
            self.noneWallAreas.pop(len(self.noneWallAreas) - 1)

            # We will now calculate the min distance from our patrolling points. This distance is used
            # as the probability to select the patrolling points as targets.

        myfood = self.getFoodYouAreDefending(gameState).asList()
        mytotal = 0  # We will first determine the min distance from our food to our patrolling points.
        for pos in self.noneWallAreas:
            closestdistofFood = "+inf"
            for foodPosition in myfood:
                distance = self.getMazeDistance(pos, foodPosition)
                if distance < closestdistofFood:
                    closestdistofFood = distance

            # While Choosing the visited points we will calculate some probabilities.
            # We will associate, each patrolling point, with a probability corresponding to
            # agent to choose to go to that position.
            # In this way, the our defending agent will move to points with a which have a dot (pac man dot )
            # nearly . Now it is important to note that the opponent will try and catch these pacman dots before us .
            # When we see that our opponents have eaten our pacman dots we will have to re-calculate the prob

            if closestdistofFood == 0:
                closestdistofFood = 1
            self.guarding[pos] = 1.0 / float(closestdistofFood)
            mytotal += self.guarding[pos]
        if mytotal == 0:
            mytotal = 1
        for p in self.guarding.keys():
            self.guarding[p] = float(self.guarding[p]) / float(mytotal)

        my_enemy = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]

        # it is expected that if the enemy passes through the patrol of the protecting agent,
        # it is possible to identify quickly that our territory was invaded,
        # as well as to estimate the position of the attacker.
        intruders = filter(lambda x: x.isPacman and x.getPosition() != None, my_enemy)
        # we need to check the positions of the intruding parties
        if len(intruders) > 0:
            pos = [agent.getPosition() for agent in intruders]
            self.selectedT = min(pos, key=lambda x: self.getMazeDistance(myposition, x))
        # If we can't see our game invaders, but our dots were eaten,
        # we will  now check the position where the dots disappeared.
        elif self.previousFoodPatrolled != None:
            food_eaten = set(self.previousFoodPatrolled) - set(self.getFoodYouAreDefending(gameState).asList())
            # We check the food_eaten
            if len(food_eaten) > 0:
                self.selectedT = food_eaten.pop()
        self.previousFoodPatrolled = self.getFoodYouAreDefending(gameState).asList()
        if self.selectedT == None and len(self.getFoodYouAreDefending(gameState).asList()) <= 4:
            food = self.getFoodYouAreDefending(gameState).asList() \
                   + self.getCapsulesYouAreDefending(gameState)
            self.selectedT = random.choice(food)
        elif self.selectedT == None:
            r = random.random()

        # it is here that we select some patrolling point to use as our targets.
        # These are selected randomly

            s = 0.0
            for p in self.guarding.keys():
                s += self.guarding[p]
                if r < s:
                    self.selectedT = p
                    # Choose actions. We will take the actions that brings us
                    # closer to the target. But we need to make sure that we never invade the enemy side.
        actions = gameState.getLegalActions(self.index)
        myActions = []
        calculatedvalues = []
        for acc in actions:
            # for the purpose of determining our game state we need our recent state and the action taken
            recentstate = gameState.generateSuccessor(self.index, acc)
            if not recentstate.getAgentState(self.index).isPacman and not acc == Directions.STOP:
                newpos = recentstate.getAgentPosition(self.index)
                myActions.append(acc)
                calculatedvalues.append(self.getMazeDistance(newpos, self.selectedT))
        b = min(calculatedvalues)
        # Randomness is key to Monte carlo and we randomly select between the t values
        t = filter(lambda x: x[0] == b, zip(calculatedvalues, myActions))
        return random.choice(t)[1]

# class QLearningAgent(CaptureAgent):
    #     """
    #     A Dummy agent to serve as an example of the necessary agent structure.
    #     You should look at baselineTeam.py for more details about how to
    #     create an agent as this is the bare minimum.
    #     """
    #
    #     def registerInitialState(self, gameState):
    #         """
    #         This method handles the initial setup of the
    #         agent to populate useful fields (such as what team
    #         we're on).
    #         A distanceCalculator instance caches the maze distances
    #         between each pair of positions, so your agents can use:
    #         self.distancer.getDistance(p1, p2)
    #         IMPORTANT: This method may run for at most 15 seconds.
    #         """
    #         '''
    #         Make sure you do not delete the following line. If you would like to
    #         use Manhattan distances instead of maze distances in order to save
    #         on initialization time, please take a look at
    #         CaptureAgent.registerInitialState in captureAgents.py.
    #         '''
    #         CaptureAgent.registerInitialState(self, gameState)
    #         '''
    #         Your initialization code goes here, if you need any.
    #         '''
    #         self.weights = util.Counter()
    #         with open('teams/Ace/weights', 'rb') as f:
    #             self.weights = pickle.load(f)
    #         self.start = gameState.getAgentPosition(self.index)
    #         self.epsilon = 0.05
    #         self.alpha = 0.2
    #         self.discount = 0.8
    #         self.lastAction = None
    #         self.lastState = None
    #         self.foodCount = len(self.getFood(gameState).asList())
    #         if self.red:
    #             self.home = (gameState.data.layout.width - 2) / 2
    #         else:
    #             self.home = ((gameState.data.layout.width - 2) / 2) + 1
    #
    #     def computeActionFromQValues(self, state):
    #         """
    #           Compute the best action to take in a state.  Note that if there
    #           are no legal actions, which is the case at the terminal state,
    #           you should return None.
    #         """
    #         "*** YOUR CODE HERE ***"
    #         actions = state.getLegalActions(self.index)
    #         if len(actions) == 0:
    #             bestAction = None
    #         else:
    #             bestAction = random.choice(actions)
    #             bestValue = self.getQValue(state, bestAction)
    #             for action in actions:
    #                 if self.getQValue(state, action) > bestValue:
    #                     bestAction = action
    #                     bestValue = self.getQValue(state, action)
    #         return bestAction
    #
    #     def chooseAction(self, gameState):
    #         """
    #         """
    #         if self.lastState is not None:
    #             self.update(self.lastState, self.lastAction, gameState)
    #         legalActions = gameState.getLegalActions(self.index)
    #         action = None
    #         "*** YOUR CODE HERE ***"
    #         # if util.flipCoin(self.epsilon):
    #         #    action = random.choice(legalActions)
    #         # else:
    #         action = self.computeActionFromQValues(gameState)
    #         foodLeft = len(self.getFood(gameState).asList())
    #         if foodLeft <= (self.foodCount - self.foodCount / 5):
    #             bestDist = 9999
    #             for option in legalActions:
    #                 successor = self.getSuccessor(gameState, option)
    #                 pos2 = successor.getAgentPosition(self.index)
    #                 if pos2[0] == self.home:
    #                     self.foodCount = foodLeft
    #                 dist = self.getMazeDistance(self.start, pos2)
    #                 if dist < bestDist:
    #                     if not self.distancer.getDistance(gameState.getAgentPosition(self.index), pos2) > 1:
    #                         action = option
    #                         bestDist = dist
    #         self.lastAction = action
    #         self.lastState = gameState
    #         return action
    #
    #     def getSuccessor(self, gameState, action):
    #         """
    #         Finds the next successor which is a grid position (location tuple).
    #         """
    #         successor = gameState.generateSuccessor(self.index, action)
    #         pos = successor.getAgentState(self.index).getPosition()
    #         if pos != nearestPoint(pos):
    #             # Only half a grid position was covered
    #             return successor.generateSuccessor(self.index, action)
    #         else:
    #             return successor
    #
    #     def update(self, gameState, action, nextState):
    #         reward = self.getReward(gameState, action, nextState)
    #         for feature in self.getFeatures(gameState, action):
    #             self.getWeights()[feature] = self.getWeights()[feature] + self.alpha * self.difference(reward,
    #                                                                                                    self.discount,
    #                                                                                                    self.getMaxValue(
    #                                                                                                        [
    #                                                                                                            self.getQValue(
    #                                                                                                                nextState,
    #                                                                                                                nextAction)
    #                                                                                                            for
    #                                                                                                            nextAction
    #                                                                                                            in
    #                                                                                                            nextState.getLegalActions(
    #                                                                                                                self.index)]),
    #                                                                                                    self.getQValue(
    #                                                                                                        gameState,
    #                                                                                                        action)) * \
    #                                                                       self.getFeatures(gameState, action)[feature]
    #         with open('tteams/Ace/weights', 'wb') as f:
    #             pickle.dump(self.getWeights(), f, pickle.HIGHEST_PROTOCOL)
    #             f.close()
    #
    #     def getMaxValue(self, thing):
    #         if len(thing) > 0:
    #             return max(thing)
    #         else:
    #             return 0
    #
    #     def difference(self, reward, discount, maxQvalue, currentQvalue):
    #         return (reward + (discount * maxQvalue)) - currentQvalue
    #
    #     def getQValue(self, state, action):
    #         """
    #           Should return Q(state,action) = w * featureVector
    #           where * is the dotProduct operator
    #         """
    #         "*** YOUR CODE HERE ***"
    #         return self.getWeights() * self.getFeatures(state, action)
    #
    #     def getWeights(self):
    #         return self.weights
    #
    #     def closestFood(self, state, pos, food, walls):
    #         """
    #         closestFood -- this is similar to the function that we have
    #         worked on in the search project; here its all in one place
    #         """
    #         fringe = [(pos[0], pos[1], 0)]
    #         expanded = set()
    #         while fringe:
    #             pos_x, pos_y, dist = fringe.pop(0)
    #             if (pos_x, pos_y) in expanded:
    #                 continue
    #             expanded.add((pos_x, pos_y))
    #             # if we find a food at this location then exit
    #             if self.getFood(state)[pos_x][pos_y]:
    #                 return dist
    #             # otherwise spread out from the location to its neighbours
    #             nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
    #             for nbr_x, nbr_y in nbrs:
    #                 fringe.append((nbr_x, nbr_y, dist + 1))
    #         # no food found
    #         return None
    #
    #     def getFeatures(self, state, action):
    #         # extract the grid of food and wall locations and get the ghost locations
    #         food = self.getFood(state)
    #         walls = state.getWalls()
    #         enemies = [state.getAgentState(i) for i in self.getOpponents(state)]
    #         ghosts = [a.getPosition() for a in enemies if not a.isPacman and a.getPosition() is not None]
    #         features = util.Counter()
    #         features["bias"] = 1.0
    #         # compute the location of pacman after he takes the action
    #         x, y = state.getAgentPosition(self.index)
    #         dx, dy = Actions.directionToVector(action)
    #         next_x, next_y = int(x + dx), int(y + dy)
    #         # count the number of ghosts 1-step away
    #         if len(ghosts) > 0:
    #             features["#-of-ghosts-1-step-away"] = sum(
    #                 (next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in ghosts)
    #         else:
    #             features["#-of-ghosts-1-step-away"] = 0
    #         # if there is no danger of ghosts then add the food feature
    #         if not features["#-of-ghosts-1-step-away"] and food[next_x][next_y]:
    #             features["eats-food"] = 1.0
    #         if self.deadEnd(next_x, next_y, walls) and state.getAgentState(self.index).isPacman:
    #             features["dead-end"] = 1.0
    #         dist = self.closestFood(state, (next_x, next_y), food, walls)
    #         if dist is not None:
    #             # make the distance a number less than one otherwise the update
    #             # will diverge wildly
    #             features["closest-food"] = float(dist) / (walls.width * walls.height)
    #         features.divideAll(10.0)
    #         # print features
    #         return features
    #
    #     def getReward(self, lastState, action, currentState):
    #         reward = 0
    #         lastpos = lastState.getAgentPosition(self.index)
    #         nowpos = currentState.getAgentPosition(self.index)
    #         nowposx = nowpos[0]
    #         nowposy = nowpos[1]
    #
    #         if self.distancer.getDistance(lastpos, nowpos) > 1:
    #             reward = -5
    #         if self.getFood(lastState)[nowposx][nowposy]:
    #             reward = 1
    #         if self.getScore(lastState) < self.getScore(currentState):
    #             reward = 10
    #         return reward
    #
    #     def deadEnd(self, x, y, walls):
    #         counter = 0
    #         if walls[x + 1][y]:
    #             counter += 1
    #         if walls[x - 1][y]:
    #             counter += 1
    #         if walls[x][y + 1]:
    #             counter += 1
    #         if walls[x][y - 1]:
    #             counter += 1
    #         if counter == 3:
    #             return True
    #         else:
    #             return False

# class ExpectimaxAgent(CaptureAgent):
#     def registerInitialState(self, gameState):
#         CaptureAgent.registerInitialState(self, gameState)
#
#         # Initial starting location of the agent.
#         self.start = gameState.getInitialAgentPosition(self.index)
#
#         # Team agent indexes.
#         self.team = self.getTeam(gameState)
#
#         # Enemy agent indexes.
#         self.enemies = self.getOpponents(gameState)
#
#         # Central location of the board where expecting to have more food pellets irrespective of the layout.
#         self.midWidth = gameState.data.layout.width / 2
#
#         self.midHeight = gameState.data.layout.height / 2
#
#         # Used for toggling the agent behaviour(Offensive/Defensive).
#         self.offensing = False
#
#         # Defensive agent instance has a belief of the opposing agent SET to 1
#         self.beliefs = {}
#         for ebelief in self.enemies:
#             self.beliefs[ebelief] = util.Counter()
#             self.beliefs[ebelief][gameState.getInitialAgentPosition(ebelief)] = 1.
#
#         # legal positions where the  agents can be part of it
#         self.legalPositions = [a for a in gameState.getWalls().asList(False) if a[1] > 1]
#
#     """ GameState and enemy objects are been sent to this methods
#         which can be used to draw how pacman can move by looking at all the possible successor positions
#
#            """
#     def legalmove(self, enemy, gameState):
#
#         new_belief = util.Counter()
#
#         for PosteriorPos in self.legalPositions:
#             # Get the new probability distribution.
#             newPosDist = util.Counter()
#
#             possiblePositions = self.getPreviousObservation()
#             if possiblePositions != None and possiblePositions.getAgentPosition(enemy) != None:
#                 new_belief[possiblePositions.getInitialAgentPosition(enemy)] = 1.0
#             else:
#                 pass
#                 # Get the new belief distibution.
#             for newPos, prob in newPosDist.items():
#                 # Update the probabilities for each of the positions.
#                 new_belief[newPos] += prob * self.beliefs[enemy][PosteriorPos]
#
#             # Normalize and update the belief.
#             new_belief.normalize()
#             self.beliefs[enemy] = new_belief
#
#     """ Intializing the beliefs dictionary
#          Every legal position we are setting the value to 1 as the agent is not having any knowledge of the state
#          and can be in any position
#                 """
#     def normalizeBeliefs(self, enemy):
#
#         self.beliefs[enemy] = util.Counter()
#         # The value could set to anything
#         for p in self.legalPositions:
#             self.beliefs[enemy][p] = 1.0
#         #normalization concept taken from the ghostAgent.py where the ghost legal action is normalized
#         self.beliefs[enemy].normalize()
#
#     """This filtered observation method provides more details about the position of an enemy
#            that recorded beyond the noisy distance reading so that the true position can
#            be narrowed down significantly.
#            """
#     def filteredobservation(self, enemy, observation, gameState):
#
#         # Record the noisy distance from the current enemy.
#         noisyDistance = observation[enemy]
#
#         # Get the position of the calling agent.
#         myPos = gameState.getAgentPosition(self.index)
#
#         # Create new dictionary to hold the new beliefs for the current enemy.
#         new_belief = util.Counter()
#
#         # For each of the legal positions get the new belief.
#         for p in self.legalPositions:
#             # Calculating true distance to the position based on the manhattan.
#             trueDistance = util.manhattanDistance(myPos, p)
#
#             # Emission model are the noisy distances to each ghost
#             # Concept taken from the Project 4 : Ghost buster - question 6
#             emissionModel = gameState.getDistanceProb(trueDistance, noisyDistance)
#
#             # Further eliminating the possible move if the agent doesn't matchup
#             if self.red:
#                 pac = p[0] < self.midWidth
#             else:
#                 # blue agent
#                 pac = p[0] > self.midWidth
#
#             if trueDistance <= 5:
#                 # we would have gotten the  noisy distance reading this cannot be a true distance. So, setting
#                 # the belief to Zer0
#                 new_belief[p] = 0.
#             elif pac != gameState.getAgentState(enemy).isPacman:
#                 # Eliminating the move if pacman is not the enemy position ruling out and updating it to Zer0
#                 new_belief[p] = 0.
#             else:
#                 # update the belief with a emission factor
#                 new_belief[p] = self.beliefs[enemy][p] * emissionModel
#
#         if new_belief.totalCount() == 0:
#             self.normalizeBeliefs(enemy)
#         else:
#             # Normalize and set the new belief.
#             new_belief.normalize()
#             self.beliefs[enemy] = new_belief
#
#     """
#          Chooses the best Action based on the Maxi and Expectimax function
#            """
#     def chooseAction(self, gameState):
#
#         # Agent Position
#         myPos = gameState.getAgentPosition(self.index)
#         # noisy distance
#         noisyDistances = gameState.getAgentDistances()
#         # new State
#         newState = gameState.deepCopy()
#
#         for enemy in self.enemies:
#             enemyPos = gameState.getAgentPosition(enemy)
#             if enemyPos:
#                 new_belief = util.Counter()
#                 new_belief[enemyPos] = 1.0
#                 self.beliefs[enemy] = new_belief
#             else:
#                 self.legalmove(enemy, gameState)
#                 self.filteredobservation(enemy, noisyDistances, gameState)
#
#         # Starting out the enemy position and ensuring that not defending against the same team
#
#         for enemy in self.enemies:
#             possibleEnemyPosition = self.beliefs[enemy].argMax()
#             gameconfig = game.Configuration(possibleEnemyPosition, Directions.STOP)
#             newState.data.agentStates[enemy] = game.AgentState(gameconfig, newState.isRed(
#                 possibleEnemyPosition) != newState.isOnRedTeam(enemy))
#
#         # We are going with expectimax with depth 2 to get the best action to use
#         action = self.maximizeFunction(newState, depth=1)[1]
#
#         return action
#
#     """
#             Choosing the best / max score move
#             """
#     def maximizeFunction(self, gameState, depth):
#
#         # If nodes are processed then the gameState is completed
#
#         if depth == 0 or gameState.isOver():
#             return self.evaluationFunction(gameState), Directions.STOP
#
#         # possible moves - Sucessor state.
#         actions = gameState.getLegalActions(self.index)
#
#         # Defending at suicidal conditions and moving will often results in better situation when the Ghost movement is
#         # Random .
#         actions.remove(Directions.STOP)
#         successorGameStates = [gameState.generateSuccessor(self.index, action)
#                                for action in actions]
#
#         # Record the expected scores of enemy moves for each and every depth until the gamestate is over.
#         scores = [self.expectiAlgo(successorGameState, self.enemies[0], depth)[0]
#                   for successorGameState in successorGameStates]
#
#         bestScore = max(scores)
#         bestIndices = [index for index in range(len(scores)) if
#                        scores[index] == bestScore]
#         chosenIndex = random.choice(bestIndices)
#
#         return bestScore, actions[chosenIndex]
#
#     """
#           Called for each of the enemey agent and use maximize function for next level.
#           """
#     def expectiAlgo(self, gameState, enemy, depth):
#
#         # Check point for gamecompletion.
#         if depth == 0 or gameState.isOver():
#             return self.evaluationFunction(gameState), Directions.STOP
#
#         #  possible moves - Sucessor state.
#         actions = gameState.getLegalActions(enemy)
#         successorGameStates = []
#         for action in actions:
#             try:
#                 successorGameStates.append(gameState.generateSuccessor(enemy, action))
#             except:
#                 pass
#
#         # more enemies nearby
#         if enemy < max(self.enemies):
#             scores = [self.expectiAlgo(successorGameState, enemy + 2, depth)[0]
#                         for successorGameState in successorGameStates]
#
#             # In case if there is  another ghost in nearby position call the expecti algorithm for the
#             # next ghost, otherwise call the maximize function for pacman.
#         else:
#             scores = [self.maximizeFunction(successorGameState, depth - 1)[0]
#                         for successorGameState in successorGameStates]
#
#         # Record the expected value.
#         bestScore = sum(scores) / len(scores)
#
#         return bestScore, Directions.STOP
#
#     """
#        Default Utility method to evaluate the gamestate .
#        """
#
#     def evaluationFunction(self, gameState):
#
#         util.raiseNotDefined()
#
#     """ This method is used to get the enemy distance in case if the agent is beyond the range
#            then we are going to return the most likely belief of the location
#            """
#     def invaderDistances(self, gameState):
#
#         dists = []
#         for enemy in self.enemies:
#             myPos = gameState.getAgentPosition(self.index)
#             enemyPos = gameState.getAgentPosition(enemy)
#             if enemyPos:
#                 pass
#             else:
#                 enemyPos = self.beliefs[enemy].argMax()  # most likely belief
#             dists.append((enemy, self.distancer.getDistance(myPos, enemyPos)))
#         return dists
#
# # class DefensiveAgent(ExpectimaxAgent):
# #
# #     def registerInitialState(self, gameState):
# #         ExpectimaxAgent.registerInitialState(self, gameState)
# #         self.offensing = False
# #
# #
# #     def chooseAction(self, gameState):
# #         # Agent isPacman.
# #         invaders = [a for a in self.enemies if
# #                     gameState.getAgentState(a).isPacman]
# #         numInvaders = len(invaders)
# #
# #         # Eat capsule - Ghost scared time starts for next 40 moves.
# #         scaredTimes = [gameState.getAgentState(enemy).scaredTimer for enemy in
# #                        self.enemies]
# #
# #         if numInvaders == 0 or min(scaredTimes) > 8:
# #             # agent will be offensive if enemy is not pacman and ghost is scared
# #             # eat the food
# #             self.offensing = True
# #         else:
# #             # Be @ defensive side
# #             self.offensing = False
# #
# #         return ExpectimaxAgent.chooseAction(self, gameState)
# #
# #     #  This method is used to get the enemy distance in case if the agent is beyond the range
# #     # then we are going to return the most likely belief of the location.
# #     def evaluationFunction(self, gameState):
# #         myPos = gameState.getAgentPosition(self.index)
# #
# #         invadersDistances = self.invaderDistances(gameState)
# #
# #         # Check if the Pacman is at our territory
# #         invaders = [a for a in self.enemies if
# #                     gameState.getAgentState(a).isPacman]
# #
# #         # Capture the distance to the pacman .
# #         pac_distances = [dist for id, dist in invadersDistances if
# #                          gameState.getAgentState(id).isPacman]
# #         # get the minimum
# #         minPacDistances = min(pac_distances) if len(pac_distances) else 0
# #
# #         # Capture the distance to the ghosts.
# #         ghost_distances = [dist for id, dist in invadersDistances if
# #                            not gameState.getAgentState(id).isPacman]
# #         # get the minimum
# #         minGhostDistances = min(ghost_distances) if len(ghost_distances) else 0
# #
# #         # Get min distance to a food.
# #         targetFood = self.getFood(gameState).asList()
# #         foodDistances = [self.distancer.getDistance(myPos, food) for food in
# #                          targetFood]
# #         minFoodDistance = min(foodDistances) if len(foodDistances) else 0
# #
# #         # Get min distance to a power capsule.
# #         capsules = self.getCapsulesYouAreDefending(gameState)
# #         capsulesDistances = [self.getMazeDistance(myPos, capsule) for capsule in
# #                              capsules]
# #         minCapsuleDistance = min(capsulesDistances) if len(capsulesDistances) else 0
# #
# #
# #         if self.offensing == False:
# #             return -999999 * len(invaders) - 10 * minPacDistances - minCapsuleDistance
# #         else:
# #             return 2 * self.getScore(gameState) - 100 * len(targetFood) - \
# #                    3 * minFoodDistance + minGhostDistances
# #
# #         #return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}
# #         #return {'successorScore': 100, 'distanceToFood': -1}
