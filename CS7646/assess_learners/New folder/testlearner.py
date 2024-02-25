""""""  		  	   		  		 			  		 			 	 	 		 		 	
"""  		  	   		  		 			  		 			 	 	 		 		 	
Test a learner.  (c) 2015 Tucker Balch  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
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
"""  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
import math  		  	   		  		 			  		 			 	 	 		 		 	
import sys  		  	   		  		 			  		 			 	 	 		 		 	
import matplotlib.pyplot as plt 		  	   		  		 			  		 			 	 	 		 		 	
import numpy as np  		  	   		  		 			  		 			 	 	 		 		 	  		  	   		  		 			  		 			 	 	 		 		 	
import LinRegLearner as lrl  		  	   		  		 			  		 			 	 	 		 		 	
import DTLearner as dt
import BagLearner as bl
import RTLearner as rt
import time

if __name__ == "__main__":  		  	   		  		 			  		 			 	 	 		 		 	
    if len(sys.argv) != 2:  		  	   		  		 			  		 			 	 	 		 		 	
        print("Usage: python testlearner.py <filename>")  		  	   		  		 			  		 			 	 	 		 		 	
        sys.exit(1)  		  	   		  		 			  		 			 	 	 		 		 	
    inf = open(sys.argv[1])  		  	   		  		 			  		 			 	 	 		 		 	
    data = data = np.genfromtxt(inf, delimiter=',', skip_header=1)  		  	   		  		 			  		 			 	 	 		 		 	
    # Remove the first column (date-time)
    data = data[:, 1:]  		  	   		  		 			  		 			 	 	 		 		 	
    # compute how much of the data is training and testing  		  	   		  		 			  		 			 	 	 		 		 	
    train_rows = int(0.6 * data.shape[0])  		  	   		  		 			  		 			 	 	 		 		 	
    test_rows = data.shape[0] - train_rows  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
    # separate out training and testing data  		  	   		  		 			  		 			 	 	 		 		 	
    train_x = data[:train_rows, 0:-1]  		  	   		  		 			  		 			 	 	 		 		 	
    train_y = data[:train_rows, -1]  		  	   		  		 			  		 			 	 	 		 		 	
    test_x = data[train_rows:, 0:-1]  		  	   		  		 			  		 			 	 	 		 		 	
    test_y = data[train_rows:, -1]  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	

    # set the range of leaf_sizes
    leaf_sizes = range(1, 50)

    # these lists will store your RMSE values for each leaf size
    in_sample_rmses = []
    out_sample_rmses = []
    in_sample_correlations = []
    out_sample_correlations = []

    # open the file for writing
    file = open("results.txt", "w")
    file.write("Results for Experiment1\n\n")
    for leaf_size in leaf_sizes:
        # train the learner
        learner = dt.DTLearner(leaf_size=leaf_size, verbose=False)
        learner.add_evidence(train_x, train_y)
        
        # compute in-sample error
        pred_y = learner.query(train_x)
        in_sample_rmse = math.sqrt(((train_y - pred_y) ** 2).sum() / train_y.shape[0])
        in_sample_rmses.append(in_sample_rmse)
        in_sample_corr = np.corrcoef(train_y, pred_y)[0, 1]
        in_sample_correlations.append(in_sample_corr)
        # compute out-of-sample error
        pred_y = learner.query(test_x)
        out_sample_corr = np.corrcoef(test_y, pred_y)[0, 1]
        out_sample_correlations.append(out_sample_corr)
        out_sample_rmse = math.sqrt(((test_y - pred_y) ** 2).sum() / test_y.shape[0])
        out_sample_rmses.append(out_sample_rmse)

        # write results to file
        file.write(f"Leaf size: {leaf_size}\n")
        file.write(f"In-sample RMSE: {in_sample_rmse}\n")
        file.write(f"Out-of-sample RMSE: {out_sample_rmse}\n")
        file.write(f"In-sample Correlation: {in_sample_corr}\n")
        file.write(f"Out-of-sample Correlation: {out_sample_corr}\n")
        file.write("\n")  # for readability


    # Create a figure with two subplots (one row, two columns)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6))

    # Plot RMSE values in the first subplot
    ax1.plot(leaf_sizes, in_sample_rmses, label="In-sample RMSE")
    ax1.plot(leaf_sizes, out_sample_rmses, label="Out-of-sample RMSE")
    ax1.set_xlabel("Leaf Size")
    ax1.set_ylabel("RMSE")
    ax1.legend()
    ax1.set_title("RMSE vs Leaf Size in DTLearner")
    ax1.grid(True)

    # Plot correlation values in the second subplot
    ax2.plot(leaf_sizes, in_sample_correlations, label="In-sample Correlation")
    ax2.plot(leaf_sizes, out_sample_correlations, label="Out-of-sample Correlation")
    ax2.set_xlabel("Leaf Size")
    ax2.set_ylabel("Correlation Coefficient")
    ax2.legend()
    ax2.set_title("Correlation Coefficient vs Leaf Size in DTLearner")
    ax2.grid(True)

    # Save the figure to a file
    plt.tight_layout()  # adjust subplot parameters to give specified padding
    plt.savefig("./images/rmse_and_corrcoef_vs_leaf_size.png")


    leaf_sizes = range(1, 50)
    num_bags = 20

    in_sample_rmses = []
    out_sample_rmses = []
    file.write("\nResults for Experiment2\n\n")

    for leaf_size in leaf_sizes:
        learner = bl.BagLearner(learner=dt.DTLearner, kwargs={"leaf_size": leaf_size}, bags=num_bags)

        learner.add_evidence(train_x, train_y)

        pred_y_train = learner.query(train_x)
        in_sample_rmse = math.sqrt(((train_y - pred_y_train) ** 2).sum() / train_y.shape[0])
        in_sample_rmses.append(in_sample_rmse)

        pred_y_test = learner.query(test_x)
        out_sample_rmse = math.sqrt(((test_y - pred_y_test) ** 2).sum() / test_y.shape[0])
        out_sample_rmses.append(out_sample_rmse)

        # write results to file
        file.write(f"Leaf size: {leaf_size}\n")
        file.write(f"In-sample RMSE: {in_sample_rmse}\n")
        file.write(f"Out-of-sample RMSE: {out_sample_rmse}\n")
        file.write("\n")  # for readability

    plt.figure(figsize=(10, 6))
    plt.plot(leaf_sizes, in_sample_rmses, label="In-sample RMSE")
    plt.plot(leaf_sizes, out_sample_rmses, label="Out-of-sample RMSE")
    plt.xlabel("Leaf Size")
    plt.ylabel("RMSE")
    plt.legend()
    plt.title("RMSE vs Leaf Size in BagLearner")
    plt.grid(True)
    plt.savefig("./images/baglearner_rmse_vs_leaf_size.png")



    file.write("\nResults for Experiment3\n\n")
    def mean_absolute_error(y_true, y_pred):
        return np.mean(np.abs(y_true - y_pred))

    def r2_score(y_true, y_pred):
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        return 1 - (ss_res / ss_tot)

    leaf_sizes = np.arange(1, 51, 1)
    dt_metrics = []
    rt_metrics = []

    for leaf_size in leaf_sizes:
        dt_learner = dt.DTLearner(leaf_size=leaf_size, verbose=False) 
        rt_learner = rt.RTLearner(leaf_size=leaf_size, verbose=False) 

        dt_start = time.time()
        dt_learner.add_evidence(train_x, train_y)
        dt_end = time.time()
        dt_train_time = dt_end - dt_start
        dt_tree_size = dt_learner.tree.shape[0]

        rt_start = time.time()
        rt_learner.add_evidence(train_x, train_y)
        rt_end = time.time()
        rt_train_time = rt_end - rt_start
        rt_tree_size = rt_learner.tree.shape[0]

        dt_pred_y = dt_learner.query(test_x)
        dt_mae = mean_absolute_error(test_y, dt_pred_y)
        dt_r2 = r2_score(test_y, dt_pred_y)

        rt_pred_y = rt_learner.query(test_x)
        rt_mae = mean_absolute_error(test_y, rt_pred_y)
        rt_r2 = r2_score(test_y, rt_pred_y)

        dt_metrics.append((dt_tree_size, dt_mae, dt_r2, dt_train_time))
        rt_metrics.append((rt_tree_size, rt_mae, rt_r2, rt_train_time))

        file.write(f"Leaf Size: {leaf_size}\n")
        file.write(f"DT Learner tree size: {dt_tree_size}, MAE: {dt_mae}, R2: {dt_r2}, training time: {dt_train_time}\n")
        file.write(f"RT Learner tree size: {rt_tree_size}, MAE: {rt_mae}, R2: {rt_r2}, training time: {rt_train_time}\n\n")
    file.close()

    # Convert lists to numpy arrays for plotting
    dt_metrics = np.array(dt_metrics)
    rt_metrics = np.array(rt_metrics)

    # Create a figure with 2x2 grid of subplots
    fig, axs = plt.subplots(2, 2, figsize=(20, 12))

    # Plot Tree Size vs Leaf Size in the first subplot
    axs[0, 0].plot(leaf_sizes, dt_metrics[:, 0], label='DT Tree Size')
    axs[0, 0].plot(leaf_sizes, rt_metrics[:, 0], label='RT Tree Size')
    axs[0, 0].set_xlabel('Leaf Size')
    axs[0, 0].set_ylabel('Tree Size')
    axs[0, 0].legend()
    axs[0, 0].set_title('Tree Size vs Leaf Size')
    axs[0, 0].grid(True)

    # Plot MAE vs Leaf Size in the second subplot
    axs[0, 1].plot(leaf_sizes, dt_metrics[:, 1], label='DT MAE')
    axs[0, 1].plot(leaf_sizes, rt_metrics[:, 1], label='RT MAE')
    axs[0, 1].set_xlabel('Leaf Size')
    axs[0, 1].set_ylabel('Mean Absolute Error (MAE)')
    axs[0, 1].legend()
    axs[0, 1].set_title('MAE vs Leaf Size')
    axs[0, 1].grid(True)

    # Plot R2 vs Leaf Size in the third subplot
    axs[1, 0].plot(leaf_sizes, dt_metrics[:, 2], label='DT R2')
    axs[1, 0].plot(leaf_sizes, rt_metrics[:, 2], label='RT R2')
    axs[1, 0].set_xlabel('Leaf Size')
    axs[1, 0].set_ylabel('R-Squared (R2)')
    axs[1, 0].legend()
    axs[1, 0].set_title('R2 vs Leaf Size')
    axs[1, 0].grid(True)

    # Plot Training Time vs Leaf Size in the fourth subplot
    axs[1, 1].plot(leaf_sizes, dt_metrics[:, 3], label='DT Training Time')
    axs[1, 1].plot(leaf_sizes, rt_metrics[:, 3], label='RT Training Time')
    axs[1, 1].set_xlabel('Leaf Size')
    axs[1, 1].set_ylabel('Training Time (Seconds)')
    axs[1, 1].legend()
    axs[1, 1].set_title('Training Time vs Leaf Size')
    axs[1, 1].grid(True)

    # Adjust subplot parameters and save the figure to a file
    plt.tight_layout()  # adjust subplot parameters to give specified padding
    plt.savefig('./images/metrics_vs_leaf_size.png')
