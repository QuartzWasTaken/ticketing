## Adaptateurs de persistance

### TicketRepository

**Implementations disponibles** :
- `InMemoryTicketRepository` : stockage en memoire (tests)
- `SQLiteTicketRepository` : stockage SQLite (persistance)

**Interchangeabilite** : les use cases utilisent uniquement le port `TicketRepository`.
Le choix de l'implementation se fait a l'instanciation (injection de dependances).
