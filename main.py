
class Bloom:
 """ Bloom Filter """
 def __init__(self,m,k,hash_fun):
  """
   m, size of the vector
   k, number of hash fnctions to compute
   hash_fun, hash function to use
  """
  self.m = m
  # initialize the vector 
  # (attention a real implementation 
  #  should use an actual bit-array)
  self.vector = [0]*m
  self.k = k
  self.hash_fun = hash_fun
  self.data = {} # data structure to store the data
  self.false_positive = 0

 def insert(self,key,value):
  """ insert the pair (key,value) in the database """
  self.data[key] = value
  for i in range(self.k):
   self.vector[self.hash_fun(key+str(i)) % self.m] = 1

 def contains(self,key):
  """ check if key is cointained in the database
      using the filter mechanism """
  for i in range(self.k):
   if self.vector[self.hash_fun(key+str(i)) % self.m] == 0:
    return False # the key doesn't exist
  return True # the key can be in the data set

 def get(self,key):
  """ return the value associated with key """
  if self.contains(key):
   try:
    return self.data[key] # actual lookup
   except KeyError:
    self.false_positive += 1

import hashlib

def hash_f(x):
 x=x.encode('utf-8')
 h = hashlib.sha256(x) # we'll use sha256 just for this example
 return int(h.hexdigest(),base=16)

b = Bloom(100,10,hash_f)
b.insert('this is a key','this is a value')
print(b.get('this is a key'))

import random

def rand_data(n, chars):
 """ generate random strings using the characters in chars """
 return ''.join(random.choice(chars) for i in range(n))

def bloomTest(m,n,k):
 """ return the percentage of false positive """
 bloom = Bloom(m,k,hash_f)
 # generating a random data
 rand_keys = [rand_data(10,'abcde') for i in range(n)]
 # pushing the items into the data structure
 for rk in rand_keys:
  bloom.insert(rk,'data')
 # adding other elements to the dataset
 rand_keys = rand_keys + [rand_data(10,'fghil') for i in range(n)]
 # performing a query for each element of the dataset
 for rk in rand_keys:
  bloom.get(rk)
 return float(bloom.false_positive)/n*100.0

m = 10000
n = 1000
k = range(1,64)
perc = [bloomTest(m,n,kk) for kk in k] # k is varying

# plotting the result of the test
from pylab import plot,show,xlabel,ylabel
plot(k,perc,'--ob',alpha=.7)
ylabel('false positive %')
xlabel('k')
show()
