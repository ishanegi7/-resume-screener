import Link from "next/link";

interface AuthLayoutProps {
  title: string;
  description: string;
  children: React.ReactNode;
}

export function AuthLayout({ title, description, children }: AuthLayoutProps) {
  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto flex min-h-screen max-w-4xl items-center justify-center px-4 py-16">
        <div className="w-full space-y-8">
          <div className="rounded-3xl border border-slate-200 bg-white p-10 shadow-sm">
            <div className="mb-10 text-center">
              <h1 className="text-3xl font-semibold">{title}</h1>
              <p className="mt-3 text-sm text-slate-500">{description}</p>
            </div>
            {children}
          </div>
          <p className="text-center text-sm text-slate-500">
            Need an account? <Link href="/signup" className="font-semibold text-slate-900">Sign up</Link>
          </p>
        </div>
      </div>
    </main>
  );
}
