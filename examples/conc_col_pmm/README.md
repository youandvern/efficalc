# Scope
This program supports the analysis of rectangular, symmetric, perimeter-reinforced concrete columns in accordance with ACI 318-19 and using the exact capacity method. 

# Program Features
- **PMM Diagrams**: Creates 3D Axial-Moment-Moment interaction diagrams. 
- **PM Diagrams**: For each load case entered, creates a 2D PM interaction diagram including the location of the load case on the PM axes relative to the capacity curve.  
- **Demand-to-Capacity Ratios (DCRs)**: Calculates the PM Vector DCR (defined below) for each load case entered.
- **Calculation Reports**: Generates a calc report for the column showing the full capacity calculation for all selected load cases, including cross-section diagrams, code references, and DCR calculations. 

# Definitions and Theory
- **Axial force ($P$)**: The force in the column parallel to its length, where a positive value indicates compression. 
- **Ultimate axial force ($P_u$)**: The axial force applied to a column (typically calculated using a factored load combination).  
- **Nominal axial capacity ($P_n$)**: The calculated axial load capacity, without a safety factor. 
- **Moments ($M_x$, $M_y$)**: These measure moments about axes indicated by their subscripts, i.e., positive $M_{x}$ indicates compression in the +y region and positive $M_{y}$ indicates compression in the +x region. 
- **Ultimate moments ($M_{ux}$, $M_{uy}$)**: The moments applied to a column (typically calculated using a factored load combination).  
- **Nominal moment capacity ($M_{nx}$, $M_{ny}$)**: The calculated moment capacities, without a safety factor. 
- **Load case**: A given combination of axial load and moments ($P_{u}$, $M_{ux}$, $M_{uy}$).
- **Eccentricity ($e_x$, $e_y$)**: This is the location that a load would have to have on the x or y axis to produce an equivalent moment to the moment at the given load case with the same axial load.

$$
e_x=\frac{M_x}{P}
$$

$$
e_y=\frac{M_y}{P}
$$
- **Eccentricity angle (λ)**: The angle taken clockwise from the positive y-axis to a vector from the column centroid to the location where an equivalent axial load could be applied that would be equivalent to the combination of $P$, $M_{x}$, and $M_{y}$ for a given load case.

$$
\lambda = \arctan\left(\frac{e_x}{e_y}\right) = \arctan\left(\frac{M_{ny}}{M_{nx}}\right)
$$
- **Neutral axis**: The line across the column section on which strain is assumed to be 0. 
- **Neutral axis angle (θ)**: The angle from the positive x-axis to the neutral axis. Counter-clockwise is taken as positive, and the region of compression is on the side of the neutral axis further counter-clockwise than θ. The neutral axis angle can be understood in the graphic below, which shows the neutral axis as a dashed line and the equivalent compression zone as gray. 
<img src="https://github.com/janderson4/efficalc/blob/main/examples/conc_col_pmm/images/ColumnNA-cropped.svg" width="350">

- **Neutral axis depth (c)**: The distance from the neutral axis to a parallel line passing through the column corner in maximum compression. 
- **PMM diagram**: The 3D plot of the PMM surface, which describes the capacity of a given column in $P$, $M_x$, $M_y$ (any load case whose plot falls inside the PMM surface is within capacity, and any load case falling outside the PMM surface exceeds capacity). 
- **PM diagram**: The 2D plot of a cut of the PMM surface at a given eccentricity angle (λ). This diagram is useful for visualizing the capacity of the column relative to demand for a given load case. 
- **PM Vector DCR**: The ratio of the length of the demand vector (in PMM space) to the length of a parallel vector beginning at the origin and continuing until it reaches the capacity surface. 
- **Axial to Moment Angle (α)**: This is a custom-defined variable used in this program that describes the height of a load case above the $M_x-M_y$ plane. It is a proxy for the inverse of the eccentricity resultant.

$$
\alpha = \arctan\left(\frac{P_n}{\sqrt{M_{nx}^2+M_{ny}^2}}\right)
$$

It seems intuitive that the neutral axis should be parallel to the axis of the resultant moment, which would mean the relation λ=-θ would hold. However, this holds only in special cases, which means determining the neutral axis angle required to produce a given eccentricity is not straightforward. For more information see [1]. 

# How It Works
- **PMM Diagrams**: The PMM diagrams created by this program compose a mesh of capacity points which are evenly spaced in both the vertical load ($P$) direction and in their angles about the origin (λ). To achieve this even spacing, it is necessary to find points on the PMM surface that have a given combination of λ and $P$. $P$ tends to increase as the neutral axis depth increases and λ tends to increase as θ decreases, but neither of the output variables (λ and $P$) can be calculated in closed form. This means that the domain of the two input variables (θ and c) must be searched to find the target point on the PMM diagram. The search algorithm is [below](#search-algorithm). 
- **PM Diagrams**: This program uses sets of control points interpolated from the points on the PMM diagram to create PM diagrams for each load case. 
- **DCRs**: These are calculated by finding a point on the PMM surface such that a vector from the origin to that point is parallel to a vector from the origin to the PMM point for the given load case and then taking a ratio of the lengths of the two vectors. To find the capacity point, a search of the PMM surface is again required, but in this case, the target variables are λ and α. Searching this domain is equivalent to searching in the domain of spherical coordinates. Unlike in the case of the point search for the PMM diagram, this search is performed on the fully-factored PMM surface (including the plateau). The search algorithm is [below](#search-algorithm).
- **Calculation Reports**: The program uses the efficalc library to generate calc reports. 

# Search Algorithm
## Summary
In both search problems, there are two input and two output variables and the target output variables are known. The algorithm is given a starting point, and it proceeds as follows:
1.	Calculate first derivatives—the full 4x4 Jacobian—at the current input point using finite differences. 
2.	Use the derivatives as linear approximations for the two output variables as functions of the two variables and solve for the input point at which both output variables are expected to equal their target values. 
3.	Move to the input point calculated in (2) and repeat from (1).

## Update Method
For simplicity, assume that the two input variables are x and y and the two output functions are f and g, where f and g have been shifted so that the target outputs are f=0 and g=0. Then the Jacobian is as follows:

$$
J =
\begin{bmatrix}
\frac{\partial f}{\partial x} & \frac{\partial f}{\partial y} \\
\frac{\partial g}{\partial x} & \frac{\partial g}{\partial y}
\end{bmatrix}
$$

Then the linear approximator can be written:

$$
\begin{bmatrix}
f_1 \\
g_1
\end{bmatrix}=
\begin{bmatrix}
\frac{\partial f}{\partial x} & \frac{\partial f}{\partial y} \\
\frac{\partial g}{\partial x} & \frac{\partial g}{\partial y}
\end{bmatrix}
\begin{bmatrix}
x \\
y
\end{bmatrix}+
\begin{bmatrix}
f_0 \\
g_0
\end{bmatrix}
$$

Since the target is f=0, g=0, this is equivalent to the following system:

$$
-\begin{bmatrix}
f_0 \\
g_0
\end{bmatrix}=
\begin{bmatrix}
\frac{\partial f}{\partial x} & \frac{\partial f}{\partial y} \\
\frac{\partial g}{\partial x} & \frac{\partial g}{\partial y}
\end{bmatrix}
\begin{bmatrix}
x \\
y
\end{bmatrix}
$$

This equation yields solutions for x and y:

$$
x = -\frac{\frac{\partial g}{\partial y} f_0 - \frac{\partial f}{\partial y} g_0}{\frac{\partial f}{\partial x} \frac{\partial g}{\partial y} - \frac{\partial f}{\partial y} \frac{\partial g}{\partial x}} 
$$

$$
y = -\frac{-\frac{\partial g}{\partial x} f_0 + \frac{\partial f}{\partial x} g_0}{\frac{\partial f}{\partial x} \frac{\partial g}{\partial y} - \frac{\partial f}{\partial y} \frac{\partial g}{\partial x}} 
$$

This program uses the formulas above to calculate the next guess of both inputs at each iteration. The situation can be visualized with the following plot of the projected zero-contours of the two functions f and g, where both zero-contours are estimated by calculating the gradient at the current point. The solution to the linear system above effectively finds the intersection between the two zero-contours, which is the target point. 

<img src="https://github.com/janderson4/efficalc/blob/main/examples/conc_col_pmm/images/minimizer-cropped.svg" width="570">


# Summary of Program Structure by Package and Module

## 1. `calc_document`
Contains modules linked to the `efficalc` package which are used for generating the calc report.

### 1.1. `add_col_inputs_document`
Adds the column inputs and assumptions to the calc report.

### 1.2. `col_inputs`
Collects information from the user about the column and loads. Calls `full_calc_document` to begin creating the calc report.

### 1.3. `document_wrapper`
Creates the calc report. It calls `col_inputs`, and from there, all information is added to the calc report.

### 1.4. `full_calc_document`
Receives a column and load cases, then runs the calculations for the column capacity and DCRs for all load cases.

### 1.5. `show_dcr_calc`
Adds the calculation of a particular DCR to the calc report. Optionally called depending on whether the user selects a given load case to be shown.

### 1.6. `try_axis_document`
Adds the calculations for the reaction of a column to bending on a given neutral axis to the calc report.

### 1.7. Plotting (sub-package)
Contains plotting functions.

#### 1.7.1. `draw_column`
Draws the cross-section of the column on an `efficalc` Canvas, including rebar. Includes options for drawing compression areas.

#### 1.7.2. `get_capacity`
Accepts parameters like the quarter PMM mesh and a loading point, then returns a list of resultant moment and axial points which form the PM diagram at the angle of the given load point.

#### 1.7.3. `pmm_mesh`
Creates the mesh for the PMM diagram by iterating over the range of axial loads and λ.

#### 1.7.4. `pmm_plotter_plotly`
Creates a Plotly figure for the column’s PMM diagram and returns a quarter of the PMM mesh.

#### 1.7.5. `point_plotter`
Creates a Matplotlib figure showing the PM diagram for a given load case, along with the point for the given load case.

## 2. `col`
Contains the definition of the column being analyzed.

### 2.1. `assign_max_min`
Performs calculations for the maximum and minimum axial capacity of a given column, adds them to the calc report, and assigns the calculated values to the given `Column` object.

### 2.2. `column`
Contains the class defining a `Column` object, including various properties.

## 3. `constants`
Contains constants used by other packages.

### 3.1. `rebar_data`
Stores data on rebar properties.

## 4. `pmm_search`
Contains functions used for searching the PMM surface for target points.

### 4.1. `ecc_search`
Used to find a PMM point for DCR calculation.

#### 4.1.1. `change_ecc`
Calculates the next iteration point in the search.

#### 4.1.2. `get_dcr_ecc`
Runs the point search for finding the capacity point for a given load point and calculates the DCR. Optionally adds the DCR calculation to the calc report.

#### 4.1.3. `get_error_ecc`
Calculates the distance of the current iteration point from the target point in normalized λ-α space.

#### 4.1.4. `limit_comp_ecc`
Calculates the results for a given iteration point by running `try_axis`. Also limits the axial load to a range in which nonzero derivatives can be calculated.

#### 4.1.5. `point_search_ecc`
Controls the convergence of the search for a point for a DCR calculation.

### 4.2. `load_search`
Used to find a PMM point for the PMM diagram.

#### 4.2.1. `bisect_load`
Searches for a point aligned with the Mx or My axes by changing only the neutral axis depth while holding λ constant.

#### 4.2.2. `change_load`
Calculates the next iteration point in the search.

#### 4.2.3. `get_error_load`
Calculates the distance of the current iteration point from the target point in normalized λ-P space.

#### 4.2.4. `limit_comp_load`
Calculates the results for a given iteration point by running `try_axis`. Also limits the axial load to a range in which nonzero derivatives can be calculated.

#### 4.2.5. `point_search_load`
Controls the convergence of the search for a point for creating a PMM diagram.

#### 4.2.6. `starting_pts`
Selects starting points for the `bisect_load` algorithm. Both starting points are near the initial guess point.

## 5. `struct_analysis`

### 5.1. `triangles`
Contains functions for calculating the area and centroid of a triangle, for use in `try_axis`.

### 5.2. `try_axis`
Calculates the reaction of a column (axial load and moments) due to bending on a given neutral axis angle and depth.

# Graphic Summary of Program Structure
The complete program structure, including dependencies on efficalc, is shown below (created using pydeps):
<img src="https://github.com/janderson4/efficalc/blob/main/examples/conc_col_pmm/images/structure.svg" width=100%>

# Reference
[1] Design of Concrete Structures, 15th ed. Darwin, Dolan, and Nilson. McGraw, 2016. 
