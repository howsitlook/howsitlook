
import React from 'react';
import { Outfit } from '../types';

interface OutfitDetailsProps {
  outfit: Outfit;
  onBack: () => void;
  isFavorited: boolean;
  toggleFavorite: () => void;
}

const OutfitDetails: React.FC<OutfitDetailsProps> = ({ outfit, onBack, isFavorited, toggleFavorite }) => {
  return (
    <div className="min-h-screen bg-background-dark pb-32">
        <div className="relative aspect-[3/4] w-full">
            <img src={outfit.imageUrl} className="absolute inset-0 w-full h-full object-cover" />
            <div className="absolute inset-0 bg-gradient-to-t from-background-dark via-transparent to-black/20"></div>
            
            <header className="absolute top-0 left-0 right-0 p-6 pt-12 flex items-center justify-between z-10">
                <button onClick={onBack} className="size-10 flex items-center justify-center rounded-full bg-black/20 backdrop-blur-md active:scale-90 transition-transform">
                  <span className="material-symbols-outlined">arrow_back</span>
                </button>
                <div className="flex gap-3">
                    <button 
                      onClick={toggleFavorite}
                      className={`size-10 flex items-center justify-center rounded-full backdrop-blur-md transition-all ${isFavorited ? 'bg-primary text-white' : 'bg-black/20 text-white'}`}
                    >
                      <span className={`material-symbols-outlined ${isFavorited ? 'fill-current' : ''}`}>favorite</span>
                    </button>
                    <button className="size-10 flex items-center justify-center rounded-full bg-black/20 backdrop-blur-md"><span className="material-symbols-outlined">share</span></button>
                </div>
            </header>

            <div className="absolute bottom-10 w-full flex justify-center">
                <div className="px-4 py-2 bg-black/40 backdrop-blur-md border border-white/10 rounded-full flex items-center gap-2 text-[10px] font-bold text-white uppercase tracking-wider">
                    <span className="material-symbols-outlined text-lg">360</span> VIEW 360°
                </div>
            </div>
        </div>

        <div className="px-6 -mt-4 relative z-20">
            <div className="mb-8">
                <span className="px-3 py-1 bg-primary/20 text-primary text-[10px] font-bold uppercase tracking-widest rounded border border-primary/30">Trending</span>
                <h1 className="text-[32px] font-bold leading-tight mt-2">{outfit.name}</h1>
                <p className="text-gray-500 text-xs font-bold uppercase tracking-widest">Created by AI Stylist</p>
            </div>

            <div className="bg-surface-dark p-6 rounded-3xl border border-white/5 mb-8 relative overflow-hidden">
                <div className="absolute top-4 right-4 text-primary/10 opacity-50"><span className="material-symbols-outlined text-6xl">sparkles</span></div>
                <div className="flex items-center gap-3 mb-3">
                    <span className="material-symbols-outlined text-primary">psychology</span>
                    <h3 className="text-xs font-bold uppercase tracking-widest text-primary">Why This Works</h3>
                </div>
                <p className="text-sm text-gray-300 leading-relaxed">
                    Match Score: <span className="text-primary font-bold">{outfit.matchScore}%</span> — The {outfit.tags[0].toLowerCase()} vibe perfectly matches your selected style DNA.
                </p>
            </div>

            <div className="flex justify-between items-center mb-6">
                <h4 className="text-xl font-bold uppercase tracking-tight">Outfit Breakdown</h4>
                <span className="text-xs text-gray-500 font-bold uppercase tracking-widest">{outfit.items.length} Items</span>
            </div>

            <div className="space-y-4">
                {outfit.items.map(item => (
                    <div key={item.id} className="bg-surface-dark p-4 rounded-3xl border border-white/5 flex items-center gap-4 group hover:bg-white/5 transition-all active:scale-[0.98] cursor-pointer">
                        <div className="size-20 bg-white rounded-2xl overflow-hidden shrink-0">
                            <img src={item.image} className="w-full h-full object-cover group-hover:scale-110 transition-transform" />
                        </div>
                        <div className="flex-1 min-w-0">
                            <div className="flex justify-between items-start">
                                <span className="text-[10px] font-bold text-gray-500 uppercase">{item.brand}</span>
                                <div className="flex items-center gap-1 text-[10px] font-bold text-orange-400">4.8 <span className="material-symbols-outlined text-[10px]">star</span></div>
                            </div>
                            <h5 className="font-bold truncate mb-2">{item.name}</h5>
                            <div className="flex justify-between items-center">
                                <span className="text-lg font-bold">{item.currency}{item.price}</span>
                                <button className="px-4 py-1.5 bg-primary/20 text-primary text-[10px] font-bold uppercase tracking-widest rounded-full border border-primary/30 flex items-center gap-1 hover:bg-primary hover:text-white transition-colors">Buy <span className="material-symbols-outlined text-xs">north_east</span></button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>

        <div className="fixed bottom-0 left-0 right-0 p-4 pb-8 max-w-md mx-auto bg-background-dark/95 backdrop-blur-xl border-t border-white/5 z-50 flex items-center gap-6 shadow-[0_-10px_40px_rgba(0,0,0,0.5)]">
            <div className="flex flex-col">
                <span className="text-[10px] font-bold uppercase tracking-widest text-gray-500">Total Est.</span>
                <span className="text-xl font-bold">${outfit.items.reduce((acc, curr) => acc + curr.price, 0)}</span>
            </div>
            <button className="flex-1 h-14 bg-primary text-white font-bold text-lg rounded-full shadow-glow flex items-center justify-center gap-3 active:scale-95 transition-all">
                <span className="material-symbols-outlined">shopping_bag</span>
                Shop Full Look
            </button>
        </div>
    </div>
  );
};

export default OutfitDetails;
