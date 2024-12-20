import React from "react";

const GeneratingMessage: React.FC = () => {
  return (
    <>
      <p>generating...</p>
      <div className="flex flex-col space-y-2 w-full my-2">
        <div className="h-1 rounded-xl bg-gray-300 w-full animate-loading-bar1"></div>
        <div className="h-1 rounded-xl bg-gray-300 w-full animate-loading-bar2"></div>
        <div className="h-1 rounded-xl bg-gray-300 w-full animate-loading-bar3"></div>
      </div>
    </>
  );
};

export default GeneratingMessage;
