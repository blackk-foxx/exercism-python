from dataclasses import dataclass


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


@dataclass
class ComboFinder:
    denoms: list[int]
    target: int
    max_length: int

    def find(self):
        combos = []
        for starting_denom_index in range(len(self.denoms)):
            for denom in self.denoms[starting_denom_index:]:
                combos += self.find_combos_for_denom(denom)
        return combos

    def find_combos_for_denom(self, denom):
        result = []
        max_count = min(self.target // denom, self.max_length)
        for count in range(max_count, 0, -1):
            base_combo = [denom] * count
            combos = self.find_combos_with_base(base_combo, denom)
            if combos:
                result += combos
                self.update_max_length(combos)
        return result

    def update_max_length(self, combos):
        min_combo_length = min(len(c) for c in combos)
        self.max_length = min(min_combo_length, self.max_length)

    def find_combos_with_base(self, base_combo, denom):
        if sum(base_combo) == self.target:
            return [base_combo]
        if denom == self.denoms[-1]:
            return []
        return self.find_combos_with_suboptimal_base(base_combo, denom)

    def find_combos_with_suboptimal_base(self, base_combo, denom):
        next_denom_index = self.denoms.index(denom) + 1
        finder = ComboFinder(
            denoms=self.denoms[next_denom_index:],
            target=self.target - sum(base_combo),
            max_length=self.max_length - len(base_combo),
        )
        return [base_combo + c for c in finder.find()]
