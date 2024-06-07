import os

from openpyxl import load_workbook

from linkml.generators.excelgen import ExcelGenerator


def test_excel_generation(input_path, tmp_path):
    organization_schema = str(input_path("organization.yaml"))
    xlsx_filename = str(tmp_path / "schema.xlsx")

    # call ExcelGenerator generator class
    ExcelGenerator(organization_schema, output=xlsx_filename).serialize()

    # load Excel workbook object from temporary file path
    wb_obj = load_workbook(xlsx_filename)

    # check the names of the created worksheets that are part of the workbook
    assert wb_obj.sheetnames == ["organization", "employee", "manager"]

    # test case to check the column names in Employee worksheet
    employee_cols_list = []
    max_col = wb_obj["employee"].max_column

    for i in range(1, max_col + 1):
        cell_obj = wb_obj["employee"].cell(row=1, column=i)
        employee_cols_list.append(cell_obj.value)

    assert sorted(employee_cols_list) == [
        "age in years",
        "aliases",
        "first name",
        "id",
        "last name",
    ]

    # test case to check the column names in Manager worksheet
    manager_cols_list = []
    max_col = wb_obj["manager"].max_column

    for i in range(1, max_col + 1):
        cell_obj = wb_obj["manager"].cell(row=1, column=i)
        manager_cols_list.append(cell_obj.value)

    assert sorted(manager_cols_list) == [
        "age in years",
        "aliases",
        "first name",
        "has employees",
        "id",
        "last name",
    ]

    # test case to check the column names in Organization worksheet
    organization_cols_list = []
    max_col = wb_obj["organization"].max_column

    for i in range(1, max_col + 1):
        cell_obj = wb_obj["organization"].cell(row=1, column=i)
        organization_cols_list.append(cell_obj.value)

    assert sorted(organization_cols_list) == ["has boss", "id", "name"]


def test_multiple_excel_workbooks_generation(input_path, tmp_path):
    organization_schema = str(input_path("organization.yaml"))
    excel_files_folder = str(tmp_path)

    ExcelGenerator(organization_schema, split_workbook_by_class=True, output=excel_files_folder).serialize()

    _, _, files = next(os.walk(excel_files_folder))
    file_count = len(files)

    assert file_count == 3

    expected_files = ["employee.xlsx", "manager.xlsx", "organization.xlsx"]
    assert sorted(files) == expected_files

    def verify_workbook_columns(excel_file_path, worksheet_name):
        wb_obj = load_workbook(excel_file_path)
        worksheet = wb_obj[worksheet_name]

        column_names = []
        max_col = worksheet.max_column

        for i in range(1, max_col + 1):
            cell_obj = worksheet.cell(row=1, column=i)
            column_names.append(cell_obj.value)

        return column_names

    for file in files:
        file_path = os.path.join(excel_files_folder, file)
        wb_obj = load_workbook(file_path)
        worksheet_count = len(wb_obj.sheetnames)
        assert worksheet_count == 1

        if file == "employee.xlsx":
            column_names = verify_workbook_columns(file_path, "employee")
            assert sorted(column_names) == [
                "age in years",
                "aliases",
                "first name",
                "id",
                "last name",
            ]

        if file == "manager.xlsx":
            column_names = verify_workbook_columns(file_path, "manager")
            assert sorted(column_names) == [
                "age in years",
                "aliases",
                "first name",
                "has employees",
                "id",
                "last name",
            ]

        if file == "organization.xlsx":
            column_names = verify_workbook_columns(file_path, "organization")
            assert sorted(column_names) == ["has boss", "id", "name"]


def test_file_generation_for_mixins(input_path, tmp_path):
    kitchen_sink_schema = str(input_path("kitchen_sink.yaml"))
    excel_files_folder = str(tmp_path)

    # Call ExcelGenerator generator class without including mixins
    ExcelGenerator(kitchen_sink_schema, split_workbook_by_class=True, output=excel_files_folder).serialize()

    _, _, files = next(os.walk(excel_files_folder))
    file_count = len(files)

    # Check that HasAliases.xlsx and WithLocation.xlsx have not been generated
    assert file_count == 31

    assert "HasAliases.xlsx" not in files
    assert "WithLocation.xlsx" not in files

    # Call ExcelGenerator generator class with mixins
    ExcelGenerator(
        kitchen_sink_schema, split_workbook_by_class=True, output=excel_files_folder, include_mixins=True
    ).serialize()

    _, _, files = next(os.walk(excel_files_folder))
    file_count = len(files)

    # Check if HasAliases.xlsx and WithLocation.xlsx have been generated
    assert file_count == 33

    assert "HasAliases.xlsx" in files
    assert "WithLocation.xlsx" in files
