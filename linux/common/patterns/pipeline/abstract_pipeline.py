from abc import ABC, abstractmethod
from typing import Any, List

from common.patterns.pipeline.pipe import IPipe


class AbPipeline(ABC):
    def __init__(self):
        self._pipes: List[IPipe] = []

    def _add_step(self, step: IPipe):
        self._pipes.append(step)

    def flow(self, data: Any):
        """Makes the pipeline flow; run its steps/pipes."""
        for pipe in self._pipes:
            data = pipe.flow(data)
        return data

    @abstractmethod
    def build_pipeline(self):
        """
        Method to be implemented by subclasses.
        This method should populate the pipeline with steps using the add_step method.
        """
        pass
