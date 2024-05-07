# Sudoku Solver

This is a Python program to solve Sudoku puzzles, with CSP approach and depth-first search.

## Installation

Before running the program, you need to install the required packages. 

1. First, clone the repository to your local machine:

```bash
git clone https://github.com/adriancho91s/ai-sudoku-solver.git
cd ai-sudoku-solver
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the program

Before you run the program you must make sure that you have created the `board` file with the sudoku to solve.

To run the program, use the following command:

```bash
python sudoku.py
```

Make sure you are in the correct directory (sudoku-solver) when you run this command.

## Virtual enviroment

You can create a virtual environment in Python using the venv module too. Here's how you can do it:

   1. Navigate to the directory where you want to create the virtual enviroment

   2. Run the following command to create a virtual enviroment named env:

        ```bash
        python3 -m venv env
        ```

   3. To activate the virtual environment, use the following command:

        ```bash
        source env/bin/activate
        ```

Now, you're in the virtual environment. You can install packages that will only be available in this environment. To deactivate the virtual environment, simply type `deactivate` in the terminal.
