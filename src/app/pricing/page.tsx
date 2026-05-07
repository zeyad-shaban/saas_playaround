"use client";

import { PricingTable, Show, SignInButton } from "@clerk/nextjs";
import Link from "next/link";

export default function PricingPage() {
  return (
    <main className="min-h-screen bg-linear-to-br from-slate-900 via-slate-800 to-slate-900 p-8 text-slate-100">
      <div className="mx-auto w-full max-w-4xl space-y-6">
        <div className="rounded-2xl border border-slate-700/50 bg-slate-800/60 p-6">
          <h1 className="text-3xl font-bold">Upgrade your plan</h1>
          <p className="mt-2 text-slate-300">
            Free users cannot generate ideas. Choose a paid plan below to unlock this feature.
          </p>
        </div>

        <Show when="signed-out">
          <div className="rounded-2xl border border-slate-700/50 bg-slate-800/60 p-6">
            <p className="mb-4 text-slate-300">Please sign in before subscribing.</p>
            <SignInButton mode="modal">
              <button className="rounded-xl bg-blue-600 px-4 py-2 font-semibold text-white hover:bg-blue-500">
                Sign in with Clerk
              </button>
            </SignInButton>
          </div>
        </Show>

        <Show when="signed-in">
          <div className="rounded-2xl border border-slate-700/50 bg-slate-800/60 p-6">
            <PricingTable />
          </div>
          <div>
            <Link className="text-cyan-300 hover:text-cyan-200" href="/">
              Back to idea generator
            </Link>
          </div>
        </Show>
      </div>
    </main>
  );
}
