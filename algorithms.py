# Copyright 2008 Bjorn Edstrom
# from http://blog.bjrn.se/2008/04/lexicographic-permutations-using.html
# A Python implementation of Algorithm L
"""
Lexicographic permutations using Algorithm L (STL next_permutation in Python)
One of the more useful functions in the C++ Standard Library is next_permutation
in <algorithm>. The STL function has a desirable property that almost every
other permutation generating functions I've seen lack, namely lexicographic
awareness of the elements being permuted.

A typical function will, given a sequence of elements such as (1, 1, 2, 2),
permute on indices only. This will in our case give 4! permutations, which is
often not what we want. The STL implementation will “correctly” generate only
unique permutations, in our case 4! / 2!2!, and also generate them in the right
order.

What's special about most STL implementations is the use of a fairly unknown
algorithm for finding permutations in lexicographic order. A canonical templated
implementation is usually about 25 lines of code. It is also non-recursive and
very fast.

Here's a Python implementation of next_permutation with user-defined comparison.
Use freely.
"""

def next_permutation(seq, pred=cmp):
    """Like C++ std::next_permutation() but implemented as
    generator. Yields copies of seq."""

    def reverse(seq, start, end):
        # seq = seq[:start] + reversed(seq[start:end]) + \
        #       seq[end:]
        end -= 1
        if end <= start:
            return
        while True:
            seq[start], seq[end] = seq[end], seq[start]
            if start == end or start+1 == end:
                return
            start += 1
            end -= 1
    
    if not seq:
        raise StopIteration

    try:
        seq[0]
    except TypeError:
        raise TypeError("seq must allow random access.")

    first = 0
    last = len(seq)
    seq = seq[:]

    # Yield input sequence as the STL version is often
    # used inside do {} while.
    yield seq
    
    if last == 1:
        raise StopIteration

    while True:
        next = last - 1

        while True:
            # Step 1.
            next1 = next
            next -= 1
            
            if pred(seq[next], seq[next1]) < 0:
                # Step 2.
                mid = last - 1
                while not (pred(seq[next], seq[mid]) < 0):
                    mid -= 1
                seq[next], seq[mid] = seq[mid], seq[next]
                
                # Step 3.
                reverse(seq, next1, last)

                # Change to yield references to get rid of
                # (at worst) |seq|! copy operations.
                yield seq[:]
                break
            if next == first:
                raise StopIteration
    raise StopIteration
