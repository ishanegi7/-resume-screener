"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { AuthForm } from "@/components/AuthForm";
import { AuthLayout } from "@/components/AuthLayout";
import { apiFetch } from "@/lib/api";

export default function SignInPage() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(data: { email: string; password: string }) {
    setError(null);
    try {
      await apiFetch("/api/auth/login", {
        method: "POST",
        body: JSON.stringify({ username: data.email, password: data.password }),
      });
      router.push("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    }
  }

  return (
    <AuthLayout title="Welcome back" description="Sign in to access resume screening tools.">
      <div className="space-y-4">
        <AuthForm mode="login" onSubmit={handleSubmit} />
        {error ? <p className="text-sm text-red-600">{error}</p> : null}
      </div>
    </AuthLayout>
  );
}
