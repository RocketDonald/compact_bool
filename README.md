# compact_bool
This library provides a space-saving solution for storing 2D boolean array / matrix.

This solution takes the advantage of 2-fold rotational symmetric property of square,  
such that only half the size is needed for storing such square matrix.

## Usage:
Download the python file and save it at the working directory.  
Import this library:    
`import compact_bool`

Create object and initiate all values  
```
size = 5
mat = CompactBoolMatrix(size)  
mat.all_false()
```

*all_false() and all_true() are used to initiate the values*

Change value  
```
mat.set_true(4, 3)  
mat.set_false(2, 4)  
mat.switch(1, 0) 
```

*switch(x, y) change the value to opposite boolean value*  

Get value  
```
a = mat.get(4, 0)  
    for i in range(size):  
        for j in range(size):  
            print(mat.get(i, j)
```

    
## Algorithm:
### Space complexity:  
-   Split a n*n sized matrix into 4 domains ==> **1/4 space**
-   using ctypes.c_int8 to represent 16 different cases of bool value combination in 4 domains  
--> 1 byte c_int8 representing 1 cell == representing 4 domains
-   Recommended to use this library no matter what size the matrix is  
--> ***size of a 5x5 CompactBoolMatrix = 36 bytes*** vs ***size of bool[5][5] = 120 bytes***
    
### Time complexity:
-   The process for looking up values will still remain O(1)
-   The process of changing values is slightly slower than changing values in a normal matrix, but it still remains O(1)

- Split the square matrix into 4 domains:  
```
+-----+-----+  
|  0  |  1  |  
+-----+-----+  
|  2  |  3  |  
+-----+-----+
```

- Identify 16 different cases of boolean combinations  
e.g.:  
```
Case 0:  
+-----+-----+  
|  X  |  X  |  
+-----+-----+  
|  X  |  X  |  
+-----+-----+  

Case 5:  
+-----+-----+  
|  O  |  O  |  
+-----+-----+  
|  X  |  X  |  
+-----+-----+

Case 15:  
+-----+-----+  
|  O  |  O  |  
+-----+-----+  
|  O  |  O  |  
+-----+-----+
```
 
*For more detailed list of combinations, please see the comment section of compact_bool.py*

- Using truth table and value table to change and get value in O(1)
