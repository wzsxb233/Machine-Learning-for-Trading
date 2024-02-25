""""""  		  	   		  		 			  		 			 	 	 		 		 	
"""  		  	   		  		 			  		 			 	 	 		 		 	
Template for implementing QLearner  (c) 2015 Tucker Balch  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  		 			  		 			 	 	 		 		 	
Atlanta, Georgia 30332  		  	   		  		 			  		 			 	 	 		 		 	
All Rights Reserved  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
Template code for CS 4646/7646  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  		 			  		 			 	 	 		 		 	
works, including solutions to the projects assigned in this course. Students  		  	   		  		 			  		 			 	 	 		 		 	
and other users of this template code are advised not to share it with others  		  	   		  		 			  		 			 	 	 		 		 	
or to make it available on publicly viewable websites including repositories  		  	   		  		 			  		 			 	 	 		 		 	
such as github and gitlab.  This copyright statement should not be removed  		  	   		  		 			  		 			 	 	 		 		 	
or edited.  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
We do grant permission to share solutions privately with non-students such  		  	   		  		 			  		 			 	 	 		 		 	
as potential employers. However, sharing with other current or future  		  	   		  		 			  		 			 	 	 		 		 	
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  		 			  		 			 	 	 		 		 	
GT honor code violation.  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
-----do not edit anything above this line---  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
Student Name: Yicun Deng (replace with your name)  		  	   		  		 			  		 			 	 	 		 		 	
GT User ID: ydeng335 (replace with your User ID)  		  	   		  		 			  		 			 	 	 		 		 	
GT ID: 903859623 (replace with your GT ID)  		  	   		  		 			  		 			 	 	 		 		 	
"""  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
import numpy as np

class QLearner:
    def __init__(self, num_states=100, num_actions=4, alpha=0.2, gamma=0.9, rar=0.5, radr=0.99, dyna=0, verbose=False):
        """Constructor method"""
        self.verbose = verbose
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        self.s = 0
        self.a = 0
        self.q_table = np.zeros((num_states, num_actions))
        self.experiences = []

    def querysetstate(self, s):
        """Update the state without updating the Q-table"""
        self.s = s
        if np.random.uniform(0, 1) < self.rar:
            # Take a random action
            self.a = np.random.randint(self.num_actions)
        else:
            # Take the action with the highest Q-value
            self.a = np.argmax(self.q_table[s, :])

        if self.verbose:
            print(f"s = {s}, a = {self.a}")

        return self.a

    def query(self, s_prime, r):
        """Update the Q table and return an action"""
        # Update Q-table based on the reward and the maximum Q-value for next state
        self.q_table[self.s, self.a] = (1 - self.alpha) * self.q_table[self.s, self.a] + \
                                        self.alpha * (r + self.gamma * np.max(self.q_table[s_prime, :]))

        # Add this experience to the list of experiences
        self.experiences.append((self.s, self.a, r, s_prime))

        # Perform Dyna-Q update if enabled
        if self.dyna > 0:
            # Repeat experiences
            for _ in range(self.dyna):
                # Randomly sample an experience
                s, a, r, sp = self.experiences[np.random.randint(len(self.experiences))]

                # Update Q-table based on the sampled experience
                self.q_table[s, a] = (1 - self.alpha) * self.q_table[s, a] + \
                                     self.alpha * (r + self.gamma * np.max(self.q_table[sp]))

        # Update state, action, and rar
        self.s = s_prime
        self.a = self.querysetstate(s_prime)
        self.rar *= self.radr

        return self.a

    
    def author(self): 
        return 'ydeng335' # replace tb34 with your Georgia Tech username. 




 		  	   		  		 			  		 			 	 	 		 		 	
