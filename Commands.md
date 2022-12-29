# Commands

# Server to Client

---

### CONNECTION
    The Client is Connected Sucessfully
**Attributes:**
- to: str → Name of the Client to send the Command to
- name: str → The Name of the Client that is now connected

### CONNECTION_REFUSE
    There is already a Client connected with the given name


### NEW_CARD
    The Client Receives new Cards
**Attributes:**
- to: str → Name of the Client to send the Command to
- cards: list[int] → The ID of the Cards you get

### PLAYER_NAMES
    The Client receives the Names of the other Clients (Client is first)

**Attributes:**
- to: str → Name of the Client to send the Command to
- players: list[str] → The List of the Names of the Players (to is first)

### HIGHEST
    The players that chose the highest card will get the ID of the highest one

**Attributes:**
- to: str → Name of the Client to send the Command to
- highest: int → The ID of the highest card

### PLAYER_TURN
    A Client has to play a card

**Attributes:**
- to: str → Name of the Client to send the Command to
- available: list[int] → The List of the Card_ids the Player can play

### UPDATE_TURN
    Send an update to the clients (something changed)

**Attributes:**
- to: str → Name of the Client to send the Command to
- played: list[int] → The cards that have been played already

# Client to Server

### PLAY_CARD
    The client sents the card to play to the server

**Attributes:**
- from: str → The Name of the Client the message comes from
- card: int → The Card the Client wants to play