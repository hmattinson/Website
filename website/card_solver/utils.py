from itertools  import permutations, combinations, product, chain
from itertools import zip_longest
from fractions  import Fraction as F

def decode_cards(cards):
    return ['13' if c=='K' or c=='k' else
            '12' if c=='Q' or c=='q' else
            '11' if c=='J' or c=='j' else
            '1' if c=='A' or c=='a' else
            c for c in cards]

def solve(digits, target):
    digits = decode_cards(digits)
    exprlen = 2 * len(digits) - 1
    # permute all the digits
    digiperm = sorted(set(permutations(digits)))
    # All the possible operator combinations
    opcomb   = list(product('+-*/', repeat=len(digits)-1))
    # All the bracket insertion points:
    brackets = ( [()] + [(x,y)
                         for x in range(0, exprlen, 2)
                         for y in range(x+4, exprlen+2, 2)
                         if (x,y) != (0,exprlen+1)]
                 + [(0, 4, 6, 10)] ) # double brackets case
    print(brackets)
    for d in digiperm:
        for ops in opcomb:
            if '/' in ops:
                d2 = [('F(%s)' % i) for i in d] # Use Fractions for accuracy
            else:
                d2 = d
            ex = list(chain.from_iterable(zip_longest(d2, ops, fillvalue='')))
            for b in brackets:
                exp = ex[::]
                for insertpoint, bracket in zip(b, '()'*(len(b)//2)):
                    exp.insert(insertpoint, bracket)
                txt = ''.join(exp)
                try:
                    num = eval(txt)
                except ZeroDivisionError:
                    continue
                if num == target:
                    if '/' in ops:
                        exp = [ (term if not term.startswith('F(') else term[2:term.find(')')])
                               for term in exp ]
                    ans = ' '.join(exp).rstrip()
                    return (True,"Solution found: " + ans)
    return (False,f"No solution found for: {' '.join(digits)}")
