import { createContext, useContext, useEffect, useState } from 'react'
import toast from 'react-hot-toast'
import * as cartService from '../services/cartService'
import { useAuth } from './AuthContext'

const CartContext = createContext(null)
const STORAGE_KEY = 'giftgenius_cart'

function readLocalCart() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || []
  } catch {
    return []
  }
}

function writeLocalCart(items) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(items))
}

export function CartProvider({ children }) {
  const { isAuthenticated } = useAuth()
  const [items, setItems] = useState(readLocalCart)
  const [loading, setLoading] = useState(false)

  // Whenever the guest cart changes, persist it to localStorage.
  useEffect(() => {
    if (!isAuthenticated) writeLocalCart(items)
  }, [items, isAuthenticated])

  // On login, push any locally-held guest items into the backend cart, then
  // treat the backend cart as the single source of truth going forward.
  useEffect(() => {
    if (!isAuthenticated) return
    setLoading(true)
    const guestItems = readLocalCart()
    Promise.all(guestItems.map((item) => cartService.addToCart(item.product.id, item.quantity)))
      .catch(() => {})
      .then(() => {
        writeLocalCart([])
        return cartService.getCart()
      })
      .then((data) => setItems(normalizeBackendItems(data.items)))
      .finally(() => setLoading(false))
  }, [isAuthenticated])

  const normalizeBackendItems = (backendItems) =>
    backendItems.map((i) => ({ id: i.id, product: i.product_detail, quantity: i.quantity }))

  const refreshFromBackend = async () => {
    const data = await cartService.getCart()
    setItems(normalizeBackendItems(data.items))
  }

  const addItem = async (product, quantity = 1) => {
    if (isAuthenticated) {
      await cartService.addToCart(product.id, quantity)
      await refreshFromBackend()
    } else {
      setItems((prev) => {
        const existing = prev.find((i) => i.product.id === product.id)
        if (existing) {
          return prev.map((i) =>
            i.product.id === product.id ? { ...i, quantity: i.quantity + quantity } : i
          )
        }
        return [...prev, { id: `local-${product.id}`, product, quantity }]
      })
    }
    toast.success(`${product.name} added to cart`)
  }

  const updateQuantity = async (itemId, quantity) => {
    if (quantity <= 0) return removeItem(itemId)
    if (isAuthenticated) {
      await cartService.updateCartItem(itemId, quantity)
      await refreshFromBackend()
    } else {
      setItems((prev) => prev.map((i) => (i.id === itemId ? { ...i, quantity } : i)))
    }
  }

  const removeItem = async (itemId) => {
    if (isAuthenticated) {
      await cartService.removeCartItem(itemId)
      await refreshFromBackend()
    } else {
      setItems((prev) => prev.filter((i) => i.id !== itemId))
    }
    toast.success('Removed from cart')
  }

  const clearCart = async () => {
    if (isAuthenticated) {
      await cartService.clearCart()
    }
    setItems([])
    writeLocalCart([])
  }

  const total = items.reduce((sum, item) => sum + Number(item.product.price) * item.quantity, 0)
  const itemCount = items.reduce((sum, item) => sum + item.quantity, 0)

  return (
    <CartContext.Provider
      value={{ items, loading, total, itemCount, addItem, updateQuantity, removeItem, clearCart, refreshFromBackend }}
    >
      {children}
    </CartContext.Provider>
  )
}

export const useCart = () => useContext(CartContext)
