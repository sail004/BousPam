async def check(number):
    summary = 0
    for i in range(10):
        if i % 2 == 0:
            buffer = int(number[i]) * 2
            if buffer > 9:
                buffer -= 9
            summary += buffer
        else:
            summary += int(number[i])
    return summary % 10 == 0


async def set_luhn(number):
    summary = 0
    for i in range(9):
        if i % 2 == 0:
            buffer = int(number[i]) * 2
            if buffer > 9:
                buffer -= 9
            summary += buffer
        else:
            summary += int(number[i])
    luhn = 10 - summary % 10
    return number + str(luhn)
