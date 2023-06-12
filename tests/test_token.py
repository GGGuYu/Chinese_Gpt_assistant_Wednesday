from nls.token import getToken

from test_utils import TEST_ACCESS_AKID, TEST_ACCESS_AKKEY


info = getToken(TEST_ACCESS_AKID, TEST_ACCESS_AKKEY)
print(info)
