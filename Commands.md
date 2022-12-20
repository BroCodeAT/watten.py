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

### PLAYER_TURN
    A Client has to play a card

**Attributes:**
- to: str → Name of the Client to send the Command to
- available: list[int] → The List of the Cards the Player can play

# Client to Server