"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { AuthForm } from "@/components/AuthForm";
import { AuthLayout } from "@/components/AuthLayout";
import { apiFetch } from "@/lib/api";

export default function SignUpPage() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(data: { email: string; password: string; name?: string }) {
    setError(null);
    try {
      await apiFetch("/api/auth/signup", {
        method: "POST",
        body: JSON.stringify(data),
      });
      router.push("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Signup failed");
    }
  }

  return (
    <AuthLayout title="Create your account" description="Get started with AI-powered resume screening.">
      <div className="space-y-4">
        <AuthForm mode="signup" onSubmit={handleSubmit} />
        {error ? <p className="text-sm text-red-600">{error}</p> : null}
      </div>
    </AuthLayout>
  );
}
