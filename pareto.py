import pandas as pd
import numpy as np
from typing import Union

class ParetoOptimalPointsFinder:
    """
    A class to find Pareto-optimal points in a dataset.
    """

    def __init__(self, data:Union[pd.DataFrame, np.ndarray], accuracy_minimise: bool=True, fairness_minimise: bool=True) -> None:
        """
        Initialize the class with data, user preferences for minimization.

        Parameters:
        - data (Union[pd.DataFrame, np.ndarray]): 2D data with two columns representing accuracy and fairness scores.
        - accuracy_minimise (bool, optional): Whether to minimize the first objective (accuracy). Defaults to True.
        - fairness_minimise (bool, optional): Whether to minimize the second objective (fairness score). Defaults to True.
        """
        if isinstance(data, pd.DataFrame):
            self.data = data.to_numpy()
        else:
            self.data = data
        self.accuracy_minimise = accuracy_minimise
        self.fairness_minimise = fairness_minimise

    def find(self):
        """
        Find Pareto-optimal points in the stored data based on user preferences.

        Returns:
        - Union[pd.DataFrame, np.ndarray]: Pareto-optimal points from the input data.
        """

        pareto_points = []

        for i, (accuracy_1, fair_1) in enumerate(self.data):
            is_pareto = True

            for j, (accuracy_2, fair_2) in enumerate(self.data):
                if i == j:
                    continue  # Skip self-comparison

                # Check Pareto dominance based on user preferences stored in init
                if (
                    (accuracy_1 < accuracy_2 if self.accuracy_minimise else accuracy_1 > accuracy_2) and
                    (fair_1 < fair_2 if self.fairness_minimise else fair_1 > fair_2)
                ):
                    is_pareto = False
                    break

            if is_pareto:
                pareto_points.append((accuracy_1, fair_1))

        return np.array(pareto_points)
    
    def explain_pareto_points(self, pareto_points):
        """
        Provide explanations for why each point in the Pareto frontier is considered optimal.

        Parameters:
        - pareto_points (Union[pd.DataFrame, np.ndarray]): The Pareto-optimal points found by the `find` method.

        Returns:
        - List[Dict[str, str]]: A list of explanations for each Pareto-optimal point.

        This function analyzes the data and Pareto points to explain why each point is not dominated by others.
        """

        explanations = []
        for i, point in enumerate(pareto_points):
            explanation = {
                'Point': f'Point {i + 1}',
                'Explanation': 'This point satisfies the following criteria:'
            }

            for j, (accuracy_2, fair_2) in enumerate(self.data):
                if i == j:
                    continue  # Skip self-comparison

                # Analyze why this point is not dominated by point j
                domination_text = (
                    f'better accuracy' if (point[0] < accuracy_2 if self.accuracy_minimise else point[0] > accuracy_2) else 'worse accuracy'
                )
                domination_text += (
                    f' and better fairness' if (point[1] < fair_2 if self.fairness_minimise else point[1] > fair_2) else ' and worse fairness'
                )
                explanation[f'Criteria {j + 1}'] = f'Not dominated ({domination_text})'

            explanations.append(explanation)

        return explanations


