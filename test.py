import numpy as np
import pytest

from pareto import ParetoOptimalPointsFinder  # Assuming the class is in a separate file


@pytest.fixture
def sample_data():
    """
    Fixture to provide sample data for testing.
    """
    return np.array([[0.8, 0.7], [0.9, 0.6], [0.7, 0.8], [0.6, 0.9]])


def test_init_default_preferences(sample_data):
    """
    Test that the class is initialized with default accuracy and fairness minimization preferences.
    """
    finder = ParetoOptimalPointsFinder(data=sample_data)
    assert finder.accuracy_minimise is True
    assert finder.fairness_minimise is True


@pytest.mark.parametrize(
    "accuracy_minimise,fairness_minimise,expected_pareto_points",
    [
        (True, True, np.array([[0.8, 0.7], [0.9, 0.6]])),
        (False, True, np.array([[0.7, 0.8], [0.6, 0.9]])),
        (True, False, np.array([[0.9, 0.6]])),
        (False, False, np.array([])),
    ],
)
def test_find_pareto_points(sample_data, accuracy_minimise, fairness_minimise, expected_pareto_points):
    """
    Test the find_pareto_points method with different minimization preferences and expected results.
    """
    finder = ParetoOptimalPointsFinder(accuracy_minimise, fairness_minimise, data=sample_data)
    pareto_points = finder.find()
    assert np.array_equal(pareto_points, expected_pareto_points)


def test_explain_pareto_points(sample_data):
    """
    Test the explain_pareto_points method with sample data.
    """
    finder = ParetoOptimalPointsFinder(data=sample_data)
    pareto_points = finder.find()
    explanations = finder.explain_pareto_points()

    # Assert the length of explanations matches the number of Pareto points
    assert len(explanations) == len(pareto_points)

    # Check explanation format (without specific content verification)
    assert isinstance(explanations[0], dict)
    assert 'Point' in explanations[0]
    assert 'Explanation' in explanations[0]
