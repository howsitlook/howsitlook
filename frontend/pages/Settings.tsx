
import React from 'react';
import { AppScreen } from '../types';
import BottomNav from '../components/BottomNav';

interface SettingsProps {
  onNavigate: (screen: AppScreen) => void;
  onBack: () => void;
}

const Settings: React.FC<SettingsProps> = ({ onNavigate, onBack }) => {
  return (
    <div className="bg-background-dark min-h-screen pb-32">
      <header className="p-6 pt-12 flex items-center justify-between sticky top-0 z-50 bg-background-dark/80 backdrop-blur-md">
        <button onClick={onBack} className="size-10 flex items-center justify-center rounded-full hover:bg-white/10"><span className="material-symbols-outlined">arrow_back</span></button>
        <h2 className="text-xl font-bold">Settings</h2>
        <div className="size-10"></div>
      </header>

      <div className="px-5 mb-6">
        <div className="bg-surface-dark rounded-3xl p-5 border border-white/5 flex items-center gap-4">
            <div className="relative shrink-0">
                <div className="size-20 rounded-full bg-cover bg-center border-2 border-primary p-0.5" style={{ backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuClR-SkLWpb51Tc8V10wurWjxIVe7Oq4eAEIV-zbpKYFBMPNB8aSI8fM30Quwdvdv6v_um9WSGBNXPi7dAh3_MkZhOkTi3mVPM-OsBtQsGC5cqqLLn-1GezqJT5cfSctpQULPGqpsm7GwTm3yAK-y7IxDQg8NNbUq6WtwWgf-wVGwEIVCyzkxOndzNzhcv-gWocpKgMvDGknlp12kY22cONscjeaLNHy2m6mj5GwRQoIkZQOPtjAp2CMmhVGqSSVZA5_1plsBAa0djw')" }}></div>
                <div className="absolute -bottom-1 -right-1 bg-primary text-white text-[10px] font-bold px-2 py-0.5 rounded-full border-2 border-surface-dark">PRO</div>
            </div>
            <div className="flex-1">
                <h3 className="text-xl font-bold">Alex StyleBot</h3>
                <p className="text-gray-500 text-sm mb-3">alex.bot@example.com</p>
                <button className="px-4 py-1.5 bg-gray-800 rounded-full text-[10px] font-bold uppercase tracking-widest">Edit Profile</button>
            </div>
        </div>
      </div>

      <div className="px-5 space-y-6">
        <section>
            <h3 className="text-[10px] font-bold uppercase tracking-widest text-gray-500 mb-3 px-2">AI Configuration</h3>
            <div className="bg-surface-dark rounded-3xl overflow-hidden border border-white/5 divide-y divide-white/5">
                {[
                    { label: 'Body Measurements', sub: 'Updated 2 days ago', icon: 'accessibility_new', action: () => onNavigate('profile-setup') },
                    { label: 'Style DNA', sub: 'Streetwear, Cyberpunk', icon: 'palette', action: () => onNavigate('quiz') },
                    { label: 'Virtual Wardrobe', sub: 'Manage 3D assets', icon: 'checkroom', action: () => onNavigate('wardrobe') }
                ].map(item => (
                    <button key={item.label} onClick={item.action} className="w-full p-4 flex items-center gap-4 hover:bg-white/5 transition-colors text-left group">
                        <div className="size-10 rounded-full bg-primary/10 flex items-center justify-center text-primary"><span className="material-symbols-outlined text-xl">{item.icon}</span></div>
                        <div className="flex-1">
                            <p className="font-bold">{item.label}</p>
                            <p className="text-[10px] text-gray-500">{item.sub}</p>
                        </div>
                        <span className="material-symbols-outlined text-gray-600 group-hover:text-primary transition-colors">chevron_right</span>
                    </button>
                ))}
            </div>
        </section>

        <section>
            <h3 className="text-[10px] font-bold uppercase tracking-widest text-gray-500 mb-3 px-2">App Preferences</h3>
            <div className="bg-surface-dark rounded-3xl overflow-hidden border border-white/5 divide-y divide-white/5">
                <button onClick={() => onNavigate('notifications')} className="w-full p-4 flex items-center gap-4 hover:bg-white/5 transition-colors text-left group">
                    <div className="size-10 rounded-full bg-gray-800 flex items-center justify-center text-gray-400"><span className="material-symbols-outlined text-xl">notifications</span></div>
                    <div className="flex-1 font-bold">Daily Outfit Push</div>
                    <div className="size-10 flex items-center justify-end"><div className="w-11 h-6 bg-primary rounded-full p-1"><div className="size-4 bg-white rounded-full ml-auto"></div></div></div>
                </button>
                <div className="p-4 flex items-center gap-4 hover:bg-white/5 transition-colors text-left group">
                    <div className="size-10 rounded-full bg-gray-800 flex items-center justify-center text-gray-400"><span className="material-symbols-outlined text-xl">view_in_ar</span></div>
                    <div className="flex-1 font-bold">Auto 3D Render</div>
                    <div className="size-10 flex items-center justify-end"><div className="w-11 h-6 bg-gray-700 rounded-full p-1"><div className="size-4 bg-white rounded-full"></div></div></div>
                </div>
                <button onClick={() => onNavigate('orders')} className="w-full p-4 flex items-center gap-4 hover:bg-white/5 transition-colors text-left group">
                    <div className="size-10 rounded-full bg-gray-800 flex items-center justify-center text-gray-400"><span className="material-symbols-outlined text-xl">history</span></div>
                    <div className="flex-1 font-bold">Order History</div>
                    <span className="material-symbols-outlined text-gray-600">chevron_right</span>
                </button>
            </div>
        </section>

        <button className="w-full py-4 rounded-full border border-red-500/30 text-red-500 font-bold text-sm tracking-widest uppercase flex items-center justify-center gap-2 hover:bg-red-500/10 transition-colors">
            <span className="material-symbols-outlined text-lg">logout</span> Sign Out
        </button>

        <p className="text-center text-[10px] text-gray-700 uppercase tracking-widest font-mono">Version 2.0.4 AI-Beta</p>
      </div>

      <BottomNav current="settings" onNavigate={onNavigate} />
    </div>
  );
};

export default Settings;
