def unique(string):
    set_string = set(string)
    return len(set_string) == len(string)

import random

import time
import math


def initGrid(inputGrid):
    grid = {}
    width, height = len(inputGrid[0]), len(inputGrid)
    for y in xrange(len(inputGrid)):
        for x in xrange(len(inputGrid[0])):
            grid[(x, y)] = Node(inputGrid[y][x])
    return grid, width, height

def search(inputGrid, start, end):
    grid, width, height = initGrid(inputGrid)
    return _search(grid, start, end, width, height)

def searchWaypoints(inputGrid, waypoints):
    path = []
    gridInfo = {}
    totalTime = 0
    
    grid, width, height = initGrid(inputGrid)
    
    for index in xrange(1, len(waypoints)):
        subPath, subInfo, subTime = _search(grid, waypoints[index - 1], waypoints[index], width, height)
        totalTime += subTime
        path.extend(subPath[:-1])
        gridInfo.update(subInfo)

    return path, gridInfo, totalTime

def _search(grid, start, end, width, height):  # works in O((width * height)^0.5) = O(n^2)
    time1 = time.time()
    
    closedset = set()
    openset = {start}

    grid[start].g = 0
    grid[start].h = heuristic(start, end)

    while len(openset) > 0:
        current = smallestF(grid, openset)

        if current == end:
            time2 = time.time()
            return traceParents(grid, start, end), grid, time2 - time1

        openset.remove(current)
        closedset.add(current)

        for neighbor in neighbors(current, width, height):
            if neighbor in closedset or grid[neighbor].blocked:
                continue
            gscore = grid[current].g + movementCost(current, neighbor)

            if (neighbor not in openset) or (gscore < grid[neighbor].g):
                grid[neighbor].parent = current
                grid[neighbor].g = gscore
                grid[neighbor].h = heuristic(neighbor, end)
                if neighbor not in openset:
                    openset.add(neighbor)
    time2 = time.time()
    print "No path found!"
    return traceParents(grid, start, current), grid, time2 - time1

def dictToList(grid):
    lenX = max(grid.keys(), key=lambda element: element[0])[0] + 1
    lenY = max(grid.keys(), key=lambda element: element[1])[1] + 1
    output = [[None for _ in xrange(lenX)] for _ in xrange(lenY)]
    for x in xrange(lenX):
        for y in xrange(lenY):
            output[y][x] = grid[(x, y)]
    return output

def printGrid(grid):
    lenX = max(grid.keys(), key=lambda element: element[0])[0] + 1
    lenY = max(grid.keys(), key=lambda element: element[1])[1] + 1
    print "{"
    for x in xrange(lenX):
        for y in xrange(lenY):
            print "\t%3.2f" % grid[(x, y)].f,
        print
    print "}"


#def neighbors(current, width, height):
#    adjacent = []
#    for x in [-1, 0, 1]:
#        for y in [-1, 0, 1]:
#            gridX, gridY = x + current[0], y + current[1]
#            if (x, y) != (0, 0) and 0 <= gridX < width and 0 <= gridY < height:
#                adjacent.append((gridX, gridY))
#
#    return adjacent

def neighbors(current, width, height):
    adjacent = []
    for [x, y] in [[0, 1], [1, 0]]:
        gridX, gridY = x + current[0], y + current[1]
        if (x, y) != (0, 0) and 0 <= gridX < width and 0 <= gridY < height:
            adjacent.append((gridX, gridY))

    return adjacent

def smallestF(grid, indices):
    minLoc = None
    minF = Node
    for index in indices:
        if grid[index].f < minF or minF is None:
            minLoc = index
            minF = grid[index].f
    return minLoc


def traceParents(grid, start, end):
    current = end
    path = [current]
    while current != start:
        current = grid[current].parent
        path.append(current)
    return path[::-1]


def heuristic(index, end):
    return abs(index[0] - end[0]) + abs(index[1] - end[1])


def movementCost(current, adjacentIndex):
    x, y = adjacentIndex[0] - current[0], adjacentIndex[1] - current[1]
    if abs(x) == abs(y) == 1:
        return 14
    else:
        return 10


def movementCostHeading(current, adjacentIndex, heading):
    # amplitude * math.sin(heading - phase - math.pi/2) + offset
    x, y = adjacentIndex[0] - current[0], adjacentIndex[1] - current[1]
    return 15.0 * math.sin(heading - math.atan2(y, x) - math.pi) + 25.0


class Node(object):
    def __init__(self, blocked=False):
        self.g = 0
        self.h = 0
        self.blocked = blocked
        self.parent = None
        self.heading = None

    @property
    def f(self):
        return self.g + self.h


def make_slope(width, height):
    slope = []
    for index in xrange(width):
        slope.append([])
        for _ in xrange(height):
            if random.random() > 0.2:
                slope[index].append(0)
            else:
                slope[index].append(1)
    slope[0][0] = 0
    slope[width - 1][height - 1] = 0
    return slope

def print_slope(slope):
    for row in xrange(len(slope)):
        print "[",
        for col in xrange(len(slope[0])):
            print slope[row][col],
        print "]"

width, height = 200, 200
slope1 = make_slope(width, height)
print_slope(slope1)
result = search(slope1, (0, 0), (width - 1, height - 1))
print result[0]
# result[1] is meant for drawing the resulting path and grid
print result[2]


