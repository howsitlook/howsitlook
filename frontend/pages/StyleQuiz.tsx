
import React, { useState } from 'react';
import { STYLE_OPTIONS } from '../constants';

interface StyleQuizProps {
  onBack: () => void;
  onNext: () => void;
}

const StyleQuiz: React.FC<StyleQuizProps> = ({ onBack, onNext }) => {
  const [selectedId, setSelectedId] = useState('edgy');

  return (
    <div className="min-h-screen bg-background-dark flex flex-col pb-32">
      <div className="flex flex-col w-full px-6 pt-12 pb-4 sticky top-0 bg-background-dark z-50">
        <div className="flex items-center justify-between mb-4">
          <span className="text-[10px] font-bold tracking-widest uppercase text-gray-500">Refine Your Style</span>
          <span className="text-sm font-bold text-primary">3 / 5</span>
        </div>
        <div className="flex w-full gap-2">
          <div className="h-1.5 flex-1 rounded-full bg-primary shadow-neon"></div>
          <div className="h-1.5 flex-1 rounded-full bg-primary shadow-neon"></div>
          <div className="h-1.5 flex-1 rounded-full bg-primary shadow-neon"></div>
          <div className="h-1.5 flex-1 rounded-full bg-gray-800"></div>
          <div className="h-1.5 flex-1 rounded-full bg-gray-800"></div>
        </div>
      </div>

      <main className="flex-1 px-6 pt-4">
        <div className="text-center mb-8">
            <h1 className="text-3xl font-bold leading-tight mb-3">Pick an outfit for a night out</h1>
            <p className="text-gray-400 text-sm max-w-[240px] mx-auto">Tap the style that speaks to your weekend vibe.</p>
        </div>

        <div className="grid grid-cols-2 gap-4">
            {STYLE_OPTIONS.map(opt => (
                <button 
                    key={opt.id}
                    onClick={() => setSelectedId(opt.id)}
                    className={`group relative aspect-[3/4] rounded-2xl overflow-hidden transition-all duration-300 ${selectedId === opt.id ? 'ring-4 ring-primary ring-offset-4 ring-offset-[#211121] shadow-neon scale-95' : 'hover:ring-2 hover:ring-gray-700'}`}
                >
                    <div 
                        className="absolute inset-0 bg-cover bg-center group-hover:scale-110 transition-transform duration-700" 
                        style={{ backgroundImage: `url('${opt.image}')` }}
                    >
                        <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/20 to-transparent"></div>
                    </div>
                    {selectedId === opt.id && (
                        <div className="absolute top-3 right-3 size-8 bg-primary rounded-full flex items-center justify-center shadow-lg animate-in zoom-in">
                            <span className="material-symbols-outlined text-white font-bold">check</span>
                        </div>
                    )}
                    <div className="absolute bottom-0 left-0 w-full p-4 text-left">
                        {opt.highMatch && (
                            <span className="inline-block px-2 py-0.5 rounded bg-primary/20 backdrop-blur-md border border-primary/30 text-[9px] font-bold tracking-widest uppercase text-primary mb-1">High Match</span>
                        )}
                        <p className="text-white text-xl font-bold leading-tight">{opt.name}</p>
                    </div>
                </button>
            ))}
        </div>

        <div className="mt-12 flex items-center justify-center gap-2 opacity-50">
            <span className="material-symbols-outlined text-primary text-sm animate-pulse">auto_awesome</span>
            <span className="text-[10px] font-bold uppercase tracking-widest text-gray-400">AI Analyzing Preferences...</span>
        </div>
      </main>

      <div className="fixed bottom-0 left-0 right-0 p-4 pb-8 max-w-md mx-auto bg-gradient-to-t from-background-dark via-background-dark to-transparent z-50">
        <div className="flex gap-4 items-center">
            <button onClick={onBack} className="size-14 flex items-center justify-center rounded-full bg-surface-dark border border-white/5 hover:bg-white/10 transition-colors">
                <span className="material-symbols-outlined">arrow_back</span>
            </button>
            <button 
                onClick={onNext}
                className="flex-1 h-14 bg-primary rounded-full text-white font-bold text-lg shadow-neon flex items-center justify-center gap-2 group active:scale-95 transition-all"
            >
                Next
                <span className="material-symbols-outlined group-hover:translate-x-1 transition-transform">arrow_forward</span>
            </button>
        </div>
      </div>
    </div>
  );
};

export default StyleQuiz;
