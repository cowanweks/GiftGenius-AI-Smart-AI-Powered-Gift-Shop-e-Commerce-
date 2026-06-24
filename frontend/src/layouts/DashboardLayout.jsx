import { NavLink, Outlet } from 'react-router-dom'
import { FaUser, FaBoxOpen, FaHeart, FaBell } from 'react-icons/fa'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

const LINKS = [
  { to: '/dashboard', label: 'Profile', icon: <FaUser />, end: true },
  { to: '/dashboard/orders', label: 'Order History', icon: <FaBoxOpen /> },
  { to: '/dashboard/wishlist', label: 'Wishlist', icon: <FaHeart /> },
  { to: '/dashboard/reminders', label: 'Reminders', icon: <FaBell /> },
]

export default function DashboardLayout() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 grid grid-cols-1 md:grid-cols-[220px_1fr] gap-8">
        <aside className="bg-white rounded-2xl border border-purple-50 shadow-sm p-4 h-fit">
          <nav className="flex flex-col gap-1">
            {LINKS.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                end={link.end}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-colors ${
                    isActive ? 'bg-purple-100 text-brand-purple-dark' : 'text-gray-600 hover:bg-purple-50'
                  }`
                }
              >
                {link.icon}
                {link.label}
              </NavLink>
            ))}
          </nav>
        </aside>
        <section>
          <Outlet />
        </section>
      </main>
      <Footer />
    </div>
  )
}
