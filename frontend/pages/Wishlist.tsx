
import React from 'react';
import { MOCK_PRODUCTS } from '../constants';

interface WishlistProps {
  onBack: () => void;
  favorites: string[];
  toggleFavorite: (id: string) => void;
}

const Wishlist: React.FC<WishlistProps> = ({ onBack, favorites, toggleFavorite }) => {
  // We'll show both favorited products and a few curated suggestions
  const items = MOCK_PRODUCTS.filter(p => favorites.includes(p.id)).length > 0 
    ? MOCK_PRODUCTS.filter(p => favorites.includes(p.id))
    : MOCK_PRODUCTS; // Fallback to all if empty for demo

  return (
    <div className="min-h-screen bg-background-dark pb-32">
        <header className="p-6 pt-12 flex items-center justify-between sticky top-0 z-50 bg-background-dark/80 backdrop-blur-md">
            <button onClick={onBack} className="size-10 flex items-center justify-center rounded-full hover:bg-white/10 active:scale-90 transition-transform">
              <span className="material-symbols-outlined">arrow_back</span>
            </button>
            <h2 className="text-xl font-bold">Wishlist</h2>
            <button className="size-10 flex items-center justify-center rounded-full hover:bg-white/10"><span className="material-symbols-outlined">shopping_bag</span></button>
        </header>

        <div className="px-6 mb-6 flex justify-between items-baseline">
            <p className="text-gray-400 text-sm font-medium">{items.length} items <span className="text-gray-600">saved</span></p>
            <button className="text-primary text-xs font-bold uppercase tracking-widest flex items-center gap-1">
                <span className="material-symbols-outlined text-sm">filter_list</span> Filter
            </button>
        </div>

        {items.length === 0 ? (
          <div className="flex flex-col items-center justify-center pt-20 px-12 text-center">
            <div className="size-20 rounded-full bg-surface-dark flex items-center justify-center mb-6 text-gray-600">
              <span className="material-symbols-outlined text-5xl">favorite</span>
            </div>
            <h3 className="text-lg font-bold mb-2">Nothing saved yet</h3>
            <p className="text-gray-500 text-sm">Tap the heart icon on any product or outfit to save it here.</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-4 px-4">
              {items.map((item, idx) => (
                  <div key={item.id} className="bg-surface-dark rounded-3xl overflow-hidden border border-white/5 flex flex-col group cursor-pointer animate-in fade-in slide-in-from-bottom-4 duration-300" style={{ animationDelay: `${idx * 50}ms` }}>
                      <div className="relative aspect-[3/4] overflow-hidden">
                          <img src={item.image} className="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" />
                          <button 
                            onClick={(e) => { e.stopPropagation(); toggleFavorite(item.id); }}
                            className={`absolute top-3 right-3 size-10 rounded-full backdrop-blur-md flex items-center justify-center shadow-lg transition-all ${favorites.includes(item.id) ? 'bg-primary text-white' : 'bg-black/20 text-white'}`}
                          >
                            <span className={`material-symbols-outlined ${favorites.includes(item.id) ? 'fill-current' : ''}`}>favorite</span>
                          </button>
                          {item.lowStock && <div className="absolute top-3 left-0 bg-orange-500 text-white text-[8px] font-bold uppercase tracking-widest px-2 py-1 rounded-r shadow-lg">Low Stock</div>}
                      </div>
                      <div className="p-4 flex-1 flex flex-col justify-between">
                          <div>
                              <span className="text-[10px] font-bold text-gray-500 uppercase">{item.brand}</span>
                              <h4 className="font-bold text-sm mt-1 group-hover:text-primary transition-colors truncate">{item.name}</h4>
                          </div>
                          <div className="flex justify-between items-center mt-3">
                              <span className="text-lg font-bold">{item.currency}{item.price}</span>
                              <button className="size-10 rounded-full bg-white/5 flex items-center justify-center hover:bg-primary transition-colors active:scale-90"><span className="material-symbols-outlined text-xl">shopping_cart</span></button>
                          </div>
                      </div>
                  </div>
              ))}
          </div>
        )}
    </div>
  );
};

export default Wishlist;
