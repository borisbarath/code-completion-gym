from lib import Predictor, Counter

test_function = """
import numpy as np

def get_zeros(length):
    zeros = np.zeros(length)
    return zeros
"""
test_counter = Counter()
test_saved_keystrokes = 0


class DummyPredictor(Predictor):
    def predict(self, line, lineno, column, limit=5):
        return []


class VoidPredictor(Predictor):
    def predict(self, line, lineno, column, limit=5):
        return ['']


class PerfectPredictor(Predictor):
    def __init__(self, ground_truth_code):
        self.lines = ground_truth_code.split("\n")

    def predict(self, line, lineno, column, limit=5):
        completion = self.lines[lineno][column+1:column+3]
        global test_saved_keystrokes
        if len(completion) == 2:
            test_saved_keystrokes += 1

        return [completion]


class SecondChoicePredictor(Predictor):
    def __init__(self, ground_truth_code):
        self.lines = ground_truth_code.split("\n")

    def predict(self, line, lineno, column, limit=5):
        completion = self.lines[lineno][column+1:column+5]
        global test_saved_keystrokes
        if len(completion) > 2:
            # as it takes 2 keystrokes to select this completion
            test_saved_keystrokes += len(completion) - 2
        print("==============================")
        print("Got", line)
        print("Returning", repr(completion))

        return ["wrong_completion", completion]


def test_count_keystrokes_base_returns_length_of_input():
    assert(test_counter.count_keystrokes_base(
        test_function) == len(test_function))


def test_if_no_predictions_then_count_every_keystroke():
    predictor = DummyPredictor()
    assert(test_counter.count_keystrokes_predictor(
        test_function, predictor) == len(test_function))


def test_after_completing_counter_skips_correct_number_of_characters():
    global test_saved_keystrokes
    test_saved_keystrokes = 0

    predictor = PerfectPredictor(test_function)

    assert(test_counter.count_keystrokes_predictor(test_function,
                                                   predictor) + test_saved_keystrokes == len(test_function))


def test_correct_completion_second_in_array_saves_one_less_keystroke():
    global test_saved_keystrokes
    test_saved_keystrokes = 0

    predictor = SecondChoicePredictor(test_function)

    assert(test_counter.count_keystrokes_predictor(test_function,
                                                   predictor) + test_saved_keystrokes == len(test_function))


def test_empty_completion_not_used_in_counter():
    predictor = VoidPredictor()

    assert(test_counter.count_keystrokes_predictor(
        test_function, predictor) == len(test_function))


if __name__ == "__main__":
    test_count_keystrokes_base_returns_length_of_input()
    test_if_no_predictions_then_count_every_keystroke()
    test_after_completing_counter_skips_correct_number_of_characters()
    test_correct_completion_second_in_array_saves_one_less_keystroke()
    test_empty_completion_not_used_in_counter()
    print("Everything passed")
