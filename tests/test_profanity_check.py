"""(Mostly smoke) tests"""

from profanity_check import predict, predict_prob


def test_accuracy():
    """Tests with sample text"""
    # pylint:disable=consider-using-enumerate,consider-using-in
    texts = [
        "Hello there, how are you",
        "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
        "!!!! Click this now!!! -> https://example.com",
        "fuck you",
        "fUcK u",
        "GO TO hElL, you dirty scum",
    ]
    assert list(predict(texts)) == [0, 1, 0, 1, 1, 1]

    probabilities = predict_prob(texts)
    for i in range(len(probabilities)):
        if i == 0 or i == 2:
            assert probabilities[i] <= 0.5
        else:
            assert probabilities[i] >= 0.5


def test_edge_cases():
    """Edge cases: empty and long strings"""
    texts = [
        "",
        "                    ",
        (
            "this is but a test string, "
            "there is no offensive language to be found here! :) "
        )
        * 25,
        "aaaaaaa" * 100,
    ]
    assert list(predict(texts)) == [0, 0, 0, 0]
