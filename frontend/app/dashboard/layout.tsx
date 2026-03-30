import { ApplicationShell } from "@/components/application-shell";
import { mockUser } from "@/lib/mocks";
import { redirect } from "next/navigation";

export default function DashboardLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {

  if (!mockUser) redirect('/')

  return (
    <>
      <ApplicationShell user={mockUser}>
        <main>
          {children}
        </main>
      </ApplicationShell>
    </>
  );
}
