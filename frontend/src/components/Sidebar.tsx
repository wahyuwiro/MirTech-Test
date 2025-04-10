"use client";
import React, { useState } from "react";
import { Home, Users, CreditCard, Menu, ChevronLeft  } from "lucide-react";
import Link from "next/link";

const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <div className="flex">
      {/* Sidebar */}
      <div
        className={`bg-gray-900 text-white h-screen p-4 transition-all duration-300 ${
          isOpen ? "w-64" : "w-16"
        }`}
      >
        {/* Toggle Button */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="mb-4 text-white focus:outline-none"
        >
          {isOpen ? <ChevronLeft  size={24} /> : <Menu size={24} />}
        </button>

        {/* Menu Items */}
        <nav className="flex flex-col space-y-4">
          <Link href="/products" className="flex items-center space-x-2">
            <CreditCard size={20} />
            {isOpen && <span>Products</span>}
          </Link>
          <Link href="/users" className="flex items-center space-x-2">
            <Users size={20} />
            {isOpen && <span>Users</span>}
          </Link>
          <Link href="/transactions" className="flex items-center space-x-2">
            <Home size={20} />
            {isOpen && <span>Transactions</span>}
          </Link>
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;
