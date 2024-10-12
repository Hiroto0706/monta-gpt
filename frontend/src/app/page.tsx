"use client";

import axios from "axios";
import { useEffect, useState } from "react";
import { User } from "@/types/users";

export default function Home() {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await axios.get("http://monta-gpt.com/api/users/1");
        setUser(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchUser();
  }, []);

  return (
    <>
      <p>Hello From Next.js Application</p>
      {user != null && (
        <p>
          <span>USER ID: {user.id}</span>
          <span>USER NAME: {user.name}</span>
          <span>USER EMAIL: {user.email}</span>
        </p>
      )}
    </>
  );
}
