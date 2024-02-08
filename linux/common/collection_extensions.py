from itertools import chain, pairwise
from typing import Any, Callable, Generator, Iterable, List


class CollectionExtensions:
    @staticmethod
    def split_between(predicate: Callable[[Any, Any], bool], items: Iterable) -> Generator[List[Any], None, None]:
        """Split an iterable into groups based on a predicate function.

        Args:
            predicate (callable): A predicate function that takes two arguments (before and after)
                and returns a boolean value indicating whether to split the group at that point.
            items (iterable): The iterable to split into groups.

        Yields:
            list: A list containing consecutive items from the input iterable that satisfy
                the given predicate function.

        Example:
            Consider an iterable of integers 'numbers' and a predicate function 'is_even'
            that returns True if the current number and the next number are both even.
            We can use split_between to group consecutive even numbers:

            >>> numbers = [2, 4, 6, 3, 8, 10, 7, 9, 12]
            >>> def is_even(before, after):
            ...     return before % 2 == 0 and after % 2 == 0
            ...
            >>> list(split_between(is_even, numbers))
            [[2, 4, 6], [8, 10], [12]]
        
        Credits:
            Dale from ArjanCodes Python community (server on Discord).
        """
        group = []

        sentinel = object()
        paired_items = chain(items, [sentinel])
        paired_items = pairwise(paired_items)

        for before, after in paired_items:
            if after is sentinel:
                group.append(before)
                yield group
                group = [] # shouldn't loop again
            elif predicate(before, after):
                group.append(before)
                yield group
                group = []
            else:
                group.append(before)
                
        assert len(group) == 0
