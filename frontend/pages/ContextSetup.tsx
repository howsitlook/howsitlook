
import React, { useState, useEffect } from 'react';
import { Occasion } from '../types';
import { getContextAnalysis } from '../services/geminiService';

interface ContextSetupProps {
  onBack: () => void;
  onGenerate: () => void;
  selectedOccasion: Occasion;
  setSelectedOccasion: (o: Occasion) => void;
}

const OCCASIONS: { name: Occasion; icon: string }[] = [
  { name: 'Date Night', icon: 'local_bar' },
  { name: 'Beach Outing', icon: 'beach_access' },
  { name: 'Wedding', icon: 'favorite' },
  { name: 'Office', icon: 'work' },
  { name: 'Gym', icon: 'fitness_center' },
  { name: 'Casual', icon: 'local_cafe' },
  { name: 'Gala', icon: 'diamond' },
  { name: 'Travel', icon: 'flight' }
];

const ContextSetup: React.FC<ContextSetupProps> = ({ onBack, onGenerate, selectedOccasion, setSelectedOccasion }) => {
  const [location, setLocation] = useState('New York, USA');
  const [aiInsight, setAiInsight] = useState('Analyzing context...');

  useEffect(() => {
    getContextAnalysis(location, selectedOccasion).then(setAiInsight);
  }, [location, selectedOccasion]);

  return (
    <div className="min-h-screen bg-background-dark flex flex-col pb-32">
      <header className="sticky top-0 z-50 p-6 pt-12 flex items-center justify-between bg-background-dark/80 backdrop-blur-md">
        <button onClick={onBack} className="size-10 flex items-center justify-center rounded-full hover:bg-white/10"><span className="material-symbols-outlined">arrow_back_ios_new</span></button>
        <h2 className="text-lg font-bold">Setup Context</h2>
        <div className="size-10"></div>
      </header>

      <div className="flex justify-center gap-2 py-2">
        <div className="h-1.5 w-8 rounded-full bg-primary shadow-neon"></div>
        <div className="h-1.5 w-2 rounded-full bg-surface-dark"></div>
        <div className="h-1.5 w-2 rounded-full bg-surface-dark"></div>
      </div>

      <main className="p-6">
        <div className="mb-8">
            <h1 className="text-[32px] font-bold leading-tight mb-2">Where are we going?</h1>
            <p className="text-gray-400">Select the occasion to tailor your outfit recommendations.</p>
        </div>

        <div className="grid grid-cols-2 gap-3 mb-8">
            {OCCASIONS.map(occ => (
                <button 
                    key={occ.name}
                    onClick={() => setSelectedOccasion(occ.name)}
                    className={`flex h-14 items-center gap-3 px-4 rounded-full transition-all ${selectedOccasion === occ.name ? 'bg-primary shadow-glow' : 'bg-surface-dark hover:bg-[#3d253d]'}`}
                >
                    <span className={`material-symbols-outlined ${selectedOccasion === occ.name ? 'text-white' : 'text-gray-500'}`}>{occ.icon}</span>
                    <span className={`text-sm font-bold ${selectedOccasion === occ.name ? 'text-white' : 'text-gray-400'}`}>{occ.name}</span>
                    {selectedOccasion === occ.name && (
                        <div className="ml-auto size-5 bg-white/20 rounded-full flex items-center justify-center"><span className="material-symbols-outlined text-[12px]">check</span></div>
                    )}
                </button>
            ))}
        </div>

        <div className="mb-8">
            <h3 className="text-lg font-bold mb-3">Local Forecast</h3>
            <div className="relative">
                <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-primary animate-pulse">near_me</span>
                <input 
                    type="text" 
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    className="w-full h-14 pl-12 pr-12 rounded-full bg-surface-dark border-none focus:ring-2 focus:ring-primary text-sm font-medium"
                />
                <button className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500"><span className="material-symbols-outlined">my_location</span></button>
            </div>
        </div>

        <div className="bg-gradient-to-br from-[#2a1a2a] to-surface-dark rounded-3xl p-5 border border-white/5 relative overflow-hidden group">
            <div className="absolute -top-10 -right-10 size-24 bg-primary/10 blur-2xl rounded-full"></div>
            <div className="flex items-start gap-4 relative z-10">
                <div className="size-10 rounded-full bg-primary/20 flex items-center justify-center text-primary shrink-0"><span className="material-symbols-outlined text-[20px]">auto_awesome</span></div>
                <div className="flex flex-col gap-1">
                    <span className="text-[10px] font-bold uppercase tracking-widest text-primary">AI Context Analysis</span>
                    <p className="text-sm text-gray-300 leading-relaxed">
                        Currently <span className="text-white font-bold">22°C</span> and Clear. <br/>
                        {aiInsight}
                    </p>
                </div>
            </div>
        </div>
      </main>

      <div className="fixed bottom-0 left-0 right-0 p-4 pb-8 max-w-md mx-auto bg-gradient-to-t from-background-dark via-background-dark to-transparent z-50">
        <button 
            onClick={onGenerate}
            className="w-full h-14 bg-primary text-white font-bold text-lg rounded-full shadow-glow flex items-center justify-center gap-2 active:scale-95 transition-all"
        >
            <span className="material-symbols-outlined">style</span>
            Generate Looks
        </button>
      </div>
    </div>
  );
};

export default ContextSetup;
