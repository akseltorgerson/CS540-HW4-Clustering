# CS540-HW4-Clustering
Assignment Goals
Process fun real-world data
Implement hierarchical clustering
Randomly generate your own data
Imshow your linkage process
Summary
Using the publicly available Pokemon stats, you'll be performing clustering on these stats. Each Pokemon is defined by a row in the data set. Because there are various ways to characterize how strong a Pokemon is, it is often desirable to convert a raw stats sheet into a shorter feature vector. For this assignment, you will represent a Pokemon's strength by two numbers: "x" and "y". "x" will represent the Pokemon's total offensive strength, which is defined by Attack + Sp. Atk + Speed. Similarly, "y" will represent the Pokemon's total defensive strength, which is defined by Defense + Sp. Def + HP. After each Pokemon becomes that two-dimensional feature vector, you will cluster the first 20 Pokemon with hierarchical agglomerative clustering (HAC).

Program Specification
Download the data in CSV format: Pokemon.csv 

Write the following Python functions:

load_data(filepath) — takes in a string with a path to a CSV file formatted as in the link above, and returns the first 20 data points (without the Generation and Legendary columns but retaining all other columns) in a single structure.
calculate_x_y(stats) — takes in one row from the data loaded from the previous function, calculates the corresponding x, y values for that Pokemon as specified above, and returns them in a single structure.
hac(dataset) — performs single linkage hierarchical agglomerative clustering on the Pokemon with the (x,y) feature representation, and returns a data structure representing the clustering.
random_x_y(m) — takes in the number of samples we want to randomly generate, and returns these samples in a single structure.
imshow_hac(dataset) — performs single linkage hierarchical agglomerative clustering on the Pokemon with the (x,y) feature representation, and imshow the clustering process.
You may implement other helper functions as necessary, but these are the functions we will be testing.

Load Data
Read in the file specified in the argument (the DictReader from Python's csv module (Links to an external site.) will be of use) and return a list of dictionaries, where each row in the dataset is a dictionary with the column headers as keys and the row elements as values. These dictionaries should not include the Generation and Legendary columns, as we will not be using them in this program. The integer strength of Pokemons (6 columns) including 2 other columns (#, Total) should be converted to integers.  Also, you only should have the first 20 Pokemon in this structure. Note the first 20 refers to row 1 through row 20 (From Bulbasaur to BeedrillMega Beedrill).

You may assume the file exists and is a properly formatted CSV.

Calculate Feature Values
This function takes in the data from a single row of the raw dataset as read in the previous function (i.e. a single dictionary, without the Generation and Legendary values but retaining all other columns).   This function should return the x, y values in a tuple, formatted as (x, y).

Perform HAC
For this function, we would like you to mimic the behaviour of SciPy's HAC function (Links to an external site.), linkage(). You may not use this function in your implementation, but we strongly recommend using it to verify your results!

Input: A collection of m observation vectors in n dimensions may be passed as an m by n array (for us, this will be a list of tuples, not a numpy array like for linkage()!). All elements of the condensed distance matrix must be finite, i.e. no NaNs or infs. In our case, m is the number of Pokemon (here 20) and n is 2: the x and y features for each Pokemon. (If invalid data points exit, you need to pop them out. In this case, m is the number of valid data points)

Using single linkage, perform the hierarchical agglomerative clustering algorithm as detailed on slide 19 of our class slidesLinks to an external site.. Use a standard Euclidean distance function for calculating the distance between two points.

Output: An (m-1) by 4 matrix Z. At the i-th iteration, clusters with indices Z[i, 0] and Z[i, 1] are combined to form cluster m + i. A cluster with an index less than m corresponds to one of the m original observations. The distance between clusters Z[i, 0] and Z[i, 1] is given by Z[i, 2]. The fourth value Z[i, 3] represents the number of original observations in the newly formed cluster.

That is:

Number each of your starting data points from 0 to m-1. These are their original cluster numbers.
Create an (m-1)x4 array or list. Iterate through the list row by row.
For each row, determine which two clusters you will merge and put their numbers into the first and second elements of the row. The first point listed should be the smaller of the two cluster indexes. The single-linkage distance between the two clusters goes into the third element of the row. The total number of points in the cluster goes into the fourth element.
If you merge a cluster containing more than one data point, its number (for the first or second element of the row) is given by m+the row index in which the cluster was created.
Before returning the data structure, convert it into a NumPy matrix.
If you follow these guidelines for input and output, your result should match the result of scipy.cluster.hierarchy.linkage() and you can use that function to verify your results. Be aware that this function does not contain code to filter NaN values, so this filtering should be performed before calling the function.

Tie Breaking
In the event that there are multiple pairs of points with equal distance for the next cluster:

Given a set of pairs with equal distance {(xi, xj)} where i < j, we prefer the pair with the smallest first cluster index i. If there are still ties (xi, xj), ... (xi, xk) where i is that smallest first index, we prefer the pair with the smallest second cluster index.

Be aware that this tie breaking strategy may not produce identical results to scipy.cluster.hierarchy.linkage().

Generate Random Data
Given a positive integer m, your aim is to uniformly randomly generate m Pokemons' "x" and "y", which satisfy 0<x<360, 0<y<360, and where x,y are both integers. The output of this random_x_y(m) function will further be used as the input of hac(dataset).

Imshow HAC Process
In this imshow_hac(dataset) function, given a dataset, you do the same process as hac(dataset) (you can also use or revise your hac() function to produce the imshow_hac() function). Meanwhile, you need to imshow this process including the start status (m points) and the results of (m-1) linkage processes. You should only have one plt.figure(), so in total you will need to plot m times on the same figure. Pause 0.1 seconds after each plotting, and do not close or clean the figure at the end of your function. An example of the start and the end status are shown as below. (Hint: plt.scatter(), plt.plot(), plt.pause())

Figure_1.png  Figure_2.png  
