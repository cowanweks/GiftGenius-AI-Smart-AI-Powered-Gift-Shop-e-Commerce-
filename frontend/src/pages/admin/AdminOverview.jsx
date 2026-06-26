import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { FaShoppingBag, FaMoneyBillWave, FaUsers, FaBoxOpen, FaExclamationTriangle, FaStore, FaClock } from 'react-icons/fa'
import * as productService from '../../services/productService'
import Spinner from '../../components/ui/Spinner'

const StatCard = ({ icon, label, value, accent }) => (
  <div className="bg-white rounded-2xl border border-purple-50 shadow-sm p-5 flex items-center gap-4">
    <span className={`w-12 h-12 rounded-xl flex items-center justify-center text-white text-lg ${accent}`}>{icon}</span>
    <div>
      <p className="text-2xl font-display font-bold text-gray-900">{value}</p>
      <p className="text-sm text-gray-500">{label}</p>
    </div>
  </div>
)

export default function AdminOverview() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  useEffect(() => {
    productService.getSalesStats().then(setStats).catch(() => setError(true)).finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="flex justify-center py-16">
        <Spinner className="w-8 h-8" />
      </div>
    )
  }

  if (error || !stats) {
    return <p className="text-red-500">Could not load sales overview. Please refresh the page.</p>
  }

  return (
    <div>
      <h1 className="text-2xl font-display font-bold text-gray-900 mb-6">Sales Overview</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
        <StatCard icon={<FaShoppingBag />} label="Total Orders" value={stats.total_orders} accent="bg-brand-purple" />
        <StatCard icon={<FaMoneyBillWave />} label="Total Revenue" value={`KSh ${Number(stats.total_revenue).toLocaleString()}`} accent="bg-emerald-500" />
        <StatCard icon={<FaUsers />} label="Total Users" value={stats.total_users} accent="bg-brand-pink" />
        <StatCard icon={<FaBoxOpen />} label="Total Products" value={stats.total_products} accent="bg-amber-500" />
      </div>

      {stats.low_stock_products > 0 && (
        <div className="flex items-center gap-3 bg-amber-50 border border-amber-200 text-amber-700 rounded-2xl p-4 mb-4">
          <FaExclamationTriangle />
          <span className="text-sm font-medium">{stats.low_stock_products} product(s) are running low on stock (5 or fewer left).</span>
        </div>
      )}

      {(stats.pending_companies > 0 || stats.pending_vendor_products > 0) && (
        <div className="flex flex-col sm:flex-row sm:items-center gap-3 bg-purple-50 border border-purple-200 text-brand-purple-dark rounded-2xl p-4 mb-8">
          <FaStore className="shrink-0" />
          <span className="text-sm font-medium flex-1">
            {stats.pending_companies > 0 && `${stats.pending_companies} vendor compan${stats.pending_companies === 1 ? 'y' : 'ies'} awaiting approval. `}
            {stats.pending_vendor_products > 0 && `${stats.pending_vendor_products} product listing(s) awaiting review.`}
          </span>
          <div className="flex gap-2">
            {stats.pending_companies > 0 && (
              <Link to="/admin/vendors" className="flex items-center gap-1.5 text-xs font-semibold bg-white px-3 py-1.5 rounded-full border border-purple-200">
                <FaStore /> Review Vendors
              </Link>
            )}
            {stats.pending_vendor_products > 0 && (
              <Link to="/admin/products" className="flex items-center gap-1.5 text-xs font-semibold bg-white px-3 py-1.5 rounded-full border border-purple-200">
                <FaClock /> Review Products
              </Link>
            )}
          </div>
        </div>
      )}

      <div className="bg-white rounded-2xl border border-purple-50 shadow-sm p-6">
        <h3 className="font-semibold text-gray-900 mb-4">Best Sellers</h3>
        {stats.best_sellers.length === 0 ? (
          <p className="text-sm text-gray-500">No sales data yet.</p>
        ) : (
          <ul className="space-y-3">
            {stats.best_sellers.map((item, i) => (
              <li key={i} className="flex items-center justify-between text-sm">
                <span className="text-gray-700">{item.product__name}</span>
                <span className="font-semibold text-brand-purple-dark">{item.units_sold} sold</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}
