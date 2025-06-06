"Introduction to Machine Learning"
CIS4900
April 15, 2021

Randomly generates two sets of points distributed around mean values of -1 and 1.
Finds support vectors in order to draw a line that best separates the two sets.
Implemented using numPy and cvxopt, graph representation using matplotlib.pyplot.

### Requirements

- Python 3.8+
- `cvxopt`, `cvxpy`, `numpy`, `matplotlib`

Create a virtual environment and install dependencies:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python3 SVM.py
