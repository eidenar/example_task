import pytest

from urllib.parse import urlparse
from task import is_valid_url, process_url

VALID_URL = (
    # input url
    'http://someserver.com/?B02K_VERS=0003&B02K_TIMESTMP=50020181017141433899056&B02K_IDNBR=2512408990&B02K_STAMP'
    '=20010125140015123456&B02K_CUSTNAME=FIRST%20LAST&B02K_KEYVERS=0001&B02K_ALG=03&B02K_CUSTID=9984&B02K_CUSTTYPE'
    '=02&B02K_MAC=EBA959A76B87AE8996849E7C0C08D4AC44B053183BE12C0DAC2AD0C86F9F2542',
    # output url
    'http://someserver.com/?firstname=First&lastname=Last&'
    'hash=4f6536ca2a23592d9037a4707bb44980b9bd2d4250fc1c833812068ccb000712'
)

CUSTOM_PATH_VALID_URL = (
    'http://someserver.com/test/path/?B02K_VERS=0003&B02K_TIMESTMP=50020181017141433899056&B02K_IDNBR=2512408990'
    '&B02K_STAMP'
    '=20010125140015123456&B02K_CUSTNAME=FIRST%20LAST&B02K_KEYVERS=0001&B02K_ALG=03&B02K_CUSTID=9984&B02K_CUSTTYPE'
    '=02&B02K_MAC=EBA959A76B87AE8996849E7C0C08D4AC44B053183BE12C0DAC2AD0C86F9F2542',

    'http://someserver.com/test/path/?firstname=First&lastname=Last&'
    'hash=4f6536ca2a23592d9037a4707bb44980b9bd2d4250fc1c833812068ccb000712'
)

UNICODE_URL = (
    'http://someserver.com/?B02K_VERS=0003&B02K_TIMESTMP=50020181017141433899056&B02K_IDNBR=2512408990&B02K_STAMP' 
    '=20010125140015123456&B02K_CUSTNAME=VÄINÖ%20MÄKI&B02K_KEYVERS=0001&B02K_ALG=03&B02K_CUSTID=9984&B02K_CUSTTYPE'
    '=02&B02K_MAC=D097F084296A5504BF8AEFA839B5BEC4453F5EFAD67FCB543C0EE554824151EF',

    'http://someserver.com/?firstname=V%E4in%F6&lastname=M%E4ki'
    '&hash=2cc314c864510a7fedb070a5d704239596e9778a0fab38b5009fe3eed34c032a'
)

INVALID_URLS = [
    'http://example.com/',

    'http://someserver.com/?B02K_VERS=0003&B02K_TIMESTMP=50020181017141433899056&B02K_IDNBR=2512408990&B02K_STAMP'
    '=20010125140015123456&B02K_CUSTNAME=FIRST%20LAST&B02K_KEYVERS=0001&B02K_ALG=03&B02K_CUSTID=9984&B02K_CUSTTYPE',

    'http://someserver.com/?B02K_VERS=0003&B02K_TIMESTMP=50020181017141433899056&B02K_IDNBR=2512408990&B02K_STAMP'
    '=20010125140015123416&B02K_CUSTNAME=FIRST%20LAST&B02K_KEYVERS=0003&B02K_ALG=03&B02K_CUSTID=9984&B02K_CUSTTYPE'
    '=02&B02K_MAC=EBA959A76B87AE8996849E7C0C08D4AC44B053183BE12C01234AD0C86F9F2542',

    'Hello world',
]


def test_is_valid_url_correct_url():
    url = urlparse(VALID_URL[0])
    assert is_valid_url(url)


@pytest.mark.parametrize('input_url', INVALID_URLS)
def test_is_valid_url_incorrect_urls(input_url):
    url = urlparse(input_url)
    assert not is_valid_url(url)


@pytest.mark.parametrize("input_url, output_url", (
    VALID_URL, UNICODE_URL
))
def test_process_url_valid_url(input_url, output_url):
    assert process_url(input_url) == output_url


@pytest.mark.parametrize("input_url, output_url", (
        ('http://example.com', 'http://example.com/'),
        ('http://someserver.com/?testkey=123', 'http://someserver.com/'),
        ('http://someserver.com/?B02K_VERS=0003&B02K_IDNBR=2512408990&B02K_STAMP', 'http://someserver.com/')
))
def test_process_url_invalid_urls(input_url, output_url):
    assert process_url(input_url) == output_url


def test_process_url_correct_paths():
    assert process_url(CUSTOM_PATH_VALID_URL[0]) == CUSTOM_PATH_VALID_URL[1]
