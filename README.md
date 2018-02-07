# bitcoin prediction

## Setup

### Install all the requirements

`pip install -r requirements.txt`

## What should I check out first

A good starting point would be to check out the 1.0-oo-initial-rough-lstm notebook.

It is hopefully well enough documented to get you going.

## Models

### MAE-01

This model is a simplified but more effective version of the one we build in the notebook. It can only predict one datapoint ahead, but does so with a pretty decent precision.

You can actually use this model for more serious cases than the one in the notebook. The path to the dataset is currently hardcoded, but that is easily changed.

Meaning, you can easily update and retrain the neural network to stay current!

#### visualization

`make mae.visualize`

#### predict

`make mae.predict`

#### train

`make mae.train`
