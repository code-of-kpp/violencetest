import struct
import binascii

import six

from cqlengine.columns import *
from cqlengine.columns import DateTime as DateTimeBase
from cqlengine.columns import Bytes as BytesBase

from pytz import utc


class DateTime(DateTimeBase):
    def to_python(self, val):
        if isinstance(val, six.string_types):
            val = struct.unpack('!Q', val)[0] / 1000.0
        dt = super(DateTime, self).to_python(val)
        if dt.tzinfo is None:
            return utc.localize(dt)
        else:
            return dt


class Bytes(BytesBase):
    db_type = 'ascii'

    def to_python(self, value):
        val = super(Bytes, self).to_python(value)
        return binascii.unhexlify(val)
