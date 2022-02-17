#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml


def qfunc_adder(m, wires):
    """Quantum function capable of adding m units to a basic state given as input.

    Args:
        - m (int): units to add.
        - wires (list(int)): list of wires in which the function will be executed on.
    """

    qml.QFT(wires=wires)

    # QHACK #
    # n = len(wires)
    # theta = ((2.0 * np.pi) * int(m))
    # for j in wires:
    #     qml.PhaseShift(theta/2**(n-j+1), wires=j)
    
    binary = []
    n = len(wires)

    while m != 0:
        r = m % 2
        m = m // 2
        binary.append(r)
    
    
    while len(binary) < n:
        binary.append(0)

    # Iterate through the targets.
    for i in range(n,0,-1):
        # Iterate through the controls.
        for j in range(i,0,-1):
            if binary[j-1]:
                theta = 2*np.pi/2**(i-j+1)
                qml.PhaseShift(theta, wires=i-1)
    # QHACK #

    qml.QFT(wires=wires).inv()


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    m = int(inputs[0])
    n_wires = int(inputs[1])
    wires = range(n_wires)

    dev = qml.device("default.qubit", wires=wires, shots=1)

    @qml.qnode(dev)
    def test_circuit():
        # Input:  |2^{N-1}>
        qml.PauliX(wires=0)

        qfunc_adder(m, wires)
        return qml.sample()

    output = test_circuit()
    print(*output, sep=",")
