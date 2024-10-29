import { Message } from "@/types/messages";

export const responseMockMessages = (threadId: number) => {
  const mockMessages: Message[] = [
    {
      content: `ユーザーのプロンプトがここに表示されます`,
      is_user: true,
      id: 0,
      session_id: Number(threadId),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
    {
      content: `生成AIからの回答がここに表示される`,
      is_user: false,
      id: 1,
      session_id: Number(threadId),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
    {
      content: "ユーザーのプロンプトがここに表示されます",
      is_user: true,
      id: 2,
      session_id: Number(threadId),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
    {
      content: "生成AIからの回答がここに表示される",
      is_user: false,
      id: 3,
      session_id: Number(threadId),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
    {
      content: "ユーザーのプロンプトがここに表示されます",
      is_user: true,
      id: 4,
      session_id: Number(threadId),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
    {
      content: "生成AIからの回答がここに表示される",
      is_user: false,
      id: 5,
      session_id: Number(threadId),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
    {
      content: "ユーザーのプロンプトがここに表示されます",
      is_user: true,
      id: 6,
      session_id: Number(threadId),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
    {
      content: "生成AIからの回答がここに表示される",
      is_user: false,
      id: 7,
      session_id: Number(threadId),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
    {
      content: "ユーザーのプロンプトがここに表示されます",
      is_user: true,
      id: 8,
      session_id: Number(threadId),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
    {
      content: "生成AIからの回答がここに表示される",
      is_user: false,
      id: 9,
      session_id: Number(threadId),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
    {
      content: "ユーザーのプロンプトがここに表示されます",
      is_user: true,
      id: 10,
      session_id: Number(threadId),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
    {
      content:
        "生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される",
      is_user: false,
      id: 11,
      session_id: Number(threadId),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
  ];

  return mockMessages;
};
