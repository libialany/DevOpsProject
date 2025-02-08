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


const UPDATE_USER = gql`
  mutation UpdateUser($id: Int!, $name: String, $email: String) {
    update_users(where: { id: { _eq:$id } }, _set:{ name:$name , email:$email }) {
      affected_rows 
      returning{
        id 
        name 
        email  
     }   
   }
}
`;

const DELETE_USER = gql`
  mutation DeleteUser($id: Int!) {
    delete_users_by_pk(id: $id) {
      id
    }
  }
`;



function UserList() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [selectedUserForEditting, setSelectedUserForEditting] = useState({});
  const [deleteUser] = useMutation(DELETE_USER, {
    refetchQueries: [{ query: GET_USERS }],
  });
  const [addUser] = useMutation(ADD_USER, {
    refetchQueries: [{ query: GET_USERS }],
  });
  const [updateUser] = useMutation(UPDATE_USER);
  // useMutation(UPDATE_USER, { refetchQueries: [{ query: GET_USERS }] });

  const { loading, error, data } = useQuery(GET_USERS);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error ...</p>;

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (editingId === null) {
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
    } else {
      try {
        await updateUser({
          variables:
          {
            id: selectedUserForEditting.id,
            name: selectedUserForEditting.name,
            email: selectedUserForEditting.email,
          },
        });
        // console.log(selectedUserForEditting.email, selectedUserForEditting.name, selectedUserForEditting.id);
        console.log('Existing User Updated');
        setName('');
        setEmail('');
        setSelectedUserForEditting({});
        setEditingId(null);
      } catch (error) {
        console.error('Error Updating User:', error);
      }
    }
  };

  const handleDelete = (id) => {
    deleteUser({
      variables: { id: id },
      onCompleted: () => {
        console.log(`User with id ${id} deleted`);
      },
    });
  };
  
  return (
    <div>
      <h1>Add User</h1>
      <form onSubmit={handleSubmit}>
        <input type="text" value={selectedUserForEditting.name || ''} onChange={(e) => setSelectedUserForEditting({ ...selectedUserForEditting, name: e.target.value }) || setName(e.target.value)} placeholder="Name" />
        <input type="email" value={selectedUserForEditting.email || ''} onChange={(e) => setSelectedUserForEditting({ ...selectedUserForEditting, email: e.target.value }) || setEmail(e.target.value)} placeholder="Email" />
        <button type="submit">{editingId ? 'Update' : 'Add'} User</button>
      </form>
      <h1>Users</h1>
      <ul>
        {data.users.map(user => (
          <li key={user.id}>
            Name: {user.name}
            <br />
            Email: {user.email}
            <button onClick={() => {
              setSelectedUserForEditting(user);
              setName(user.name);
              setEmail(user.email);
              setEditingId(user.id);
            }}> Edit </button>
          <button onClick={() => handleDelete(user.id)}>
            Delete
          </button>            
          </li>
        ))}
      </ul>
    </div>
  );
}

export default UserList;
