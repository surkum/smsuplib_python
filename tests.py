import unittest

import smsuplib


class TestSMSUpLib(unittest.TestCase):

    def test_hash_hmac(self):
        hash_correcto = '692bb3330fe99ee7a9184a1ca1e271fc6571d57a'.encode('utf-8')
        self.assertEqual(
            smsuplib.hash_hmac_sha1(clave='clave', texto='texto'), hash_correcto
        )
        self.assertNotEqual(
            smsuplib.hash_hmac_sha1(clave='clave2', texto='texto'), hash_correcto
        )

    def test_get_random_reference_return_30_characters_string(self):
        self.assertEqual(len(smsuplib.get_random_reference()), 30)

if __name__ == '__main__':
    unittest.main()
