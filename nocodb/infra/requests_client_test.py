from unittest import mock

import pytest

from .requests_client import NocoDBRequestsClient, requests as requests_lib
from ..exceptions import NocoDBAPIError


@mock.patch.object(requests_lib, "Session")
def test_NocoDBAPIError_raised_on_bad_response(mock_requests_session):
    mock_session = mock.Mock()
    expected_exception = NocoDBAPIError("Error 400 in the request", 400)
    mock_session.request.side_effect = expected_exception
    mock_requests_session.return_value = mock_session
    client = NocoDBRequestsClient(mock.Mock(), "")
    with pytest.raises(NocoDBAPIError) as exc_info:
        client._request("GET", "/")

    assert str(exc_info.value) == str(expected_exception)
    assert exc_info.value.status_code == expected_exception.status_code
