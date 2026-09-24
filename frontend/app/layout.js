import "./globals.css";

export const metadata = {
  title: "Agent Research",
  description: "AI multi-agent research reports",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}