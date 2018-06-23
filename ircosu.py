import socket
import sys
import time
 
name = "your osu nickname here"
password = "irc password here"
channel = input("lobby id: ") 
match_type = input("match_type: ") # types: 1v1, 4v4 (none working yet)
 
### These variables should not be changed
server = "irc.ppy.sh"
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
### Used to establish connection with the server and provide account information
def connect(nickname, password):
    ircsock.connect((server, 6667))
    ircsock.send(bytes("PASS " + password + "\n", "UTF-8"))
    ircsock.send(bytes("NICK " + nickname +"\n", "UTF-8"))
    ircsock.send(bytes("USER " + nickname + " " + nickname + " " + nickname + " :" + nickname + "\n", "UTF-8"))
 
### Used to connect to the lobby and receive a list of users in it
def joinlobby(mp_id):
    channel = f"#mp_{mp_id}" ### Creates a channel name from provided ID
    ircsock.send(bytes("JOIN " + channel + "\n", "UTF-8"))
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)
 
### Responds to pings
def pingresponder(pingcontent):
    ircsock.send(bytes("PONG " + pingcontent + "\n", "UTF-8"))
 
### Used to send messages
def sendmsg(msg, mp_id=channel):
    target = f"#mp_{mp_id}" ### Creates a channel name from provided ID
    ircsock.send(bytes("PRIVMSG " + target + " :" + msg + "\n", "UTF-8"))
    time.sleep(0.2)
 
def receiver_1v1():
    player1 = input("player1: ")
    player2 = input("player2: ")
    roll1 = 0
    roll2 = 0
    sentrolls = False
    rollsreminder = False
    nextpick = "null"
    score1 = 0
    score2 = 0
    while True:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        if ircmsg.find("PING") != -1: ### Reacts to pings
            pingcontent = ircmsg.split('PING')[1]
            pingresponder(pingcontent)
        if ircmsg.find("PRIVMSG") != -1:
            name = ircmsg.split('PRIVMSG',1)[0].split(':')[-1][:-12]
            content = ircmsg.split('PRIVMSG',1)[1].split(':', 1)[1].split("\n")[0]
            message = (f"{name}: {content}")
            print(message)
        if rollsreminder == False:
            sendmsg("Waiting for players to roll using the !roll command")
            rollsreminder = True
        if roll1 == 0 and ircmsg.find(f":BanchoBot!cho@ppy.sh PRIVMSG #mp_{channel} :{player1} rolls") != -1: ### Gets player1's roll
            roll = ircmsg.split(f"rolls ")[-1].split(" point(s)")[0]
            roll1 = int(roll)
        if roll2 == 0 and ircmsg.find(f":BanchoBot!cho@ppy.sh PRIVMSG #mp_{channel} :{player2} rolls") != -1: ### Gets player2's roll
            roll = ircmsg.split(f"rolls ")[-1].split(" point(s)")[0]
            roll2 = int(roll)
        if roll1 != 0 and roll2 !=0 and sentrolls == False: ### Informs the players who won the roll
            if roll1 > roll2:
                sendmsg(f"{player1} wins the roll")
                sentrolls = True
            if roll2 > roll1:
                sendmsg(f"{player2} wind the roll")
                sentrolls = True
            if roll1 == roll2:
                sendmsg("Draw! Please roll again")
                roll1 = 0
                roll2 = 0

def receiver_4v4():
    player1team1 = input("player1team1: ")
    player2team1 = input("player2team1: ")
    player3team1 = input("player2team1: ")
    player4team1 = input("player2team1: ")
    player1team2 = input("player1team2: ")
    player2team2 = input("player2team2: ")
    player3team2 = input("player2team2: ")
    player4team2 = input("player2team2: ")
    captainteam1 = input("captainteam1: ")
    captainteam2 = input("captainteam2: ")
    roll1 = 0
    roll2 = 0
    sentrolls = False
    rollsreminder = False
    nextpick = "null"
    score1 = 0
    score2 = 0
    while True:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        if ircmsg.find("PING") != -1: ### Reacts to pings
            pingcontent = ircmsg.split('PING')[1]
            pingresponder(pingcontent)
        if ircmsg.find("PRIVMSG") != -1:
            name = ircmsg.split('PRIVMSG',1)[0].split(':')[-1][:-12]
            content = ircmsg.split('PRIVMSG',1)[1].split(':', 1)[1].split("\n")[0]
            message = (f"{name}: {content}")
            print(message)
        if rollsreminder == False:
            sendmsg("Waiting for the captains to roll using the !roll command")
            rollsreminder = True
        if roll1 == 0 and ircmsg.find(f":BanchoBot!cho@ppy.sh PRIVMSG #mp_{channel} :{captainteam1} rolls") != -1: ### Gets player1's roll
            roll = ircmsg.split(f"rolls ")[-1].split(" point(s)")[0]
            roll1 = int(roll)
        if roll2 == 0 and ircmsg.find(f":BanchoBot!cho@ppy.sh PRIVMSG #mp_{channel} :{captainteam2} rolls") != -1: ### Gets player2's roll
            roll = ircmsg.split(f"rolls ")[-1].split(" point(s)")[0]
            roll2 = int(roll)
        if roll1 != 0 and roll2 !=0 and sentrolls == False: ### Informs the players who won the roll
            if roll1 > roll2:
                sendmsg(f"{captainteam1} wins the roll")
                sentrolls = True
            if roll2 > roll1:
                sendmsg(f"{captainteam2} wins the roll")
                sentrolls = True
            if roll1 == roll2:
                sendmsg("Draw! Please roll again")
                roll1 = 0
                roll2 = 0

 
match_types = {"1v1": receiver_1v1, "4v4": receiver_4v4}
 
connect(name, password)
joinlobby(channel)
match_types[match_type]()