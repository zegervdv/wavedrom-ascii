import pytest
from wavedrom_ascii import BitfieldASCII

class TestBitfield:
    @pytest.fixture
    def data(self):
        return {
            'reg': [
                {
                    'bits': 7,
                    'name': 3,
                },
                {
                    'bits': 4,
                    'name': 'foo',
                },
                {
                    'bits': 1,
                    'name': 'bar',
                }
            ]
        }

    @pytest.fixture
    def large_data(self):
        return {
            'reg': [
                {
                    'bits': 7,
                    'name': 'a',
                },
                {
                    'bits': 25,
                    'name': 'foobar',
                },
                {
                    'bits': 18,
                    'name': 'overflow',
                }
            ]
        }

    def test_bitfield(self, data):
        field = BitfieldASCII.from_dict(data)
        exp = """\
31                                    121110     7 6           0
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│                                       │b│  foo  │0 0 0 0 0 1 1│
└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘\
"""
        assert exp == str(field)

    def test_large_field(self, large_data):
        field = BitfieldASCII.from_dict(large_data)
        exp = """\
63                        5049                                32
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│                           │             overflow              │
└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘
31                                               7 6           0
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│                     foobar                      │      a      │
└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘\
"""
        assert exp == str(field)

    def test_large_field_wrap(self, large_data):
        large_data['reg'][1]['bits'] = 30
        field = BitfieldASCII.from_dict(large_data)
        exp = """\
63              5554                                3736      32
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│                 │             overflow              │ foobar  │
└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘
31                                               7 6           0
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│                     foobar                      │      a      │
└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘\
"""
        assert exp == str(field)


    def test_wavedrom_bitfield(self):
        field = BitfieldASCII.from_json('./test/fields.json5')
        exp = """\
31  2928  262524      2019      1514  1211       7 6           0
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│ nf  │ mop │v│  lumop  │   rs1   │width│   vd    │0 0 0 0 1 1 1│
└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘\
"""
        assert exp == str(field)

    def test_large_field_64(self, large_data):
        BitfieldASCII.fieldsize = 64
        field = BitfieldASCII.from_dict(large_data)
        exp = """\
63                        5049                                3231                                               7 6           0
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│                           │             overflow              │                     foobar                      │      a      │
└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘\
"""
        assert exp == str(field)

    def test_triple_digit_sizes(self, large_data):
        large_data['reg'].append({'bits': 43, 'name': 'expansion'})
        field = BitfieldASCII.from_dict(large_data)
        exp = """\
                                                                                                                                
 1                                                                                                                              
 2                                                                   9 9                                                       6
 7                                                                   3 2                                                       4
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│                                                                     │                        expansion                        │
└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘
                                                                                                                                
                                                                                                                                
 6                         5 4                                 3 3                                                              
 3                         0 9                                 2 1                                               7 6           0
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│         expansion         │             overflow              │                     foobar                      │      a      │
└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘\
"""
        assert exp == str(field)

