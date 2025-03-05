import unittest
from unittest.mock import patch, MagicMock
from pyintelbras import IntelbrasAPI
from pyintelbras.exceptions import IntelbrasAPIException
from requests.auth import HTTPDigestAuth


class TestIntelbrasAPI(unittest.TestCase):

    def setUp(self):
        self.api = IntelbrasAPI(server='http://localhost',
                                user='user', password='pass')

    @patch('pyintelbras.api.requests.request')
    def test_server(self, mock_request):
        self.api = IntelbrasAPI(server='http://localhost')
        self.assertEqual(self.api.server, 'http://localhost')
        self.api = IntelbrasAPI(server='localhost/test/')
        self.assertEqual(self.api.server, 'http://localhost/test')
        self.api = IntelbrasAPI(server='https://localhost:443/')
        self.assertEqual(self.api.server, 'https://localhost:443')

    @patch('pyintelbras.api.requests.request')
    def test_login(self, mock_request):
        self.api.login('user', 'pass')
        self.assertEqual(self.api.user, 'user')
        self.assertEqual(self.api.password, 'pass')
        self.assertIsInstance(self.api.auth, HTTPDigestAuth)

    @patch('pyintelbras.api.requests.request')
    def test_api_version(self, mock_request):
        mock_response = MagicMock()
        mock_response.text = 'version=2.84'
        mock_request.return_value = mock_response
        version = self.api.api_version
        self.assertEqual(version['version'], 2.84)

    @patch('pyintelbras.api.requests.request')
    def test_channels(self, mock_request):
        mock_response = MagicMock()
        mock_response.text = 'table.ChannelTitle[0].Name=Lab01'
        mock_request.return_value = mock_response
        channels = self.api.channels
        self.assertEqual(channels[0]['Name'], 'Lab01')

    def test_rtsp_url(self):
        self.api = IntelbrasAPI(server='http://localhost')
        url = self.api.rtsp_url(channel=1, subtype=0)
        self.assertEqual(
            url, 'rtsp://localhost:554/cam/realmonitor?channel=1&subtype=0')
        url = self.api.rtsp_url(port=445, channel=2, subtype=1)
        self.assertEqual(
            url, 'rtsp://localhost:445/cam/realmonitor?channel=2&subtype=1')
        url = self.api.rtsp_url(protocol='rtsps', channel=3)
        self.assertEqual(
            url, 'rtsps://localhost:554/cam/realmonitor?channel=3&subtype=0')
        self.api.login('user', 'pass')
        url = self.api.rtsp_url(channel=1, subtype=0)
        self.assertEqual(
            url, 'rtsp://user:pass@localhost:554/cam/realmonitor?channel=1&subtype=0')

    @patch('pyintelbras.api.requests.request')
    def test_find_media_files(self, mock_request):
        mock_response = MagicMock()
        mock_response.text = 'result=1\nfound=1\nitems[0].Channel=1'
        mock_request.return_value = mock_response
        params = {'condition.Channel': 1, 'condition.StartTime': '2024-8-27 12:00:00',
                  'condition.EndTime': '2024-8-29 12:00:00'}
        result = self.api.find_media_files(params)
        self.assertEqual(result['found'], 1)

    @patch('pyintelbras.api.requests.request')
    def test_do_request(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_request.return_value = mock_response
        response = self.api.do_request('GET', 'path', {})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
