from abc import ABC, abstractmethod

import numpy as np


class Parameter(ABC):
    """
    Encapsulates a numpy array and keeps track of its gradient.
    """

    def __init__(self, data: np.array, requires_grad: bool = True):
        self.data = data
        self.grad = np.zeros_like(data, dtype=np.float32)
        self.requires_grad = requires_grad

    def __repr__(self):
        return f"Parameter(shape={self.data.shape}, requires_grad={self.requires_grad})"


class Module(ABC):
    """
    A module is a stateful object, encapsulating a function and keeping track
    of the trainable parameters. It also keeps track of cached activations.
    """

    def __init__(self):
        self._params = {}
        self._cache = {}
        self._training = True

    def __call__(self, inputs, mubatch_id=0):
        return self.forward(inputs, mubatch_id=mubatch_id)

    @abstractmethod
    def forward(self, inputs: np.array, mubatch_id=0):
        raise NotImplementedError

    @abstractmethod
    def backward(self, dout: np.array, mubatch_id=0):
        raise NotImplementedError

    def train(self):
        self._training = True

    def eval(self):
        self._training = False

    def zero_grad(self):
        for param in self.parameters():
            param.grad.fill(0.0)

    def parameters(self):
        return list(self._params.values())
