/** @jsxImportSource @emotion/react */
import React from "react";
import { css } from "@emotion/react";

// Dynamically import all PNGs from assets folder
const importAllImages = (r: ReturnType<typeof require.context>) => r.keys().map(r);
const images: string[] = importAllImages(require.context("../assets", false, /\.png$/));

// Individual image card
const imageCard = {
  width: "100%",
  borderRadius: "12px",
  overflow: "hidden" as "hidden",
  boxShadow: "0 2px 5px rgba(0,0,0,0.08)",
};

// Columns
const columnStyle = {
  flex: "0 0 calc(30%)", // fixed width for each column
  display: "flex",
  flexDirection: "column" as "column",
  gap: "12px",
};

// Container
const containerStyle = {
  display: "flex",
  justifyContent: "center", // center the columns horizontally
  gap: "12px",
  width: "100%",
  padding: "16px",
};

export default function ImageMasonry() {
  // Create three columns arrays
  const columns: string[][] = [[], [], []];

  images.forEach((img, index) => {
    const colIndex = index % 3;
    columns[colIndex].push(img);
  });

  return (
    <div style={containerStyle}>
      {columns.map((colImages, colIdx) => (
        <div key={colIdx} style={columnStyle}>
          {colImages.map((img, i) => (
            <img key={i} src={img} alt={`asset-${i}`} style={imageCard} />
          ))}
        </div>
      ))}
    </div>
  );
}
