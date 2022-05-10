# Path Planning Technical Challenge - Víctor Andueza
This repository is the solution to the problem proposed as 'Path Planning Technical Challenge'

## Initial Assumptions

- The ideal path and the planned path will be in 3 dimensions.
- The acceptable desviation depends on the length of the ideal path segments.
- The range has been set between 0 to 500 cm in each dimension
- Discretization distance is fixed to 10cm, not being possible to reduce this distance
- The pose of the robot link (XLocal orientation) starts being parallel once the first point (A) has been reached.
- The system knows the ideal path before start the movement.
- Two different ways to use the system: 

	-Random origin, path points (from 5 to 10) and initial XLocal orientation
	
	-Choosing the points and orientation manually

## Usage
- Random use

`$ python3 PathPlanner.py`

`Do you want random points to make the path? (yes/no)`

`$ yes`

- Manual use

`$ python3 PathPlanner.py`

`Do you want random points to make the path? (yes/no)`

`$ no`

`Enter number of points:`

`$ 3`

`Enter origin coordinate 'x y z':`

`$ 0 0 0`

`Enter point A 'x y z':`

`$ 100 0 0`

`Enter point B 'x y z':`

`$ 100 100 0`

`Enter point C 'x y z':`

`$ 100 100 100`

`Enter XLocal orientation 'x y z': `

`$ 1 1 1`

## Output
### Console output
First results is a comparison between ideal path points and last planned point of each segment. 
A local error is shown. This is the largest error produced at each corner.

`Results:`

`Ideal path vs Real path:`

`Origin Ideal:  [0 0 0]  - Planned:  [0. 0. 0.]`

 `Error:  0.0 cm`
 
`A Ideal:  [100   0   0]  - Planned:  [100.   0.   0.]`

`Error:  0.0 cm`

`B Ideal:  [100 100   0]  - Planned:  [100. 100.   0.]`

 `Error:  0.0 cm`
 
`C Ideal:  [100 100 100]  - Planned:  [100. 100. 100.]`

 `Error:  0.0 cm`
 
 
 After that, each rotation matrix is shown:
 
`Rotation Matrix:`

`A :`

`[[ 1.   -0.37  0.  ]`

 `[ 0.79  1.    0.79]`
 
 `[ 0.   -0.37  1.  ]]`
 
`B :`

`[[1. 0. 0.]`

` [0. 1. 0.]`

 `[0. 2. 1.]]`
 
### Plot output

https://drive.google.com/file/d/1ZFdYiLRlHJZLzMM9Gtm9CkgL2bgDQFNz/view

https://drive.google.com/file/d/1pMi6Xk-kIr58JX0E2BW3B3m2kNVWD04s/view)

- Red path and points: Ideal path
- Green path and points: Planned path and points
- Grey arrows: robot link XLocal orientation

## General results considerations

- As was consired before, discretization has been set at 10cm, not being possible to reduce it. So, due to that reason,the corner error is the largest of each segment

- Initial XLocal orientation is maintained until point A is reached 

https://drive.google.com/file/d/1SLwCqa6-bSRH2YZao2zMS50Ty-pf3PJv/view

- XLocal orientation is maintained parallel to the ideal path segment

https://drive.google.com/file/d/1mqZTvFkhFX1KYGe6IayFD_FomaT4Tgn-/view

(This is hard to see on the graph when the path has long segments)

### Planner algorithm

- The error is not cumulative because in each segment the distance to travel is recalculated

		for i in initialPath:
    		realDistance = np.linalg.norm(i-currentPosition)
    		idealDistance = np.linalg.norm(i-lastPosition)
			
- The number of segments is rounded to minimize the error

		numSegments = round(realDistance/discretization)
		
- Two different unit vectors are calculated. One for the path and another for the XLocal orientation

		realUnitVector = (i - currentPosition) / realDistance
        if not isFirstMovement:
        	idealUnitVector = (i - lastPosition) / idealDistance
        isFirstMovement = False
		
(Initial XLocal orientation is maintained until point A is reached )

- Rotation matrix is saved in an array for each ideal segment

		rotArray.append(rotation_matrix(currentOrientation, idealUnitVector))
		
		
- Each planned position is calculated and saved in an array

		for j in range(numSegments):
                currentPosition = nextPosition(currentPosition, discretization, realUnitVector)
                plannedPath.append(currentPosition)
				
		def nextPosition(currentPosition, discretization, unitVector):
			    return currentPosition + discretization * unitVector
				
- Each planned segment XLocal orientation is equal to ideal orientation segment path

		currentOrientation = idealUnitVector

### Improvement attempts

To minimize the deviation of the trajectory from the point of maximum error to the next ideal point, a solution has been tried to recalculate the first point of the next ideal segment, as shown in the image:

https://drive.google.com/file/d/1hsMQyelZASHzi8NI0vK_rXx2GBuHZ9oc/view

https://drive.google.com/file/d/1lencdL7x_w_hse9MZ-A8tyFtU3eu_meK/view

This development is under analysis and is not included on this solution.


## Tests

Different unit tests have been developed in order to mantain the consistency and reliability of the code. 

- Build Path test -> Test the main function: From the ideal path, the discretization and the XLolcal orientation to the planned path, the final points of each segment, the planned orientation and the rotation matrix array

- Next Position test -> Test the next position calculation: From the current position, the discretization and the unit vector to the next position

- Rotation Matrix test ->Test the rotation matrix calculation: From two vectors (current orientation and next orientation) to rotation matrix

- Unit Vector test -> Test the unit vector calculation: From any vector to the unit vector

### Usage

`$ python3 -m unittest test_planner.py`

`....`

`----------------------------------------------------------------------`

`Ran 4 tests in 0.002s`

`OK`


## Video

https://drive.google.com/file/d/1Bsvp46Bf7XsVuIcawokUsynNc-BC9qcs/view
