"use client";

import { useState } from "react";

interface AuthFormProps {
  mode: "login" | "signup";
  onSubmit: (data: { email: string; password: string; name?: string }) => void;
}

export function AuthForm({ mode, onSubmit }: AuthFormProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit({ email, password, name: mode === "signup" ? name : undefined });
      }}
      className="space-y-4 rounded-xl border border-slate-200 bg-white p-8 shadow-sm"
    >
      <div>
        <label className="mb-2 block text-sm font-medium text-slate-700">Email</label>
        <input
          type="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          className="w-full rounded-lg border border-slate-300 bg-slate-50 px-4 py-3 focus:border-slate-500 focus:outline-none"
          required
        />
      </div>
      {mode === "signup" && (
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">Name</label>
          <input
            type="text"
            value={name}
            onChange={(event) => setName(event.target.value)}
            className="w-full rounded-lg border border-slate-300 bg-slate-50 px-4 py-3 focus:border-slate-500 focus:outline-none"
          />
        </div>
      )}
      <div>
        <label className="mb-2 block text-sm font-medium text-slate-700">Password</label>
        <input
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          className="w-full rounded-lg border border-slate-300 bg-slate-50 px-4 py-3 focus:border-slate-500 focus:outline-none"
          required
        />
      </div>
      <button
        type="submit"
        className="w-full rounded-lg bg-slate-900 px-4 py-3 text-sm font-semibold text-white hover:bg-slate-700"
      >
        {mode === "signup" ? "Create account" : "Sign in"}
      </button>
    </form>
  );
}
