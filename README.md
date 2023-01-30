Finding the Hamiltonian path and Hamiltonian Circuit by Solve system of linear inequalities
======

# 1. Introduce
This algorithm is a consequence of the ['Solve system of linear inequalities' algorithm](https://github.com/Truongphi20/inequaltion). The procedure rapidly finds the pathways across all of the points on the graph by resolving the system of linear inequalities to determine the coefficients of the $\phi$-matrice of vectors to fulfill the final matrix's requirements.

The algorithm promises a general and systematic way of solving graph problems.

# 2. Usage
## 2.1 Download
To download the tool, select ``Code > Zip Download`` on Github page or type in Command Prompt on Windows or Terminal on other operating systems as follows:
    
    git clone https://github.com/Truongphi20/hamilpath.git

## 2.2 Check settings
Move the terminal's working directory to the downloaded "hamilpath" directory (`cd hamilpath`).
    
    python .\findpath.py -h
    
Output:

    usage: findpath.py [-h] [-t VECTORS] [-v] [-c CIRCUIT]

    optional arguments:
      -h, --help            show this help message and exit
      -t VECTORS, --vectors VECTORS
      -v, --version         show version
      -c CIRCUIT, --circuit CIRCUIT
                            Circuit (c) or path (p)?

## 2.3 Example
Suppose we need to find the hamiltonian path for the following graph:

<img src="https://user-images.githubusercontent.com/96680644/215405497-19cdb4c6-d01b-45e7-818a-c6276783c9c0.png" alt="drawing" width="400"/>

In the graph we see the following vectors: $\overrightarrow {AD}$, $\overrightarrow {AB}$, $\overrightarrow {BD}$, $\overrightarrow {DC}$, $\overrightarrow {CD}$, $\overrightarrow {BC}$, $\overrightarrow {CA}$ 

From those vectors, we run the algorithm to find the hamiltonian path with the following syntax:

    python .\findpath.py -t AD,AB,BD,DC,CD,BC,CA
    
Output:

    ['ABDC', 'ABCD', 'CABD', 'DCAB', 'BDCA', 'BCAD']
    
As a result, the paths pass through all the points. Here we have 6 paths: 

$A \to B \to D \to C$; 

$A \to B \to C \to D$;

$C \to A \to B \to D$;

$D \to C \to A \to B$;

$B \to D \to C \to A$;

$B \to C \to A \to D$

Furthermore, finding Hamiltonian Circuit could be done by adding `-c` tag. As the following command.
           
    python .\findpath.py -t AD,AB,BD,DC,CD,BC,CA -c c

Output:

    ['ABDCA']

So, the Hamiltonian circuit for the above example is: $A \to B \to D \to C \to A$

# 3. Explaining algorithm
## 3.1 Definition of $\phi$-matrice
$\phi$-matrice is a matrix with the number of rows 2 and the number of columns is the number of points in the graph. Where row one is the number of times the corresponding points have passed through and row two is the number of times the corresponding points are left

For example, a graph has points $A$, $B$, $C$, and $D$. So the $\phi$-matrice of vector $\overrightarrow {BD}$ has the following form with columns corresponding to points $A$, $B$, $C$, and $D$.

$$
M_{\overrightarrow {BD}} = \left( {\begin{array}{*{20}{c}}
0 & 0 & 0 & 1\\
0 & 1 & 0 & 0
\end{array}} \right)
$$ 

**The $\phi$-matrice has plus able characteristics.** Suppose the $p$ path goes from point A through points $C$ and $D$ along the $\overrightarrow {AC}$ and $\overrightarrow {CD}$, respectively. $\phi$-matrice of the $p$ path is equal to the sum of the $\phi$-matrice of $\overrightarrow {AC}$ and $\overrightarrow {CD}$.

$$
{M_p} = {M_{\overrightarrow {AC} }} + {M_{\overrightarrow {CD} }}
$$

$$
\leftrightarrow {M_p} = \left( {\begin{array}{*{20}{c}}
0&0&1&0\\
1&0&0&0
\end{array}} \right) + \left( {\begin{array}{*{20}{c}}
0&0&0&1\\
0&0&1&0
\end{array}} \right)
$$

$$
\leftrightarrow {M_p} = \left( {\begin{array}{*{20}{c}}
0&0&1&1\\
1&0&1&0
\end{array}} \right)
$$

**From above, we see that the matrix is commutative**. Although vectors are not commutative, their  $\phi$-matrice can do it.

From the above two properties, we can use them to establish inequalities based on the $\phi$-matrice condition of the whole path.

## 3.2 Processing 
The algorithm process goes through the following basic steps:
  1. Prepare a system of linear inequalities
  2. Solve and find the coefficients for the $\phi$-matrices of the vectors
  3. Returns the results of the paths which pass through the points
