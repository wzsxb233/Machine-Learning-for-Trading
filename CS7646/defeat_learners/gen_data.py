""""""  		  	   		  		 			  		 			 	 	 		 		 	
"""  		  	   		  		 			  		 			 	 	 		 		 	
template for generating data to fool learners (c) 2016 Tucker Balch  		  	   		  		 			  		 			 	 	 		 		 	
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
  		  	   		  		 			  		 			 	 	 		 		 	
import math  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
import numpy as np  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
		  	   		  		 			  		 			 	 	 		 		 	
def best_4_lin_reg(seed=1489683273):
    np.random.seed(seed)
    x = np.random.normal(size=(1000, 5)) # Reduced from 10 features to 5
    # Create a linear relationship between features and the target variable
    y = 2*x[:,0] + 3*x[:,1] + 4*x[:,2] + 5*x[:,3] + 6*x[:,4] + np.random.normal(size=1000)  
    return x, y


	  	   		  		 			  		 			 	 	 		 		 	
 		 			  		 			 	 	 		 		 	
def best_4_dt(seed=1489683273):
    np.random.seed(seed)
    x = np.random.uniform(-1, 1, size=(1000, 5))  # Decreased the number of features from 10 to 5
    
    # Create a more complex relationship with multiple conditions
    y = np.where((x[:,0] > 0) & (x[:,1] < 0), np.sin(x[:,2]**3), np.cos(x[:,3]**2)) + \
        np.where((x[:,4] > 0) & (x[:,1] < 0), np.sin(x[:,0]**2), np.cos(x[:,2]**3))

    return x, y



  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
def author():  		  	   		  		 			  		 			 	 	 		 		 	
    """  		  	   		  		 			  		 			 	 	 		 		 	
    :return: The GT username of the student  		  	   		  		 			  		 			 	 	 		 		 	
    :rtype: str  		  	   		  		 			  		 			 	 	 		 		 	
    """  		  	   		  		 			  		 			 	 	 		 		 	
    return "ydeng335"  # Change this to your user ID  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
		  	   		  		 			  		 			 	 	 		 		 	
  	   		  		 			  		 			 	 	 		 		 	
