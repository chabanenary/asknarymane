import ChatWidget from "@/components/ChatWidget";

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-4">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">Ask Narymane</h1>
      <p className="text-gray-500 mb-8 text-center">
        Posez vos questions sur mon parcours professionnel et ma formation
      </p>
      <ChatWidget />
    </main>
  );
}
