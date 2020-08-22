import pytest
from wavedrom_ascii import WavedromASCII


class TestWaves:
    @pytest.fixture
    def data(self):
        return {
            "signal": [
                {
                    "name": 'clk',
                    "wave": 'p......',
                },
                {
                    "name": "valid",
                    "wave": '01.0...',
                }
            ]
        }

    def test_signals(self, data):
        waves = WavedromASCII.from_dict(data)
        exp = """\
         ┌────┐    ┌────┐    ┌────┐    ┌────┐    ┌────┐    ┌────┐    ┌────┐    
  clk    ┘    └────┘    └────┘    └────┘    └────┘    └────┘    └────┘    └────
                   ┌───────────────────┐                                       
  valid  ──────────┘                   └───────────────────────────────────────\
"""
        res = str(waves)
        for line_res, line_exp in zip(res.splitlines(), exp.splitlines()):
            for i, (char_res, char_exp) in enumerate(zip(line_res, line_exp)):
                assert char_res == char_exp
        assert exp == str(waves)

    def test_json_file(self):
        waves = WavedromASCII.from_json('./test/waves.json5')
        exp = """\
         ┌────┐    ┌────┐    ┌────┐    ┌────┐    ┌────┐    ┌────┐    ┌────┐    
  clk    ┘    └────┘    └────┘    └────┘    └────┘    └────┘    └────┘    └────
                   ┌───────────────────┐                                       
  valid  ──────────┘                   └───────────────────────────────────────\
"""
        assert exp == str(waves)
