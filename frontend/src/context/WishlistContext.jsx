import { createContext, useContext, useEffect, useState } from 'react'
import toast from 'react-hot-toast'
import * as wishlistService from '../services/wishlistService'
import { useAuth } from './AuthContext'

const WishlistContext = createContext(null)

export function WishlistProvider({ children }) {
  const { isAuthenticated } = useAuth()
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(false)

  const refresh = async () => {
    if (!isAuthenticated) {
      setItems([])
      return
    }
    setLoading(true)
    try {
      const data = await wishlistService.getWishlist()
      setItems(data)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    refresh()
  }, [isAuthenticated])

  const isWishlisted = (productId) => items.some((i) => i.product_detail.id === productId)

  const toggleWishlist = async (product) => {
    if (!isAuthenticated) {
      toast.error('Please log in to save items to your wishlist')
      return
    }
    const existing = items.find((i) => i.product_detail.id === product.id)
    if (existing) {
      await wishlistService.removeFromWishlist(existing.id)
      setItems((prev) => prev.filter((i) => i.id !== existing.id))
      toast.success('Removed from wishlist')
    } else {
      const created = await wishlistService.addToWishlist(product.id)
      setItems((prev) => [...prev, created])
      toast.success('Added to wishlist')
    }
  }

  const removeItem = async (itemId) => {
    await wishlistService.removeFromWishlist(itemId)
    setItems((prev) => prev.filter((i) => i.id !== itemId))
  }

  const moveToCart = async (itemId) => {
    await wishlistService.moveToCart(itemId)
    setItems((prev) => prev.filter((i) => i.id !== itemId))
  }

  return (
    <WishlistContext.Provider
      value={{ items, loading, isWishlisted, toggleWishlist, removeItem, moveToCart, refresh }}
    >
      {children}
    </WishlistContext.Provider>
  )
}

export const useWishlist = () => useContext(WishlistContext)
