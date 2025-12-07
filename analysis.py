import marimo

__generated_with__ = "0.9.16"

app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    # Contact email for this notebook: 24f3000312@ds.study.iitm.ac.in
    #
    # Data flow note:
    # - This cell defines core libraries and returns them.
    # - Later cells depend on mo, np, pd, and plt to build UI, data, and plots.
    return mo, np, pd, plt


@app.cell
def __(mo):
    # UI cell:
    # - Defines interactive widgets.
    # - Downstream cells will read slider values through these objects.
    corr_slider = mo.ui.slider(
        0.0,
        0.99,
        0.01,
        value=0.5,
        label="Correlation strength ρ",
    )
    sample_size = mo.ui.slider(
        50,
        1000,
        50,
        value=200,
        label="Sample size n",
    )

    controls = mo.ui.hstack([corr_slider, sample_size])
    controls  # Display stacked sliders in the notebook UI

    return corr_slider, sample_size


@app.cell
def __(np, corr_slider, sample_size):
    # Data generation cell:
    # - Depends on corr_slider and sample_size from the UI cell.
    # - Produces synthetic (x, y) data for a bivariate normal distribution.
    rho = corr_slider.value
    n = int(sample_size.value)

    cov = np.array([[1.0, rho], [rho, 1.0]])
    mean = np.array([0.0, 0.0])

    x, y = np.random.multivariate_normal(mean, cov, size=n).T
    return rho, n, x, y


@app.cell
def __(pd, x, y):
    # Tabular view cell:
    # - Depends on x, y from the data-generation cell.
    # - Wraps data in a DataFrame for inspection / further analysis.
    df = pd.DataFrame({"x": x, "y": y})
    df.head()  # Show top rows in the UI
    return df,


@app.cell
def __(mo, rho, n):
    # Dynamic markdown cell:
    # - Depends on rho and n from the data-generation cell.
    # - Renders explanatory text that updates when sliders change.
    md = mo.md(
        f"""
        # Interactive correlation demo

        - **Sample size**: `{n}`
        - **Target correlation (ρ)** from slider: `{rho:.2f}`

        Use the sliders above to explore how changing ρ and n affects
        the apparent relationship between variables `x` and `y`.

        - Higher ρ → points fall closer to a line.
        - Lower ρ → relationship becomes weaker and more scattered.
        """
    )
    md


@app.cell
def __(plt, x, y, rho):
    # Visualization cell:
    # - Depends on x, y, and rho.
    # - Produces a scatter plot that updates automatically when the
    #   upstream sliders change.
    fig, ax = plt.subplots()
    ax.scatter(x, y, alpha=0.5)
    ax.set_title(f"Scatter of x vs y (approx ρ ≈ {rho:.2f})")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    fig


@app.cell
def __(app):
    # Entry point cell:
    # - Allows running the notebook as a script: `python analysis.py`
    # - marimo will launch an interactive UI in the browser.
    if __name__ == "__main__":
        app.run()
