#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml


def deutsch_jozsa(fs):
    """Function that determines whether four given functions are all of the same type or not.

    Args:
        - fs (list(function)): A list of 4 quantum functions. Each of them will accept a 'wires' parameter.
        The first two wires refer to the input and the third to the output of the function.

    Returns:
        - (str) : "4 same" or "2 and 2"
    """

    # QHACK #

    f1, f2, f3, f4 = fs

    dev = qml.device("default.qubit", wires=8, shots=1)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=[0])
        qml.Hadamard(wires=[1])
        qml.PauliX(wires=[2])
        qml.Hadamard(wires=[2])
        f1([0, 1, 2])
        qml.Hadamard(wires=[0])
        qml.Hadamard(wires=[1])
        qml.Hadamard(wires=[2])
        qml.PauliX(wires=[2])

        qml.Hadamard(wires=[2])
        qml.Hadamard(wires=[3])
        qml.PauliX(wires=[4])
        qml.Hadamard(wires=[4])
        f2([2, 3, 4])
        qml.Hadamard(wires=[2])
        qml.Hadamard(wires=[3])
        qml.Hadamard(wires=[4])
        qml.PauliX(wires=[4])

        qml.Hadamard(wires=[4])
        qml.Hadamard(wires=[5])
        qml.PauliX(wires=[6])
        qml.Hadamard(wires=[6])
        f3([4, 5, 6])
        qml.Hadamard(wires=[4])
        qml.Hadamard(wires=[5])
        qml.Hadamard(wires=[6])
        qml.PauliX(wires=[6])

        return qml.sample(wires=range(6))

    res = circuit()
    r1, r2, r3 = res[:2], res[2:4], res[4:6]
    count = 0
    for r in [r1, r2, r3]:
        if r[0] == 0 and r[1] == 0:
            count += 1
    if count == 3 or count == 0:
        return "4 same"
    else:
        return "2 and 2"

    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    numbers = [int(i) for i in inputs]

    # Definition of the four oracles we will work with.

    def f1(wires):
        qml.CNOT(wires=[wires[numbers[0]], wires[2]])
        qml.CNOT(wires=[wires[numbers[1]], wires[2]])

    def f2(wires):
        qml.CNOT(wires=[wires[numbers[2]], wires[2]])
        qml.CNOT(wires=[wires[numbers[3]], wires[2]])

    def f3(wires):
        qml.CNOT(wires=[wires[numbers[4]], wires[2]])
        qml.CNOT(wires=[wires[numbers[5]], wires[2]])
        qml.PauliX(wires=wires[2])

    def f4(wires):
        qml.CNOT(wires=[wires[numbers[6]], wires[2]])
        qml.CNOT(wires=[wires[numbers[7]], wires[2]])
        qml.PauliX(wires=wires[2])

    output = deutsch_jozsa([f1, f2, f3, f4])
    print(f"{output}")
