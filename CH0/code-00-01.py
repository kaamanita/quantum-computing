############################################################
#
# Author: Prachya Boonkwan
# Affiliation: SIIT, Thammasat Univeristy
# License: CC-BY-NC 4.0
#
############################################################

import multiprocessing as mp

########################################

# This is our task: computing the factorial of x
def factorial(x):
    result = 1
    for i in range(2, x+1):
        result *= i
    return result

########################################

# Main module
def main():

    # We will parallelize the computation of these inputs
    items = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    # Create a task pool of four workers
    pool = mp.Pool(processes=4)
    
    # All of these workers compute the factorial in paralell
    # But the results will be combined sequentially
    results = pool.map(factorial, items)
    
    # Print out the combined results
    print(results)

########################################

if __name__ == '__main__':

    # Enable the function freezing support for parallelization
    mp.freeze_support()

    # Call the main function
    main()
