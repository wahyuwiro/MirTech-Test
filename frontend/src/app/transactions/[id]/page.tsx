"use client";

import React, { useEffect, useState, useRef } from "react";
import { useParams } from "next/navigation";
import axios from "axios";
import { Loader2 } from "lucide-react";
import ErrorMessage from "@/components/ErrorMessage";

export default function TransactionDetailPage() {
  const { id } = useParams() as { id: string }; // Ensure `id` is a string

  interface Transaction {
    id: string;
    username: string;
    user_id: string;
    created_at: string;
    transactions: {
      id: string;
      product_name: string;
      product_price: number;
      quantity: number;
      total_price: number;
    }[];
  }

  const [transaction, setTransaction] = useState<Transaction | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const fetched = useRef(false); // Prevents duplicate requests

  useEffect(() => {
    if (!id || fetched.current) return;
    fetched.current = true; // Mark request as initiated

    async function fetchTransaction() {
      try {
        setLoading(true);
        const res = await axios.get(`http://localhost:8000/api/v1/orders/${id}`);
        setTransaction(res.data);
      } catch (err) {
        setError("Failed to fetch transaction details");
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    fetchTransaction();
  }, [id]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen w-full">
        <Loader2 className="w-10 h-10 animate-spin text-gray-500" />
      </div>
    );
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  if (!transaction) {
    return <p className="text-center text-gray-500">No transaction details available.</p>;
  }

  return (
    <div className="p-6 bg-white rounded shadow-lg">
      <h1 className="text-2xl font-bold mb-4">Transaction Details</h1>
      <p><strong>Transaction ID:</strong> {transaction.id}</p>
      <p><strong>User:</strong> {transaction.username} (ID: {transaction.user_id})</p>
      <p><strong>Date:</strong> {new Date(transaction.created_at).toLocaleString()}</p>
      
      <h2 className="text-xl font-semibold mt-4">Products</h2>
      <table className="w-full border mt-2">
        <thead>
          <tr className="bg-gray-100">
            <th className="p-2 border">Product</th>
            <th className="p-2 border">Price</th>
            <th className="p-2 border">Quantity</th>
            <th className="p-2 border">Total</th>
          </tr>
        </thead>
        <tbody>
          {transaction.transactions.map((item) => (
            <tr key={item.id} className="border">
              <td className="p-2 border">{item.product_name}</td>
              <td className="p-2 border">${item.product_price.toFixed(2)}</td>
              <td className="p-2 border text-center">{item.quantity}</td>
              <td className="p-2 border">${item.total_price.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
