# Commands

# Server to Client

---

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

# Client to Server