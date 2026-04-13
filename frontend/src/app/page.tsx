import ChatWidget from "@/components/ChatWidget";

export default function Home() {
  return (
    <main className="flex flex-col h-screen bg-gradient-to-b from-slate-50 to-slate-100">
      <ChatWidget />
    </main>
  );
}
