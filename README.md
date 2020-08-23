# Wavedrom ASCII

An ASCII (actually Unicode) representation of [Wavedrom](https://github.com/wavedrom/wavedrom) waves and bitfields.

## Comparison

Example Wavedrom JSON:
``` json
{
  "signal": [
    {
      "name": "clk",
      "wave": "p......"
    },
    {
      "name": "bus",
      "wave": "x.34.5x",
      "data": "head body tail"
    },
    {
      "name": "wire",
      "wave": "0.1..0."
    }
  ]
}
```

Wavedrom image:

<img src="https://svg.wavedrom.com/{signal:[{name:'clk',wave:'p......'},{name:'bus',wave:'x.34.5x',data:'head body tail'},{name:'wire',wave:'0.1..0.'}]}"/>

ASCII representation:
```
        ┌────┐    ┌────┐    ┌────┐    ┌────┐    ┌────┐    ┌────┐    ┌────┐    
  clk   ┘    └────┘    └────┘    └────┘    └────┘    └────┘    └────┘    └────
        ────────────────────╥─────────╥───────────────────╥─────────╥─────────
  bus   XXXXXXXXXXXXXXXXXXXX║ head    ║ body              ║ tail    ║XXXXXXXXX
        ────────────────────╨─────────╨───────────────────╨─────────╨─────────
                            ┌─────────────────────────────┐                   
  wire  ────────────────────┘                             └───────────────────
```


The Bitfield example from Wavedrom:

![reg vl](https://svg.wavedrom.com/github/wavedrom/wavedrom/master/test/reg-vl.json5)

Will be rendered as:

```
31  2928  262524      2019      1514  1211       7 6           0
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│ nf  │ mop │v│  lumop  │   rs1   │width│   vd    │0 0 0 0 1 1 1│
└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘
```
