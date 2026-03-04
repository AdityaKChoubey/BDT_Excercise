# BDT Examples

This repository contains simple examples demonstrating the use of **Boosted Decision Trees (BDTs)** for classification problems. The examples focus on illustrating the difference between **linear classifiers** and **non-linear ensemble methods** such as Gradient Boosted Decision Trees.

The goal is to build intuition for how different machine learning models separate **signal and background distributions**, particularly in contexts similar to **high energy physics (HEP)** analyses.

## Contents

### Fisher vs BDT Example

This example compares a **linear classifier (Fisher discriminant)** with a **Boosted Decision Tree (BDT)** using TMVA.

The example demonstrates:

* How linear classifiers attempt to separate data using a **linear decision boundary**
* How BDTs can learn **non-linear decision boundaries**
* The difference in **separation power** between the two methods

Typical outputs include:

* Classifier response distributions
* ROC curves
* Signal vs background separation plots

## Tools Used

* ROOT
* TMVA (Toolkit for Multivariate Analysis)
* Python

## Purpose

These examples are meant for:

* Learning how BDTs work
* Understanding why BDTs outperform linear classifiers in many problems
* Demonstrating classifier performance in a simple and controlled setting

## Future Additions

Planned additions include:

* More complex toy datasets
* Feature correlation studies
* Decision boundary visualizations
* Comparison with other classifiers (e.g., neural networks)

## Author

Aditya Kumar Choubey

