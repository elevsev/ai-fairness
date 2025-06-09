import pandas as pd

sample_df = pd.DataFrame({
    "Gaurdrail": ["Bias", "Misalignment", "Hallucination", "Hallucination"],
    "Method": ["AIAssistedGuardrails", "AIAssistedGuardrails", "AIAssistedGuardrails", "CosineSimilarity"],
    "ACCURACY": [0.650966, 0.646552, 0.664679, 0.556805],
    "TPR": [0.512241, 0.719298, 0.652418, 0.391451],
    "FPR": [0.210179, 0.724123, 0.31946, 0.27784],
    "F1": [0.594861, 0.742138, 0.661723, 0.469003],
    "LATENCY (S)": [1.471627, 2.263252, 2.2027, 0.408035],
    "FIN COST (USD)": [0.000653, 0.004334, 0.00203, 0.0],
    "ENV COST (GCO2)": [0.100474, 0.85975, 0.366783, 0.0]
})

available_metrics = [
    "ACCURACY", "TPR", "FPR", "F1", "LATENCY (S)", "FIN COST (USD)", "ENV COST (GCO2)"
]

guardrail_info = {
    "Bias": "Bias refers to systematic unfairness in model outcomes, often related to sensitive attributes.",
    "Hallucination": "Hallucinations occur when the model produces plausible but incorrect or fabricated information.",
    "Misalignment": "Misalignment measures how far a model's output strays from intended goals or user intent."
}

metric_info = {
    "ACCURACY": {"definition": "Proportion of correct predictions.",
                 "formula": "(TP + TN) / (TP + TN + FP + FN)",
                 "interpretation": "Higher is better."},
    "TPR": {"definition": "True Positive Rate.",
            "formula": "TP / (TP + FN)",
            "interpretation": "Higher is better."},
    "FPR": {"definition": "False Positive Rate.",
            "formula": "FP / (FP + TN)",
            "interpretation": "Lower is better."},
    "F1": {"definition": "Harmonic mean of precision and recall.",
           "formula": "2 * (Precision * Recall) / (Precision + Recall)",
           "interpretation": "Higher is better."},
    "LATENCY (S)": {"definition": "Time taken for a response.",
                    "formula": "Seconds.",
                    "interpretation": "Lower is better."},
    "FIN COST (USD)": {"definition": "Financial cost per query.",
                        "formula": "US Dollars.",
                        "interpretation": "Lower is better."},
    "ENV COST (GCO2)": {"definition": "Environmental cost.",
                         "formula": "Grams of CO2 emitted.",
                         "interpretation": "Lower is better."}
}