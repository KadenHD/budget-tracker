// TODO: IMPLEMENT HERE DATA CONSTANTS FROM DATABASE STRUCTURE OF TABLES AND API RETURNS
// TODO: THEN USE THEMS INSIDE THE 'ApplicationShell' COMPONENT
// TODO: HANDLE ROUTING AND CHECKING IF THERE IS A SESSION TO REDIRECT

import { User, Account, Category, Transaction, TransactionType } from '@/lib/types';

// Mock Users
export const mockUsers: User[] = [
  {
    id: "user_1",
    username: "johndoe",
    email: "johndoe@example.com",
    created_at: "2026-03-30T10:00:00Z",
    updated_at: "2026-03-30T10:00:00Z",
  },
  {
    id: "user_2",
    username: "janedoe",
    email: "janedoe@example.com",
    created_at: "2026-03-28T08:30:00Z",
    updated_at: "2026-03-28T08:30:00Z",
  },
];

// Mock Accounts
export const mockAccounts: Account[] = [
  {
    id: "account_1",
    name: "Checking Account",
    user_id: "user_1",
    created_at: "2026-03-25T12:00:00Z",
    updated_at: "2026-03-25T12:00:00Z",
  },
  {
    id: "account_2",
    name: "Savings Account",
    user_id: "user_1",
    created_at: "2026-03-26T14:20:00Z",
    updated_at: "2026-03-26T14:20:00Z",
  },
  {
    id: "account_3",
    name: "Business Account",
    user_id: "user_2",
    created_at: "2026-03-27T09:45:00Z",
    updated_at: "2026-03-27T09:45:00Z",
  },
];

// Mock Categories
export const mockCategories: Category[] = [
  {
    id: "category_1",
    name: "Salary",
    account_id: "account_1",
    created_at: "2026-03-20T09:00:00Z",
    updated_at: "2026-03-20T09:00:00Z",
  },
  {
    id: "category_2",
    name: "Groceries",
    account_id: "account_1",
    created_at: "2026-03-21T11:15:00Z",
    updated_at: "2026-03-21T11:15:00Z",
  },
  {
    id: "category_3",
    name: "Investments",
    account_id: "account_2",
    created_at: "2026-03-22T16:45:00Z",
    updated_at: "2026-03-22T16:45:00Z",
  },
  {
    id: "category_4",
    name: "Office Supplies",
    account_id: "account_3",
    created_at: "2026-03-23T13:00:00Z",
    updated_at: "2026-03-23T13:00:00Z",
  },
];

// Mock Transactions
export const mockTransactions: Transaction[] = [
  {
    id: "transaction_1",
    amount: 5000,
    description: "Monthly salary",
    date: "2026-03-01",
    type: TransactionType.INCOME,
    account_id: "account_1",
    category_id: "category_1",
    created_at: "2026-03-01T09:00:00Z",
    updated_at: "2026-03-01T09:00:00Z",
  },
  {
    id: "transaction_2",
    amount: 120,
    description: "Weekly groceries",
    date: "2026-03-05",
    type: TransactionType.EXPENSE,
    account_id: "account_1",
    category_id: "category_2",
    created_at: "2026-03-05T15:00:00Z",
    updated_at: "2026-03-05T15:00:00Z",
  },
  {
    id: "transaction_3",
    amount: 1000,
    description: "Investment in stocks",
    date: "2026-03-10",
    type: TransactionType.EXPENSE,
    account_id: "account_2",
    category_id: "category_3",
    created_at: "2026-03-10T10:30:00Z",
    updated_at: "2026-03-10T10:30:00Z",
  },
  {
    id: "transaction_4",
    amount: 200,
    description: "Office stationery",
    date: "2026-03-12",
    type: TransactionType.EXPENSE,
    account_id: "account_3",
    category_id: "category_4",
    created_at: "2026-03-12T14:00:00Z",
    updated_at: "2026-03-12T14:00:00Z",
  },
  {
    id: "transaction_5",
    amount: 300,
    description: "Freelance payment",
    date: "2026-03-15",
    type: TransactionType.INCOME,
    account_id: "account_3",
    created_at: "2026-03-15T11:00:00Z",
    updated_at: "2026-03-15T11:00:00Z",
  },
];
