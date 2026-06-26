import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function VendorRoute() {
  const { isAuthenticated, isVendor, loading } = useAuth()

  if (loading) return null
  if (!isAuthenticated) return <Navigate to="/login" replace />
  if (!isVendor) return <Navigate to="/dashboard" replace />
  return <Outlet />
}
