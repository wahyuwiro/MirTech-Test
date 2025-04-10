"use client";
import React, { useEffect, useState, useCallback } from "react";
import axios from "axios";
import dynamic from "next/dynamic";
import GlobalFilter from "@/components/GlobalFilter"; // Import Global Filter Component
import { Loader2 } from "lucide-react"; // Lucide-react spinner icon
import ErrorMessage from "@/components/ErrorMessage";

const DataTable = dynamic(() => import("@/components/DataTable"), { ssr: false });

interface User {
  id: number;
  name: string;
  email: string;
}

const PAGE_SIZES = [10, 20, 50, 100];

export default function UsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(PAGE_SIZES[0]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [isClient, setIsClient] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [filters, setFilters] = useState<{ search?: string; email?: string }>({});

  // Sorting state
  const [sortBy, setSortBy] = useState<string | null>(null);
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");


  // Ensure component only runs on client
  useEffect(() => {
    setIsClient(true);
  }, []);

  const fetchUsers = useCallback(async () => {
    try {
      setLoading(true);
      const skip = (page - 1) * pageSize;
      const params: Record<string, string | number | undefined> = { skip, limit: pageSize };

        // Add filters
        if (filters.search) params.search = filters.search;
        if (filters.email) params.email = filters.email;
        if (sortBy) {
            params.sort_by = sortBy;
            params.sort_order = sortOrder;
        }

      const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/users`, { params });

      setUsers(res.data.items);
      setTotal(res.data.total);
    } catch (err) {
      console.error("Failed to fetch users", err);
      setError("Failed to fetch users");
    } finally {
      setLoading(false);
    }
  }, [page, pageSize, sortBy, sortOrder, filters.search, filters.email]);

  useEffect(() => {
    if (isClient) {
      fetchUsers();
    }
  }, [fetchUsers, isClient]);

  const totalPages = Math.ceil(total / pageSize);

  // Function to handle sorting changes
  const handleSortChange = (columnKey: string) => {
    if (sortBy === columnKey) {
        setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
        setSortBy(columnKey);
        setSortOrder("asc");
    }
  };
      
  if (!isClient) {
    return (
      <div className="flex justify-center items-center h-screen w-full">
        <Loader2 className="w-10 h-10 animate-spin text-gray-500" />
      </div>
    );
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">List of Users</h1>

      {/* Global Filter Component */}
      <GlobalFilter
        options={[
          { label: "Name", value: "search" },
          { label: "Email", value: "email" },
        ]}
        onApply={({ field, value }) => {
            setFilters((prev) => ({ ...prev, [field]: value }));
            setPage(1); // Reset to first page when filters change
          }}
          onReset={() => {
            setFilters({});
            setPage(1);
          }}        
      />

      {/* Page Size Dropdown */}
      <div className="my-4">
        <label className="mr-2">Page Size:</label>
        <select
          value={pageSize}
          onChange={(e) => setPageSize(Number(e.target.value))}
          className="p-2 border rounded"
        >
          {PAGE_SIZES.map((size) => (
            <option key={size} value={size}>
              {size}
            </option>
          ))}
        </select>
      </div>

      {/* DataTable Component */}
      {loading ? (
        <div className="flex justify-center items-center h-screen w-full">
          <Loader2 className="w-10 h-10 animate-spin text-gray-500" />
        </div>
      ) : (
        <DataTable
          data={users}
          columns={[
            { key: "id", label: "ID", align: "center", sortable: true },
            { key: "name", label: "Name", sortable: true },
            { key: "email", label: "Email", sortable: true },
          ]}
          containerHeight={500} // Adjust height as needed
          sortBy={sortBy}
          sortOrder={sortOrder}
          onSortChange={handleSortChange}
        />
      )}
    {/* Pagination Controls */}
    <div className="flex justify-between mt-4">
        <button
          disabled={page <= 1}
          onClick={() => setPage((prev) => Math.max(1, prev - 1))}
          className="px-4 py-2 bg-gray-200 rounded disabled:opacity-50"
        >
          Prev
        </button>
        <span className="self-center">Page {page} of {totalPages}</span>
        <button
          disabled={page >= totalPages}
          onClick={() => setPage((prev) => Math.min(totalPages, prev + 1))}
          className="px-4 py-2 bg-gray-200 rounded disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </div>
  );
}
