from Tables.TableModel import TableModel


class CategoryTable(TableModel):
    tableName = "category_urls"


if __name__ == "__main__":
    categoryTable = CategoryTable()
    print(categoryTable.getAll())
