from unittest import TestCase

from .app.app import sum_two_numbers

class AppTest(TestCase):

    def test_sum_two_numbers_Should_return_their_sum(self):
        self.assertEqual(sum_two_numbers(1, 2), 3)


if __name__ == "__main__":
     unittest.main()