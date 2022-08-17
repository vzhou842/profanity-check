"""For Command Line Interface"""
import sys

from .profanity_check import predict
from .profanity_check import predict_prob


def main() -> None:
    """Main command line entry point

    First implementation is experimental hence suboptimal, will improve
    """
    if len(sys.argv) <= 1:
        print("Specify at least one string to check", file=sys.stderr)
        sys.exit(1)

    # print(sys.argv[1:])
    texts_vector = sys.argv[1:]

    print("Binary Predictions:")
    print()
    for item_and_prediction in zip(texts_vector, predict(texts_vector)):
        print(f"{item_and_prediction[0]}: {item_and_prediction[1]}")
    print()

    print("Probabilistic Predictions:")
    print()
    for item_and_prediction in zip(texts_vector, predict_prob(texts_vector)):
        print(f"{item_and_prediction[0]}: {item_and_prediction[1]}")
    print()

    sys.exit(0)
