import { useRouter } from "next/navigation";

const LogOutButton = () => {
  const router = useRouter();
  const logoutHandler = () => {
    router.push("/");
  };

  return (
    <div
      className="mt-4 py-1 px-4 bg-gray-600 border-2 border-gray-600 rounded-xl text-white hover:bg-white hover:text-gray-600 duration-300 cursor-pointer text-center font-bold"
      onClick={logoutHandler}
    >
      Log Out
    </div>
  );
};

export default LogOutButton;
