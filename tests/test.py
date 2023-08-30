import json
from unittest import TestCase

from meta_msg import MetaMsg, ServerError, GrpcStatus


class SimpleTestCase(TestCase):
    @staticmethod
    def _get_mock_data():
        return {
            "name": "Alex",
            "message": "Hello"
        }

    def test_smoke(self):
        raw_message = json.dumps(self._get_mock_data()).encode()

        # Serialize ->
        payload = MetaMsg.dump_message(raw_message)

        # <- Deserialize
        test_data = MetaMsg.load_message(payload)

        assert json.loads(test_data) == self._get_mock_data()

    def test_raise_error(self):
        err_message = b"Oh no!! ERROR!!"
        payload = MetaMsg.err_message(err_message, status_code=GrpcStatus.INTERNAL)

        # This message should raise an error
        try:
            _ = MetaMsg.load_message(payload)
        except ServerError as err:
            assert err.status_code, GrpcStatus.INTERNAL
            assert err.message, err_message
        else:
            raise Exception("Failed")
