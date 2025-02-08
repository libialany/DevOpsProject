##  User List

### Set up

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



### Run 
```
npm i
cp .env.EXAMPLE .env
npm run dev
```

## explanation

```
GET 
query MyQuery {
  users {
    email
    id
    name
  }
}



### link video

:)