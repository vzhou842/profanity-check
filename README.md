# profanity-check

[![Build Status](https://travis-ci.com/vzhou842/profanity-check.svg?branch=master)](https://travis-ci.com/vzhou842/profanity-check)

A fast, robust Python library to check for profanity or offensive language in strings.

## Installation

```
$ pip install profanity-check
```

## Usage

```python
from profanity_check import predict, predict_prob

print(
  predict([
    'predict() returns a 1 if the string is offensive and 0 otherwise.',
    'fuck you',
  ])
) # [0, 1]

print(
  predict_prob([
    'predict_prob() returns the probability the string is offensive',
    'go to hell, you scum',
  ])
) # [0.11799814 0.7618861]
```
