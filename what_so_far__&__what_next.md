- so i hereby state that
### Sudoku Madness has been resolved

- yeah i did what i wanted to do
- of course just like compression madness it is not my desired result but hey i got it
- i wanted that probability matrix to be correct so i can use that myself to solve Sudoku
- or even better use that to improve bruteforce instead of mindlessly trying
- like the first digit we put and check for bruteforce is the one with highest probabilty and whenever we wanted to backtrack
- we can just choose the next highest prob digit

### What i have done and what i didn't get

- well it turns out it is not possible to build that exact probabilty matrix i was looking for
- atleast not with my current math knowledge
- it turns out this rabbit hole goes deeper to the point of unsolved NP Completeness problem
- if you are curious here is the math that gemini told me

### The Math You Would Need

1. **Karush-Kuhn-Tucker (KKT) Conditions & Quadratic Programming (QP)**
* **Why you need it:** Standard linear algebra (like matrix inverses or simple subtraction) only handles equality constraints ($\sum = 1$). The moment you add inequality constraints ($M_{i,j} \ge 0$), simple equations break.
* **What it does:** KKT conditions determine which cells get pushed to exactly $0.0$ (the active boundary) versus which cells absorb the residual probability when you force one cell to $1.0$.


2. **Projected Gradient Descent on the Birkhoff Polytope**
* **Why you need it:** Setting a entry to $1$ kicks your matrix off the surface of valid doubly stochastic matrices.
* **What it does:** You compute the gradient towards your fixed target and use algorithms like **Dykstra’s Projection Algorithm** to iteratively project the matrix back onto the intersection of non-negative matrices and row/column sum affine spaces.


3. **Multi-Marginal Optimal Transport (3D Tensors)**
* **Why you need it:** Sudoku isn't 2D (Row vs. Column). It is a 3D matching problem across $9 \text{ Rows} \times 9 \text{ Cols} \times 9 \text{ Digits}$.
* **What it does:** Instead of $9 \times 9$ matrices, you normalize a $9 \times 9 \times 9$ tensor across three axes simultaneously using entropy-regularized optimal transport (Sinkhorn in 3D).

### but it worked so... what i did

- well yes it's highly useful but imperfect
- not wrong, just imperfect
- like it is doubly stochastic matrix and i have used the Sinkhorn-Knopp algo to normalize it
- but it's not locking the values
- for example if we know for certain that a value will come at a place then all the other element in that row and column should be 0
- but it's not one even when we wanted it to be, let alone columns and rows of it being zero
- it makes sense because that Algo is just repeated normalization and division to get the doubly stochastic property
- so no it's not accurate 
- but IT'S NOT WRONG AS WELL
- i can still use that for improved Backtracking brute force solver
- or even use this as a hint for solving the Sudoku in my morning newspaper (I'm not into those stuff for now but... yeah it's useful)
- maybe it's better to call that as Priority matrix instead of Probabilty matrix

### so is this project a success and what's the status

- there is no defined failure
- there is learnings
- like i wouldn't understood the mathematical depth of Sudoku if i didn't hit the wall
- it sucks to find that the tresure we are looking for is really complicated to find 
- but hey hitting walls teach you and let you explore so much 
- so I'm humble enough to admit that i didn't achieve what i wanted to 
- but I'm happy enough to admit that this is so fun and made me read newspaper (if i found a intresting news on my way to Sudoku, of course)
- as the great Philosopher Mateo Aaron said "Everything is a success if your goal is to enjoy" (not sure but it looks something this)
- SO YES **IT'S A GREAT SUCCESS**
- the current status is **COMPLETED, BUT OPEN FOR EXPLORATION IN THE FUTURE**

### what next, If I'm really curious

- first of all 
- madness is resolved
- if it ever scratches once again, maybe we can do a lot of stuff
- [Green Code's Video](https://youtu.be/0roAZFaqSjw) helped me explore a lot in this subject
- these papers tell about how to make Sudoku
- [Paper 1](https://zhangroup.aporc.org/images/files/Paper_3485.pdf) and [SudokuWiki.org's Paper](https://www.sudokuwiki.org/Sudoku_Creation_and_Grading.pdf)
- btw checkout [SudokuWiki.org](https://www.sudokuwiki.org/Main_Page) to see their analysis on the techniques and method (a treasure trove of knowledge)
- they also have other puzzles like Cryptic Crosswords if you are intrested
- i can even make a solving Algorithm based on techiniques in SudokuWiki.org
- if you want to dive headfirst into this madness
- here are the wikipedia articles that might help
- https://en.wikipedia.org/wiki/Sudoku_graph
- https://en.wikipedia.org/wiki/Mathematics_of_sudoku
- https://en.wikipedia.org/wiki/Sudoku
- https://en.wikipedia.org/wiki/Sudoku_solving_algorithms

