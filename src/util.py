import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression

def plot_logistic_regression_feature_importance(fitted_lr_pipe, head=None, precision=3, cmap="PiYG", vmin=None, vmax=None):
    """
    Plots the feature importance for a fitted logistic regression model.

    Parameters:
    ----------
    fitted_lr_pipe : sklearn.pipeline.Pipeline
        Fitted pipeline containing a ColumnTransformer and LogisticRegression as its components.
    head : int, default=None
        Number of top features to display in the plot. If None, all features are displayed.
    precision : int, default=3
        Number of decimal places to round the coefficients.
    cmap : str, default="PiYG"
        Colormap for the background gradient in the plot.
    vmin : float, default=None
        Minimum value for the colormap scale.
    vmax : float, default=None
        Maximum value for the colormap scale.

    Returns:
    ----------
    pandas.io.formats.style.Styler
        Styled data frame containing the sorted feature importance with columns: 'feature' and 'coef'.

    Raises:
    ----------
    TypeError
        If `fitted_lr_pipe` does not have exactly 2 components: ColumnTransformer and LogisticRegression.
        If the 1st component in `fitted_lr_pipe` is not a ColumnTransformer.
        If the 2nd component in `fitted_lr_pipe` is not a LogisticRegression.
        If ColumnTransformer has no Encoder.
        If LogisticRegression is not fitted.

    ValueError
        If the number of features does not match the number of coefficients.
    """

    if len(fitted_lr_pipe.named_steps) != 2:
        raise TypeError("`fitted_lr_pipe` is expected to have exactly two components: ColumnTransformer and LogisticRegression")
    
    ct, lr = fitted_lr_pipe.named_steps.values()
    
    if not isinstance(ct, ColumnTransformer):
        raise TypeError("1st component in the `fitted_lr_pipe` is expected to be a ColumnTransformer")
    if not isinstance(lr, LogisticRegression):
        raise TypeError("2nd component in the `fitted_lr_pipe` is expected to be a LogisticRegression")
    if len(ct.named_transformers_) == 0:
        raise TypeError("ColumnTransformer has no Encoder")
    try:
        coef = lr.coef_[0]
    except AttributeError as e:
        raise TypeError("LogisticRegression is not fitted (`fitted_lr_pipe.fit(X_train, y_train))")
        
    features = []
    for enc in ct.named_transformers_.values():
        features += enc.get_feature_names_out().tolist()
        
    if len(features) != len(coef):
        raise ValueError("The number of features does not match the number of coefficients")
    
    feature_importance = pd.DataFrame({
        'feature': features,
        'coef': coef.tolist(),
        'coef_abs': abs(coef).tolist()
    })

    feature_importance = (
        feature_importance
        .sort_values('coef_abs', ascending=False)
        .reset_index(drop=True)
        .drop(columns=["coef_abs"])
        .head(head)
        .style.format(
            precision=3)
        .background_gradient(
            cmap=cmap,
            vmin=vmin,
            vmax=vmax,
            axis=None)
    )

    return feature_importance
