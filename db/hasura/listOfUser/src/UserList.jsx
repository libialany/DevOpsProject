import React, { useState } from 'react';
import { useQuery, useMutation, gql } from '@apollo/client';

const GET_USERS = gql`
  query GetUsers {
    users {
      email
      id
      name
    }
  }
`;

const ADD_USER = gql`
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
`;


function UserList() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  const [addUser] = useMutation(ADD_USER, {
    refetchQueries: [{ query: GET_USERS }],
  });

  const { loading, error, data } = useQuery(GET_USERS);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error ...</p>;

  const handleSubmit = async (event) => {

    event.preventDefault();

    try {

      await addUser({
        variables:
        {
          objects:
            [{
              name,
              email,
            }],
        },
      });
      console.log('User added successfully!');
      setName('');
      setEmail('');
    } catch (error) {
      console.error('Error adding user:', error);
    }
  };


  return (
    <div>
      <h1>Add User</h1>
      <form onSubmit={handleSubmit}>
        <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" />
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
        <button type="submit">Add User</button>
      </form>
      <h1>Users</h1>
      <ul>
        {data.users.map(user => (
          <li key={user.id}>
            Name: {user.name}
            <br />
            Email: {user.email}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default UserList;
