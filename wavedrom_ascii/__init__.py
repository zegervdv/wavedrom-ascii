# -*- coding: utf-8 -*-
from collections import deque
import json5

class WavedromASCII:
    symbol_top = {
        'rise': "┌────",
        'fall': "┐    ",
        'low' : "     ",
        'high': "─────",
    }
    symbol_bot = {
        'rise': "┘    ",
        'fall': "└────",
        'low' : "─────",
        'high': "     ",
    }

    signals = {
        '0': 'low',
        '1': 'high',
    }
    def __init__(self):
        self._waves = {}

    @classmethod
    def from_dict(cls, data):
        wave = cls()
        for item in data['signal']:
            wave.add_wave(item['name'], item['wave'])
        return wave

    @classmethod
    def from_json(cls, file):
        with open(file, 'r') as f:
            data = json5.load(f)
            wave = cls.from_dict(data)
            return wave

    def add_wave(self, name, wave):
        self._waves[name] = self._parse_wavedrom_wave(wave)

    def _parse_wavedrom_wave(self, wave: str):
        if wave[0] == 'p':
            return [('rise', 'fall') for _ in range(len(wave))]
        else:
            result = []
            waves = deque(wave)
            prev = None
            last_cycle = None
            while waves:
                cycle = waves.popleft()

                if cycle == '.':
                    posedge = last_cycle[1]
                    negedge = last_cycle[1]
                else:
                    if (last_cycle is None or last_cycle[1] == 'low') and cycle == '1':
                        posedge = 'rise'
                    elif last_cycle is not None and last_cycle[1] == 'high' and cycle == '0':
                        posedge = 'fall'
                    else:
                        posedge = self.signals.get(cycle, None)

                    negedge = self.signals.get(cycle, None)

                result.append((posedge, negedge))
                prev = cycle
                last_cycle = (posedge, negedge)
            return result

    def __str__(self):
        max_key = max(len(key) for key in self._waves.keys())
        output = []
        for name, waveform in self._waves.items():
            topline = f"  {' ':{max_key}s}  "
            botline = f"  {name:{max_key}s}  "

            for posedge, negedge in waveform:
                topline += self.symbol_top.get(posedge, "     ")
                botline += self.symbol_bot.get(posedge, "     ")

                topline += self.symbol_top.get(negedge, "     ")
                botline += self.symbol_bot.get(negedge, "     ")

            output.append(topline)
            output.append(botline)
        return '\n'.join(output)
