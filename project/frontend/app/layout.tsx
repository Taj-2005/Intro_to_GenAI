import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Fake Job Posting Detector',
  description: 'AI-powered system to detect fake job postings',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
