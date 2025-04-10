"use client";

import React, { useEffect, useRef } from "react";
import { AlertTriangle } from "lucide-react";
import toast from "react-hot-toast";

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void; // Optional retry function
}

export default function ErrorMessage({ message, onRetry }: ErrorMessageProps) {
  const toastShown = useRef(false); // Track if toast is already shown

  useEffect(() => {
    if (message && !toastShown.current) {
      toast.error(message);
      toastShown.current = true; // Mark toast as shown
    }
  }, [message]);

  if (!message) return null;

  return (
    <div className="flex items-center p-4 bg-red-100 border border-red-400 text-red-700 rounded-md shadow-md">
      <AlertTriangle className="w-5 h-5 mr-2" />
      <span className="flex-1">{message}</span>
      {onRetry && (
        <button
          onClick={() => {
            toastShown.current = false; // Allow retry toast
            onRetry();
          }}
          className="ml-4 px-3 py-1 text-sm font-semibold text-white bg-red-500 rounded hover:bg-red-600 transition"
        >
          Retry
        </button>
      )}
    </div>
  );
}
