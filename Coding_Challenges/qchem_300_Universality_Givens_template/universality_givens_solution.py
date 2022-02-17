#! /usr/bin/python3

import sys
import numpy as np
import pennylane as qml

def givens_rotations(a, b, c, d):
    """Calculates the angles needed for a Givens rotation to output the state with amplitudes a,b,c and d
    Args:
        - a,b,c,d (float): real numbers which represent the amplitude of the relevant basis states (see problem statement).
        Assume they are normalized.
    Returns:
        - (list(float)): a list of real numbers ranging in the intervals provided in the challenge statement, which represent
        the angles in the Givens rotations, in order, that must be applied.
    """
    # QHACK #
    # get required thetas by solving equations (done by hand)
    y = 2 * np.arctan(-c/b)
    x = 2 * np.arcsin(c/np.sin(y/2))
    z = 2 * np.arctan(-d/a)

    dev = qml.device('default.qubit', wires=6)

    @qml.qnode(dev)
    def circuit4(x, y, z):
        qml.BasisState(np.array([1, 1, 0, 0, 0, 0]), wires=[i for i in range(6)])
        # apply double excitation 01 -> 23
        qml.DoubleExcitation(x, wires=[0, 1, 2, 3])
        # apply double excitation 23 -> 45
        qml.DoubleExcitation(y, wires=[2, 3, 4, 5])
        # single excitation controlled on qubit 0 -> 13
        qml.ctrl(qml.SingleExcitation, control=0)(z, wires=[1, 3])
        return qml.state()

    return x,y,z

    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    theta_1, theta_2, theta_3 = givens_rotations(float(inputs[0]), float(inputs[1]), float(inputs[2]), float(inputs[3]))
    print(*[theta_1, theta_2, theta_3], sep=",")
