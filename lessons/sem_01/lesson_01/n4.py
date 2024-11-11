def is_there_any_good_subarray(nums: list[int], k: int) -> bool:
    prefix_sum = 0
    remainder_map = {0: -1}  # Изначально нулевой префикс имеет индекс -1
    
    for i in range(len(nums)):
        prefix_sum += nums[i]
        if k != 0:
            remainder = prefix_sum % k
        else:
            remainder = prefix_sum  # Если k == 0, просто используем сумму
        
        # Проверяем, если остаток уже есть в словаре
        if remainder in remainder_map:
            # Проверяем длину подмассива
            if i - remainder_map[remainder] > 1:
                return True
        else:
            # Если остатка нет, сохраняем текущий индекс
            remainder_map[remainder] = i
    
    return False