
import React, { useState } from 'react';
import { UserProfile } from '../types';
import { VIBE_TAGS, SKIN_TONES } from '../constants';

interface ProfileSetupProps {
  onComplete: (profile: UserProfile) => void;
  onBack: () => void;
}

const ProfileSetup: React.FC<ProfileSetupProps> = ({ onComplete, onBack }) => {
  const [gender, setGender] = useState<'Masculine' | 'Feminine' | 'Unisex'>('Feminine');
  const [height, setHeight] = useState(172);
  const [weight, setWeight] = useState(64);
  const [skinTone, setSkinTone] = useState(SKIN_TONES[3]);
  const [selectedVibes, setSelectedVibes] = useState<string[]>(['Streetwear', 'Y2K', 'Cyberpunk']);

  const toggleVibe = (vibe: string) => {
    setSelectedVibes(prev => 
      prev.includes(vibe) ? prev.filter(v => v !== vibe) : [...prev, vibe]
    );
  };

  const handleGenerate = () => {
    onComplete({ gender, height, weight, skinTone, vibe: selectedVibes });
  };

  return (
    <div className="min-h-screen bg-background-dark pb-32">
      <div className="sticky top-0 z-50 bg-background-dark/80 backdrop-blur-md p-4 flex items-center justify-between border-b border-gray-800">
        <button onClick={onBack} className="size-10 flex items-center justify-center rounded-full hover:bg-white/10">
          <span className="material-symbols-outlined">arrow_back</span>
        </button>
        <h2 className="text-lg font-bold">Profile Setup</h2>
        <div className="size-10"></div>
      </div>

      <div className="p-6">
        <div className="flex gap-2 mb-8 justify-center">
            <div className="h-1.5 w-8 rounded-full bg-primary shadow-neon"></div>
            <div className="h-1.5 w-8 rounded-full bg-primary/30"></div>
            <div className="h-1.5 w-8 rounded-full bg-primary/30"></div>
            <div className="h-1.5 w-8 rounded-full bg-primary/30"></div>
        </div>

        <h1 className="text-3xl font-bold leading-tight mb-2">Let's get to know you.</h1>
        <p className="text-gray-400 mb-8">Help our AI curate the perfect look for your digital twin.</p>

        <section className="mb-8">
          <h3 className="text-primary text-xs font-bold uppercase tracking-widest mb-4">The Basics</h3>
          <p className="text-sm font-medium mb-3">Which style fit do you prefer?</p>
          <div className="grid grid-cols-3 gap-3">
            {(['Masculine', 'Feminine', 'Unisex'] as const).map(g => (
              <button 
                key={g}
                onClick={() => setGender(g)}
                className={`flex flex-col items-center justify-center gap-2 h-24 rounded-2xl border transition-all ${gender === g ? 'border-primary bg-primary/5 shadow-glow' : 'border-gray-700 bg-surface-dark'}`}
              >
                <span className={`material-symbols-outlined text-3xl ${gender === g ? 'text-primary' : 'text-gray-500'}`}>
                  {g === 'Masculine' ? 'man' : g === 'Feminine' ? 'woman' : 'wc'}
                </span>
                <span className={`text-[10px] font-bold ${gender === g ? 'text-primary' : 'text-gray-500'}`}>{g}</span>
              </button>
            ))}
          </div>

          <div className="mt-8">
            <div className="flex justify-between items-end mb-2">
                <label className="text-sm font-medium">Height</label>
                <span className="text-xl font-bold text-primary">{height} <span className="text-sm font-normal text-gray-500">cm</span></span>
            </div>
            <input type="range" min="140" max="210" value={height} onChange={(e) => setHeight(Number(e.target.value))} />
          </div>

          <div className="mt-8">
            <div className="flex justify-between items-end mb-2">
                <label className="text-sm font-medium">Weight</label>
                <span className="text-xl font-bold text-primary">{weight} <span className="text-sm font-normal text-gray-500">kg</span></span>
            </div>
            <input type="range" min="40" max="150" value={weight} onChange={(e) => setWeight(Number(e.target.value))} />
          </div>
        </section>

        <section className="mb-8 pt-8 border-t border-gray-800">
          <h3 className="text-primary text-xs font-bold uppercase tracking-widest mb-4">Appearance</h3>
          <p className="text-sm font-medium mb-3">Select your skin tone</p>
          <div className="flex gap-3 overflow-x-auto no-scrollbar pb-2">
            {SKIN_TONES.map(tone => (
              <button 
                key={tone}
                onClick={() => setSkinTone(tone)}
                className={`size-12 rounded-full shrink-0 transition-transform ${skinTone === tone ? 'ring-2 ring-primary ring-offset-2 ring-offset-[#211121] scale-110' : 'hover:scale-105'}`}
                style={{ backgroundColor: tone }}
              >
                {skinTone === tone && <span className="material-symbols-outlined text-white text-xl">check</span>}
              </button>
            ))}
          </div>
        </section>

        <section className="mb-8 pt-8 border-t border-gray-800">
          <div className="flex justify-between items-baseline mb-4">
            <h3 className="text-primary text-xs font-bold uppercase tracking-widest">Your Vibe</h3>
            <span className="text-[10px] text-gray-500">Select at least 3</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {VIBE_TAGS.map(vibe => (
              <button 
                key={vibe}
                onClick={() => toggleVibe(vibe)}
                className={`px-4 py-2 rounded-full text-sm font-medium border transition-all ${selectedVibes.includes(vibe) ? 'bg-primary border-primary text-white shadow-glow' : 'bg-transparent border-gray-600 text-gray-400'}`}
              >
                {vibe}
              </button>
            ))}
          </div>
        </section>

        <section className="pt-8 border-t border-gray-800">
          <div className="flex items-center gap-2 mb-4">
            <h3 className="text-primary text-xs font-bold uppercase tracking-widest">Digital Twin</h3>
            <span className="material-symbols-outlined text-gray-500 text-sm">lock</span>
            <span className="text-[10px] text-gray-500 uppercase tracking-widest">Encrypted</span>
          </div>
          <p className="text-xs text-gray-500 mb-4">Upload reference photos to create your 3D avatar. Ensure good lighting.</p>
          <div className="grid grid-cols-2 gap-3">
            <div className="relative aspect-[3/4] rounded-2xl overflow-hidden group cursor-pointer border border-white/10">
                <img 
                    src="https://lh3.googleusercontent.com/aida-public/AB6AXuCklrYChh2gS1eu5h3XoFvX0-un5gFVAJeR5BOrnqv6lVnIgJLbhbw1tWOApJN3kdh3cmCLSkt_fn4H8CfBDHZbeu-LEy08ok7lFveawojzubBuMtQNRvAiyXmK7uK5F6u0xc9cHRzo6CHcNm_XwWFnBv-d9Zs7nywRTaiZ-HGjacXSsWaWoPjBrNSRig74-4xLzbp1N1xSXMjxtEaovyU0GbYwDbyqfTXk02FvFQANzADBB4YynsMS3Gg3hMjJMqq1aorW0tg4iFcy" 
                    className="w-full h-full object-cover opacity-80"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent"></div>
                <div className="absolute bottom-3 left-3 flex items-center gap-1.5">
                    <div className="size-5 rounded-full bg-green-500 flex items-center justify-center"><span className="material-symbols-outlined text-[12px]">check</span></div>
                    <span className="text-[10px] font-bold text-white">Front</span>
                </div>
            </div>
            <button className="aspect-[3/4] rounded-2xl bg-surface-dark border-2 border-dashed border-gray-700 flex flex-col items-center justify-center gap-2 text-gray-500 hover:border-primary hover:text-primary transition-colors">
                <span className="material-symbols-outlined text-3xl">add_a_photo</span>
                <span className="text-[10px] font-bold">Side Face</span>
            </button>
          </div>
        </section>
      </div>

      <div className="fixed bottom-0 left-0 right-0 p-4 pb-8 max-w-md mx-auto bg-background-dark/95 backdrop-blur-xl border-t border-gray-800 z-50">
        <button 
          onClick={handleGenerate}
          className="w-full h-14 bg-primary text-white font-bold text-lg rounded-full shadow-glow flex items-center justify-center gap-2 active:scale-95 transition-all"
        >
          Generate Digital Twin
          <span className="material-symbols-outlined">auto_awesome</span>
        </button>
      </div>
    </div>
  );
};

export default ProfileSetup;
