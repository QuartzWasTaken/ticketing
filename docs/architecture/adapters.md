## Adaptateurs de persistance

### TicketRepository

**Implementations disponibles** :
- `InMemoryTicketRepository` : stockage en memoire (tests)
- `SQLiteTicketRepository` : stockage SQLite (persistance)

**Interchangeabilite** : les use cases utilisent uniquement le port `TicketRepository`.
Le choix de l'implementation se fait a l'instanciation (injection de dependances).

## UserRepository

**Implementations disponibles** :
- `InMemoryUserRepository` : stockage en memoire (tests)
- `SQLiteUserRepository` : stockage SQLite (persistance)

**Methodes specifiques** :
- `find_by_username(username)` : recherche par username
