#!/usr/bin/env python3

import argparse
import logging
import random

class Copycat():

    """
    update time in slipnet (/ workspace¿)
    initial knowledge parsing: letter cat + object cat + string pos
        initially fully activate letter-cat/string-pos AND clamp activation 
    
    """

    def __init__(self, rng_seed) -> None:
        pass

    def run_iter(self, initial, modified, target):
        """
        runs ONE iteration of the copycat program on the input strings
        
        reset everything
            slipnet + workspace + temperature + coderack

        initially parse strings
            letter-category, object-category, and string-position
        
        output: (answer, temperature, time)
        """
        
        pass

    def run(self, initial, modified, target, iterations):
        """
        takes in three strings as an input
        runs 'n' iterations of the copycat program on them

        answer has form
            {'rqd': {'count': 3, 'avgtemp': 20.848603874416604, 'avgtime': 1803.6666666666667}, 
            'rqq': {'count': 4, 'avgtemp': 34.53911829931333, 'avgtime': 2200.0}, 
            ... }
        """
        answers = {}
        for i in range(iterations):
            answer = self.run_iter(initial, modified, target)

            if answer[0] not in answers:
                answers[answer[0]] = {'count': 1, 'avgtemp':answer[1], 'avgtime':answer[2]}
            else:
                ans = answers[answer[0]]
                newtemp = ((ans['count'] * ans['avgtemp']) + answer[1]) / (ans['count'] + 1)
                newtime = ((ans['count'] * ans['avgtime']) + answer[2]) / (ans['count'] + 1)

                ans['count'] += 1
                ans['avgtemp'] = newtemp
                ans['avgtime'] = newtime
        
        return answers


def main():
    """Program's main entrance point.  Self-explanatory code.
    
        spits out an aggregated answer of the form
            iiijjjlll: 670 (avg time 1108.5, avg temp 23.6)
            iiijjjd: 2 (avg time 1156.0, avg temp 35.0)
            iiijjjkkl: 315 (avg time 1194.4, avg temp 35.5)
            ...etc
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=None, help='Provide a deterministic seed for the RNG.')
    parser.add_argument('--iterations', type=int, default=1, help='Run the given case this many times.')
    parser.add_argument('--plot', action='store_true', help='Plot a bar graph of answer distribution')
    parser.add_argument('--noshow', action='store_true', help='Don\'t display bar graph at end of run')
    parser.add_argument('initial', type=str, help='A...')
    parser.add_argument('modified', type=str, help='...is to B...')
    parser.add_argument('target', type=str, help='...as C is to... what?')
    options = parser.parse_args()

    copycat = Copycat(rng_seed=options.seed)
    answers = copycat.run(options.initial, options.modified, options.target, options.iterations)

    for answer, d in sorted(iter(answers.items()), key=lambda kv: kv[1]['avgtemp']):
        print('%s: %d (avg time %.1f, avg temp %.1f)' % (answer, d['count'], d['avgtime'], d['avgtemp']))


if __name__ == '__main__':
    main()
