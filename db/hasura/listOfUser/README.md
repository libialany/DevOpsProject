## Hasura
Hasura is an open-source GraphQL engine that simplifies the process of building robust, scalable, and secure applications by providing an instant GraphQL API on top of new or existing databases. It supports various databases such as PostgreSQL, SQL Server, MySQL, and Oracle.

## Key Features

- Instant Real-time GraphQL: Automatically generates a real-time GraphQL API from a database schema without requiring backend code.
- Extensibility: Allows integration of custom business logic through Actions, Remote Schemas, and Event Triggers.

## Architecture

Hasura's architecture enables developers to create a unified GraphQL API over existing databases and REST APIs. It supports Apollo Federation for composing unified APIs from multiple data sources.

## Hands-On

I created a simple user application (CRUD application).

### Set up


**Database** In Postgres: 

```
# create table

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

# insert records

INSERT INTO users (name, email)
VALUES 
('John Doe', 'john@example.com'),
('Jane Smith', 'jane@example.com'),
('Mike Brown', 'mike@example.com'),
('Emily Davis', 'emily@example.com'),
('Tom Johnson', 'tom@example.com'),
('Lily White', 'lily@example.com'),
('David Lee', 'david@example.com'),
('Sophia Martin', 'sophia@example.com'),
('Oliver Hall', 'oliver@example.com'),
('Isabella Taylor', 'isabella@example.com');
```
**Aplication**

```
git clone <repository-url>
cd DevOpsProject/db/hasura/listOfUser
npm i
cp .env.EXAMPLE .env
npm run dev
```

## Explanation

GET 

```
query MyQuery {
  users {
    email
    id
    name
  }
}
```

POST

note: for refresh the list. we have to use the function `refetchQueries`.

```
mutation AddUser($objects: [users_insert_input!]!) {
  insert_users(objects: $objects) {
    affected_rows
    returning {
      id
      name
      email
    }
  }
}
```

PUT

```
mutation UpdateUser($id: Int!, $set: users_set_input!) {
  update_users(where: { id: { _eq: $id } }, _set: $set) {
    affected_rows
    returning {
      id
      name
      email
    }
  }
}
```

DELETE

```
mutation DeleteUser($id: Int!) {
    delete_users_by_pk(id: $id) {
      id
    }
  }
```

## Link video

:)
