from common_py.utils.yaml_reader import read_yaml
from definitions import TESTS_ROOT_DIR

TEST_FILE_PATH = TESTS_ROOT_DIR.joinpath("unit/utils/test_yaml_file.yaml")


class TestYamlReader:
    def test_join_constructor(self) -> None:
        data = read_yaml(path=TEST_FILE_PATH)
        assert data["test_join_constructor"] == {
            "key1": "value1",
            "key2": "value2",
            "key3": "value1-value2",
        }
