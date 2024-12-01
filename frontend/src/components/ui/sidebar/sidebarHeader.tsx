import Link from "next/link";
import React from "react";

interface Props {
  onClick: (target: string) => void;
}

const SidebarHeader: React.FC<Props> = ({ onClick }) => {
  return (
    <>
      <div>
        <Link
          href="/new"
          className="text-2xl my-4 flex justify-center hover:opacity-70 duration-300"
          onClick={() => onClick("/new")}
        >
          MontaGPT
        </Link>
        <Link
          className="mb-2 px-2 py-1 w-full bg-white border rounded-xl border-gray-300 text-sm block shadow hover:bg-gray-100 duration-300"
          href="/new"
          onClick={() => onClick("/new")}
        >
          New chat
        </Link>
      </div>
    </>
  );
};

export default SidebarHeader;
