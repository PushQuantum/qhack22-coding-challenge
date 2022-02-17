#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml


def qRAM(thetas):
    """Function that generates the superposition state explained above given the thetas angles.

    Args:
        - thetas (list(float)): list of angles to apply in the rotations.

    Returns:
        - (list(complex)): final state.
    """

    # QHACK #

    # Use this space to create auxiliary functions if you need it.
    def apply_roation(idx):
        binary_idx = format(idx, '03b')
        for i in range(3):
            if binary_idx[i]=='0':
                qml.PauliX(wires=i)
        

        U = np.identity(16)
        rotation = np.array([[np.cos(thetas[idx]/2), -np.sin(thetas[idx]/2)],[np.sin(thetas[idx]/2), np.cos(thetas[idx]/2)]])
        U[14:17,14:17] = rotation
        qml.QubitUnitary(U, wires=range(4))

        for i in range(3):
            if binary_idx[i]=='0':
                qml.PauliX(wires=i)

    # QHACK #

    dev = qml.device("default.qubit", wires=range(4))

    @qml.qnode(dev)
    def circuit():

        # QHACK #

        # Create your circuit: the first three qubits will refer to the index, the fourth to the RY rotation.
        qml.Hadamard(wires=0)
        qml.Hadamard(wires=1)
        qml.Hadamard(wires=2)

        for idx in range(len(thetas)):
            apply_roation(idx)

        # QHACK #

        return qml.state()

    return circuit()


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    thetas = np.array(inputs, dtype=float)

    output = qRAM(thetas)
    output = [float(i.real.round(6)) for i in output]
    print(*output, sep=",")
