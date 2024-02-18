# def change_password(password, a, b):
#     old_password = list(password)
#     old_password[a-1], old_password[b-1] = old_password[b-1], old_password[a-1]
#
#     return ''.join(old_password)
#
# password = input()
# a, b = map(int, input().split())
#
# new_password = change_password(password, a, b)
#
# print(new_password)
#



# N = int(input())
# cards = list(map(int, input().split()))
# missing_number = 0
#
# count = {}
# for num in cards:
#     count[num] = count.get(num, 0) + 1
#
# for num, cnt in count.items():
#     if cnt < 4:
#         missing_number = num
#
# print(missing_number)
#
# values = list(map(int, input().split()))
# x = list(map(int, input().split()))
#
# print(values[1]-values[0]*values[2])

# def factor(N, password):
#     sadness = 0
#     for i in range(N):
#         for j in range(i+1, N):
#             if password[:i] + password[i+1:] == password[:j] + password[j+1:]:
#                 sadness += 1
#     return sadness
#
# N = int(input())
# password = input()
#
# result = factor(N, password)
# print(result)

# x = int(input())
#
# count = 0
# q = 2
# used = set()
#
# while x > 1:
#     if x % q == 0 and q not in used:
#         x /= q
#         count += 1
#         used.add(q)
#     else:
#         q += 1
#
# print(count)

A, B, N, Q = map(int, input().split())
p = []
for i in range(Q):
    p.append(list(map(int, input().split())))

rows = [0] * A
cols = [0] * B
for i in p:
    t, n, color = i
    if t == 1:
        rows[n - 1] = color
    else:
        cols[n - 1] = color

count = [0] * (N + 1)
for i in range(A):
    for j in range(B):
        if rows[i] != 0:
            color = rows[i]
        else:
            color = cols[j]
        count[color] += 1

print(*count[1:])