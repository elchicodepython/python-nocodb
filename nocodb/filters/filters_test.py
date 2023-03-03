import pytest

from .. import filters

from ..nocodb import WhereFilter


@pytest.mark.parametrize('filter_class, expected_operator', [
    (filters.EqFilter, 'eq'),
    (filters.EqualFilter, 'eq'),
    (filters.NotEqualFilter, 'neq'),
    (filters.GreaterOrEqualFilter, 'ge'),
    (filters.GreaterThanFilter, 'gt'),
    (filters.LessThanFilter, 'lt'),
    (filters.LessOrEqualFilter, 'le'),
    (filters.LikeFilter, 'like')
    ])
def test_basic_filters_are_correctly_created(filter_class: WhereFilter, expected_operator: str):
    test_filter = filter_class('column', 'value')
    assert test_filter.get_where() == f'(column,{expected_operator},value)'
