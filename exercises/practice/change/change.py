def find_fewest_coins(coins, target):
    if target == 0:
        return []
    if target < 0:
        raise ValueError("target can't be negative")

    denoms = list(reversed(coins))
    max_length = target // denoms[-1]
    combos = ComboFinder(denoms, target, max_length).find()
    if not combos:
        raise ValueError("can't make target with given coins")
    return sorted(min(combos, key=len))


class ComboFinder:
    def __init__(self, denoms, target, max_length):
        self._denoms = denoms
        self._target = target
        self._max_length = max_length

    def find(self):
        counts_for_denom = self.get_counts_for_denom()

        combos = []
        for starting_denom in self._denoms:
            for denom in self._denoms[self._denoms.index(starting_denom):]:
                counts = [c for c in counts_for_denom[denom] if c <= self._max_length]
                combos += self.find_combos_for_denom(counts, denom)
        return combos

    def find_combos_for_denom(self, counts, denom):
        result = []
        for count in counts:
            if count <= self._max_length:
                combos = self.find_combos_for_denom_and_count(count, denom)
                if combos:
                    result += combos
                    self._max_length = min(min(len(c) for c in combos), self._max_length)
        return result

    def get_counts_for_denom(self):
        result = {}
        for denom in self._denoms:
            max_count = min(self._target // denom, self._max_length)
            result[denom] = [count for count in reversed(range(1, max_count + 1))]
        return result

    def find_combos_for_denom_and_count(self, count, denom):
        base_combo = [denom] * count
        total = denom * count
        if total == self._target:
            return [base_combo]
        if denom == self._denoms[-1]:
            return []

        next_denom_index = self._denoms.index(denom) + 1
        finder = ComboFinder(
            denoms=self._denoms[next_denom_index:],
            target=self._target - total,
            max_length=self._max_length - len(base_combo),
        )
        return [base_combo + c for c in finder.find()]
