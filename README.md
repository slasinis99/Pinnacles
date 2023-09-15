# Pinnacles of Graph Labelings

Given a simple, connected, undirected, finite graph G with n vertices, we can arbitrarily label the vertices with the integers 1 through n.
For any vertex whose label l is larger than the label of its neighbors, we say that l is a pinnacle for this labeling. This code allows you 
to create a graph based from an assortment of predefined graph families, choose a pinnacle set, and calculate how many labelings of your
graph yield the desired pinnacle set.

There is also the option in the driver to brute force every possible pinnacle set along with the number of occurences of each for the
created graph. This is very slow but will give you every admissible pinnacle set for your graph without having to specify which
pinnacle set to use. This can be very slow for graphs with more than 10 or eleven vertices/nodes.

## Installation / Setup

In order to run the program, download the entire repository and simple run the "driver.py" file. This assumes that you have the latest version
of python installed in order to run the file. Once the driver is running, it is self-explanatory on how to use it.

## Modifications

All of the code for creating graphs and enumerating the labeling is documented in the "main.py" file. See the license in the repository
for proper attribution.
