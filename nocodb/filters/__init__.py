from .factory import basic_filter_class_factory
from .logical import And, Not, Or

EqFilter = basic_filter_class_factory("eq")
EqualFilter = EqFilter
NotEqualFilter = basic_filter_class_factory("neq")
GreaterThanFilter = basic_filter_class_factory("gt")
GreaterOrEqualFilter = basic_filter_class_factory("ge")
LessThanFilter = basic_filter_class_factory("lt")
LessOrEqualFilter = basic_filter_class_factory("le")
LikeFilter = basic_filter_class_factory("like")

__all__ = [
    "And",
    "Not",
    "Or",
    "EqFilter",
    "EqualFilter",
    "NotEqualFilter",
    "GreaterThanFilter",
    "GreaterOrEqualFilter",
    "LessThanFilter",
    "LessOrEqualFilter",
    "LikeFilter",
]
