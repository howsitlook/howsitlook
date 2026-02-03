
import React, { useState, useEffect } from 'react';
import { AppScreen, Outfit } from '../types';
import BottomNav from '../components/BottomNav';
import { getStylistInsight } from '../services/geminiService';
import { MOCK_OUTFITS } from '../constants';

interface HomeProps {
  onNavigate: (screen: AppScreen) => void;
  onViewDetails: (outfit: Outfit) => void;
  favorites: string[];
  toggleFavorite: (id: string) => void;
}

const Home: React.FC<HomeProps> = ({ onNavigate, onViewDetails, favorites, toggleFavorite }) => {
  const [insight, setInsight] = useState<string>("Analyzing your wardrobe for today's weather...");
  const outfit = MOCK_OUTFITS[0];
  const isFavorited = favorites.includes(outfit.id);

  useEffect(() => {
    getStylistInsight('Dinner Date', outfit.name, 'Rainy, 22°C').then(setInsight);
  }, []);

  return (
    <div className="bg-background-dark min-h-screen pb-32">
      <header className="p-6 pt-12 flex items-center justify-between sticky top-0 z-50 bg-background-dark/80 backdrop-blur-md">
        <button onClick={() => onNavigate('settings')} className="size-10 flex items-center justify-center rounded-full hover:bg-white/10 active:scale-90 transition-transform">
          <span className="material-symbols-outlined">menu</span>
        </button>
        <h1 className="text-xl font-bold tracking-tight">Today's Look</h1>
        <button className="size-10 flex items-center justify-center rounded-full hover:bg-white/10 active:scale-90 transition-transform">
          <span className="material-symbols-outlined">share</span>
        </button>
      </header>

      <div className="px-6 flex gap-2 justify-center mb-4">
        <div className="px-4 py-1.5 rounded-full bg-surface-dark border border-white/5 flex items-center gap-2 text-[10px] font-bold uppercase tracking-wider text-fuchsia-400">
            <span className="material-symbols-outlined text-[16px]">local_bar</span> Dinner Date
        </div>
        <div className="px-4 py-1.5 rounded-full bg-surface-dark border border-white/5 flex items-center gap-2 text-[10px] font-bold uppercase tracking-wider text-blue-400">
            <span className="material-symbols-outlined text-[16px]">cloudy_snowing</span> Rainy
        </div>
      </div>

      <div className="relative aspect-[3/4] w-full flex items-center justify-center overflow-hidden">
        <div className="absolute w-64 h-64 bg-primary/20 blur-[100px]"></div>
        <img 
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuDSqHSEWDZaPzfLG4QoYLTxvicE5deYZTlNw6Yr2K2zoNZHDjb4jSH_-u0mwwznu-9z93PPIGZU7s-7sfNEqQkQvr5gfEm3-Sr-h1IBelRNycJfV7eUZ65_49Revv7ythSghlS8vmUeQwp_GY933WlM-DWezuI4QoS4wQhdmDZ_dPaQtmXj7E49HMQJzp9BpqkIrHSJtSV-7WAYVHSuQPvlg9ziJlxoOc9HXD8GxSPLaC5TOimK612DD2qHc3nI0v9q1zonblRvJqQB" 
            className="h-full object-contain relative z-10" 
            style={{ maskImage: "linear-gradient(to bottom, black 80%, transparent 100%)", WebkitMaskImage: "linear-gradient(to bottom, black 80%, transparent 100%)" }}
        />
        <div className="absolute bottom-10 flex flex-col items-center gap-4 z-20">
            <div className="px-4 py-2 bg-black/40 backdrop-blur-md rounded-full border border-white/10 flex items-center gap-2 text-[10px] font-medium text-white/80">
                <span className="material-symbols-outlined text-sm">360</span> VIEW 360°
            </div>
        </div>
        <button 
          onClick={() => toggleFavorite(outfit.id)}
          className={`absolute top-4 right-6 size-12 rounded-full backdrop-blur-md border border-white/10 flex items-center justify-center z-30 transition-all ${isFavorited ? 'bg-primary text-white shadow-neon' : 'bg-black/20 text-white hover:bg-black/40'}`}
        >
          <span className={`material-symbols-outlined ${isFavorited ? 'fill-current' : ''}`}>favorite</span>
        </button>
      </div>

      <div className="px-6 -mt-6 relative z-30">
        <div className="bg-surface-dark/90 backdrop-blur-xl p-5 rounded-3xl border border-white/5 shadow-2xl">
            <div className="flex items-start gap-3 mb-4">
                <div className="size-8 rounded-full bg-primary/20 flex items-center justify-center text-primary shrink-0"><span className="material-symbols-outlined text-sm">auto_awesome</span></div>
                <div className="flex flex-col gap-1">
                    <h3 className="text-xs font-bold uppercase tracking-widest text-primary">AI Stylist Insight</h3>
                    <p className="text-sm text-gray-300 leading-relaxed italic">"{insight}"</p>
                </div>
            </div>

            <div className="flex justify-between items-center mb-4">
                <h4 className="text-lg font-bold">Outfit Breakdown</h4>
                <button onClick={() => onViewDetails(outfit)} className="text-primary text-xs font-bold uppercase tracking-wider hover:underline underline-offset-4">View All</button>
            </div>

            <div className="flex gap-4 overflow-x-auto no-scrollbar pb-2">
                {outfit.items.map(item => (
                    <div key={item.id} className="min-w-[120px] group cursor-pointer" onClick={() => onViewDetails(outfit)}>
                        <div className="aspect-square rounded-2xl bg-white/5 border border-white/5 overflow-hidden mb-2 relative">
                            <img src={item.image} className="w-full h-full object-cover group-hover:scale-110 transition-transform" />
                            <div className="absolute inset-0 bg-black/10 group-hover:bg-transparent transition-colors"></div>
                        </div>
                        <p className="text-[10px] font-bold text-gray-500 uppercase">{item.brand}</p>
                        <p className="text-xs font-bold truncate">{item.name}</p>
                    </div>
                ))}
            </div>

            <button 
                onClick={() => onViewDetails(outfit)}
                className="w-full h-14 bg-primary text-white font-bold text-lg rounded-full shadow-glow mt-8 flex items-center justify-center gap-3 active:scale-95 transition-all"
            >
                <span className="material-symbols-outlined">shopping_bag</span>
                Shop Full Look $315
            </button>
        </div>
      </div>

      <BottomNav current="home" onNavigate={onNavigate} />
    </div>
  );
};

export default Home;
