def calculate_prefixes(array_list: list[int]) -> list[int]:
    prefix_sums = [0]
    
    for i, elem in enumerate(array_list, start=1):
        prefix_sums.append(prefix_sums[i - 1] + elem)
    return prefix_sums

def range_sum(array_list: list[int], ranges: list[tuple[int, int]]) -> list[int]:
    prefix_sums = calculate_prefixes(array_list)
    return [(prefix_sums[range_[1]] - prefix_sums[range_[0]]) for range_ in ranges]
