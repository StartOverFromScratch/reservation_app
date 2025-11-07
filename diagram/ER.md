
# 拡張後ER図
``` mermaid
erDiagram
    users ||--o{ reservations : makes
    users ||--o{ categories : manages

    categories ||--o{ equipments : contains
    reservations ||--o{ reservation_items : includes
    equipments ||--o{ reservation_items : part_of

    users {
        int id PK
        string username
        string role
    }

    categories {
        int id PK
        string name
        int manager_user_id FK
    }

    equipments {
        int id PK
        string name
        string location
        string status
        int category_id FK
    }

    reservations {
        int id PK
        string name
        string start_date
        string end_date
        int created_by_user_id FK
    }

    reservation_items {
        int reservation_id FK
        int equipment_id FK
    }
```

# 初期ER図
``` mermaid
erDiagram
    reservations {
        int id PK
        string name
        string equipment
        string start_date
        string end_date
    } 

```
