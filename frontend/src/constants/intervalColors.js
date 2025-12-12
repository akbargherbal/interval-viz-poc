export const INTERVAL_COLORS = {
  blue: { bg: "bg-blue-600", text: "text-white", border: "border-blue-500" },
  green: { bg: "bg-green-600", text: "text-white", border: "border-green-500" },
  yellow: { bg: "bg-yellow-600", text: "text-white", border: "border-yellow-500" },
  red: { bg: "bg-red-600", text: "text-white", border: "border-red-500" },
  purple: { bg: "bg-purple-600", text: "text-white", border: "border-purple-500" },
  pink: { bg: "bg-pink-600", text: "text-white", border: "border-pink-500" },
  indigo: { bg: "bg-indigo-600", text: "text-white", border: "border-indigo-500" },
  amber: { bg: "bg-amber-500", text: "text-black", border: "border-amber-400" },
};

export const getIntervalColor = (color) =>
  INTERVAL_COLORS[color] || {
    bg: "bg-gray-500",
    text: "text-white",
    border: "border-gray-400",
  };
