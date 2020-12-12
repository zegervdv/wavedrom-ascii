# -*- coding: utf-8 -*-
from collections import deque, defaultdict
from math import ceil
import json5

class Waveform:
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
        self._cycles = []

    def parse_waveform(self, wave, data=None):
        if wave[0] == 'p':
            self._cycles = [('rise', 'fall') for _ in range(len(wave))]
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
            self._cycles = result

    @property
    def topline(self):
        topline = ''
        for posedge, negedge in self._cycles:
            topline += self.symbol_top.get(posedge, "     ")
            topline += self.symbol_top.get(negedge, "     ")
        return topline

    @property
    def midline(self):
        return "     " * (len(self._cycles) * 2)

    @property
    def botline(self):
        botline = ''
        for posedge, negedge in self._cycles:
            botline += self.symbol_bot.get(posedge, "     ")
            botline += self.symbol_bot.get(negedge, "     ")
        return botline



class VectorWaveform(Waveform):
    change_top = '╥'
    change_mid = '║'
    change_bot = '╨'

    def parse_waveform(self, wave, data):
        prev = None
        last_cycle = None
        waves = deque(wave)
        data = data.split(' ')
        while waves:
            cycle = waves.popleft()

            value = ''
            if cycle == '.':
                posedge = last_cycle[1]
                negedge = posedge
            else:
                if cycle == 'x':
                    if last_cycle and last_cycle[0] != 'x':
                        posedge = 'changex'
                    else:
                        posedge = 'x'
                    negedge = 'x'
                else:
                    if last_cycle is None and cycle == '.':
                        posedge = 'hold'
                        negedge = 'hold'
                        value = ''
                    elif last_cycle is None:
                        posedge = 'change'
                        negedge = 'hold'
                        value = data.pop(0)
                    elif cycle in '23456789':
                        posedge = 'change'
                        negedge = 'hold'
                        value = data.pop(0)
                    else:
                        posedge = 'hold'
                        negedge = 'hold'

            prev = cycle
            last_cycle = (posedge, negedge, value)
            self._cycles.append((posedge, negedge, value))

    @property
    def topline(self):
        output = ''
        for posedge, _, _ in self._cycles:
            if posedge in {'change', 'changex'}:
                output += f"{self.change_top}────"
            else:
                output += "─────"

            output += "─────"
        return output

    @property
    def botline(self):
        output = ''
        for posedge, _, _ in self._cycles:
            if posedge in {'change', 'changex'}:
                output += f"{self.change_bot}────"
            else:
                output += "─────"

            output += "─────"
        return output

    @property
    def midline(self):
        output = ''
        for posedge, negedge, value in self._cycles:
            if posedge == 'x':
                output += "XXXXX"
            elif posedge == 'change':
                output += f"{self.change_mid} {value[0:3]:3s}"
            elif posedge == 'changex':
                output += f"{self.change_mid}XXXX"
            else:
                output += "     "

            if negedge == 'x':
                output += "XXXXX"
            elif posedge == 'change':
                output += f"{value[3:8]:5s}"
            else:
                output += "     "

        return output

class WavedromASCII:
    vector_symbols = {
        'x',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
    }
    def __init__(self):
        self._waves = {}

    @classmethod
    def from_dict(cls, data):
        wave = cls()
        for item in data['signal']:
            wave.add_wave(item['name'], item['wave'], item.get('data', None))
        return wave

    @classmethod
    def from_json(cls, file):
        with open(file, 'r') as f:
            data = json5.load(f)
            wave = cls.from_dict(data)
            return wave

    def add_wave(self, name, wave, data=None):
        self._waves[name] = self._parse_wavedrom_wave(wave, data)

    def _parse_wavedrom_wave(self, wave: str, data):
        if any(w in self.vector_symbols for w in wave):
            cls = VectorWaveform
        else:
            cls = Waveform
        form = cls()
        form.parse_waveform(wave, data)
        return form

    def __str__(self):
        max_key = max(len(key) for key in self._waves.keys())
        output = []
        for name, waveform in self._waves.items():
            topline = f"  {' ':{max_key}s}  "
            topline += waveform.topline

            if isinstance(waveform, VectorWaveform):
                midline = f"  {name:{max_key}s}  "
                botline = f"  {' ':{max_key}s}  "
            else:
                midline = ''
                botline = f"  {name:{max_key}s}  "

            midline += waveform.midline
            botline += waveform.botline

            output.append(topline)
            if isinstance(waveform, VectorWaveform):
                output.append(midline)
            output.append(botline)
        return '\n'.join(output)


class BitfieldASCII:
    fieldsize = 32
    def __init__(self):
        self._fields = []

    @classmethod
    def from_dict(cls, data):
        bitfield = cls()
        for item in data['reg']:
            bitfield.add_field(item['name'], item['bits'])
        return bitfield

    @classmethod
    def from_json(cls, file):
        with open(file, 'r') as f:
            data = json5.load(f)
            return cls.from_dict(data)

    def add_field(self, name, size):
        self._fields.append((size, name))

    def bitsize(self):
        return sum(x[0] for x in self._fields)

    def format_name(self, name):
        return name

    def __str__(self):
        lines = int(ceil(self.bitsize()/self.fieldsize))
        msb = lines * self.fieldsize

        output = []
        if self.bitsize() < msb:
            pad = msb - self.bitsize()
            fields = [(pad, '')] + list(reversed(self._fields))
        else:
            pad = 0
            fields = reversed(self._fields)

        field_ranges = []
        offset = 0
        for size, data in fields:
            field_ranges.append((
                data,
                msb - offset - 1,
                msb - offset - size,
            ))
            offset += size

        digits = 1
        if msb > 100:
            digits = 4

        field_lines = defaultdict(list)
        index = 0
        for field in reversed(field_ranges):
            if field[1] < (index+1) * self.fieldsize:
                field_lines[index].append(field)
            elif field[2] < (index+1) * self.fieldsize:
                field_lines[index].append((field[0],  (index+1) * self.fieldsize - 1, field[2]))
                index += 1
                field_lines[index].append((field[0], field[1], index * self.fieldsize))
            else:
                index += 1
                field_lines[index].append(field)

        for i in range(lines):
            line_out = []
            bit_numbers = [[] for _ in range(digits)]
            topline = []
            midline = []
            botline = []
            first = True
            for data, high, low in reversed(field_lines[i]):
                size = high - low + 1
                if digits > 1:
                    bit = f"{high:>{digits}d}"
                    for i in range(digits):
                        bit_numbers[i].append(f" {bit[i]}")
                else:
                    bit_numbers[0].append(f"{high:>2d}")
                if first:
                    topline.append('┌')
                    midline.append('│')
                    botline.append('└')
                    first = False
                else:
                    topline.append('┬')
                    midline.append('│')
                    botline.append('┴')
                chars = size * 2 - 1
                if isinstance(data, int):
                    bit = f"{data:0{size}b}"
                    name = " ".join(bit)
                else:
                    name = f"{data:^{chars}s}"[0:chars]
                for i in range(digits):
                    bit_numbers[i].extend(['  ' * (size - 2)])
                if size > 1:
                    if digits > 1:
                        bit = f"{low:>{digits}d}"
                        for i in range(digits):
                            bit_numbers[i].append(f" {bit[i]}")
                    else:
                        bit_numbers[0].append(f"{low:>2d}")
                topline.append('─')
                topline.extend(['┬─' * (size - 1)])
                midline.append(self.format_name(name))
                botline.append('─')
                botline.extend(['┴─' * (size - 1)])
            topline.append('┐')
            midline.append('│')
            botline.append('┘')

            for i in range(digits):
                line_out.append(''.join(bit_numbers[i]))
            line_out.append(''.join(topline))
            line_out.append(''.join(midline))
            line_out.append(''.join(botline))

            output.append('\n'.join(line_out))

        return '\n'.join(reversed(output))

