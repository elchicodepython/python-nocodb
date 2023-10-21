from nocodb import filters


def test_or_with_two_filters():
    filter1 = filters.EqFilter("column1", "value1")
    filter2 = filters.EqFilter("column2", "value2")
    or_filter = filters.Or(filter1, filter2)
    assert or_filter.get_where() == "((column1,eq,value1)~or(column2,eq,value2))"


def test_and_with_two_filters():
    filter1 = filters.And(filters.EqFilter("column1", "value1"))
    filter2 = filters.And(filters.EqFilter("column2", "value2"))
    and_filter = filters.And(filter1, filter2)
    assert and_filter.get_where() == "(((column1,eq,value1))~and((column2,eq,value2)))"


def test_not_filter():
    filter = filters.EqFilter("column", "value")
    not_filter = filters.Not(filter)
    assert not_filter.get_where() == "~not(column,eq,value)"
