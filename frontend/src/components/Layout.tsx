"use client";
import React from "react";
import Sidebar from "./Sidebar";
import { Toaster } from "react-hot-toast";

const Layout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="flex">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <div className="flex-1 p-6">
        <Toaster position="top-right" />
        {children}
        </div>
    </div>
  );
};

export default Layout;
