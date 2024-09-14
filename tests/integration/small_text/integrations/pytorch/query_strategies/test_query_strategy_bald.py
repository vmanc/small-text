"""BALD is in the main small_text.query_strategies package but all strategies that provide
bayesian uncertainties (or more accurately something that allows them to be treated as such)
are neural networks which are located in the integration packages."""
import unittest

import pytest

from small_text.integrations.pytorch.exceptions import PytorchNotFoundError

from tests.integration.small_text.query_strategies.test_query_strategies import (
    QueryStrategiesExhaustiveIntegrationTest
)

try:
    import torch
    from small_text.integrations.pytorch.classifiers import KimCNNClassifierFactory
    from small_text.query_strategies.bayesian import BALD

    from tests.utils.datasets import random_text_classification_dataset
except (ImportError, PytorchNotFoundError):
    pass


@pytest.mark.pytorch
class BaldTest(QueryStrategiesExhaustiveIntegrationTest, unittest.TestCase):

    def _get_dataset(self, num_classes, multi_label=False):
        return random_text_classification_dataset(num_samples=60, max_length=10,
                                                  multi_label=multi_label, num_classes=num_classes)

    def _get_factory(self, num_classes, multi_label=False):

        return KimCNNClassifierFactory(num_classes, {'embedding_matrix': torch.rand(10, 20), 'num_epochs': 2})

    def test_bald(self):
        query_strategy = BALD(dropout_samples=3)
        self._simple_exhaustive_active_learning_test(query_strategy, num_classes=2)

    def test_bald_multiclass(self):
        query_strategy = BALD(dropout_samples=3)
        self._simple_exhaustive_active_learning_test(query_strategy)
