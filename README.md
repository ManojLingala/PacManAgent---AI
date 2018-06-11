# PacManAgent---AI
Participated in University level competition and secured 52nd position out-of 252 teams .

Brief Description :

We have implemented the below agents and tried all possible combinations . Based upon the results from the competition with staff team Monte Carlo offensive with Monte Carlo defensive outperformed the competition and in some suicidal positions in some random layout "Expectimax Defensive/ Offensive " agent performed well.
 

Monte Carlo Aggressive Agent:
The Aggressive Agent uses simulations for each action for at any point of time. The game is played randomly until it terminates. Uncertainty and lack of visibility of our opponents make the game more complex. To cater for this complexity, we choose the agent to use 10 simulations where only actions taken by the agents are simulated. The number of simulations selected here plays an important part as it affects the final action taken by the agent. However, we also had to consider the time limit for the game execution, hence we opted to choose for a random value 10. Taking some assistance from the Baseline Agents we implemented some features like finding distance to the food, finding minimum distance to the Ghosts and evaluating weights and features for the given game state. The weights are chosen dynamically and evaluated with the features for every simulation. 
 
Monte Carlo Protecting Agent:
The task of the defending agent is to find a target position which helps the defensive in surveying central positions in the layouts, defend the food in its territory and pursue the opponent. Surveying the central position in the layout is the most important task of our defensive agent where he will choose a point on the edge of territory and needs to move towards it. The way the agent selects the target position is calculated entirely based on probability. The agent also needs to re-calculate the probabilities in the game state to find the most recent or the latest target position. Probability calculation and recalculation is a costly operation of our defending agent, however it tradeoff is that, it makes the defender more efficient in his during the contest. Another task of the defensive agent was to chase the opponent, if he finds an opponent in his area. 

Q- Learning Offensive Agent:
When chooseAction() is called by the game file, if it is the first action of the game, an action is chosen randomly from the legal actions. Every time after that, the update() function is first called to update the dictionary of weights with the state-action-nextstate-reward information observed in the last action. Then, either an action is chosen randomly with a probability of epsilon, or the action with the largest Q-Value is chosen.

The update() function makes use of a getFeatures() function which extracts information about the game state and stores it in a dictionary. It also uses the getWeights() function which just returns the weights, and the getReward() function which returns a reward based on what happened with the last action. 

At the start of the game, the learned weights are read from a file using the pickle module, and every time the weights are updated the file is updated too.

Expectimax Defensive Agent : 
This agent is designed to safeguard the territory By estimating the position of enemies and attacking when the opportunity is available based on the  best maximized moves which are drawn from the  Expectimax algorithm

−We are going to toggle the evaluation function whether the enemy is on to attack. In this case, the action will minimise the distance to the closest attacking agent to defend. If enemy has no attacking agent we are going to switch the offensive flag to true to collect the no of food pellets

Steps -Code walkthrough: 
1.Initialises the game state with agent index , enemy index, positions <<legal>>, toggle flag , normalising the beliefs of the defensive agent with SET to 1 assuming the agent is not having any knowledge-of the state and can be in any position.

2. GameState and enemy objects are been sent to the legal move method which can be used to draw how pacman can move by looking at all the possible successor positions.

3. This filtered observation method provides more details about the position of an enemy that recorded beyond the noisy distance reading so that the true position can be narrowed down significantly.

4. Chooses the best Action based on the Maxi and Expectimax function and the movement is from the Max score of the Avg weighted score of the chance node which is Called for each of the enemy agent and use maximize function for next level.

5. Invaders distance is used to get the enemy distance in case if the agent is beyond the range then we are going to return the most likely belief of the location.

6. Defensive agent is implemented as mentioned in the above steps. 

Execution:

To run , simply run 'python capture.py' and specify “myTeam” as the agent on either the red/blue team as desired. No additional setup is required.

