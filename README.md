<h1>Description</h1>

<p>This project was created as part of the MSc Computing Dissertation. The brief was to develop an application that may allow lecturers to divide students into diverse teams using constraints optimisation. The lecturer was to be able to specify team size and which constraints to apply to the allocation process.</p>

<p>The algorithm behind the team generation process can be found in the 'groupy.py' file. Originally, a brute-force algorithm was written, but it was found to be too computationally demanding, and so a heuristic method was implemented. Firstly, the user may upload a .csv file containing student information. The application will read the .csv file and check which student attributes have been provided, and each student will be allocated a score which is based on attribute frequency or numerical scores such as an academic score. The algorithm will then attempt to evenly distubute students across the required number of groups to achieve maximally diverse teams. Users may sign up for an account and save any generated solutions to their user profile, and may also download solutions to their local machine. Saved solutions are viewable only by the user who saved them.</p>

<p>The main body of the dissertation report was centered around improvement of the underlying algorithm, however Django was chosen as a framework within which to implement the algorithm and user interface due to it's ease of implementation, as well as the ability to implement required features such as user accounts and databases.</p>

