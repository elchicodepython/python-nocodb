import pytest

from .. import filters

from ..nocodb import WhereFilter


@pytest.mark.parametrize(
    "filter_class, expected_operator",
    [
        (filters.EqFilter, "eq"),
        (filters.EqualFilter, "eq"),
        (filters.NotEqualFilter, "neq"),
        (filters.GreaterOrEqualFilter, "ge"),
        (filters.GreaterThanFilter, "gt"),
        (filters.LessThanFilter, "lt"),
        (filters.LessOrEqualFilter, "le"),
        (filters.LikeFilter, "like"),
    ],
)
def test_basic_filters_are_correctly_created(
    filter_class: WhereFilter, expected_operator: str
):
    test_filter = filter_class("column", "value")
    assert test_filter.get_where() == f"(column,{expected_operator},value)"


def test_or_filter():
    nick_filter = filters.EqFilter("nickname", "elchicodepython")
    country_filter = filters.EqFilter("country", "es")
    nick_or_country_filter = filters.Or(nick_filter, country_filter)
    assert (
        nick_or_country_filter.get_where()
        == "((nickname,eq,elchicodepython)~or(country,eq,es))"
    )


def test_and_filter():
    nick_filter = filters.EqFilter("nickname", "elchicodepython")
    country_filter = filters.EqFilter("country", "es")
    nick_or_country_filter = filters.And(nick_filter, country_filter)
    assert (
        nick_or_country_filter.get_where()
        == "((nickname,eq,elchicodepython)~and(country,eq,es))"
    )


def test_combined_filter():
    nick_filter = filters.EqFilter("nickname", "elchicodepython")
    country_filter = filters.EqFilter("country", "es")
    girlfriend_code = filters.EqFilter("gfcode", "404")
    current_mood_code = filters.EqFilter("moodcode", "418")
    or_filter = filters.Or(nick_filter, country_filter)
    and_filter = filters.And(girlfriend_code, current_mood_code)
    or_combined_filter = filters.Or(or_filter, and_filter)
    and_combined_filter = filters.And(or_filter, and_filter)

    assert (
        or_combined_filter.get_where()
        == "(((nickname,eq,elchicodepython)~or(country,eq,es))~or((gfcode,eq,404)~and(moodcode,eq,418)))"
    )
    assert (
        and_combined_filter.get_where()
        == "(((nickname,eq,elchicodepython)~or(country,eq,es))~and((gfcode,eq,404)~and(moodcode,eq,418)))"
    )


def test_not_filter():
    me = filters.EqFilter("nickname", "elchicodepython")
    not_me = filters.Not(me)
    assert not_me.get_where() == "~not(nickname,eq,elchicodepython)"
