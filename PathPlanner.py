import random
import numpy as np
import string as st

import Planner
import Output

def main():
    discretization = 10 #cm
    maxRange = 500
    originXLocal = np.array([])
    idealPath = np.array([])
    
    #Get input data
    randomPoints = input("Do you want random points to make the path? (yes/no)")
    if randomPoints == "no":
        numberOfPoints = int(input("Enter number of points: "))
        x,y,z = input("Enter origin coordinate 'x y z': ").split()
        originPosition = np.array([int(x),int(y),int(z)])

        idealPath = originPosition
        idealPath = np.resize(idealPath,(1,3))
        alphabet = list(st.ascii_uppercase)
        
        for i in range(numberOfPoints):
            x,y,z = input("Enter point " + alphabet[i] + " 'x y z': ").split()
            nextPoint = np.array([[int(x),int(y),int(z)]])
            idealPath = np.append(idealPath, nextPoint, axis=0)

        x, y, z = input("Enter XLocal orientation 'x y z': ").split()
        originXLocal = np.array([int(x),int(y),int(z)])

    elif randomPoints == "yes":
        originPosition = np.array([random.randint(0,maxRange),random.randint(0,maxRange),random.randint(0,maxRange)])
        idealPath = np.array(originPosition)
        idealPath = np.resize(idealPath,(1,3))

        for i in range(random.randint(5,10)):
            idealPath = np.append(idealPath,np.array([[random.randint(0,maxRange),random.randint(0,maxRange),random.randint(0,maxRange)]]), axis=0)
        originXLocal = np.array([random.randint(0,10),random.randint(0,10),random.randint(0,10)])
        
    else:
        print("error")

    #Build planner path, final points of each segment planned, planned orientation and planned rotation matrix
    plannedPath, plannedFinalPoints, plannedOrientation, plannedRotMatrix = Planner.build(idealPath, discretization, originXLocal)

    #Output reults and plot
    Output.printResult(idealPath, plannedFinalPoints, plannedRotMatrix)
    Output.plot(idealPath, plannedPath, plannedOrientation)
    
if __name__ == "__main__":
    main()