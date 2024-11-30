export interface User {
  id: number;
  name: string;
  email: string;
}

// ---

export type UserID = number;
type Name = string;
type Email = string;

interface BaseUser {
  id: UserID;
  name: string;
  email: string;
}