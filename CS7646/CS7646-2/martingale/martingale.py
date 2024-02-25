""""""  		  	   		  		 			  		 			 	 	 		 		 	
"""Assess a betting strategy.  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
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
  		  	   		  		 			  		 			 	 	 		 		 	
Student Name: Tucker Balch (replace with your name)  		  	   		  		 			  		 			 	 	 		 		 	
GT User ID: tb34 (replace with your User ID)  		  	   		  		 			  		 			 	 	 		 		 	
GT ID: 900897987 (replace with your GT ID)  		  	   		  		 			  		 			 	 	 		 		 	
"""  		  	   		  		 			  		 			 	 	 		 		 	
import numpy as np
import matplotlib.pyplot as plt  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
def author():  		  	   		  		 			  		 			 	 	 		 		 	
    """  		  	   		  		 			  		 			 	 	 		 		 	
    :return: The GT username of the student  		  	   		  		 			  		 			 	 	 		 		 	
    :rtype: str  		  	   		  		 			  		 			 	 	 		 		 	
    """  		  	   		  		 			  		 			 	 	 		 		 	
    return "ydeng335"  # replace tb34 with your Georgia Tech username.  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
def gtid():  		  	   		  		 			  		 			 	 	 		 		 	
    """  		  	   		  		 			  		 			 	 	 		 		 	
    :return: The GT ID of the student  		  	   		  		 			  		 			 	 	 		 		 	
    :rtype: int  		  	   		  		 			  		 			 	 	 		 		 	
    """
    studentid=903859623  		  	   		  		 			  		 			 	 	 		 		 	
    return studentid  # replace with your GT ID number  	

np.random.seed(gtid())  # do this only once 		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
def get_spin_result(win_prob):  		  	   		  		 			  		 			 	 	 		 		 	
    """  		  	   		  		 			  		 			 	 	 		 		 	
    Given a win probability between 0 and 1, the function returns whether the probability will result in a win.  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
    :param win_prob: The probability of winning  		  	   		  		 			  		 			 	 	 		 		 	
    :type win_prob: float  		  	   		  		 			  		 			 	 	 		 		 	
    :return: The result of the spin.  		  	   		  		 			  		 			 	 	 		 		 	
    :rtype: bool  		  	   		  		 			  		 			 	 	 		 		 	
    """  		  	   		  		 			  		 			 	 	 		 		 	
    result = False  		  	   		  		 			  		 			 	 	 		 		 	
    if np.random.random() <= win_prob:  		  	   		  		 			  		 			 	 	 		 		 	
        result = True  		  	   		  		 			  		 			 	 	 		 		 	
    return result  			  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
def simulator(num_episodes=1000, num_spins=1000, upper_limit=80, lower_limit=float('-inf')):
    winnings = np.zeros((num_episodes+1, num_spins+1)) # Initializing winnings with zeros
    win_prob = 18/38 # Probability of winning
    for i in range(1,num_episodes+1):
        episode_winnings = 0
        bet_amount = 1
        for j in range(num_spins):
            # If the episode winnings have not reached the upper limit and are above the lower limit
            if episode_winnings < upper_limit and episode_winnings > lower_limit:
                # Simulate spin of roulette wheel
                won = get_spin_result(win_prob)
                if won:
                    episode_winnings += bet_amount
                    bet_amount = 1
                else:
                    episode_winnings -= bet_amount
                    bet_amount *= 2
                    # If bet_amount exceeds available money, adjust bet to remaining money
                    if episode_winnings - bet_amount < lower_limit:
                        bet_amount = episode_winnings - lower_limit
            # Track winnings at each spin
            winnings[i, j+1] = episode_winnings
            # Stop betting and fill all future winnings with current value if upper or lower limit is reached
            if episode_winnings >= upper_limit or episode_winnings <= lower_limit:
                winnings[i, j+2:] = episode_winnings
                break
    return winnings	  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
def main():
    # Experiment 1
    winnings = simulator(num_episodes=10, num_spins=1000)

    # Generate Figures 1
    plt.figure()
    for i in range(11):
        plt.plot(winnings[i, :],label='Episode {}'.format(i+1))
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spins')
    plt.ylabel('Winnings in Dollars')
    plt.title('Figure1. 10 episodes of Martingale strategy')
    plt.legend()
    plt.savefig('./images/figure1.png')
    
    # Generate Figures 2 and 3
    winnings = simulator(num_episodes=1000, num_spins=1000)
    plt.figure()
    plt.plot(np.mean(winnings, axis=0), label='Mean')
    plt.plot(np.mean(winnings, axis=0) + np.std(winnings, axis=0), label='Mean + STD')
    plt.plot(np.mean(winnings, axis=0) - np.std(winnings, axis=0), label='Mean - STD')
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spins')
    plt.ylabel('Winnings in Dollars')
    plt.title('Figure2. Mean and STD of winnings over 1000 episodes')
    plt.legend()
    plt.savefig('./images/figure2.png')

    plt.figure()
    plt.plot(np.median(winnings, axis=0), label='Median')
    plt.plot(np.median(winnings, axis=0) + np.std(winnings, axis=0), label='Median + STD')
    plt.plot(np.median(winnings, axis=0) - np.std(winnings, axis=0), label='Median - STD')
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spins')
    plt.ylabel('Winnings in Dollars')
    plt.title('Figure3. Median and STD of winnings over 1000 episodes')
    plt.legend()
    plt.savefig('./images/figure3.png')

    # Experiment 2
    winnings = simulator(num_episodes=1000, num_spins=1000, lower_limit=-256)

    # Generate Figures 4 and 5
    plt.figure()
    plt.plot(np.mean(winnings, axis=0), label='Mean')
    plt.plot(np.mean(winnings, axis=0) + np.std(winnings, axis=0), label='Mean + STD')
    plt.plot(np.mean(winnings, axis=0) - np.std(winnings, axis=0), label='Mean - STD')
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spins')
    plt.ylabel('Winnings in Dollars')
    plt.title('Figure4. Mean and STD of winnings over 1000 episodes')
    plt.legend()
    plt.savefig('./images/figure4.png')

    plt.figure()
    plt.plot(np.median(winnings, axis=0), label='Median')
    plt.plot(np.median(winnings, axis=0) + np.std(winnings, axis=0), label='Median + STD')
    plt.plot(np.median(winnings, axis=0) - np.std(winnings, axis=0), label='Median - STD')
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spins')
    plt.ylabel('Winnings in Dollars')
    plt.title('Figure5. Median and STD of winnings over 1000 episodes')
    plt.legend()
    plt.savefig('./images/figure5.png')
   
if __name__ == "__main__":
    main() 		  	   		  		 			  		 			 	 	 		 		 	
