import unittest
from util import aprox_time
from datetime import datetime, timedelta


class Util(unittest.TestCase):

    def test_aprox_time(self):
        now = datetime.now()
        aprox_1 = aprox_time('just now', now)
        self.assertEqual(now, aprox_1)

        now_2 = now - timedelta(minutes=2)
        aprox_2 = aprox_time('2 minutes ago', now)
        self.assertEqual(aprox_2, now_2)

        now_3 = now - timedelta(hours=4)
        aprox_3 = aprox_time('4 hours ago', now)
        self.assertEqual(aprox_3, now_3)

        aprox_4 = aprox_time('', now)
        self.assertEqual(aprox_4, now)

        aprox_5 = aprox_time(None, now)
        self.assertEqual(aprox_5, now)


if __name__ == '__main__':
    unittest.main()
