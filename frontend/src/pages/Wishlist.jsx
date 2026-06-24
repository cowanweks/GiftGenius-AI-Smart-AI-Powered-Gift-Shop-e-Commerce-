import { Link } from 'react-router-dom'
import toast from 'react-hot-toast'
import { FaHeart, FaTrash, FaShoppingCart } from 'react-icons/fa'
import { useWishlist } from '../context/WishlistContext'
import EmptyState from '../components/ui/EmptyState'
import Spinner from '../components/ui/Spinner'

export default function Wishlist() {
  const { items, loading, removeItem, moveToCart } = useWishlist()

  if (loading) {
    return (
      <div className="flex justify-center py-24">
        <Spinner className="w-10 h-10" />
      </div>
    )
  }

  if (items.length === 0) {
    return (
      <EmptyState
        icon={<FaHeart />}
        title="Your wishlist is empty"
        message="Save gifts you love so you can find them again later."
        actionLabel="Discover Gifts"
        actionTo="/products"
      />
    )
  }

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <h1 className="text-3xl font-display font-bold text-gray-900 mb-6">Your Wishlist</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
        {items.map((item) => (
          <div key={item.id} className="flex items-center gap-4 bg-white rounded-2xl border border-purple-50 shadow-sm p-4">
            <Link to={`/products/${item.product_detail.slug}`}>
              <img
                src={item.product_detail.image || 'https://placehold.co/100x100?text=Gift'}
                alt={item.product_detail.name}
                className="w-20 h-20 rounded-xl object-cover bg-purple-50"
              />
            </Link>
            <div className="flex-1">
              <Link to={`/products/${item.product_detail.slug}`} className="font-medium text-gray-900 hover:text-brand-purple">
                {item.product_detail.name}
              </Link>
              <p className="text-brand-purple-dark font-semibold mt-1">
                KSh {Number(item.product_detail.price).toLocaleString()}
              </p>
              <div className="flex items-center gap-3 mt-2">
                <button
                  onClick={() => moveToCart(item.id).then(() => toast.success('Moved to cart')).catch(() => toast.error('Failed to move'))}
                  className="flex items-center gap-1.5 text-xs font-semibold text-brand-purple"
                >
                  <FaShoppingCart /> Move to cart
                </button>
                <button
                  onClick={() => removeItem(item.id)}
                  className="flex items-center gap-1.5 text-xs font-semibold text-gray-400 hover:text-red-500"
                >
                  <FaTrash /> Remove
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
