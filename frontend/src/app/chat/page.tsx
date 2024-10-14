import axios from "axios";

// TODO: getServerSidePropsを使ってリダイレクト処理を実装する

const fetchUser = async (): Promise<any> => {
  try {
    const response = await axios.get("http://backend:8000/api/messages/4");
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
};

export default async function Chat() {
  const user = await fetchUser();

  return (
    <>
      <p>This is Chat Page</p>
      {user.map((chat) => {
        <>{chat.content}</>;
      })}
    </>
  );
}
