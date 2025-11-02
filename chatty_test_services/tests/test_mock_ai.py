from chatty_test_services.mocks import mock_ai


class TestMockAi:
    def test_mock_ai(self):
        mock = mock_ai()
        assert mock is not None
