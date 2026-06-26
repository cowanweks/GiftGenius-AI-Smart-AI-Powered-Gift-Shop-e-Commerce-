import { useEffect, useState } from 'react'
import toast from 'react-hot-toast'
import { FaCheck, FaTimes } from 'react-icons/fa'
import * as vendorService from '../../services/vendorService'
import Spinner from '../../components/ui/Spinner'

const STATUS_STYLES = {
  pending: 'bg-amber-100 text-amber-700',
  approved: 'bg-emerald-100 text-emerald-700',
  rejected: 'bg-red-100 text-red-700',
}

export default function AdminVendors() {
  const [companies, setCompanies] = useState([])
  const [loading, setLoading] = useState(true)

  const loadCompanies = () => vendorService.adminListCompanies().then(setCompanies)

  useEffect(() => {
    loadCompanies().finally(() => setLoading(false))
  }, [])

  const handleStatusChange = async (company, status) => {
    try {
      await vendorService.adminUpdateCompanyStatus(company.id, status)
      toast.success(`${company.name} ${status}`)
      loadCompanies()
    } catch {
      toast.error('Could not update company status')
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center py-16">
        <Spinner className="w-8 h-8" />
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-2xl font-display font-bold text-gray-900 mb-6">Vendor Companies</h1>
      {companies.length === 0 ? (
        <p className="text-gray-500">No companies have registered yet.</p>
      ) : (
        <div className="bg-white rounded-2xl border border-purple-50 shadow-sm overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-purple-50/60 text-gray-500 text-left">
              <tr>
                <th className="px-4 py-3">Company</th>
                <th className="px-4 py-3">Account</th>
                <th className="px-4 py-3">Contact</th>
                <th className="px-4 py-3">Products</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              {companies.map((company) => (
                <tr key={company.id} className="border-t border-purple-50">
                  <td className="px-4 py-3 font-medium text-gray-800">{company.name}</td>
                  <td className="px-4 py-3 text-gray-600">{company.username}</td>
                  <td className="px-4 py-3 text-gray-600">
                    <div>{company.contact_email}</div>
                    <div className="text-xs text-gray-400">{company.contact_phone}</div>
                  </td>
                  <td className="px-4 py-3 text-gray-600">{company.product_count}</td>
                  <td className="px-4 py-3">
                    <span className={`text-xs font-semibold px-3 py-1 rounded-full capitalize ${STATUS_STYLES[company.status]}`}>
                      {company.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-right space-x-2">
                    {company.status !== 'approved' && (
                      <button
                        onClick={() => handleStatusChange(company, 'approved')}
                        className="inline-flex items-center gap-1 text-xs font-semibold text-emerald-600 hover:text-emerald-700 px-2 py-1"
                      >
                        <FaCheck /> Approve
                      </button>
                    )}
                    {company.status !== 'rejected' && (
                      <button
                        onClick={() => handleStatusChange(company, 'rejected')}
                        className="inline-flex items-center gap-1 text-xs font-semibold text-red-500 hover:text-red-600 px-2 py-1"
                      >
                        <FaTimes /> Reject
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
