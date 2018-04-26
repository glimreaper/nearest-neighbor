import argparse
import os
import sys
import time
import profile
from operator import itemgetter 

# Command line arguments
parser=argparse.ArgumentParser(description='Calculate the nearest two points on a plan')
parser.add_argument('--algorithm',default='a',\
    help='Algorithm: Select the algorithm to run, default is all. (a)ll, (b)ruteforce only or (d)ivide and conquer only')
parser.add_argument('-v','--verbose',action='store_true')
parser.add_argument('--profile',action='store_true')
parser.add_argument('filename',metavar='<filename>',\
    help='Input dataset of points')

def dist(p0,p1):
    return (((p0[0] - p1[0])**2) + ((p0[1] - p1[1])**2))**.5
#Divide and conquer version of the nearest neighbor algorithm
#Input: points := unsorted array of (x,y) coordinates
#Output: tuple of smallest distance and coordinates (distance,(x1,y1),(x2,y2))
def closestY(points, size, minDist):
    min = minDist[0]
    point1 = minDist[1]
    point2 = minDist[2]
    points.sort(key=itemgetter(1))
    for i in range(size):
        for j in range(i+1,size):
            if (dist(points[i], points[j]) < min):
                min = dist(points[i], points[j])
                point1 = points[i]
                point2 = points[j]
    if point1[0] > point2[0]:
        temp = point1
        point1 = point2
        point2 = temp
    return (min, point1, point2) 

def divAndConquerRecursive(points):

    if len(points) <= 3:
        return bruteForceNearestNeighbor(points)
    
    midIndex = int(len(points)/2)
    midPoint = points[midIndex]
    leftHalf = divAndConquerRecursive(points[:midIndex])
    rightHalf = divAndConquerRecursive(points[midIndex:])
    if leftHalf[0] < rightHalf[0]:
        smaller = leftHalf
    else:
        smaller = rightHalf
    #creating an array that holds points whos distance to the line in the middle point is lower than 'smaller' variable above
    middleHalf = []
    i = 0
    for x in range(len(points)):
        if abs(points[x][0] - midPoint[0]) < smaller[0]:
            middleHalf.append(points[x])
            i = i+1
    if smaller[0] < closestY(middleHalf, i, smaller)[0]:
        return smaller
    else:
        return closestY(middleHalf, i, smaller) 

def divideAndConquerNearestNeighbor(points):
    points.sort(key=itemgetter(0))
    results = divAndConquerRecursive(points)
    #TODO: Complete this function

    print("Divide and Conquer algorithm is complete")
    return (results[0],results[1],results[2])
#end def divide_and_conquer(points):

#Brute force version of the nearest neighbor algorithm
#Input: points := unsorted array of (x,y) coordinates 
#   [(x,y),(x,y),...,(x,y)]
#Output: tuple of smallest distance and coordinates (distance,(x1,y1),(x2,y2))
def bruteForceNearestNeighbor(points):
    minimum_distance = 0
    point1 = (-1, -1)
    point2 = (-1, -1)
    #TODO: Complete this function
    minimum_distance = dist(points[0], points[1])
    point1 = points[0]
    point2 = points[1]
    for x in range(len(points)-1):
        for y in range(x+1, len(points)):
            if dist(points[x], points[y]) < minimum_distance:
                minimum_distance = dist(points[x], points[y])
                point1 = points[x]
                point2 = points[y]
            #endif
        #endfor
    #endfor
    if point1[0] > point2[0]:
        temp = point1
        point1 = point2
        point2 = temp
    print("Brute force algorithm is complete")
    return (minimum_distance,point1,point2)
#end def brute_force_nearest_neighbor(points):

#Parse the input file
#Input: filename := string of the name of the test case
#Output: points := unsorted array of (x,y) coordinates
#   [(x,y),(x,y),...,(x,y)]
def parseFile(filename):
    points = []
    f = open(filename,'r') 
    lines = f.readlines()
    for line in lines:
        coordinate = line.split(' ')
        points.append((float(coordinate[0]),float(coordinate[1])))
    return points
#end def parse_file(filename):

#Main
#Input: filename  := string of the name of the test case
#       algorithm := flag for the algorithm to run, 'a': all 'b': brute force, 'd': d and c
def main(filename,algorithm):
    points = parseFile(filename)
    result = bruteForceResult = divideAndConquerResult = None
    if algorithm == 'a' or algorithm == 'b':
        #TODO: Insert timing code here
        bruteForceResult = bruteForceNearestNeighbor(points)
    if algorithm == 'a' or algorithm == 'd':
        #TODO: Insert timing code here
        divideAndConquerResult = divideAndConquerNearestNeighbor(points)
    if algorithm == 'a': # Print whether the results are equal (check)
        if args.verbose:
            print('Brute force result: '+str(bruteForceResult))
            print('Divide and conquer result: '+str(divideAndConquerResult))
            print('Algorithms produce the same result? '+str(bruteForceResult == divideAndConquerResult))
        result = bruteForceResult if bruteForceResult == divideAndConquerResult else ('Error','N/A','N/A')
    else:
        print("hijoj")  
        result = bruteForceResult if bruteForceResult is not None else divideAndConquerResult
    with open(os.path.splitext(filename)[0]+'_distance.txt','w') as f:
        f.write(str(result[1])+'\n')
        f.write(str(result[2])+'\n')
        f.write(str(result[0])+'\n')
#end def main(filename,algorithm):

if __name__ == '__main__':
    args=parser.parse_args()
    main(args.filename,args.algorithm)
#end if __name__ == '__main__':
