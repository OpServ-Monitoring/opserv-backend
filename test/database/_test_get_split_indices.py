from unittest import TestCase

from database import historical_data_retrieve_dumb as method_holder


class TestGet_split_indices(TestCase):
    def test_get_split_indices_when_limit_is_zero(self):
        with self.assertRaises(ValueError):
            method_holder.get_split_indices(1, 0)

    def test_get_split_indices_when_limit_is_negative(self):
        with self.assertRaises(ValueError):
            method_holder.get_split_indices(0, -10)

    def test_get_split_indices_when_limit_is_greater_than_count(self):
        with self.assertRaises(ValueError):
            method_holder.get_split_indices(5, 10)

    def test_get_split_indices_when_limit_is_equal_count(self):
        with self.assertRaises(ValueError):
            method_holder.get_split_indices(1000, 1000)

    def test_get_split_indices_when_limit_is_below_count(self):
        self.assertEqual(
            method_holder.get_split_indices(2, 1),
            [(0, 1)]
        )

        self.assertEqual(
            method_holder.get_split_indices(79, 7),
            [
                (0, 11),
                (12, 22),
                (23, 33),
                (34, 45),
                (46, 56),
                (57, 67),
                (68, 78)
            ]
        )

        self.assertEqual(
            method_holder.get_split_indices(27, 9),
            [(0, 2), (3, 5), (6, 8), (9, 11), (12, 14), (15, 17), (18, 20), (21, 23), (24, 26)]
        )
