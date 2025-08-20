/** @jsxImportSource @emotion/react */
import React from "react";
import SendageFeed from "./components/SendageFeed";
import { css } from "@emotion/react";
import { ApolloProvider } from "@apollo/client";
import client from "./apolloClient"; // if separated
import SendsCard from "./components/SendsCard";

const appStyles = {
  backgroundColor: "#f0f2f5",
  minHeight: "100vh",
  fontFamily: "system-ui, sans-serif",
};

const headerStyles = {
  backgroundColor: "#fff",
  padding: "16px 24px",
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
  position: "sticky" as "sticky",
  top: 0,
  zIndex: 10,
};

const navButton = {
  color: "#4b4f56",
  fontWeight: 600,
  marginLeft: "12px",
  background: "none",
  border: "none",
  cursor: "pointer",
  ":hover": {
    color: "#1877f2",
  },
};

const mainStyles = {
  margin: "0 16px",
  padding: "16px",
};

export default function App() {
  return (
    <div css={appStyles}>
      <header css={headerStyles}>
        <h1 style={{ color: "#1877f2", fontWeight: "bold" }}>Squamish Send Data</h1>
        <nav>
          <button css={navButton}>Home</button>
          <button css={navButton}>Settings</button>
        </nav>
      </header>

      <main css={mainStyles}>
        <SendageFeed />
        <ApolloProvider client={client}>
          <SendsCard />
        </ApolloProvider>
      </main>
    </div>
  );
}
