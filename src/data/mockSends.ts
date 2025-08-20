export interface Send {
  name: string;
  date: string;
  description: string;
  weather: {
    tempHigh: number;
    tempLow: number;
    conditions: string;
  };
  avatarUrl?: string;
}

export const mockSends: Send[] = [
  {
    name: "Alex Johnson",
    date: "2025-08-10",
    description: "Sent the classic V5 at Superfly! Feeling pumped!",
    weather: { tempHigh: 22, tempLow: 14, conditions: "Sunny" },
    avatarUrl: "https://i.pravatar.cc/50?img=1",
  },
  {
    name: "Maria Lopez",
    date: "2025-08-09",
    description: "Struggled a bit on the dyno section but made it!",
    weather: { tempHigh: 20, tempLow: 13, conditions: "Cloudy" },
    avatarUrl: "https://i.pravatar.cc/50?img=2",
  },
  {
    name: "Sam Jennings",
    date: "2025-08-08",
    description: "First V6 send! Totally stoked.",
    weather: { tempHigh: 21, tempLow: 12, conditions: "Partly Cloudy" },
    avatarUrl: "https://i.pravatar.cc/50?img=3",
  },
];
