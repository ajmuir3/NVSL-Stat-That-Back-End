import csv

csv_files = {
    "meet": "./data/Meet.csv",
    "dual_meet": "./data/DualMeet.csv",
    "champs_meet": "./data/ChampsMeet.csv",
    "event": "./data/Event.csv",
    "meet_event": "./data/MeetEvent.csv",
    "result": "./data/Result.csv",
    "swimmer": "./data/Swimmer.csv",
    "meet_participant": "./data/MeetParticipant.csv"
}

def write_csv_headers():
    headers = {
    "meet": "meetID,year,date,course,title,meet_type\n",
    "dual_meet": "dualMeetID,meetID,homeTeamID,awayTeamID,homeTeamPoints,awayTeamPoints\n",
    "champs_meet": "champsMeetID,meetID,meet_type\n",
    "event": "eventID,number,gender,ageGroup,distance,stroke,individual\n",
    "meet_event": "meetEventID,meetID,eventID\n",
    "result": "resultID,meetEventID,swimmerID,time,place,points,powerIndex\n",
    "swimmer": "swimmerID,teamID,name\n",
    "meet_participant": "participantID,meetID,teamID\n"
}
    for key, file_path in csv_files.items():
        with open(file_path, "w") as file:
            file.write(headers[key])

def write_csv(entity, data):
    with open(csv_files[entity], "a") as file:
        file.write(",".join(map(str, data)) + "\n")

