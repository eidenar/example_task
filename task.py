from hashlib import sha256
from logging import getLogger
from urllib.parse import urlparse, parse_qs, urlencode, ParseResult

SIGNATURE_PARAM = 'B02K_MAC'
SIGNATURE_ARGUMENTS = [
    'B02K_VERS', 'B02K_TIMESTMP', 'B02K_IDNBR', 'B02K_STAMP', 'B02K_CUSTNAME',
    'B02K_KEYVERS', 'B02K_ALG', 'B02K_CUSTID', 'B02K_CUSTTYPE',
]

INPUT_SECRET = 'inputsecret'
OUTPUT_SECRET = 'outputsecret'
ERROR_URL = '/'

logger = getLogger(__name__)


def is_valid_url(url: ParseResult, params: dict=None, secret: str=INPUT_SECRET) -> bool:
    """Simple validation of URL, params and signature."""
    logger.debug('Start URL validation')
    params = params if params else parse_qs(url.query)

    try:
        assert all((url.scheme, url.netloc, params)), 'Incorrect URL'
        assert len(params.keys()) == len(SIGNATURE_ARGUMENTS) + 1, 'Incorrect amount of request params'
        assert all((key in SIGNATURE_ARGUMENTS + [SIGNATURE_PARAM] for key in params.keys())), 'Wrong params passed'
    except AssertionError as ex:
        logger.info('URL validation failed: %s', ex)
        return False

    signature_str = '&'.join([params[val][0] for val in SIGNATURE_ARGUMENTS] + [secret]) + '&'
    signature = sha256(signature_str.encode()).hexdigest().upper()

    if params[SIGNATURE_PARAM][0] != signature:
        logger.info("Wrong signature")
        return False

    logger.debug("URL validation successfull")
    return True


def process_url(url: str, secret: str=OUTPUT_SECRET) -> str:
    """Calculate output signature and create new signed URL"""
    logger.debug('Process URL')
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)

    if not is_valid_url(parsed_url, params=params):
        return '{}://{}'.format(parsed_url.scheme, parsed_url.netloc + ERROR_URL)

    first_name, last_name = map(lambda x: x.capitalize(), params['B02K_CUSTNAME'][0].split())

    output_hash_str = 'firstname={}&lastname={}#{}'.format(
        first_name,
        last_name,
        secret
    )
    output_hash = sha256(output_hash_str.encode()).hexdigest()

    output_params = urlencode(
        {
            'firstname': first_name.encode('windows-1252'),
            'lastname': last_name.encode('windows-1252'),
            'hash': output_hash
        }
    )
    output_url = "{}://{}?{}".format(parsed_url.scheme, parsed_url.netloc + parsed_url.path, output_params)
    return output_url
