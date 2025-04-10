"use client";
import React, { useRef, useState } from "react";
import { useVirtualizer } from "@tanstack/react-virtual";
import { ArrowUp, ArrowDown } from "lucide-react"; // For sorting icons

interface Column<T> {
    key: string;
    label: string;
    align?: "left" | "center" | "right";
    render?: (value: unknown, row: T) => React.ReactNode;
    sortable?: boolean;
  }
  
  interface DataTableProps<T> {
    data: T[];
    columns: Column<T>[];
    containerHeight?: number;
    sortBy?: string | null;
    sortOrder?: "asc" | "desc";
    onSortChange?: (columnKey: string) => void;
  }
  
  export default function DataTable<T extends { id: number }>({
    data,
    columns,
    containerHeight = 400,
    sortBy,
    sortOrder,
    onSortChange,
  }: DataTableProps<T>) {

  const parentRef = useRef<HTMLDivElement>(null);
  const [sortColumn] = useState<string | null>(null);

  // Sorting logic
  const sortedData = React.useMemo(() => {
    if (!sortColumn) return data;

    return [...data].sort((a, b) => {
      const valueA = a[sortColumn as keyof T];
      const valueB = b[sortColumn as keyof T];

      if (typeof valueA === "number" && typeof valueB === "number") {
        return sortOrder === "asc" ? valueA - valueB : valueB - valueA;
      } else {
        return sortOrder === "asc"
          ? String(valueA).localeCompare(String(valueB))
          : String(valueB).localeCompare(String(valueA));
      }
    });
  }, [data, sortColumn, sortOrder]);

  // Virtualization setup
  const rowVirtualizer = useVirtualizer({
    count: sortedData.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
    overscan: 10,
  });


  return (
    <div className="border rounded-lg overflow-x-auto">
      {/* Header */}
        <div className="min-w-full flex bg-gray-200 font-semibold text-sm">
        {columns.map((col) => (
            <div
            key={col.key}
            className={`p-3 flex-1 cursor-pointer select-none border-r last:border-r-0
            ${col.align === "right" ? "text-right" : col.align === "center" ? "text-center" : "text-left"}`}
            style={{ flexBasis: "20%", flexGrow: 1, minWidth: "100px" }} // ✅ Ensure consistent width
            onClick={() => col.sortable && onSortChange?.(col.key)}
            >
            <div className="flex items-center justify-between">
                {col.label}
                {col.sortable && (
                <span className="ml-1">
                    {sortBy === col.key ? (
                    sortOrder === "asc" ? <ArrowUp size={16} /> : <ArrowDown size={16} />
                    ) : (
                    <ArrowUp size={16} className="opacity-30" />
                    )}
                </span>
                )}
            </div>
            </div>
        ))}
        </div>

        {/* Virtualized Body */}
        <div
        ref={parentRef}
        className="min-w-full relative"
        style={{ height: containerHeight, overflow: "auto" }}
        >
            <div style={{ height: `${rowVirtualizer.getTotalSize()}px`, position: "relative" }}>
                {rowVirtualizer.getVirtualItems().map((virtualRow) => {
                const row = sortedData[virtualRow.index];
                return (
                    <div
                    key={row.id}
                    style={{
                        position: "absolute",
                        top: 0,
                        transform: `translateY(${virtualRow.start}px)`,
                        width: "100%",
                    }}
                    className="flex border-b"
                    >
                    {columns.map((col) => (
                        <div
                        key={col.key}
                        className={`p-3 flex-1 text-sm border-r last:border-r-0
                        ${col.align === "right" ? "text-right" : col.align === "center" ? "text-center" : "text-left"}`}
                        style={{ flexBasis: "20%", flexGrow: 1, minWidth: "100px" }} // ✅ Match header width
                        >
                        {col.render ? col.render(row[col.key as keyof T], row) : (row[col.key as keyof T] as React.ReactNode)}
                        </div>
                    ))}
                    </div>
                );
                })}
            </div>
        </div>

      
    </div>
  );
}
