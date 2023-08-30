from struct import pack, unpack

from meta_msg.exceptions import DeserializationError, ServerError


class MetaMsg:
    _MESSAGE_STRUCT = ">i%ds"

    @classmethod
    def _get_struct(cls, payload: bytes, shift: int = 0):
        payload_length = len(payload) + shift

        return cls._MESSAGE_STRUCT % payload_length

    @classmethod
    def load_message(cls, message: bytes) -> bytes:
        try:
            status_code, body = unpack(cls._get_struct(message, -4), message)
        except Exception:
            raise DeserializationError

        if status_code:
            raise ServerError(message=body, status_code=status_code)
        return body

    @classmethod
    def dump_message(cls, message: bytes) -> bytes:
        return pack(cls._get_struct(message), 0, message)

    @classmethod
    def err_message(cls, message: bytes, *, status_code: int = 0) -> bytes:
        return pack(cls._get_struct(message), status_code, message)
