import React from "react";

const LeftBar = () => {
  return (
    <div className="fixed top-0 left-0 h-full w-16 bg-white shadow-md flex flex-col items-center justify-start py-4 space-y-4 z-20 opacity-0">
      <button className="text-gray-600 hover:text-gray-800">☰</button>
      <button className="text-gray-600 hover:text-gray-800">🔖</button>
      <button className="text-gray-600 hover:text-gray-800">⏳</button>
      <hr className="w-10 border-gray-300" />
      <button className="text-gray-600 hover:text-gray-800">🌄</button>
      <button className="text-gray-600 hover:text-gray-800">🏝️</button>
      <hr className="w-10 border-gray-300" />
      <button className="text-gray-600 hover:text-gray-800">📱</button>
    </div>
  );
};

export default LeftBar;
