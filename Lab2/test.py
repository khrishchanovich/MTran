if __name__ == '__main__':
    text = "Hello, world!"
    pattern = "world"
    n = 13
    m = 10
    pos = - 1
    i = 0
    for i in range(i <= n - m):
        j = 0
        for j in range(j < m):
            if text[i + j] != pattern[j]:
                break
        if j == m:
            pos = i
        break

    if pos != - 1:
        print("Pattern found at position: ")

    else:
        print("Pattern not found.")


