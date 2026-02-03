
import React from 'react';
import { AppScreen } from '../types';

interface BottomNavProps {
  current: AppScreen;
  onNavigate: (screen: AppScreen) => void;
}

const BottomNav: React.FC<BottomNavProps> = ({ current, onNavigate }) => {
  return (
    <nav className="fixed bottom-0 left-0 right-0 max-w-md mx-auto bg-surface-dark/95 backdrop-blur-lg border-t border-white/5 pb-6 pt-3 px-6 z-50 flex justify-between items-center">
      <button 
        onClick={() => onNavigate('home')}
        className={`flex flex-col items-center gap-1 transition-colors ${current === 'home' ? 'text-primary font-bold' : 'text-gray-400'}`}
      >
        <span className={`material-symbols-outlined text-[26px] ${current === 'home' ? 'fill-current' : ''}`}>home</span>
        <span className="text-[10px]">Home</span>
      </button>

      <button 
        onClick={() => onNavigate('wardrobe')}
        className={`flex flex-col items-center gap-1 transition-colors ${current === 'wardrobe' ? 'text-primary font-bold' : 'text-gray-400'}`}
      >
        <div className="relative">
          <span className={`material-symbols-outlined text-[26px] ${current === 'wardrobe' ? 'fill-current' : ''}`}>checkroom</span>
          {current === 'wardrobe' && <span className="absolute -top-0.5 -right-0.5 size-2 bg-primary rounded-full"></span>}
        </div>
        <span className="text-[10px]">Wardrobe</span>
      </button>

      <button 
        onClick={() => onNavigate('quiz')}
        className="relative -top-6 bg-primary text-white rounded-full size-14 shadow-neon flex items-center justify-center transition-transform active:scale-95"
      >
        <span className="material-symbols-outlined text-3xl">magic_button</span>
      </button>

      <button 
        onClick={() => onNavigate('wishlist')}
        className={`flex flex-col items-center gap-1 transition-colors ${current === 'wishlist' ? 'text-primary font-bold' : 'text-gray-400'}`}
      >
        <span className={`material-symbols-outlined text-[26px] ${current === 'wishlist' ? 'fill-current' : ''}`}>favorite</span>
        <span className="text-[10px]">Saved</span>
      </button>

      <button 
        onClick={() => onNavigate('settings')}
        className={`flex flex-col items-center gap-1 transition-colors ${current === 'settings' ? 'text-primary font-bold' : 'text-gray-400'}`}
      >
        <span className={`material-symbols-outlined text-[26px] ${current === 'settings' ? 'fill-current' : ''}`}>settings</span>
        <span className="text-[10px]">Settings</span>
      </button>
    </nav>
  );
};

export default BottomNav;
