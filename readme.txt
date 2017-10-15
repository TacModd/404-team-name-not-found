An agent for the UC Berkeley Pacman Capture The Flag Competition

http://ai.berkeley.edu/contest.html

Made as a part of the assesment in COMP90054 AI Planning for Autonomy at the University of Melbourne semester 2 fall 2017.


---
IMPLEMENTATION
---

The agent is for all moves in one of four states, which all has its own specified behaviour as follows:

'Guard'
Uses the captureAgent method getMazeDistance(self, pos1, pos2) as a hueristic and makes a greedy best first search to the center position of the top half and bottom half of the board, respectively. 

'Defence'
If opponent is observed or it is detected that opponent is eating food, one of the agents will be assigned to defend this position. It will then do a greedy best first search to the position using the captureAgent method getMazeDistance(self, pos1, pos2) as a huersitc. Actions that will make the agent leave its home territory is not allowed. 

'Offence'
If our agent is scared or the team have killed an opponent, the agent enters offence mode. 
Uses a modified Monte Carlo Search that executes a search starting from the state reached with all legal actions, once ‘STOP’ and has been removed, and an average of scores for each ‘move tree’  is calculate for each move. The features contributing to the score are: food eaten on path, food in proximity, food distances in proximity, closest enemy distance, closest teammate distance, and closest capsule distance. The weighting of these features can be adjusted in getOffenciveWeigths().


'Flee'
If the agent is in 'Offence' and detects a nearby ghost, or it has been eating a set amount of food, it enters 'Flee'
It will then do a breadth first search to a position in its home territory, and take the first action on the shortest path that does not contain an observable ghost. 

---
HOW TO RUN
---

To run a game, use the following command:

python capture.py -r <redteam> -b <blueteam>

To set a random board, add the extension (<seed> is optional):

-l RANDOM<seed>






