export interface User {
  id: string;
  username: string;
  email: string;
  created_at: string;
  updated_at: string;
}

export interface Account {
  id: string;
  name: string;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface Category {
  id: string;
  name: string;
  account_id: string;
  created_at: string;
  updated_at: string;
}

export enum TransactionType {
  INCOME = "income",
  EXPENSE = "expense",
}

export interface Transaction {
  id: string;
  amount: number;
  description?: string;
  date: string;
  type: TransactionType;
  account_id: string;
  category_id?: string;
  created_at: string;
  updated_at: string;
}
