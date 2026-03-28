import { ApplicationShell } from "@/components/application-shell";

export default function DashboardLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
      <ApplicationShell>
        <main>
          {children}
        </main>
      </ApplicationShell>
    </>
  );
}
