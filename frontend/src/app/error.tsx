"use client";

import { useEffect } from "react";

const Error = ({ error }: { error: Error & { digest?: string } }) => {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => console.log("hello world. hogehoge.")}>
        Try again
      </button>
    </div>
  );
};

export default Error;
