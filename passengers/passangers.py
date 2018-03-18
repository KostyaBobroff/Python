# -*- encoding: utf-8 -*-
import json


def passenger_walk(trains, passenger_name, steps):
    for train in trains:
        for car_index, car in enumerate(train['cars']):
            if passenger_name in car['people']:
                if 0 <= steps + car_index <= len(train['cars']):
                    car['people'].remove(passenger_name)
                    train['cars'][car_index + steps]['people'].append(passenger_name)
                    return 1
                else:
                    return -1
    return -1


# def cars_switch(event, trains):
#     taking_train = None
#     coupling_cars = None
#     flag1 = False
#     flag2 = False
#     for train in trains:
#         if train['name'] == event['train_from']:
#             print('this is cars ', event['cars'])
#             coupling_cars = train['cars'][len(train) - event['cars']:]
#             #for i in range(len(train) - event['cars'], len(train)):
#               #  del train['cars'][i]
#
#             train['cars'] = train['cars'][:- event['cars']]
#             if taking_train is not None:
#                 # train['cars'].extend(coupling_cars)
#                 taking_train['car'].extend(coupling_cars)
#             flag1 = True
#         if train['name'] == event['train_to']:
#             taking_train = train
#             if coupling_cars is not None:
#                 train['cars'].extend(coupling_cars)
#             coupling_cars = None
#         flag2 = True
#     if flag1 and flag2:
#         return 1
#     else:
#         return -1

def cars_switch(event, trains):
    first_train = None
    second_train = None
    for train_index, train in trains:

        if train['name'] == event['train_from']:
            first_train = train
        if train['name'] == event['train_to']:
            second_train = train

    if second_train and first_train and 1 <= event['cars'] <= len(first_train['cars']):
        coupling_cars = first_train['cars'][-event['cars']:]
        first_train['cars'] = first_train['cars'][:-event['cars']]
        second_train['cars'].extend(coupling_cars)
        return 1
    else:
        return -1


def process(data, events, car):
    for event in events:
        if event['type'] == 'walk':

            if passenger_walk(data, event['passenger'], event['distance']) == -1:
                return -1

        if event['type'] == 'switch':

            if cars_switch(event, data) == -1:
                return -1

    for dat in data:
        for carriage in dat['cars']:
            if car == carriage['name']:
                return len(carriage['people'])
    return -1

# error_message = 'ERROR in file {}. Expected: "{}", got: "{}"'
# data = json.load(open('./tests/test6.json'))
# trains, events, result = data['trains'], data['events'], data['result']
# got = process(trains, events, result['car'])
# expected = result['amount']
# if got != expected:
#     print(error_message.format('./tests/test6.json', expected, got))
# print("All tests passed!")
