export default function ProductCardSkeleton() {
  return (
    <div className="bg-white rounded-2xl shadow-sm border border-purple-50 overflow-hidden">
      <div className="skeleton aspect-square" />
      <div className="p-4 space-y-2">
        <div className="skeleton h-3 w-1/3 rounded" />
        <div className="skeleton h-4 w-3/4 rounded" />
        <div className="skeleton h-3 w-1/2 rounded" />
        <div className="flex items-center justify-between mt-3">
          <div className="skeleton h-5 w-16 rounded" />
          <div className="skeleton h-9 w-9 rounded-full" />
        </div>
      </div>
    </div>
  )
}
