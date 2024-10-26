def find_fewest_coins(coins, target):
    if target == 0:
        return []
    if target < 0:
        raise ValueError("target can't be negative")

    denoms = list(reversed(coins))
    max_length = target // denoms[-1]
    combos = find_combos(denoms, target, max_length)
    if not combos:
        raise ValueError("can't make target with given coins")
    return sorted(min(combos, key=len))


def find_combos(denoms, target, max_length):
    counts_for_denom = get_counts_for_denom(denoms, target, max_length)

    combos = []
    for starting_denom in denoms:
        for denom in denoms[denoms.index(starting_denom):]:
            counts = [c for c in counts_for_denom[denom] if c <= max_length]
            add_sub_combos(combos, denoms, target, counts, denom, max_length)
    return combos


def add_sub_combos(combos, denoms, target, counts, denom, max_length):
    for count in counts:
        sub_combos = find_combos_for_denom_and_count(denoms, count, denom, target, max_length)
        if sub_combos:
            combos += sub_combos
            max_length = min(min(len(c) for c in combos), max_length)


def get_counts_for_denom(denoms, target, max_length):
    result = {}
    for denom in denoms:
        max_count = min(target // denom, max_length)
        result[denom] = [count for count in reversed(range(1, max_count + 1))]
    return result


def find_combos_for_denom_and_count(denoms, count, denom, target, max_length):
    combo = [denom] * count
    total = denom * count
    if total == target:
        return [combo]
    if len(combo) >= max_length:
        return []

    next_denom_index = denoms.index(denom) + 1
    if next_denom_index >= len(denoms):
        return []
    
    sub_denoms = denoms[next_denom_index:]
    new_target = target - total
    sub_combos = find_combos(sub_denoms, new_target, max_length - len(combo))
    return [combo + c for c in sub_combos]


# [2, 5, 10, 20, 50], 21

# 50: []
# 20: [(1, 1)]
# 10: [(2, 1), (1, 11)]
#  5: [(4, 1), (3, 6), (2, 11), (1, 16)]
#  2: [(10, 1), (9, 3), (8, 5), (7, 7), (6, 9), (5, 11), (4, 13), (3, 15), (2, 17), (1, 19)]

# 50: []
# 20: [1]
# 10: [2, 1]
#  5: [4, 3, 2, 1]
#  2: [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

# denoms: [50, 20, 10, 5, 2]


# denoms = reversed(coins) = [50, 20, 10, 5, 2]
# target=21
# next_denom_index = 0
# combos = []
#
# for starting_denom in denoms[next_denom_index:]:
#     combo = []
#     for denom in denoms[index(starting_denom):]:
#         for count in counts_for_denom[denom]:
#             if count * denom > target:
#                 continue
#             total = denon * count
#             target = target - total
#             if target == 0
#                 combo += [denom] * count
#                 combos.append(combo)
#                 combo = []
#                 continue
#             next_denom_index = index(denom) + 1
#             if target <= denoms[next_denom_index]:
#                 continue
#             combo += [denom] * count
#             recur
#
#             
#             ------------
#             denom = 20
#             count = 1
#             total = 20
#             target = 1
#             next_denom_index = 2
#         
#             ------------
#             denom = 10
#             count = 2
#             total = 20
#             target = 1
#             next_denom_index = 3
#
#             ------------
#             denom = 10
#             count = 1
#             total = 10
#             target = 11
#             next_denom_index = 3
#             combo = [10]
#
#             for starting_denom in denoms[next_denom_index:]:
#                 for denom in denoms[index(starting_denom):]:
#                     for count in counts_for_denom[denom]:
#                         if count * denom > target:
#                             continue
#                         --------
#                         denom = 5
#                         count = 2
#                         total = denom * count = 10
#                         target = target - total = 1
#                         if target <= denoms[next_denom_index]:
#                             continue
#
#                         ---------
#                         denom = 5
#                         count = 1
#                         total = denom * count = 5
#                         target = target - total = 6
#                         if target <= denoms[next_denom_index]:
#                             continue
#                         combo += [denom] * count = [10, 5]
#
#                         next_denom_index = index(denom) + 1 = 4
#                         for starting_denom in denoms[next_denom_index]:
#                             for denom in denoms[index(startind_denom)]:
#                                 for count in counts_for_denom[denom]:
#                                     if count * denom > target:
#                                         continue
#                                     ------
#                                     denom = 2
#                                     count = 3
#                                     total = denom * count = 6
#                                     target = target - total = 0
#                                     if target <= denoms[next_denom_index]:
#                                         continue
#                                     combo += [denom] * count = [10, 5, 2, 2, 2]



# min count: 19
