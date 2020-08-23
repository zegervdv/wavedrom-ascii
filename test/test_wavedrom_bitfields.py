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

    def test_bitfield(self, data):
        field = BitfieldASCII.from_dict(data)
        exp = """\
31                                    121110     7 6           0
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│                                       │b│  foo  │0 0 0 0 0 1 1│
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
