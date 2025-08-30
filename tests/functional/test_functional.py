import pytest

pytestmark = pytest.mark.parametrize(("input_values", "expected_result"), [([1, 1], 2), ([1, 2], 3)])


EXPECTED_CLASS_VARIABLE = 123


class TestFunctional:
    """Example Functional test class."""

    class_variable = EXPECTED_CLASS_VARIABLE

    def test_example(self, input_values: str, expected_result: int) -> None:
        """Example Functional test."""
        assert self.class_variable == EXPECTED_CLASS_VARIABLE
        assert sum(input_values) == expected_result
