def get_len_of_longest_substring(string: str) -> int:
    char_set = set()  # Множество для хранения уникальных символов
    max_length = 0    # Максимальная длина подстроки
    start = 0         # Начало подстроки

    for end in range(len(string)):
        # Если символ уже в множестве, сдвигаем `start`
        while string[end] in char_set:
            char_set.remove(string[start])
            start += 1
            
        char_set.add(string[end])
        
        # Обновляем максимальную длину подстроки
        max_length = max(max_length, end - start + 1)

    return max_length