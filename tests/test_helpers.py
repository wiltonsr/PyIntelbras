import unittest
from pyintelbras.helpers import parse_response
from pyintelbras.exceptions import IntelbrasAPIException


class TestHelpers(unittest.TestCase):

    def test_parse_response(self):
        response = """
                   caps.MaxPreRecordTime=30
                   caps.PacketLengthRange[0]=1
                   caps.PacketLengthRange[1]=60
                   caps.PacketSizeRange[0]=131072
                   caps.PacketSizeRange[1]=2097152
                   caps.SupportExtraRecordMode=true
                   caps.SupportHoliday=true
                   caps.SupportPacketType[0]=Time
                   caps.SupportPacketType[1]=Size
                   caps.SupportResumeTransmit=false
                   """
        parsed = parse_response(response)
        self.assertEqual(parsed['caps']['MaxPreRecordTime'], 30)
        self.assertEqual(parsed['caps']['PacketLengthRange'][0], 1)
        self.assertEqual(parsed['caps']['PacketLengthRange'][1], 60)

    def test_parse_response_invalid(self):
        response = None
        with self.assertRaises(IntelbrasAPIException):
            parse_response(response)


if __name__ == '__main__':
    unittest.main()
