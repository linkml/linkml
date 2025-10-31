from abc import ABC, abstractmethod


class ModelTransform(ABC):
    @abstractmethod
    def explode_unnest_dataframe(self, df, column_name):
        """Abstract method for exploding and unnesting dataframes."""
        pass
