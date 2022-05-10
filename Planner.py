from asyncio import DatagramTransport
import numpy as np

def build(initialPath, discretization, originXLocal):
    #All the variables are initialized 
    currentPosition = initialPath[0]
    lastPosition = initialPath[0]

    #Unit vector of XLocal orientation is calculated
    unitVectorXLocal = unit_vector(originXLocal)

    currentOrientation = unitVectorXLocal
    plannedPath = [currentPosition] #Array to save each point of the planned path
    plannedOrientation = [unitVectorXLocal] #Array to save each orientation of the planned path
    plannedFinalPoints = [currentPosition]
    rotArray = [] #Array to save each rotation matrix between each vectors of the planned path
    idealUnitVector = unitVectorXLocal

    #First movement is referred to the movement from Origin to point A where the orientation must be the initial one
    isFirstMovement = True

    for i in initialPath:
        #There are two different distances: From current position of the last movement to next ideal point and
        # from the last ideal point to the next ideal point
        #Both are calculated as the normalization of the diference between two points: sqrt((bx - ax)^2 + (by - ay)^2 + (bz - az)^2)
        realDistance = np.linalg.norm(i-currentPosition)
        idealDistance = np.linalg.norm(i-lastPosition)

        if realDistance > 0: #The first point of the path is the distance with itself
            # The number of segments is rounded to minimize the error            
            numSegments = round(realDistance/discretization)
            realUnitVector = (i - currentPosition) / realDistance

            #During the first movement approaching to point A the orientation is maintained
            if not isFirstMovement:
                idealUnitVector = (i - lastPosition) / idealDistance
            isFirstMovement = False
            
            #Each point, orientation vector and rotation matrix is saved
            rotArray.append(rotation_matrix(currentOrientation, idealUnitVector))
            for j in range(numSegments):
                currentPosition = nextPosition(currentPosition, discretization, realUnitVector)
                plannedPath.append(currentPosition)
                plannedOrientation.append(idealUnitVector)
                #As is specified in the instructions the orientation of the link is the nearest segment orientation of the ideal path
                currentOrientation = idealUnitVector
            plannedFinalPoints.append(currentPosition)
        lastPosition = i

    plannedPath = np.array(plannedPath)
    plannedFinalPoints = np.array(plannedFinalPoints)
    plannedOrientation = np.array(plannedOrientation)
    rotArray = np.array(rotArray)

    return plannedPath, plannedFinalPoints, plannedOrientation, rotArray

def nextPosition(currentPosition, discretization, unitVector):
    return currentPosition + discretization * unitVector

def rotation_matrix(vec1, vec2):
    #Normalize both vectors
    a, b = (unit_vector(vec1)).reshape(3), (unit_vector(vec2)).reshape(3)
    #Cross product
    v = np.cross(a, b)
    #Dot product
    c = np.dot(a, b)
    #Normalize the cross vector
    s = np.linalg.norm(v)
    #Finally the rotation matrix is built
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    s2 = s ** 2 if s > 0 else 1
    rotation_matrix = np.eye(3) + kmat + np.square(kmat) * ((1 - c) / s2)
    return rotation_matrix

def unit_vector(vector):
    print(vector, vector / np.linalg.norm(vector))
    return vector / np.linalg.norm(vector)