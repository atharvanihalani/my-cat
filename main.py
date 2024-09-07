#!/usr/bin/env python3
"""
    > python main.py abc abd ppqqrr --interations 10

    iiijjjlll: 670 (avg time 1108.5, avg temp 23.6)
    iiijjjd: 2 (avg time 1156.0, avg temp 35.0)
    iiijjjkkl: 315 (avg time 1194.4, avg temp 35.5)
    iiijjjkll: 8 (avg time 2096.8, avg temp 44.1)
    iiijjjkkd: 5 (avg time 837.2, avg temp 48.0)
"""

import argparse
import logging

# from copycat import Copycat, Reporter, plot_answers, save_answers

class Copycat():
    def __init__(self, rng_seed) -> None:

        # main loop?? idk
        pass

    def run(self, initial, modified, target, iterations):
        print('testing 123')
        condition = True
        while condition:
            # codelet loop
            # update slipnet
            pass
        pass
    
    pass




def main():
    """Program's main entrance point.  Self-explanatory code."""

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

    # for answer, d in sorted(iter(answers.items()), key=lambda kv: kv[1]['avgtemp']):
    #     print('%s: %d (avg time %.1f, avg temp %.1f)' % (answer, d['count'], d['avgtime'], d['avgtemp']))


if __name__ == '__main__':
    main()
