# Code Completion Gym

Code completion gym is a toolkit for evaluating code completion systems on source code of your choice. The toolkit measures how many % of keystrokes are needed to complete a source code file using a user-provided code completion tool.

All you have to do is create a wrapper (a Predictor) for your code completion system implementing the interface defined in `lib/predictor.py`. The `lib` folder contains an example wrapper for the popular `jedi` code completion library.

The `evaluator.py` file provides an example on how to run the evaluation tool, which, in our case, creates a file listing the number of keystrokes saved given a path to Python source code. The example code is pre-configured to use the provided Jedi predictor. 

To run the evaluation on all python files in a library of your choice, execute:
`python3 evaluator.py -p your_library/**/*.py`
