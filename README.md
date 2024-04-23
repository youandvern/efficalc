<p align="center">
  <img src="https://github.com/youandvern/efficalc/raw/main/docs_src/efficalc.png" alt="Logo" width="200"/>
</p>

<p align="center">
  <a href="https://github.com/youandvern/efficalc/actions/workflows/tests.yml"><img alt="Tests" src="https://github.com/youandvern/efficalc/actions/workflows/tests.yml/badge.svg"></a>&nbsp;&nbsp;&nbsp;
  <a href="https://coveralls.io/github/youandvern/efficalc?branch=main"><img alt="Coverage Status" src="https://coveralls.io/repos/github/youandvern/efficalc/badge.svg?branch=main&v=1.1.0"></a>&nbsp;&nbsp;&nbsp;
  <a href="https://github.com/youandvern/efficalc/blob/main/LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>&nbsp;&nbsp;&nbsp;
  <a href="https://badge.fury.io/py/efficalc"><img alt="PyPI version" src="https://badge.fury.io/py/efficalc.svg?version=1.1.0"></a>
</p>


# efficalc

### A feature-rich Python library for reimagined engineering calculations.

<!-- TABLE OF CONTENTS -->
<details>
  <summary style="font-size:1.5rem;"><b>Contents</b></summary>
  <ul>
    <li><a href="#introduction">Introduction</a><ul>
        <li><a href="#examples">Examples</a></li>
        <li><a href="#documentation-and-distribution">Documentation</a></li></ul></li>
    <li><a href="#quickstart">Quickstart</a><ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#first-calculation-function">First Calculation</a></li>
        <li><a href="#view-the-report">View Report</a></li></ul></li>
    <li><a href="#features">Features</a></li>
  </ul>
</details>


# Introduction

##### efficalc provides an extensible, testable, and powerful framework for building and managing complex calculations.

**efficalc** is designed to transform how engineers approach calculations, moving away from traditional methods like manual spreadsheets and toward a more efficient, accurate, and collaborative engineering calculation process.

### Simple syntax for Python calculations:

![Efficalc Demo Typing](https://github.com/youandvern/efficalc/raw/main/docs_src/_static/efficalc_basic_demo_typing.jpg?raw=true)

### Turns into submittal-ready reports:

![Efficalc Demo Report](https://github.com/youandvern/efficalc/raw/main/docs_src/_static/efficalc_basic_demo2.png?raw=true)


## Examples

- [Simple Examples](https://github.com/youandvern/efficalc/tree/main/examples/simple)
- [More Advanced Examples](https://github.com/youandvern/efficalc/tree/main/examples/advanced)

## Documentation and Distribution

- [Full documentation](https://youandvern.github.io/efficalc)
- [PyPI distribution](https://pypi.org/project/efficalc/)



# Quickstart

### Installation

Install efficalc with pip:

```bash
pip install efficalc
```

### First Calculation Function

Calculations in efficalc are written as a function. 

These calculation functions are primarily composed of `Input` and `Calculation` elements, but there are also many more options to make a clear and accurate calculation.

```python
from efficalc import Calculation, Input, Title, sqrt

def calculation():
    Title("Pythagorean's Theorem and Perimeter")
    
    a = Input("a", 3, description="Length of side a")
    b = Input("b", 4, description="Length of side b")
    
    c = Calculation("c", sqrt(a**2 + b**2), description="Length of the hypotenuse")
    
    Calculation("P", a + b + c, description="Perimeter of the triangle")
```

### View the Report

Instantly view or print a report for your calculation in your browser with the `ReportBuilder`.

```python
from efficalc.report_builder import ReportBuilder
from pythagorean_perimeter import calculation

builder = ReportBuilder(calculation)
builder.view_report()
```

![The resulting calculation report](https://github.com/youandvern/efficalc/raw/main/docs_src/_static/pythagorean_default.png)


### Updating Input Values

The value provided to the `Input` class in your calculation function is treated as a default value. 

When you run your calculation with different input values, pass in a dictionary of the default overrides into the optional second parameter of the `ReportBuilder`:


```python
new_inputs = {"a": 9.2, "b": 0.87}
builder = ReportBuilder(calculation, new_inputs)
builder.view_report()
```


# Features


#### Automated report generation
Generate detailed, professional reports automatically, ensuring clarity and precision in communication.

#### Open source
efficalc welcomes community contributions. Request features or contribute directly to enhance its capabilities.

#### Engineering-specific features
Benefit from built-in tools tailored to solving common engineering challenges. [See our section property library in action](https://github.com/youandvern/efficalc/blob/main/examples/advanced/steel_beam_moment_strength.py#L53).

#### Reusable
Create calculation templates once and reuse them across multiple designs and projects, saving time and ensuring consistency.

#### Testable
Easily test your calculations to reduce errors and improve confidence every design. [Read the testing guide.](https://youandvern.github.io/efficalc/testing.html)

#### Integrate with other workflows
Seamlessly integrate with your existing Python-enabled workflows to boost efficiency and connectivity across tools and platforms. [See some examples of this.](https://youandvern.github.io/efficalc/integration.html)

#### Figures now supported
Easily add figures to your calculation reports for even more clarity. [Read the full documentation for figures.](https://youandvern.github.io/efficalc/figures.html)

#### Control your content
Tailor your calculation reports to include only the most relevant information, making them as concise or detailed as you prefer.

# Contributing

We welcome contributions of all kinds from the community! Whether it's reporting a bug, requesting a feature, or submitting a pull request, your input and engagement is invaluable to efficalc's development.

- Report issues [here](https://github.com/youandvern/efficalc/issues).
- Submit pull requests [here](https://github.com/youandvern/efficalc/pulls).

# Built With

* [latexexpr](https://github.com/kajusK/latexexpr) - [we use a forked version](https://github.com/youandvern/latexexpr_efficalc)
* [pylatexenc](https://github.com/phfaist/pylatexenc)

#### Documentation

* [sphinx](https://www.sphinx-doc.org/en/master/)
* [furo](https://github.com/pradyunsg/furo/)
* [sphinx-copybutton](https://github.com/executablebooks/sphinx-copybutton)
* [sphinxcontrib-video](https://github.com/sphinx-contrib/video)

# License

efficalc is released under the [MIT License](https://github.com/youandvern/efficalc/tree/main/LICENSE).

