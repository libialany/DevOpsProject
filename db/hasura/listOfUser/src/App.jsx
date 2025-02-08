import { ApolloClient, InMemoryCache, HttpLink } from '@apollo/client';
import { ApolloProvider } from '@apollo/client';
import UserList from './UserList';
const client = new ApolloClient({
  link: new HttpLink({
    uri: import.meta.env.VITE_HASURA_GRAPHQL_ENDPOINT,
    headers: {
      'x-hasura-admin-secret': import.meta.env.VITE_HASURA_ADMIN_SECRET,
    },
  }),
  cache: new InMemoryCache(),
});

function App() {
  return (
    <ApolloProvider client={client}>
      <UserList />
    </ApolloProvider>
  );
}

export default App;
