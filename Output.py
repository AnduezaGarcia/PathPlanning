import matplotlib.pyplot as plt
import numpy as np
import string as st

def plot(idealPath, plannedPath, plannedOrientation):
    #Ideal path points labels:
    labels = np.array(["Origin"])
    alphabet = list(st.ascii_uppercase)
    labels = np.append(labels, alphabet[0 : len(idealPath)-1])

    #Ideal and planned path are separated in three coordinate arrays
    x_values = np.array([])
    y_values = np.array([])
    z_values = np.array([])
    for i in idealPath:
        x_values = np.append(x_values, i[0])
        y_values = np.append(y_values, i[1])
        z_values = np.append(z_values, i[2])

    x_plann = np.array([])
    y_plann = np.array([])
    z_plann= np.array([])
    for i in plannedPath:
        x_plann = np.append(x_plann, i[0])
        y_plann = np.append(y_plann, i[1])
        z_plann = np.append(z_plann, i[2])

    #Plot 
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111, projection='3d')
    
    j = 0
    for i in plannedPath:
        #Orientation arrows
        ax.quiver(*i,*plannedOrientation[j]*10, color='grey')
        j += 1
    #Ideal and planned path points
    ax.scatter(x_values, y_values, z_values, marker="x", c="red")
    ax.scatter(x_plann, y_plann, z_plann, marker="+", c="green")
    #Ideal and planner path lines
    ax.plot(x_values, y_values, z_values, c="red")
    ax.plot(x_plann, y_plann, z_plann, c="green")

    #Ideal path labels
    for i, labels in enumerate(labels):
        ax.text(x_values[i], y_values[i], z_values[i], '%s' % (labels), size=10, zorder=1, color='r')

    ax.set_xlabel("X (cm)")
    ax.set_ylabel("Y (cm)")
    ax.set_zlabel("Z (cm)")

    plt.show()

def printResult(idealPath, plannedFinalPoints,  plannedRotMatrix):
    np.set_printoptions(precision=2)

    plannedFinalPoints = plannedFinalPoints
    plannedRotMatrix = plannedRotMatrix

    pointLabels = np.array(["Origin"])
    alphabet = list(st.ascii_uppercase)
    pointLabels = np.append(pointLabels, alphabet[0 : len(idealPath)-1])

    print("")
    print("Results:")
    print("Ideal path vs Real path:")
    count = 0
    for i in idealPath:
        print(pointLabels[count], "Ideal: ", i, " - Planned: ", plannedFinalPoints[count])
        print(" Error: ", np.abs(np.linalg.norm(i) - np.linalg.norm(plannedFinalPoints[count])), "cm")
        count += 1
    
    print("")
    print("Rotation Matrix:")
    count = 0
    for i in plannedRotMatrix:
        if not np.array_equal(np.eye(3), i):
            print(pointLabels[count], ":")
            print(i)
        count += 1

