/** @jsxImportSource @emotion/react */
import React from "react";
import { ApolloClient, InMemoryCache, ApolloProvider, gql, useQuery } from "@apollo/client";

const client = new ApolloClient({
  uri: "http://localhost:4000/graphql",
  cache: new InMemoryCache(),
});

const GET_SENDS = gql`
  query GetSends {
    sends {
      id
      name
      date
      description
      weather {
        tempHigh
        tempLow
        conditions
      }
      avatarUrl
    }
  }
`;

export default function SendsCard() {
  const { loading, error, data } = useQuery(GET_SENDS);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "16px", padding: "16px" }}>
      {data.sends.map((send: any) => (
        <div key={send.id} style={{
          backgroundColor: "#fff",
          padding: "16px",
          borderRadius: "12px",
          boxShadow: "0 2px 5px rgba(0,0,0,0.08)"
        }}>
          <div style={{ display: "flex", alignItems: "center", marginBottom: "8px" }}>
            <img src={send.avatarUrl} alt={send.name} style={{ width: "40px", height: "40px", borderRadius: "50%", marginRight: "12px" }} />
            <div>
              <p style={{ fontWeight: 600 }}>{send.name}</p>
              <p style={{ fontSize: "0.875rem", color: "#65676b" }}>{send.date}</p>
            </div>
          </div>
          <p>{send.description}</p>
          <div style={{ display: "flex", gap: "8px", marginTop: "8px" }}>
            <span style={{ backgroundColor: "#e7f3ff", padding: "4px 8px", borderRadius: "6px", color: "#1877f2" }}>High: {send.weather.tempHigh}°C</span>
            <span style={{ backgroundColor: "#e7f3ff", padding: "4px 8px", borderRadius: "6px", color: "#1877f2" }}>Low: {send.weather.tempLow}°C</span>
            <span style={{ backgroundColor: "#e7f3ff", padding: "4px 8px", borderRadius: "6px", color: "#1877f2" }}>{send.weather.conditions}</span>
          </div>
        </div>
      ))}
    </div>
  );
}
