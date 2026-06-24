import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { FaMoneyBillWave, FaMobileAlt, FaCheckCircle } from 'react-icons/fa'
import * as orderService from '../services/orderService'
import { useCart } from '../context/CartContext'
import { useAuth } from '../context/AuthContext'

const initialForm = { full_name: '', phone_number: '', address: '', city: '', notes: '', payment_method: 'cod' }

export default function Checkout() {
  const { items, total, clearCart } = useCart()
  const { user } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ ...initialForm, full_name: `${user?.first_name || ''} ${user?.last_name || ''}`.trim() })
  const [loading, setLoading] = useState(false)
  const [placedOrder, setPlacedOrder] = useState(null)

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (items.length === 0) {
      toast.error('Your cart is empty')
      return
    }
    setLoading(true)
    try {
      const order = await orderService.checkout(form)
      setPlacedOrder(order)
      await clearCart()
      toast.success('Order placed successfully!')
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Checkout failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  if (placedOrder) {
    return (
      <div className="max-w-lg mx-auto px-4 py-20 text-center">
        <FaCheckCircle className="text-6xl text-emerald-500 mx-auto mb-5" />
        <h1 className="text-2xl font-display font-bold text-gray-900 mb-2">Order Confirmed!</h1>
        <p className="text-gray-500 mb-6">
          Order #{placedOrder.id} for KSh {Number(placedOrder.total_amount).toLocaleString()} has been placed via{' '}
          {placedOrder.payment_method === 'mpesa' ? 'M-Pesa' : 'Cash on Delivery'}.
        </p>
        <button
          onClick={() => navigate('/dashboard/orders')}
          className="gradient-brand text-white font-semibold px-6 py-3 rounded-full hover:opacity-90 transition-opacity"
        >
          View My Orders
        </button>
      </div>
    )
  }

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <h1 className="text-3xl font-display font-bold text-gray-900 mb-8">Checkout</h1>
      <div className="grid grid-cols-1 lg:grid-cols-[1fr_320px] gap-8">
        <form onSubmit={handleSubmit} className="bg-white rounded-2xl border border-purple-50 shadow-sm p-6 space-y-4">
          <h3 className="font-semibold text-gray-900 mb-2">Shipping Information</h3>
          <input
            name="full_name" required value={form.full_name} onChange={handleChange}
            placeholder="Full name" className="w-full px-4 py-3 rounded-xl bg-purple-50 focus:outline-none"
          />
          <input
            name="phone_number" required value={form.phone_number} onChange={handleChange}
            placeholder="Phone number" className="w-full px-4 py-3 rounded-xl bg-purple-50 focus:outline-none"
          />
          <input
            name="address" required value={form.address} onChange={handleChange}
            placeholder="Delivery address" className="w-full px-4 py-3 rounded-xl bg-purple-50 focus:outline-none"
          />
          <input
            name="city" required value={form.city} onChange={handleChange}
            placeholder="City / Town" className="w-full px-4 py-3 rounded-xl bg-purple-50 focus:outline-none"
          />
          <textarea
            name="notes" value={form.notes} onChange={handleChange}
            placeholder="Delivery notes (optional)" rows={3}
            className="w-full px-4 py-3 rounded-xl bg-purple-50 focus:outline-none resize-none"
          />

          <h3 className="font-semibold text-gray-900 pt-2">Payment Method</h3>
          <div className="grid grid-cols-2 gap-3">
            <label className={`flex items-center gap-3 border rounded-xl px-4 py-3 cursor-pointer ${form.payment_method === 'cod' ? 'border-brand-purple bg-purple-50' : 'border-purple-100'}`}>
              <input type="radio" name="payment_method" value="cod" checked={form.payment_method === 'cod'} onChange={handleChange} className="hidden" />
              <FaMoneyBillWave className="text-brand-purple" />
              <span className="text-sm font-medium">Cash on Delivery</span>
            </label>
            <label className={`flex items-center gap-3 border rounded-xl px-4 py-3 cursor-pointer ${form.payment_method === 'mpesa' ? 'border-brand-purple bg-purple-50' : 'border-purple-100'}`}>
              <input type="radio" name="payment_method" value="mpesa" checked={form.payment_method === 'mpesa'} onChange={handleChange} className="hidden" />
              <FaMobileAlt className="text-emerald-600" />
              <span className="text-sm font-medium">M-Pesa</span>
            </label>
          </div>
          {form.payment_method === 'mpesa' && (
            <p className="text-xs text-gray-500 bg-emerald-50 border border-emerald-100 rounded-xl px-4 py-3">
              You will receive an M-Pesa STK push prompt on your phone to complete payment (placeholder for demo purposes).
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full gradient-brand text-white font-semibold py-3.5 rounded-full hover:opacity-90 transition-opacity disabled:opacity-50 mt-2"
          >
            {loading ? 'Placing order...' : `Place Order - KSh ${total.toLocaleString()}`}
          </button>
        </form>

        <div className="bg-white rounded-2xl border border-purple-50 shadow-sm p-6 h-fit">
          <h3 className="font-semibold text-gray-900 mb-4">Order Summary</h3>
          <div className="space-y-3 max-h-64 overflow-y-auto pr-1">
            {items.map((item) => (
              <div key={item.id} className="flex items-center justify-between text-sm">
                <span className="text-gray-600 line-clamp-1">{item.product.name} x{item.quantity}</span>
                <span className="font-medium text-gray-800">
                  KSh {(Number(item.product.price) * item.quantity).toLocaleString()}
                </span>
              </div>
            ))}
          </div>
          <div className="flex justify-between font-display font-bold text-lg border-t border-purple-50 pt-4 mt-4">
            <span>Total</span>
            <span>KSh {total.toLocaleString()}</span>
          </div>
        </div>
      </div>
    </div>
  )
}
