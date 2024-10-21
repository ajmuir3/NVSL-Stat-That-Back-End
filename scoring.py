def dual_meet_points(place,event):

    if event[-1] == True:
        dual_meet_scoring = {
            "1": 5,
            "2": 3,
            "3": 1,
            "4": 0,
            "5": 0,
            "6": 0
    }
    else:
        dual_meet_scoring = {
            "1":5,
            "2":0
        }

    return dual_meet_scoring[place]

def divisional_relays_points(place):

    divisional_relays_scoring = {
        "1": 14,
        "2": 10,
        "3": 8,
        "4": 6,
        "5": 4,
        "6": 2
    }

    return divisional_relays_scoring[place]

def divisional_ind_points(place):

    divisional_scoring = {
        "1": 28,
        "2": 24,
        "3": 22,
        "4": 20,
        "5": 18,
        "6": 16,
        "7": 14,
        "8": 10,
        "9": 8,
        "10": 6,
        "11": 4,
        "12": 2,
        "13": 1,
        "14": 0.5,
        "15": 0.0
    }

    return divisional_scoring[place]

def all_star_points(place):

    all_star_scoring = {
        "1": 44,
        "2": 38,
        "3": 36,
        "4": 34,
        "5": 32,
        "6": 30,
        "7": 28,
        "8": 26,
        "9": 24,
        "10": 20,
        "11": 16,
        "12": 14,
        "13": 12,
        "14": 10,
        "15": 8,
        "16": 6,
        "17": 4,
        "18": 2,
        "19": 1,
        "20": 0.5
    }

    return all_star_scoring[place]

#print(all_star_scoring("1"))