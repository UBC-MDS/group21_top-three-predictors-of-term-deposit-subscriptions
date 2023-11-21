import pytest
import numpy as np
import pandas as pd
import altair as alt
import sys
sys.path.append("../")

from src.util import *

def test_eda_none():
    np.random.seed(123)
    test_data = pd.DataFrame({
        "cate1": ["a", "a", "b", "b", "b", "c", "a", "b", "a", "c"],
        "cate2": ["c", "c", "b", "b", "b", "a", "c", "b", "c", "a"],
        "num1": np.random.normal(size=10),
        "num2": np.random.normal(size=10)
    })

    num_chart_1, cate_chart_1 = eda_plots(test_data, categorical_cols=["cate1"])
    num_chart_2, cate_chart_2 = eda_plots(test_data, numerical_cols=["num1"])
    num_chart_3, cate_chart_3 = eda_plots(test_data)

    assert num_chart_1 is None, "Numerical chart should be None without input for numerical columns."
    assert isinstance(cate_chart_1, alt.RepeatChart), "Incorrect data type for categorical chart."
    assert isinstance(num_chart_2, alt.RepeatChart), "Incorrect data type for numerical chart."
    assert cate_chart_2 is None, "Categorical chart should be None without input for numerical columns."
    assert num_chart_3 is None, "Numerical chart should be None without input for numerical columns."
    assert cate_chart_3 is None, "Categorical chart should be None without input for numerical columns."