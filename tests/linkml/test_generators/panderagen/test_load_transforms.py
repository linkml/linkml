import pytest
from linkml.generators.panderagen.transforms import CollectionDictLoader, SimpleDictLoader

pl = pytest.importorskip("polars", minversion="1.0", reason="PolaRS >= 1.0 not installed")


@pytest.fixture
def simple_dict_of_literals_dataframe():
    """A column that is inlined as a simple dict can only be stored as a generic object
    when loaded via the dataframe constructor.
    """
    data = {
        "col1": [
            {"a": 1, "b": 2},
            {"c": 3},
            {},
        ]
    }
    return pl.DataFrame(data, schema={"col1": pl.Object})


@pytest.fixture
def simple_dict_of_structs_dataframe():
    """A column that is inlined as a simple dict can only be stored as a generic object
    when loaded via the dataframe constructor.
    """
    data = {
        "col1": [
            {"a": {"x": 1, "y": 2}, "b": {"x": 3, "y": 4}},
            {"c": {"x": 5, "y": 6}},
            {},
        ]
    }
    return pl.DataFrame(data, schema={"col1": pl.Object})


@pytest.fixture
def collection_dict_dataframe():
    """An object that is inlined within a dict can only be parsed
    as an inefficient generic pl.Object when loaded with the dataframe constructor.
    """
    data = {
        "col1": [
            {"a": {"x": 1, "y": 2}, "b": {"x": 3, "y": 4}},
            {"c": {"x": 5, "y": 6}},
            {},
        ]
    }
    return pl.DataFrame(data, schema={"col1": pl.Object})


def test_simple_dict_literal_load(simple_dict_of_literals_dataframe):
    """Verify that a pl.Object column representing a simple dict of literals
    can be properly converted to an efficient list of structs
    """
    nested_schema = {"my_id": pl.String, "other": pl.Int64}
    loaded_df = simple_dict_of_literals_dataframe.with_columns(
        SimpleDictLoader(
            struct_schema=nested_schema, id_col="my_id", other_col="other", id_dtype=pl.String, other_dtype=pl.Int64
        ).load("col1")
    )
    assert len(loaded_df) == 3
    assert len(loaded_df.columns) == 1
    assert loaded_df.schema == {"col1": pl.List(pl.Struct(nested_schema))}
    assert loaded_df.to_dicts() == [
        {
            "col1": [
                {"my_id": "a", "other": 1},
                {"my_id": "b", "other": 2},
            ]
        },
        {
            "col1": [
                {"my_id": "c", "other": 3},
            ]
        },
        {"col1": []},
    ]


def test_simple_dict_of_structs_load(simple_dict_of_structs_dataframe):
    """Verify that a pl.Object column representing a simple dict of structs
    can be properly converted to an efficient list of structs
    """
    nested_schema = {"x": pl.Int64, "y": pl.Int64}
    simple_dict_schema = {"my_id": pl.String, "other": pl.Struct(nested_schema)}
    loaded_df = simple_dict_of_structs_dataframe.with_columns(
        SimpleDictLoader(
            struct_schema=simple_dict_schema,
            id_col="my_id",
            other_col="other",
            id_dtype=pl.String,
            other_dtype=nested_schema,
        ).load("col1")
    )
    assert len(loaded_df) == 3
    assert len(loaded_df.columns) == 1
    assert loaded_df.schema == {"col1": pl.List(pl.Struct(simple_dict_schema))}
    assert loaded_df.to_dicts() == [
        {
            "col1": [
                {"my_id": "a", "other": {"x": 1, "y": 2}},
                {"my_id": "b", "other": {"x": 3, "y": 4}},
            ]
        },
        {
            "col1": [
                {"my_id": "c", "other": {"x": 5, "y": 6}},
            ]
        },
        {"col1": []},
    ]


def test_collection_dict_struct_load(collection_dict_dataframe):
    """Verify that a pl.Object column representing a struct nested as a collection dict
    can be properly converted to an efficient list of structs
    """
    nested_schema = pl.Struct({"my_id": pl.String, "x": pl.Int64, "y": pl.Int64})
    loaded_df = collection_dict_dataframe.with_columns(
        CollectionDictLoader(struct_schema=nested_schema, id_col="my_id").load("col1")
    )
    assert len(loaded_df) == 3
    assert len(loaded_df.columns) == 1
    assert loaded_df.schema == {"col1": pl.List(nested_schema)}
    assert loaded_df.to_dicts() == [
        {
            "col1": [
                {"my_id": "a", "x": 1, "y": 2},
                {"my_id": "b", "x": 3, "y": 4},
            ]
        },
        {
            "col1": [
                {"my_id": "c", "x": 5, "y": 6},
            ]
        },
        {"col1": []},
    ]
