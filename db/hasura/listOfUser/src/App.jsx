import { ApolloClient, InMemoryCache, HttpLink } from '@apollo/client';
import { ApolloProvider } from '@apollo/client';
import UserDirectory from './components/UserDirectory';
import Hero from './components/Header';
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
    <div className="wrapper">
      <ApolloProvider client={client}>
        <Hero />
        <UserDirectory />
      </ApolloProvider>
    </div>
  );
}

export default App;
