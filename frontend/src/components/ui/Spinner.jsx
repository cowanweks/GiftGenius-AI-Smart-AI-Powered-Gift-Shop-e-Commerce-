export default function Spinner({ className = 'w-6 h-6' }) {
  return (
    <span
      className={`inline-block ${className} rounded-full border-2 border-purple-200 border-t-brand-purple animate-spin`}
    />
  )
}
