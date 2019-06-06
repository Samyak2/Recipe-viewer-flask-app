import unittest

import sw as ip


class TestIngredientParserSwedish(unittest.TestCase):
    def setUp(self):
        self.teststrings = [
            '1 mg saffran',
            '1mg saffran',
            '1                               mg saffran',
            '1 \n\r \n\r       mg saffran',
            '1 mg                            saffran',
            '1             mg            saffran',
            '1      \r\n       mg  \r\n          saffran',
        ]

    def test_normalize_whitespace(self):
        for s in self.teststrings:
            self.assertEqual('1 mg saffran', ip.normalize(s))

        res = ip.normalize('11/12   mg   saffran')
        self.assertEqual('11/12 mg saffran', res)

    def test_integer_and_metric_weight_with_whitespace_inbetween(self):
        for s in self.teststrings:
            res = ip.parse(s)
            self.assertEqual('1 mg', res['measure'])
            self.assertEqual('saffran', res['name'])

        res = ip.parse('1 g saffran')
        self.assertEqual('1 g', res['measure'])
        self.assertEqual('saffran', res['name'])

        res = ip.parse('200 gram something')
        self.assertEqual('200 gram', res['measure'])
        self.assertEqual('something', res['name'])

    def test_fractions_and_metric_weight_with_whitespace_inbetween(self):

        res = ip.parse('1/2   mg   saffran')
        self.assertEqual('1/2 mg', res['measure'])
        self.assertEqual('saffran', res['name'])

        res = ip.parse('1/2mg   saffran')
        self.assertEqual('1/2 mg', res['measure'])
        self.assertEqual('saffran', res['name'])

        res = ip.parse('11/12   mg   saffran')
        self.assertEqual('11/12 mg', res['measure'])
        self.assertEqual('saffran', res['name'])

        res = ip.parse('11/12mg   saffran')
        self.assertEqual('11/12 mg', res['measure'])
        self.assertEqual('saffran', res['name'])

        res = ip.parse('7 1/2 dl mjol')
        self.assertEqual('7 1/2 dl', res['measure'])
        self.assertEqual('mjol', res['name'])

    def test_decimals_and_metric_weight_with_whitespace_inbetween(self):
        res = ip.parse('1.5   mg   saffran')
        self.assertEqual('1.5 mg', res['measure'])
        self.assertEqual('saffran', res['name'])

        res = ip.parse('1,5mg   saffran')
        self.assertEqual('1,5 mg', res['measure'])
        self.assertEqual('saffran', res['name'])

    def test_no_measurement(self):
        res = ip.parse('salt och peppar')
        self.assertEqual('', res['measure'])
        self.assertEqual('salt och peppar', res['name'])

    def test_qty_but_no_measurement(self):
        res = ip.parse('3 red   peppar')
        self.assertEqual('3', res['measure'])
        self.assertEqual('red peppar', res['name'])

    def test_approximation_measurements(self):
        res = ip.parse('300 ca g farsk   lammkorv')
        self.assertEqual('300 ca g', res['measure'])
        self.assertEqual('farsk lammkorv', res['name'])

    def test_other_containers(self):
        res = ip.parse('33 cl porter ol')
        self.assertEqual('33 cl', res['measure'])
        self.assertEqual('porter ol', res['name'])

        res = ip.parse('4 port fisk')
        self.assertEqual('4 port', res['measure'])
        self.assertEqual('fisk', res['name'])

        # test uppercase
        res = ip.parse('4 Port fisk')
        self.assertEqual('4 Port', res['measure'])
        self.assertEqual('fisk', res['name'])

        res = ip.parse('1 KRUKA koriander')
        self.assertEqual('1 KRUKA', res['measure'])
        self.assertEqual('koriander', res['name'])


if __name__ == '__main__':
    unittest.main()
