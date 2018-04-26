if __name__ == '__main__':
    teacher = 14
    students = 326
    all = teacher + students

    car_big = 40
    car_small = 20

    prices = []
    big = 1
    while True:
        other = (all - big * car_big)
        if other < 0:
            break

        need_plus_one = ((other % car_small) != 0)
        small = int(other / car_small)
        if need_plus_one:
            small += 1

        if big + small > teacher:
            big += 1
            continue

        price = big * 900 + small * 500
        prices.append({"big": big, "small": small, "price": price})
        big += 1

    print(prices)
