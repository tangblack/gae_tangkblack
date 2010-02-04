# print denary_to_binary(255) # 11111111
# print int(denary_to_binary(255), 2) # 255
def denary_to_binary(n):
    bStr = ''
    if n < 0: raise ValueError, "must be a positive integer"
    if n == 0: return '0'
    while n > 0:
        bStr = str(n % 2) + bStr
        n = n >> 1
    return bStr
     

# print int_to_bin(255, 12) # 000011111111
# print int("000011111111", 2) # 255
def int_to_bin(n, count=24):
    return "".join([str((n >> y) & 1) for y in range(count - 1, -1, -1)])
        