from abc import ABC, abstractmethod


class Simulator(ABC):
    """Abstract class for a simulator."""

    def run(self):
        self.pre_run()
        self.run_simulation()
        self.post_run()

    @abstractmethod
    def pre_run(self):
        return NotImplemented

    @abstractmethod
    def run_simulation(self):
        return NotImplemented

    @abstractmethod
    def post_run(self):
        return NotImplemented
