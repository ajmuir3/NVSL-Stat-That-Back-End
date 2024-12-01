CREATE TABLE Team (
    teamID VARCHAR(5) PRIMARY KEY,
    teamName VARCHAR(255) NOT NULL,
    location VARCHAR(255)
);

CREATE TABLE Swimmer (
    swimmerID VARCHAR(255) PRIMARY KEY,
    teamID VARCHAR(5),
    name VARCHAR(255) NOT NULL,
    FOREIGN KEY (teamID) REFERENCES Team(teamID)
);

CREATE TABLE Season (
    seasonID VARCHAR(10) PRIMARY KEY,
    teamID VARCHAR(5),
    year INT NOT NULL,
    division INT NOT NULL,
    meetsWon INT,
    meetsLost INT,
    meetsTied INT,
    powerRanking DECIMAL(5, 2),
    dmPoints DECIMAL(5, 1),
    drPoints DECIMAL(5, 1),
    dPoints DECIMAL(5, 1),
    arPoints DECIMAL(5, 1),
    aPoints DECIMAL(5, 1),
    tPoints DECIMAL(5, 1),
    gtPoints DECIMAL(5, 1),
    FOREIGN KEY (teamID) REFERENCES Team(teamID)
);

CREATE TABLE Meet (
    meetID VARCHAR(255) PRIMARY KEY,
    date DATE NOT NULL,
    course ENUM('Meters', 'Yards') NOT NULL,
    title VARCHAR(255) NOT NULL,
    meet_type ENUM('Dual', 'Champs') NOT NULL
);

CREATE TABLE MeetParticipant (
    meet_partID VARCHAR(255) PRIMARY KEY,
    meetID VARCHAR(255),
    teamID VARCHAR(5),
    FOREIGN KEY (meetID) REFERENCES Meet(meetID),
    FOREIGN KEY (teamID) REFERENCES Team(teamID)
);

CREATE TABLE DualMeet (
    dual_meetID VARCHAR(255) PRIMARY KEY,
    meetID VARCHAR(255),
    team_home VARCHAR(5),
    team_away VARCHAR(5),
    home_points DECIMAL(5, 1),
    away_points DECIMAL(5, 1),
    FOREIGN KEY (meetID) REFERENCES Meet(meetID),
    FOREIGN KEY (team_home) REFERENCES Team(teamID),
    FOREIGN KEY (team_away) REFERENCES Team(teamID)
);

CREATE TABLE ChampsMeet (
    champs_meetID VARCHAR(255) PRIMARY KEY,
    meetID VARCHAR(255),
    meet_type ENUM('Divisional Relays', 'Divisionals', 'All Star Relay Carnival', 'All Stars') NOT NULL,
    FOREIGN KEY (meetID) REFERENCES Meet(meetID)
);

CREATE TABLE Event (
    eventID VARCHAR(255) PRIMARY KEY,
    number INT NOT NULL,
    gender ENUM('Boys', 'Girls') NOT NULL,
    age_group ENUM('8&U', '9-10', '11-12', '13-14', '15-18', 'Mixed Age') NOT NULL,
    distance INT NOT NULL,
    stroke ENUM('Free', 'Back', 'Breast', 'Fly', 'Medley', 'IM') NOT NULL,
    individual BOOLEAN NOT NULL
);

CREATE TABLE MeetEvent (
    meet_eventID VARCHAR(255) PRIMARY KEY,
    eventID VARCHAR(255),
    meetID VARCHAR(255),
    FOREIGN KEY (eventID) REFERENCES Event(eventID),
    FOREIGN KEY (meetID) REFERENCES Meet(meetID)
);

CREATE TABLE Result (
    resultID VARCHAR(255) PRIMARY KEY,
    meet_eventID VARCHAR(255),
    time DECIMAL(5, 2),
    place INT NOT NULL,
    points DECIMAL(2, 1),
    PowerIndex DECIMAL(6, 2),
    FOREIGN KEY (meet_eventID) REFERENCES MeetEvent(meet_eventID)
);
