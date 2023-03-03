from .factory import basic_filter_class_factory, raw_template_filter_class_factory


def test_basic_filter_class_factory():
    FilterClass = basic_filter_class_factory('eq')
    assert FilterClass('column', 'value').get_where() == '(column,eq,value)'


def test_raw_template_filter_class_factory():
    FilterClassWithoutParams = raw_template_filter_class_factory('()')
    FilterClassWithParams = raw_template_filter_class_factory('({},{},{})')
    FilterClassWithKwargs = raw_template_filter_class_factory('({},{op},{})')
    assert FilterClassWithoutParams().get_where() == '()'
    assert FilterClassWithParams('1', '2','3').get_where() == '(1,2,3)'
    assert FilterClassWithKwargs('1', '2', op='eq').get_where() == '(1,eq,2)'
