# n-way-cache-simulator
implementation of n-way set associative cache with python3. Note that it have overflow issue in LRU part.

# Issues to solve
## LRU part
 - i just set recentlyUsed variable to zero if cache finds that block. and all other block's recentlyUsed variable are plused as 1.
  - so it has overflow 

# and other many performance issues exists...
