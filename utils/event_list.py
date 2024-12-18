def map_event(event):

    event_map = {
        "Boys Free 25M 8&U": 1,
        "Girls Free 25M 8&U": 2,
        "Boys Free 50M 9-10": 3,
        "Girls Free 50M 9-10": 4,
        "Boys Free 50M 11-12": 5,
        "Girls Free 50M 11-12": 6,
        "Boys Free 50M 13-14": 7,
        "Girls Free 50M 13-14": 8,
        "Boys Free 50M 15-18": 9,
        "Girls Free 50M 15-18": 10,
        "Boys Back 25M 8&U": 11,
        "Girls Back 25M 8&U": 12,
        "Boys Back 50M 9-10": 13,
        "Girls Back 50M 9-10": 14,
        "Boys Back 50M 11-12": 15,
        "Girls Back 50M 11-12": 16,
        "Boys Back 50M 13-14": 17,
        "Girls Back 50M 13-14": 18,
        "Boys Back 50M 15-18": 19,
        "Girls Back 50M 15-18": 20,
        "Boys Breast 25M 8&U": 21,
        "Girls Breast 25M 8&U": 22,
        "Boys Breast 50M 9-10": 23,
        "Girls Breast 50M 9-10": 24,
        "Boys Breast 50M 11-12": 25,
        "Girls Breast 50M 11-12": 26,
        "Boys Breast 50M 13-14": 27,
        "Girls Breast 50M 13-14": 28,
        "Boys Breast 50M 15-18": 29,
        "Girls Breast 50M 15-18": 30,
        "Boys Fly 25M 8&U": 31,
        "Girls Fly 25M 8&U": 32,
        "Boys Fly 25M 9-10": 33,
        "Girls Fly 25M 9-10": 34,
        "Boys Fly 50M 11-12": 35,
        "Girls Fly 50M 11-12": 36,
        "Boys Fly 50M 13-14": 37,
        "Girls Fly 50M 13-14": 38,
        "Boys Fly 50M 15-18": 39,
        "Girls Fly 50M 15-18": 40,
        "Boys Free 100M Relay 8&U": 41,
        "Girls Free 100M Relay 8&U": 42,
        "Boys Medley 100M Relay 9-10": 43,
        "Girls Medley 100M Relay 9-10": 44,
        "Boys Medley 100M Relay 11-12": 45,
        "Girls Medley 100M Relay 11-12": 46,
        "Boys Medley 100M Relay 13-14": 47,
        "Girls Medley 100M Relay 13-14": 48,
        "Boys Medley 200M Relay 15-18": 49,
        "Girls Medley 200M Relay 15-18": 50,
        "Boys Free 200M Relay Mixed Age": 51,
        "Girls Free 200M Relay Mixed Age": 52,
        "Boys Free 25Y 8&U": 1,
        "Girls Free 25Y 8&U": 2,
        "Boys Free 50Y 9-10": 3,
        "Girls Free 50Y 9-10": 4,
        "Boys Free 50Y 11-12": 5,
        "Girls Free 50Y 11-12": 6,
        "Boys Free 50Y 13-14": 7,
        "Girls Free 50Y 13-14": 8,
        "Boys Free 50Y 15-18": 9,
        "Girls Free 50Y 15-18": 10,
        "Boys Back 25Y 8&U": 11,
        "Girls Back 25Y 8&U": 12,
        "Boys Back 50Y 9-10": 13,
        "Girls Back 50Y 9-10": 14,
        "Boys Back 50Y 11-12": 15,
        "Girls Back 50Y 11-12": 16,
        "Boys Back 50Y 13-14": 17,
        "Girls Back 50Y 13-14": 18,
        "Boys Back 50Y 15-18": 19,
        "Girls Back 50Y 15-18": 20,
        "Boys Breast 25Y 8&U": 21,
        "Girls Breast 25Y 8&U": 22,
        "Boys Breast 50Y 9-10": 23,
        "Girls Breast 50Y 9-10": 24,
        "Boys Breast 50Y 11-12": 25,
        "Girls Breast 50Y 11-12": 26,
        "Boys Breast 50Y 13-14": 27,
        "Girls Breast 50Y 13-14": 28,
        "Boys Breast 50Y 15-18": 29,
        "Girls Breast 50Y 15-18": 30,
        "Boys Fly 25Y 8&U": 31,
        "Girls Fly 25Y 8&U": 32,
        "Boys Fly 25Y 9-10": 33,
        "Girls Fly 25Y 9-10": 34,
        "Boys Fly 50Y 11-12": 35,
        "Girls Fly 50Y 11-12": 36,
        "Boys Fly 50Y 13-14": 37,
        "Girls Fly 50Y 13-14": 38,
        "Boys Fly 50Y 15-18": 39,
        "Girls Fly 50Y 15-18": 40,
        "Boys Free 100Y Relay 8&U": 41,
        "Girls Free 100Y Relay 8&U": 42,
        "Boys Medley 100Y Relay 9-10": 43,
        "Girls Medley 100Y Relay 9-10": 44,
        "Boys Medley 100Y Relay 11-12": 45,
        "Girls Medley 100Y Relay 11-12": 46,
        "Boys Medley 100Y Relay 13-14": 47,
        "Girls Medley 100Y Relay 13-14": 48,
        "Boys Medley 200Y Relay 15-18": 49,
        "Girls Medley 200Y Relay 15-18": 50,
        "Boys Free 200Y Relay Mixed Age": 51,
        "Girls Free 200Y Relay Mixed Age": 52,
        "Boys IM 100M 10&U": 41,
        "Girls IM 100M 10&U": 42,
        "Girls Free 100M Relay 9-10": 15,
        "Boys Free 100M Relay 9-10": 16,
        "Girls Free 100M Relay 11-12": 17,
        "Boys Free 100M Relay 11-12": 18,
        "Girls Free 200M Relay 13-14": 19,
        "Boys Free 200M Relay 13-14": 20,
        "Girls Free 200M Relay 15-18": 21,
        "Boys Free 200M Relay 15-18": 22,
        "Girls Medley 200M Relay 13-14": 19,
        "Boys Medley 200M Relay 13-14": 20,
        "Girls Medley 100M Relay 8&U": 3,
        "Boys Medley 100M Relay 8&U": 4,
        'Boys IM 100M 11-12': 43,
        'Girls IM 100M 11-12': 44,
        'Boys IM 100M 13-14': 45,
        'Girls IM 100M 13-14': 46,
        'Boys IM 100M 15-18': 47,
        'Girls IM 100M 15-18': 48
    }

    return event_map[event]