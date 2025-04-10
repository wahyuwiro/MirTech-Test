"use client";
import React, { useState } from "react";

interface FilterProps {
  label?: string;
  options: { label: string; value: string; isDate?: boolean }[];
  onApply: (filter: { field: string; value?: string; startDate?: string; endDate?: string }) => void;
  onReset: () => void;
}

export default function GlobalFilter({
  label = "Filter By",
  options,
  onApply,
  onReset,
}: FilterProps) {
  const [field, setField] = useState(options[0].value);
  const [value, setValue] = useState("");

  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const selectedOption = options.find((opt) => opt.value === field);
  const isDateFilter = selectedOption?.isDate;

  return (
    <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 border p-4 rounded-lg bg-white shadow-md">
      {/* Dropdown for Field Selection */}
      <div className="flex flex-col sm:flex-row sm:items-center w-full sm:w-auto">
        <label className="text-sm font-medium sm:mr-2">{label}</label>
        <select
          value={field}
          onChange={(e) => setField(e.target.value)}
          className="p-2 border rounded-md w-full sm:w-40"
        >
          {options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </div>

      {/* Search Input or Date Fields */}
      {!isDateFilter ? (
        <div className="flex flex-col sm:flex-row sm:items-center flex-grow">
          <label className="text-sm font-medium sm:mr-2">Search</label>
          <input
            type="text"
            value={value}
            onChange={(e) => setValue(e.target.value.trim())}
            className="p-2 border rounded-md w-full"
            placeholder="Type here..."
          />
        </div>
      ) : (
        <div className="flex flex-col sm:flex-row sm:items-center gap-2 flex-grow">
          <div className="flex flex-col sm:flex-row sm:items-center">
            <label className="text-sm font-medium sm:mr-2">Start Date</label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="p-2 border rounded-md"
            />
          </div>
          <div className="flex flex-col sm:flex-row sm:items-center">
            <label className="text-sm font-medium sm:mr-2">End Date</label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="p-2 border rounded-md"
            />
          </div>
        </div>
      )}

      {/* Buttons */}
      <div className="flex gap-2 sm:ml-4">
        <button
          onClick={() =>
            onApply(
              isDateFilter
                ? { field, startDate, endDate }
                : { field, value }
            )
          }
          className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition"
        >
          Apply
        </button>
        <button
          onClick={() => {
            setField(options[0].value);
            setValue("");
            onReset();
            setStartDate("");
            setEndDate("");
          }}
          className="px-4 py-2 bg-gray-300 text-black rounded-md hover:bg-gray-400 transition"
        >
          Reset
        </button>
      </div>
    </div>
  );
}
