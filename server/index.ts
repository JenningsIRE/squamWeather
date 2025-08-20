import express from "express";
import cors from "cors";
import { ApolloServer } from "@apollo/server";
import { expressMiddleware } from "@as-integrations/express4"; 
import bodyParser from "body-parser";

// Mock data
const mockSends = [
  {
    id: "1",
    name: "Alice",
    date: "2025-08-19",
    description: "Climbed a beautiful route today!",
    weather: { tempHigh: 22, tempLow: 14, conditions: "Sunny" },
    avatarUrl: "https://i.pravatar.cc/50?img=1",
  },
];

// GraphQL schema
const typeDefs = `
  type Weather {
    tempHigh: Int
    tempLow: Int
    conditions: String
  }

  type Send {
    id: ID!
    name: String
    date: String
    description: String
    weather: Weather
    avatarUrl: String
  }

  type Query {
    sends: [Send]
  }
`;

const resolvers = {
  Query: {
    sends: () => mockSends,
  },
};

// Create Apollo server
const server = new ApolloServer({ typeDefs, resolvers });

async function startApolloServer() {
  const app = express();
  app.use(cors());
  await server.start();

  // Apply middleware
  app.use("/graphql", bodyParser.json(), expressMiddleware(server));

  app.listen(4000, () => {
    console.log("GraphQL server running at http://localhost:4000/graphql");
  });
}

startApolloServer();
