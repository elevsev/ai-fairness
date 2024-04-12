import pandas as pd
import numpy as np

# class ParetoOptimizer:

#     def __init__(self):
#        self.costs = None
#        self.sense = None

#     def set_inputs(self, costs, sense):
#         # Input validation
       
#         self.costs = costs
#         self.sense = sense

#     def _is_dominated(self, row1, row2):
#         """Check if row1 is dominated by row2""" 
#         for i in range(len(row1)):
#             if self.sense[i] == "min" and row1[i] > row2[i]:
#                 return True
#         return False
            
#     def optimize(self):
#         pareto_set = []
#         for i, row1 in self.costs.iterrows():
#             dominated = False  
#             for j, row2 in self.costs.iterrows():
#                 if i == j:
#                     continue     
#                 dominated |= self._is_dominated(row1, row2)

#             if not dominated:
#                 pareto_set.append(row1)

#         return pd.DataFrame(pareto_set, columns=self.costs.columns)

class ParetoOptimizer:

    def __init__(self): 
        self.costs = None
        self.sense = None
        self.optimize_for = None

    def set_inputs(self, costs, optimize_for="min"):
        """Set costs data and optimization approach"""
        self.costs = costs
        self.optimize_for = optimize_for

    def configure(self):
        """Configure min/max sense based on optimize_for"""
        n_cols = len(self.costs.columns)
        
        if self.optimize_for == "min":
            # Initialize columns as minimized
            self.sense = ["min"]*n_cols  
        else:
            # Initialize columns as maximized
            self.sense = ["max"]*n_cols

    def toggle_objective(self, column): 
        """Flip column's optimization sense"""
        col_idx = self.costs.columns.get_loc(column)
        self.sense[col_idx] = "min" if self.sense[col_idx]=="max" else "max"
    
    def optimize(self):
        self.configure()
        
        pareto_optimal_set = []
        for index1, row1 in self.costs.iterrows():
            dominated = False
            for index2, row2 in self.costs.iterrows():
                if index1 == index2: continue
                    
                # Check dominance 
                dominated =  self._dominates(row1, row2)

                if self.optimize_for == "max":
                    dominated = self._dominates(row2, row1)

            if not dominated:
                pareto_optimal_set.append(row1)
        
        return pd.DataFrame(pareto_optimal_set, columns=self.costs.columns)

    def _dominates(self, row1, row2):
        """Return True if row1 dominates row2"""     
        for i in range(len(row1)):
            if self.sense[i] == "min" and row1[i] > row2[i]:
                return True  
        return False