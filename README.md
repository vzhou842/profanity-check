# Alt-profanity-check

Alt profanity check is a drop-in replacement of the `profanity-check` library for the not so well
maintained <https://github.com/vzhou842/profanity-check>:

> A fast, robust Python library to check for profanity or offensive language in strings.
> Read more about how and why `profanity-check` was built in 
> [this blog post](https://victorzhou.com/blog/better-profanity-detection-with-scikit-learn/).

Our aim is to follow scikit-learn's (main dependency) versions and post models trained with the
same version number, example alt-profanity-check version 1.2.3.4 should be trained with the
1.2.3.4 version of the scikit-learn library.

For joblib which is the next major dependency we will be using the latest one which was available
when we trained the models.

Last but not least we aim to clean up the codebase a bit and **maybe** introduce some features or
datasets.

## Changelog

See
[CHANGELOG.md](https://github.com/dimitrismistriotis/alt-profanity-check/blob/master/CHANGELOG.md)

## How It Works

`profanity-check` uses a linear SVM model trained on 200k human-labeled samples of clean and
profane text strings. Its model is simple but surprisingly effective, meaning
**`profanity-check` is both robust and extremely performant**.

## Why Use profanity-check?

### No Explicit Blacklist

Many profanity detection libraries use a hard-coded list of bad words to detect and filter
profanity. For example, [profanity](https://pypi.org/project/profanity/) uses 
[this wordlist](https://github.com/ben174/profanity/blob/master/profanity/data/wordlist.txt),
and even [better-profanity](https://pypi.org/project/better-profanity/) still uses
[a wordlist](
https://github.com/snguyenthanh/better_profanity/blob/master/better_profanity/profanity_wordlist.txt).
There are obviously glaring issues with this approach, and, while they might be performant, 
**these libraries are not accurate at all**.

A simple example for which `profanity-check` is better is the phrase 
* "You cocksucker"* - `profanity` thinks this is clean because it doesn't have 
* "cocksucker"* in its wordlist.

### Performance

Other libraries like [profanity-filter](https://github.com/rominf/profanity-filter)
use more sophisticated methods that are much more accurate but at the cost of performance.
A benchmark (performed December 2018 on a new 2018 Macbook Pro) using 
[a Kaggle dataset of Wikipedia comments](
https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data) yielded roughly 
the following results:

| Package          | 1 Prediction (ms) | 10 Predictions (ms) | 100 Predictions (ms) |
|------------------|-------------------|---------------------|----------------------|
| profanity-check  | 0.2               | 0.5                 | 3.5                  |
| profanity-filter | 60                | 1200                | 13000                |
| profanity        | 0.3               | 1.2                 | 24                   |

`profanity-check` is anywhere from **300 - 4000 times faster** than `profanity-filter` in this
benchmark!

### Accuracy

This table speaks for itself:

| Package          | Test Accuracy | Balanced Test Accuracy | Precision | Recall | F1 Score |
|------------------|---------------|------------------------|-----------|--------|----------|
| profanity-check  | 95.0%         | 93.0%                  | 86.1%     | 89.6%  | 0.88     |
| profanity-filter | 91.8%         | 83.6%                  | 85.4%     | 70.2%  | 0.77     |
| profanity        | 85.6%         | 65.1%                  | 91.7%     | 30.8%  | 0.46     |

See the How section below for more details on the dataset used for these results.

## Installation

```
$ pip install alt-profanity-check
```

### For older Python versions

#### Python 3.7

From Scikit-learn's [Github page](https://github.com/scikit-learn/scikit-learn):

> scikit-learn 1.0 and later require Python 3.7 or newer.
> scikit-learn 1.1 and later require Python 3.8 or newer.

Which means that from 1.1.2 and later, Python 3.7 is not supported, hence:
If you are using 3.6 pin  alt-profanity-check to **1.0.2.1**.

#### Python 3.6

Following Scikit-learn, **Python3.6** is not supported after its 1.0 version if you are using 3.6 pin
alt-profanity-check to **0.24.2**.

## Usage

You can test from the command line:

```shell
profanity_check "Check something" "Check something else"
```

```python
from profanity_check import predict, predict_prob

predict(['predict() takes an array and returns a 1 for each string if it is offensive, else 0.'])
# [0]

predict(['fuck you'])
# [1]

predict_prob(['predict_prob() takes an array and returns the probability each string is offensive'])
# [0.08686173]

predict_prob(['go to hell, you scum'])
# [0.7618861]
```

Note that both `predict()` and `predict_prob` return [`numpy`](https://pypi.org/project/numpy/)
arrays.

## More on How/Why It Works

### How

Special thanks to the authors of the datasets used in this project. `profanity-check` hence also
`alt-profanity-check` is trained on a combined dataset from 2 sources:
- [t-davidson/hate-speech-and-offensive-language](
  https://github.com/t-davidson/hate-speech-and-offensive-language/tree/master/data),
  used in their paper *Automated Hate Speech Detection and the Problem of Offensive Language*
- the [Toxic Comment Classification Challenge](
  https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data) on Kaggle.

`profanity-check` relies heavily on the excellent [`scikit-learn`](https://scikit-learn.org/)
library. It's mostly powered by `scikit-learn` classes 
[`CountVectorizer`](
https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html),
[`LinearSVC`](https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html), and
[`CalibratedClassifierCV`](
https://scikit-learn.org/stable/modules/generated/sklearn.calibration.CalibratedClassifierCV.html).
It uses a [Bag-of-words model](https://en.wikipedia.org/wiki/Bag-of-words_model)
to vectorize input strings before feeding them to a linear classifier.

### Why

One simplified way you could think about why `profanity-check` works is this:
during the training process, the model learns which words are "bad" and how "bad" they are
because those words will appear more often in offensive texts. Thus, it's as if the training
process is picking out the "bad" words out of all possible words and using those to make future
predictions. This is better than just relying on arbitrary word blacklists chosen by humans!

## Caveats

This library is far from perfect. For example, it has a hard time picking up on less common
variants of swear words like *"f4ck you"* or *"you b1tch"* because they don't appear often 
enough in the training corpus. **Never treat any prediction from this library as 
unquestionable truth, because it does and will make mistakes.** Instead, use this library as a
heuristic.

## Developer Notes

- Create a virtual environment from the project
- `pip install -r development_requirements.txt`

### Retraining data

With the above in place:

```shell
cd profanity_check/data
python train_model.py
```

### Uploading to PyPi

Currently trying to automate it using Github Actions; see:
`.github/workflows/package_release_dry_run.yml`.

Setup:

- Set up your "~/.pypirc" with the appropriate token
- `pip install -r requirements_for_uploading.txt` which installs twine

New Version:

With `x.y.z` as the version to be uploaded:

First tag:

```shell
git tag -a vx.y.z -m "Version x.y.z"
git push --tags
```

Then upload:

```shell
python setup.py sdist
twine upload dist/alt-profanity-check-x.y.z.tar.gz
```
