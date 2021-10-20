,       input 1 in c0
> ,     input 2 in c1

### coverting ascii inputs into numbers

> ++++ ++++     c2 = 8
[               loop until c2 becomes 0
  < ---- --     add 6 to c1
  < ---- --     add 6 to c0
  >> -
]

### multiply numbers together

<              c1
[               loop until c1 becomes 0
  -
  <
  [            loop until c0 becomes 0
    -           c0 1
    >>> +         c3 1
    <<<
  ]
  >>>
  [
    -
    < +
    << +
    >>>
  ]
  <<
]

>> ++++ ++++
[
  < ++++ ++
  > -
]

< .
