# -*- encoding: utf-8 -*-

def passenger_walk(trains, passenger_name, steps):
    flag = False
    for train in trains:
        for car in train['cars']:
            if passenger_name in car['people']:
                if 0 <= steps + train['cars'].index(car) <= len(train['cars']):
                    car['people'].remove(passenger_name)
                    train['cars'][train['cars'].index(car) + steps]['people'].append(passenger_name)
                    return 1
                else:
                    return -1
    return -1


def cars_switch(event, trains):
    taking_train = None
    coupling_cars = None
    flag1 = False
    flag2 = False
    for train in trains:
        if train['name'] == event['train_from']:
            print('this is cars ', event['cars'])
            coupling_cars = train['cars'][len(train) - event['cars']:]
            for i in range(len(train) - event['cars'], len(train)):
                del train['cars'][i]
            if taking_train is not None:
                train['cars'].extend(coupling_cars)
            flag1 = True
        if train['name'] == event['train_to']:
            taking_train = train
            if coupling_cars is not None:
                train['cars'].extend(coupling_cars)
            coupling_cars = None
        flag2 = True
    if flag1 and flag2:
        return 1
    else:
        return -1


def process(data, events, car):
    print(data)
    print(events)
    for event in events:
        if event['type'] == 'walk':
            result_from_walk = passenger_walk(data, event['passenger'], event['distance'])
            if result_from_walk == -1:
                return -1

        if event['type'] == 'switch':
            result_from_switch = cars_switch(event, data)
            if result_from_switch == -1:
                return -1

    for dat in data:
        for carriage in dat['cars']:
            if car == carriage['name']:
                return len(carriage['people'])
    return -1
