import unittest

target = __import__("main")
derive_salt = target.derive_salt
derive_key = target.derive_key
generate_key = target.generate_key
encrypt = target.encrypt
decrypt = target.decrypt

SALT = "5CE7B6E7E4B4B1"
SALTB = b'5CE7B6E7E4B4B1'
PASSWORD = "B1C7FC5BE98F16"
KEYB = b'\xcc\xf3\x0c,IZ\xd5\xb9\xec\x81\xaao\xb7\x93\x0e7\x8b-\xacb\xab>\x7fs\xd5!\x85l\xa5B\xd2\x90'
KEY_GENERATED = b'zPMMLEla1bnsgapvt5MON4strGKrPn9z1SGFbKVC0pA='
RANDOM_SEED_PHRASE = "cinnamon wine pepper valid copy village spirit media slim myth kit scrub fox hawk smart opinion input doll sister crack multiply volume maze pride"


class Monolithic(unittest.TestCase):
    def test_salt(self):
        print('Testing salf derivation...')
        self.assertEqual(derive_salt(SALT), SALTB)

    def test_key(self):
        print('Testing key derivation...')
        derived_key = derive_key(PASSWORD, SALTB)
        self.assertEqual(derived_key, KEYB)

    def test_key_creation(self):
        print('Testing key creation...')
        generated_key = generate_key(PASSWORD, SALT)
        self.assertEqual(generated_key, KEY_GENERATED)

    def test_encrypt_file(self):
        print('Testing encrypt file...')
        with open("test_tmp/seed_phrase.txt", "wb") as file:
            file.write(RANDOM_SEED_PHRASE.encode())
        encrypt("test_tmp/seed_phrase.txt", generate_key(PASSWORD, SALT))

    def test_decrypt_file(self):
        print('Testing decrypt file...')
        decrypt("test_tmp/seed_phrase.txt", generate_key(PASSWORD, SALT))

    def test_decrypt_file_unicity(self):
        print('Testing decrypt file unicity...')
        with open("test_tmp/seed_phrase.txt", "rb") as file:
            file_data = file.read()
        with open("test_tmp/golden_seed_phrase.txt", "rb") as file:
            file_data_real = file.read()
        self.assertEqual(file_data, file_data_real)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(Monolithic('test_salt'))
    suite.addTest(Monolithic('test_key'))
    suite.addTest(Monolithic('test_key_creation'))
    suite.addTest(Monolithic('test_encrypt_file'))
    suite.addTest(Monolithic('test_decrypt_file'))
    suite.addTest(Monolithic('test_decrypt_file_unicity'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())
