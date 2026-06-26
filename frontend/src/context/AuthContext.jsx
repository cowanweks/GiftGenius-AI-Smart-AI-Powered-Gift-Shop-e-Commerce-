import { createContext, useContext, useEffect, useState } from 'react'
import * as authService from '../services/authService'
import * as vendorService from '../services/vendorService'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem('user')
    return stored ? JSON.parse(stored) : null
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      setLoading(false)
      return
    }
    authService
      .getProfile()
      .then((profile) => {
        setUser(profile)
        localStorage.setItem('user', JSON.stringify(profile))
      })
      .catch(() => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        setUser(null)
      })
      .finally(() => setLoading(false))
  }, [])

  const persistSession = (data) => {
    localStorage.setItem('access_token', data.access)
    localStorage.setItem('refresh_token', data.refresh)
    localStorage.setItem('user', JSON.stringify(data.user))
    setUser(data.user)
  }

  const login = async (credentials) => {
    const data = await authService.login(credentials)
    persistSession(data)
    return data.user
  }

  const register = async (payload) => {
    const data = await authService.register(payload)
    persistSession(data)
    return data.user
  }

  const registerVendor = async (payload) => {
    const data = await vendorService.registerVendor(payload)
    persistSession(data)
    return data.user
  }

  const logout = async () => {
    await authService.logout()
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    setUser(null)
  }

  const updateUser = (updatedUser) => {
    setUser(updatedUser)
    localStorage.setItem('user', JSON.stringify(updatedUser))
  }

  return (
    <AuthContext.Provider
      value={{
        user, loading, isAuthenticated: !!user, isAdmin: !!user?.is_staff, isVendor: !!user?.is_vendor,
        login, register, registerVendor, logout, updateUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
