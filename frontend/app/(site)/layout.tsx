import { Footer } from "@/components/footer";
import { Navbar } from "@/components/navbar";
import { mockUser } from "@/lib/mocks";
import { redirect } from "next/navigation";

export default function SiteLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {

  if (!!mockUser) redirect('/dashboard')

  return (
    <>
      <Navbar />
        <main className="container">
          {children}
        </main>
      <Footer />
    </>
  );
}
