### GraphQL

GraphQL is a query language for APIs and also a server runtime for executing those queries. It lets clients request exactly the data they need, and it can aggregate data from multiple sources.

#### 18.1 GraphQL introduction

GraphQL was developed by Facebook to address the shortcomings of traditional REST APIs. Unlike REST APIs, GraphQL lets clients specify the exact structure of the request, which reduces unnecessary data transfer and allows all the data you need to be fetched in a single request.

##### 18.1.1 Features of GraphQL

- **Declarative data fetching**: the client specifies the data structure it needs, and the server returns the matching data.
- **Fewer network requests**: fetch data from multiple resources in one request.
- **Strongly typed system**: types and relationships of the API are defined by a schema, which keeps the data accurate.
- **Real-time updates**: supports subscriptions, which allow real-time data updates.

##### 18.1.2 GraphQL versus REST

| Feature        | GraphQL                                 | REST                     |
| -------------- | --------------------------------------- | ------------------------ |
| Data fetching  | Client specifies the data it needs      | Server defines the data structure |
| Data transfer  | A single request can fetch data from multiple resources | Each request fetches data for one resource |
| Strongly typed system | Has a strongly typed schema      | No strong type constraints |
| Real-time updates | Supports subscriptions               | Requires extra implementation |
| Versioning     | No versioning needed, the schema evolves | Requires maintaining multiple versions |

#### 18.2 Basic concepts of GraphQL

##### 18.2.1 Query

A query is an operation used to fetch data. The client requests specific data fields through a query, and the server returns the corresponding data.

Example query:
```graphql
query {
  user(id: 1) {
    id
    name
    email
  }
}
```

##### 18.2.2 Mutation

A mutation is an operation used to modify data. The client requests data changes through a mutation, and the server performs the matching operation and returns the result.

Example mutation:
```graphql
mutation {
  createUser(input: { name: "Alice", email: "alice@example.com" }) {
    id
    name
    email
  }
}
```

##### 18.2.3 Subscription

A subscription is an operation used for real-time updates. The client requests real-time data updates through a subscription, and the server pushes updated data whenever the data changes.

Example subscription:
```graphql
subscription {
  userCreated {
    id
    name
    email
  }
}
```

##### 18.2.4 Type system

GraphQL has a strongly typed system, with types and relationships of the API defined by a schema. Common types include scalars, object types, enum types, and input types.

Example schema definition:
```graphql
type User {
  id: ID!
  name: String!
  email: String!
}

type Query {
  user(id: ID!): User
}

type Mutation {
  createUser(input: CreateUserInput!): User
}

input CreateUserInput {
  name: String!
  email: String!
}
```

#### 18.3 Using GraphQL in Go

##### 18.3.1 Installing GraphQL libraries

To use GraphQL in Go, you need to install the relevant libraries. Common GraphQL libraries include `graphql-go` and `gqlgen`.

Using the `gqlgen` library:
```bash
go get github.com/99designs/gqlgen
```

##### 18.3.2 Defining a GraphQL schema

Define a GraphQL schema file (schema.graphql):
```graphql
type User {
  id: ID!
  name: String!
  email: String!
}

type Query {
  user(id: ID!): User
}

type Mutation {
  createUser(input: CreateUserInput!): User
}

input CreateUserInput {
  name: String!
  email: String!
}
```

##### 18.3.3 Generating Go code

Use `gqlgen` to generate the corresponding Go code:
```bash
go run github.com/99designs/gqlgen init
```

##### 18.3.4 Implementing Resolvers

`gqlgen` generates a Resolver skeleton in `graph/resolver.go`; fill in the business logic there:
```go
type Resolver struct{}

func (r *Resolver) Query() QueryResolver {
    return &queryResolver{r}
}

func (r *Resolver) Mutation() MutationResolver {
    return &mutationResolver{r}
}

type queryResolver struct{ *Resolver }

func (r *queryResolver) User(ctx context.Context, id string) (*model.User, error) {
    // fetch the user record by ID
    return &model.User{ID: id, Name: "Alice"}, nil
}

type mutationResolver struct{ *Resolver }

func (r *mutationResolver) CreateUser(ctx context.Context, input model.CreateUserInput) (*model.User, error) {
    // create the user record
    return &model.User{ID: "1", Name: input.Name, Email: input.Email}, nil
}
```

##### 18.3.5 Starting a GraphQL server

Start the GraphQL server in main.go (in current `gqlgen`, the handler lives in `graphql/handler`, the Playground in `graphql/playground`, and the generated code is in the `graph` package):
```go
package main

import (
    "log"
    "net/http"

    "github.com/99designs/gqlgen/graphql/handler"
    "github.com/99designs/gqlgen/graphql/playground"
    "github.com/myapp/graph"
)

func main() {
    srv := handler.NewDefaultServer(graph.NewExecutableSchema(graph.Config{Resolvers: &graph.Resolver{}}))

    http.Handle("/", playground.Handler("GraphQL playground", "/query"))
    http.Handle("/query", srv)

    log.Println("Server is running on http://localhost:8080/")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
```

#### 18.4 Advanced features of GraphQL

##### 18.4.1 Batching

GraphQL supports batching, which uses techniques such as DataLoader to reduce repeated network requests and improve performance.

##### 18.4.2 Pagination

GraphQL offers several pagination approaches, such as offset-based and cursor-based pagination, making it easy for clients to fetch large data sets.

Example pagination query:
```graphql
query {
  users(first: 10, after: "cursor") {
    edges {
      node {
        id
        name
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
```

##### 18.4.3 Directives

GraphQL directives add metadata or trigger specific behavior in a query or schema. Common directives include `@include` and `@skip`.

Example directive (`@include` depends on a variable, which must be declared in the query first):
```graphql
query ($includeEmail: Boolean!) {
  user(id: 1) {
    id
    name
    email @include(if: $includeEmail)
  }
}
```

##### 18.4.4 Custom scalar types

GraphQL allows you to define custom scalar types such as dates and times, to cover types that the built-in scalars do not support.

Example custom scalar type:
```graphql
scalar DateTime

type User {
  id: ID!
  name: String!
  createdAt: DateTime!
}
```

The core of GraphQL is three operations — query, mutation, and subscription — plus one type system. On the Go side you use `gqlgen` to generate code from the schema and then add the business logic in the Resolvers.

## References

- [Official · Database Access Guide](https://go.dev/doc/database/)
- [Go Official Documentation · Accessing a relational database (external link)](https://go.dev/doc/tutorial/database-access)
- [database/sql standard library](https://pkg.go.dev/database/sql)
- [GraphQL Official · Learn](https://graphql.org/learn/)

## Sibling pages

- [Availability](/db/Availability.md)
- [Base](/db/Base.md)
- [ConnectPool](/db/ConnectPool.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Availability](/db/Availability.md)
- [Base](/db/Base.md)
- [ConnectPool](/db/ConnectPool.md)
- [Install](/db/Install.md)
