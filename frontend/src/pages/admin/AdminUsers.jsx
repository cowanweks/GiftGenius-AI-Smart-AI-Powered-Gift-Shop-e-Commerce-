import { useEffect, useState } from 'react'
import * as authService from '../../services/authService'
import Spinner from '../../components/ui/Spinner'

export default function AdminUsers() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    authService.getAllUsers().then((data) => setUsers(data.results ?? data)).finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="flex justify-center py-16">
        <Spinner className="w-8 h-8" />
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-2xl font-display font-bold text-gray-900 mb-6">Users</h1>
      <div className="bg-white rounded-2xl border border-purple-50 shadow-sm overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-purple-50/60 text-gray-500 text-left">
            <tr>
              <th className="px-4 py-3">Username</th>
              <th className="px-4 py-3">Email</th>
              <th className="px-4 py-3">Name</th>
              <th className="px-4 py-3">Role</th>
              <th className="px-4 py-3">Joined</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id} className="border-t border-purple-50">
                <td className="px-4 py-3 font-medium text-gray-800">{user.username}</td>
                <td className="px-4 py-3 text-gray-600">{user.email}</td>
                <td className="px-4 py-3 text-gray-600">{user.first_name} {user.last_name}</td>
                <td className="px-4 py-3">
                  <span className={`text-xs font-semibold px-3 py-1 rounded-full ${user.is_staff ? 'bg-purple-100 text-brand-purple-dark' : 'bg-gray-100 text-gray-600'}`}>
                    {user.is_staff ? 'Admin' : 'Customer'}
                  </span>
                </td>
                <td className="px-4 py-3 text-gray-500 text-xs">{new Date(user.date_joined).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
