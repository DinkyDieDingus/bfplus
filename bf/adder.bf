,       input 1 in c0
> ,     input 2 in c1

### coverting ascii inputs into numbers

> ++++ ++++     c2 = 8
[               loop until c2 becomes 0
  < ---- --     add 6 to c1
  < ---- --     add 6 to c0
  >> -
]
<


[        Start your loops with your cell pointer on the loop counter (c1 in our case)
< +      Add 1 to c0
> -      Subtract 1 from c1
]        End your loops with the cell pointer on the loop counter

++++ ++++  c1 = 8 and this will be our loop counter again
[
< +++ +++  Add 6 to c0
> -        Subtract 1 from c1
]
< .        Print out c0 which has the value 55 which translates to "7"!
