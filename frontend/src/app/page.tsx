import axios from "axios";
import { User } from "@/types/users";

const fetchUser = async (): Promise<User | null> => {
  try {
    const response = await axios.get("http://backend:8000/api/users/1");
    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
};

export default async function Home() {
  const user = await fetchUser();

  return (
    <>
      <p>Hello From Next.js Application</p>
      <p>
        {user != null && (
          <>
            <span>USER ID: {user.id}</span>
            <span>USER NAME: {user.name}</span>
            <span>USER EMAIL: {user.email}</span>
          </>
        )}
      </p>
    </>
  );
}
