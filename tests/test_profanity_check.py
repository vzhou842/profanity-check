import unittest
from profanity_check import predict, predict_prob

class test_profanity_check(unittest.TestCase):
  def test_accuracy(self):
    texts = [
      'Hello there, how are you',
      'Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
      '!!!! Click this now!!! -> https://example.com',
      'fuck you',
      'fUcK u',
      'GO TO hElL, you dirty scum',
    ]
    self.assertListEqual([0, 0, 0, 1, 1, 1], list(predict(texts)))

    probs = predict_prob(texts)
    for i in range(len(probs)):
      if i < 3:
        self.assertGreaterEqual(0.5, probs[i])
      else:
        self.assertLessEqual(0.5, probs[i])

  def test_edge_cases(self):
    texts = [
      '',
      '                    ',
      'this is but a test string, there is no offensive language to be found here! :) ' * 25,
      'aaaaaaa' * 100,
    ]

    self.assertListEqual([0, 0, 0, 0], list(predict(texts)))

if __name__ == "__main__":
  unittest.main()
