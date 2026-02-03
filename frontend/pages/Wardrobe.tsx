
import React from 'react';
import { AppScreen, Outfit } from '../types';
import BottomNav from '../components/BottomNav';
import { MOCK_OUTFITS } from '../constants';

interface WardrobeProps {
  onNavigate: (screen: AppScreen) => void;
  onViewDetails: (outfit: Outfit) => void;
}

const Wardrobe: React.FC<WardrobeProps> = ({ onNavigate, onViewDetails }) => {
  return (
    <div className="bg-background-dark min-h-screen pb-32">
      <header className="sticky top-0 z-50 bg-background-dark/95 backdrop-blur-md px-4 py-3 flex items-center justify-between border-b border-white/5">
        <button onClick={() => onNavigate('home')} className="size-10 flex items-center justify-center rounded-full hover:bg-white/10"><span className="material-symbols-outlined">arrow_back</span></button>
        <h1 className="text-xl font-bold tracking-tight">My Wardrobe</h1>
        <button className="size-10 flex items-center justify-center rounded-full hover:bg-white/10"><span className="material-symbols-outlined">search</span></button>
      </header>

      <div className="w-full overflow-x-auto no-scrollbar py-4 px-4 flex gap-3 sticky top-[65px] z-40 bg-background-dark shadow-lg">
        <button className="h-10 shrink-0 px-6 rounded-full bg-primary text-white font-medium text-sm shadow-lg shadow-primary/25">All</button>
        {['Casual', 'AI Picks', 'Formal', 'Date Night'].map(f => (
          <button key={f} className="h-10 shrink-0 px-6 rounded-full bg-surface-dark border border-white/5 text-gray-400 font-medium text-sm flex items-center gap-1.5">
            {f === 'AI Picks' && <span className="material-symbols-outlined text-[18px] text-primary">auto_awesome</span>}
            {f}
          </button>
        ))}
      </div>

      <main className="px-4 pt-4">
        <div className="flex items-end justify-between mb-6">
          <div>
            <h2 className="text-3xl font-bold">Your Collection</h2>
            <p className="text-gray-500 text-sm font-medium mt-1">24 saved looks</p>
          </div>
          <button className="text-primary text-sm font-bold flex items-center gap-1 mb-1">
            Sort by <span className="material-symbols-outlined text-[18px]">sort</span>
          </button>
        </div>

        <div className="grid grid-cols-2 gap-4">
          {MOCK_OUTFITS.map((outfit, idx) => (
            <div 
                key={outfit.id} 
                className="group relative flex flex-col gap-3 cursor-pointer" 
                onClick={() => onViewDetails(outfit)}
            >
              <div className="relative w-full aspect-[3/5] rounded-3xl overflow-hidden bg-surface-dark shadow-lg">
                <img src={outfit.imageUrl} className="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" />
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-black/20"></div>
                
                <div className="absolute top-3 right-3 flex flex-col gap-2">
                    <button className="size-8 rounded-full bg-white/10 backdrop-blur-md flex items-center justify-center text-white"><span className="material-symbols-outlined text-[18px]">favorite</span></button>
                    <button className="size-8 rounded-full bg-white/10 backdrop-blur-md flex items-center justify-center text-white"><span className="material-symbols-outlined text-[18px]">ios_share</span></button>
                </div>

                {idx % 2 === 0 && (
                    <div className="absolute top-3 left-3">
                        <div className="px-2 py-1 rounded-full bg-primary/80 backdrop-blur-md flex items-center gap-1 border border-white/20">
                            <span className="material-symbols-outlined text-[12px]">spark</span>
                            <span className="text-[10px] font-bold uppercase tracking-wider">AI Pick</span>
                        </div>
                    </div>
                )}

                <div className="absolute bottom-0 left-0 w-full p-4">
                  <h3 className="text-white text-lg font-bold leading-none">{outfit.name}</h3>
                  <p className="text-gray-400 text-[10px] mt-2 font-medium">{outfit.createdAt}</p>
                </div>
              </div>
            </div>
          ))}

          <div className="aspect-[3/5] rounded-3xl bg-surface-dark border-2 border-dashed border-gray-700 flex flex-col items-center justify-center gap-2 text-gray-500 hover:border-primary hover:text-primary transition-colors cursor-pointer">
            <span className="material-symbols-outlined text-3xl">add_circle</span>
            <span className="text-xs font-bold">Create New</span>
          </div>
        </div>
      </main>

      <div className="fixed bottom-24 right-4 z-50">
          <button 
            onClick={() => onNavigate('quiz')}
            className="flex h-14 items-center justify-center gap-2 rounded-full bg-primary pl-5 pr-6 text-white shadow-glow active:scale-95 transition-transform"
          >
            <span className="material-symbols-outlined">stylus</span>
            <span className="font-bold tracking-wide">Generate Look</span>
          </button>
      </div>

      <BottomNav current="wardrobe" onNavigate={onNavigate} />
    </div>
  );
};

export default Wardrobe;
