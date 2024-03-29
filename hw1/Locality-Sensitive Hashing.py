# Authors: Jessica Su, Wanzi Zhou, Pratyaksh Sharma, Dylan Liu, Ansh Shukla
import numpy as np
import random
import time
import pdb
import unittest
from PIL import Image
import time
import matplotlib.pyplot as plt
# Finds the L1 distance between two vectors
# u and v are 1-dimensional np.array objects
# TODO: Implement this
def l1(u, v):
    return np.linalg.norm((u - v), ord=1)
# Loads the data into a np array, where each row corresponds to
# an image patch -- this step is sort of slow.
# Each row in the data is an image, and there are 400 columns.
def load_data(filename):
    return np.genfromtxt(filename, delimiter=',')

# Creates a hash function from a list of dimensions and thresholds.
def create_function(dimensions, thresholds):
    def f(v):
        boolarray = [v[dimensions[i]] >= thresholds[i] for i in range(len(dimensions))]
        return "".join(map(str, map(int, boolarray)))
    return f

# Creates the LSH functions (functions that compute L K-bit hash keys).
# Each function selects k dimensions (i.e. column indices of the image matrix)
# at random, and then chooses a random threshold for each dimension, between 0 and
# 255.  For any image, if its value on a given dimension is greater than or equal to
# the randomly chosen threshold, we set that bit to 1.  Each hash function returns
# a length-k bit string of the form "0101010001101001...", and the L hash functions
# will produce L such bit strings for each image.
def create_functions(k, L, num_dimensions=400, min_threshold=0, max_threshold=255):
    functions = []
    for i in range(L):
        dimensions = np.random.randint(low = 0,
                                       high = num_dimensions,
                                       size = k)
                                       thresholds = np.random.randint(low = min_threshold,
                                                                      high = max_threshold + 1,
                                                                      size = k)
                                       
        functions.append(create_function(dimensions, thresholds))
    return functions

# Hashes an individual vector (i.e. image).  This produces an array with L
# entries, where each entry is a string of k bits.
def hash_vector(functions, v):
    return np.array([f(v) for f in functions])

# Hashes the data in A, where each row is a datapoint, using the L
# functions in "functions."
def hash_data(functions, A):
    return np.array(list(map(lambda v: hash_vector(functions, v), A)))

# Retrieve all of the points that hash to one of the same buckets
# as the query point.  Do not do any random sampling (unlike what the first
# part of this problem prescribes).
# Don't retrieve a point if it is the same point as the query point.
def get_candidates(hashed_A, hashed_point, query_index):
    return filter(lambda i: i != query_index and \
                  any(hashed_point == hashed_A[i]), range(len(hashed_A)))

# Sets up the LSH.  You should try to call this function as few times as
# possible, since it is expensive.
# A: The dataset.
# Return the LSH functions and hashed data structure.
def lsh_setup(A, k = 24, L = 10):
    functions = create_functions(k = k, L = L)
    hashed_A = hash_data(functions, A)
    return (functions, hashed_A)

# Run the entire LSH algorithm
def lsh_search(A, hashed_A, functions, query_index, num_neighbors):
    hashed_point = hash_vector(functions, A[query_index, :])
    candidate_row_nums = get_candidates(hashed_A, hashed_point, query_index)
    distances = map(lambda r: (r, l1(A[r], A[query_index])), candidate_row_nums)
    best_neighbors = sorted(distances, key=lambda t: t[1])[:num_neighbors]
    
    return [t[0] for t in best_neighbors]

# Plots images at the specified rows and saves them each to files.
def plot(A, row_nums, base_filename):
    i=1
    for row_num in row_nums:
        patch = np.reshape(A[row_num, :], [20, 20])
        im = Image.fromarray(patch)
        if im.mode != 'RGB':
            im = im.convert('RGB')
        im.save(base_filename + "-" + str(row_num+1) +"-"+str(i)+ ".png")
        i=i+1

# Finds the nearest neighbors to a given vector, using linear search.
def linear_search(A, query_index, num_neighbors):
    candidate_row_nums = filter(lambda i:i!=query_index, range(np.size(A,0)))
    distances = map(lambda r: (r, l1(A[r], A[query_index])), candidate_row_nums)
    best_neighbors = sorted(distances, key=lambda t: t[1])[:num_neighbors]
    return [t[0] for t in best_neighbors]
# TODO: Write a function that computes the error measure
def error_measure(A,LSH,LN):
    sum2 = 0
    for j in range(1,11,1):
        sum1 = [0,0]
        for i in range(3):
            sum1[0] = sum1[0]+l1(A[100*j-1],A[LSH[3*(j-1)+i]])
            sum1[1] = sum1[1]+l1(A[100*j-1],A[LN[3*(j-1)+i]])
        sum2 = sum2+sum1[0]/sum1[1]
    return sum2/10
# TODO: Solve Problem 4
def problem4():
    file = open('/Users/heruojin/Desktop/patches.csv')
    A = load_data(file)
    #first question:average search time
    start0 = time.time()
    setup = lsh_setup(A, k = 24, L = 10)
    functions =  setup[0]
    hashed_A = setup[1]
    elapse0 = time.time()-start0
    start1 = time.time()
    for query_index in range(99,1000,100):
        lsh = lsh_search(A, hashed_A, functions, query_index, num_neighbors = 3)
    elapse1 = time.time()-start1
    print('average search time for lsh:',elapse1)
    start2 = time.time()
    for query_index in range(99,1000,100):
        l = linear_search(A, query_index, num_neighbors=3)
    elapse2 = time.time()-start2
    print('average time for linear search:',elapse2)
    #third question: plot row 100 and top 10 near neighbors using two methods
    #using the default L = 10, k = 24
    row = [99]
    plot(A, row, "/Users/heruojin/Desktop/100")
    lsh = lsh_search(A, hashed_A, functions, 99, num_neighbors = 10)
    plot(A, lsh, "/Users/heruojin/Desktop/lsh")
    ln = linear_search(A, 99, num_neighbors=10)
    plot(A, ln, "/Users/heruojin/Desktop/ln")
    # second question: compute the error rate
    error1 = []
    error2 = []
    for l in range(10,21,2):
        setup = lsh_setup(A, k = 24, L=l)
        functions =  setup[0]
        hashed_A = setup[1]
        LSH=[]
        LN=[]
        for query_index in range(99,1000,100):
            lsh = lsh_search(A, hashed_A, functions, query_index, num_neighbors = 3)
            ln = linear_search(A, query_index, num_neighbors=3)
            LSH=LSH+lsh
            LN=LN+ln
        error1 = error1+[error_measure(A,LSH,LN)]
    for k0 in range(16,25,2):
        setup = lsh_setup(A, k = k0, L=10)
        functions =  setup[0]
        hashed_A = setup[1]
        LSH=[]
        LN=[]
        for query_index in range(99,1000,100):
            lsh = lsh_search(A, hashed_A, functions, query_index, num_neighbors = 3)
            ln = linear_search(A, query_index, num_neighbors=3)
            LSH=LSH+lsh
            LN=LN+ln
        error2 = error2+[error_measure(A,LSH,LN)]
    print(error1)
    print(error2)
    t = [10,12,14,16,18,20]
    s = error1
    fig, ax = plt.subplots()
    ax.plot(t, s)
    ax.set(xlabel='L', ylabel='error', title='error value vs. L')
    ax.grid()
    plt.show()

    t = [16,18,20,22,24]
    s = error2
    fig, ax = plt.subplots()
    ax.plot(t, s)
    ax.set(xlabel='K', ylabel='error', title='error value vs. K')
    ax.grid()
    plt.show()




#### TESTS #####

class TestLSH(unittest.TestCase):
    def test_l1(self):
        u = np.array([1, 2, 3, 4])
        v = np.array([2, 3, 2, 3])
        self.assertEqual(l1(u, v), 4)

    def test_hash_data(self):
        f1 = lambda v: sum(v)
        f2 = lambda v: sum([x * x for x in v])
        A = np.array([[1, 2, 3], [4, 5, 6]])
        self.assertEqual(f1(A[0,:]), 6)
        self.assertEqual(f2(A[0,:]), 14)

        functions = [f1, f2]
        self.assertTrue(np.array_equal(hash_vector(functions, A[0, :]), np.array([6, 14])))
        self.assertTrue(np.array_equal(hash_data(functions, A), np.array([[6, 14], [15, 77]])))

    ### TODO: Write your tests here (they won't be graded, 
    ### but you may find them helpful)
    def 

if __name__ == '__main__':
#    unittest.main() ### TODO: Uncomment this to run tests
    problem4()
