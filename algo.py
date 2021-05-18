"""Prodyct sum of arrays python 
"""
def MaxSum(arr) -> int :
    """
    Returns -1 si c'est pas possible de calculer le tout
    max_sum si c'est possible de calculer
    """
    max_sum = -50000 
    R = len(arr)
    C = len(arr[0])
    if(R < 3 or C < 3):
        return -1
    for i in range(0, R-2):
        for j in range(0, C-2):
                     
            SUM = (arr[i][j] + arr[i][j + 1] +
                   arr[i][j + 2]) + (arr[i + 1][j + 1]) +
                                          (arr[i + 2][j] +
                    arr[i + 2][j + 1] + arr[i + 2][j + 2])
 
            if(SUM > max_sum):
                max_sum = SUM
            else:
                continue
 
    return max_sum
