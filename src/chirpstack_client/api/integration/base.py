from abc import ABC, abstractmethod


class BaseIntegration(ABC):
    @abstractmethod
    def create(self, application_id, **kwargs):
        pass

    @abstractmethod
    def get(self, application_id):
        pass

    @abstractmethod
    def update(self, application_id, **kwargs):
        pass

    @abstractmethod
    def delete(self, application_id):
        pass
