import cvxopt
import cvxpy as cp
import math
    import matplotlib.pyplot as plt
import numpy as np
from cvxopt import solvers, matrix


def SVM(X, y, cov, C=0.1, fullReport = True):
    samples, features = X.shape

    # Generate Gram Matrix comparing to linear kernel
    K = np.zeros((samples, samples))
    for i in range(samples):
        for j in range(samples):
            K[i, j] = linear_kernel(X[i], X[j])

    # Create Kernel
    K = linear_kernel(X, X)

    # Uh... create "dense matrices?" is that what they're called?
    P = matrix(np.outer(y, y) * K)
    q = matrix(np.ones((samples, 1)) * -1)
    G = matrix(np.vstack((np.eye(samples) * -1, np.eye(samples))))
    A = matrix(y.reshape(1, -1))
    h = matrix(np.hstack((np.zeros(samples), np.ones(samples) * C)))

    # Initiate value for b
    b = matrix(0.0)

    #####################################################################################
    # Attempted Solution using CVXPY:
    # I started off by reading some paper (or, a billion papers) that neglected to
    # tell me about the necessity to compute both the minimum and maximum functions,
    # so I spent a really long time on only the minimization part.
    # Now, the addition of s, y and z have really complicated things- not to say that
    # it worked before, but, at least it compiled!
    #####################################################################################
    # x, s = cp.Variable(P.shape[1]), cp.Variable(P.shape[1])
    # y, z = cp.Variable(P.shape[1]), cp.Variable(P.shape[1])
    # Compiling constraintsMin = [G @ x[:, None] <= h[:, None], x[:, None] @ A == b]
    # constraintsMin = [G * x] + s.T == h[:, None], x[:, None] @ A == b, s >= 0]
    # Compiling min = cp.Minimize(0.5 * cp.quad_form(x, P) + x.T @ q)
    # min = cp.Minimize(0.5 * cp.quad_form(x, P) + x.T @ q)
    # constraintsMax = [q + G @ z[:, None].T]# + A.T] @ y in range(P), z >= 0]
    # max = cp.Maximize(-0.5 * (q + (G.T @ z[:, None]) + A.T @ y[:, None]).T * np.pinv(P) *
    #                   (q + G.T @ z[:, None] + A.T @ y[:, None]) - h.T @ z[:, None] - b.T @ y[:, None])
    # problem1 = cp.Problem(min, constraintsMin)
    # problem2 = cp.Problem(max, constraintsMax)
    # problem3 = problem1 + problem2
    # problem3.solve(x)
    # Determine Support Vectors
    # alphas = np.ravel(test.value)
    # ind = np.arange(len(alphas))[ctr]
    #####################################################################################

    # CVXOPT
    solution = solvers.qp(P, q, G, h, A, b)
    alphas = np.array(solution['x'])
    ctr = (alphas > 1e-4).flatten()
    sv_x = X[ctr]
    sv_y = y[ctr]
    alphas = alphas[ctr]

    # Calculate Bias
    bias = sv_y - np.sum(linear_kernel(sv_x, sv_x) * alphas * sv_y, axis=0)
    bias = np.sum(bias) / bias.size

    # Calculate Weight
    weight = np.zeros(features)
    for n in range(len(alphas)):
        weight += alphas[n] * sv_y[n] * sv_x[n]

    # Predictions
    pre = np.sum(linear_kernel(sv_x, X).T @ alphas * sv_y, axis=0) + b
    predictions = np.sign(pre)

    if fullReport:
        for i in range(1, len(alphas)):
            if i < 10:
                print(str(i) + ".  " + str(sv_x[i]))
            else:
                print(str(i) + ". " + str(sv_x[i]))
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        print("Found %d support vectors, coordinates above, " % (len(alphas) - 1), end="")
    else:
        print("Found %d support vectors." % len(alphas))

    return bias, weight, predictions, sv_x, sv_y, alphas


def f(x, w, b, c=0):
    return (-w[0] * x - b + c) / w[1]


def linear_kernel(x, z):
    return np.matmul(x, z.T)


def toLine(mat):
    slope = (mat[1][1] - mat[1][0])/(mat[0][1] - mat[0][0])
    intercept = mat[1][1] - 1 * mat[0][1] * slope
    line = [slope, intercept]
    return line


def determinant(model, point):
    Ax = model[0][0]
    Ay = model[1][0]
    Bx = model[0][1]
    By = model[1][1]
    x = point[0]
    y = point[1]

    sign = np.sign((Bx - Ax) * (y - Ay) - (By - Ay) * (x - Ax))
    return sign


def classifier(X, y, model, k=10):
    size = k
    SVM = model[0]
    upper = model[1]
    lower = model[2]
    success = 0
    classError = 0
    marginError = 0
    percent = "%"
    failuresX = []
    failuresY = []

    # removed "k" usage for now
    for i in range(0, len(X)):
        # if the Y of the testing data is greater than the expected Y of the SVM
        if determinant(SVM, X[i]) >= 0:
            # assign 1
            res = -1
        else:
            # assign -1
            res = 1
        if res == y[i]:
            success = success + 1
        else:
            # compare to the lower and upper margin of the function
            if y[i] == 1:
                if determinant(upper, X[i]) == -1:
                    marginError = marginError + 1
                    success = success + 1
                else:
                    classError = classError + 1
                    failuresX.append(X[i][0])   # keeps location of
                    failuresY.append(X[i][1])   # failed predictions
            if y[i] == -1:
                if determinant(lower, X[i]) != -1:
                    marginError = marginError + 1
                    success = success + 1
                else:
                    classError = classError + 1
                    failuresX.append(X[i][0])
                    failuresY.append(X[i][1])

    marginError = marginError / len(X)

    print("Out of the " + str(len(X)) + " predictions that were made, " + str(success) + " were correct.")
    print("This points to a misclassification error of ", float(1 - (success / len(X))), percent, ".", sep="")
    print(float(marginError), percent, " of points would have been misclassified without the margin.", sep="")

    return marginError, float(1 - (success / len(X))), failuresX, failuresY


def cross_validation(X, y, model, k=10):
    SVM = model[0]
    upper = model[1]
    lower = model[2]
    success = 0
    failure = 0

    return 0


def generate(cov, meanA, meanB, size=200):
    splitVal = int(size * .8)
    np.random.seed(74449)

    # class
    x = np.random.multivariate_normal(meanA, cov, size)
    y = np.ones(len(x))

    # classB
    h = np.random.multivariate_normal(meanB, cov, size)
    g = np.ones(len(h)) * -1

    xTest = np.vstack((x[splitVal:], h[splitVal:]))
    yTest = np.hstack((y[splitVal:], g[splitVal:]))
    xTrain = np.vstack((x[:splitVal], h[:splitVal]))
    yTrain = np.hstack((y[:splitVal], g[:splitVal]))

    return x, y, h, g, xTest, yTest, xTrain, yTrain, size


def graph(xTrain, yTrain, sv_x, meanA, meanB, weight, bias):
    meanA = meanA.flatten()
    meanB = meanB.flatten()

    # plot a line from x value 2.5 * meanA to 2.5 * meanB
    if float(meanA[0]) > float(meanB[0]):
        max = float(meanA[0])
        min = float(meanB[0])
    else:
        min = float(meanA[0])
        max = float(meanB[0])
    max = 2.5 * max + max
    min = 2.5 * min + min

    p1 = xTrain[yTrain == 1]
    p2 = xTrain[yTrain == -1]
    plt.plot(p1[:, 0], p1[:, 1], marker='.', c="y", linestyle='none')
    plt.plot(p2[:, 0], p2[:, 1], marker='.', c="r", linestyle='none')
    plt.scatter(sv_x[:, 0], sv_x[:, 1], s=50, c="k")

    a1 = f(min, weight, bias)
    b1 = f(max, weight, bias)
    plt.plot([min, max], [a1, b1], "k")
    svm = ([[min, max], [a1, b1]])

    a1 = f(min, weight, bias, -1)
    b1 = f(max, weight, bias, -1)
    plt.plot([min, max], [a1, b1], "k--")
    upper = ([[min, max], [a1, b1]])

    a1 = f(min, weight, bias, 1)
    b1 = f(max, weight, bias, 1)
    plt.plot([min, max], [a1, b1], "k--")
    lower = ([[min, max], [a1, b1]])
    print("Vector margin: %f." % float(toLine(upper)[1] - toLine(lower)[1]))

    return svm, upper, lower, plt, float(toLine(upper)[1] - toLine(lower)[1])


def differentC(iter, start, stop, oMa, oMi, xTrain, yTrain, cov, C, sv_x, meanA,
               meanB, weight, bias, xTest, yTest, svm, upper, lower):
    set = np.linspace(start, stop, iter)
    misError, marError = [], []
    averageMa, averageMi = 0, 0
    svMax, svMin = (0, 0), (100000, 0)
    percent = "%"
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")
    for i in range(0, iter):
        print("Using value of C =", set[i])
        C = float(set[i])
        bias, weight, predictions, sv_x, sv_y, sv = SVM(xTrain, yTrain, cov, C, False)
        svm, upper, lower, grap, margin = graph(xTrain, yTrain, sv_x, meanA, meanB, weight, bias)
        mError, maError, failuresX, failuresY = classifier(xTest, yTest, [svm, upper, lower], xTest.size)
        grap.show()
        misError.append(mError)
        marError.append(maError)
        if int(len(sv)) < svMin[0]:
            svMin = (int(len(sv)), C)
        if int(len(sv)) > svMax[0]:
            svMax = (int(len(sv)), C)
        print("\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")

    sv = np.delete(sv, 0)

    for i in range(0, iter): # average difference between the errors
        averageMa = averageMa + (marError[i] - oMa)
        averageMi = averageMi + (misError[i] - oMi)

    print("After ", iter, " iterations of evenly spaced values between ", start, " and %.4f,\n"
          % stop, "the misclassification error changed by an average of ", averageMi, percent,
          " and \nthe margin error changed by an average of ", averageMa, percent, ".", sep="")
    print("The number of support vectors varied between ", svMax[0], " at C = ", svMax[1],
          "\nand ", svMin[0], " at %.4f" % svMin[1], ".", sep="")
    print("\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")


def main():
    # Set to True to see impact of differing "C" values
    test = True
    # Set to True to see failed points on graph (so far there haven't been any)
    showFailures = False
    # Set to true to see output from cvxopt quadratic problem solver
    cvxopt.solvers.options['show_progress'] = False

    # Generate Data using these parameters
    size = 200 # optional parameter, also defaults to 200
    cov = np.array([[1, 0.25], [0.25, 1]])
    meanA = np.array([-1, -1])
    meanB = np.array([1, 1])
    C = 1.5
    x, y, h, g, xTest, yTest, xTrain, yTrain, size = generate(cov, meanA, meanB, size)

    # Find Vector
    bias, weight, predictions, sv_x, sv_y, sv = SVM(xTrain, yTrain, cov, C)
    print("out of %d total points." % (size*2))
    svm, upper, lower, grap, margin = graph(xTrain, yTrain, sv_x, meanA, meanB, weight, bias)

    # Cross Validation
    # so, this works, but i don't think it's actually a cross-validation algorithm.
    mError, maError, failuresX, failuresY = classifier(xTest, yTest, (svm, upper, lower), xTest.size)

    if showFailures:
        plt.scatter(failuresX, failuresY, s=60, c="b")

    # Demonstrate differing values for C
    if test:
        print("Close the graph to see the results of differing C values.\n")
    grap.show()
    if test:
        differentC(4, mError, margin, maError, maError, xTrain, yTrain, cov, C, sv_x, meanA,
                   meanB, weight, bias, xTest, yTest, svm, upper, lower)
    else:
        print("\nSet 'test' == True to see the impact of differing C values.")
        print("\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")


if __name__ == '__main__':
    main()




# Things that I tried, that didn't end up working out, but
# that I might pursue again in the future.

def RBF(x, y, cov):
    trnorms1 = np.mat([(v * v.T)[0, 0] for v in x]).T
    trnorms2 = np.mat([(v * v.T)[0, 0] for v in y]).T

    k1 = trnorms1 * np.mat(np.ones((y.shape[0], 1), dtype=np.float64)).T
    k2 = np.mat(np.ones((x.shape[0], 1), dtype=np.float64)) * trnorms2.T

    k = k1 + k2
    k -= 2 * np.mat(x * y.T)

    k *= - 1. / (2 * np.power(cov, 2))

    return np.exp(k)


def gaussian_kernel(x, z, sigma):
    # https://medium.com/@ahlawat.randeep/svm-from-scratch-using-quadratic-programming-90b4dbc5e1d2
    # not implemented because i don't really get it? but, interested in looking into it
    n = x.shape[0]
    m = z.shape[0]
    xx = np.dot(np.sum(np.power(x, 2), 1).reshape(n, 1), np.ones((1, m)))
    zz = np.dot(np.sum(np.power(z, 2), 1).reshape(m, 1), np.ones((1, n)))

    return np.exp(-(xx + zz.T - 2 * np.dot(x, z.T)) / (2 * sigma ** 2))
