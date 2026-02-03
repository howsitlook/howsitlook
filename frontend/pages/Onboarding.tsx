
import React from 'react';

interface OnboardingProps {
  onStart: () => void;
  onSkip: () => void;
}

const Onboarding: React.FC<OnboardingProps> = ({ onStart, onSkip }) => {
  return (
    <div className="relative h-screen flex flex-col justify-between overflow-hidden bg-background-dark">
      <div className="flex justify-end p-6">
        <button onClick={onSkip} className="text-sm font-bold text-gray-400 hover:text-white transition-colors">Skip</button>
      </div>

      <div className="flex-1 flex flex-col justify-center px-4 py-2 relative">
        <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-primary/20 blur-[100px] pointer-events-none"></div>
        <div className="relative z-10 mx-auto w-full max-w-sm aspect-[4/5] rounded-3xl overflow-hidden shadow-2xl shadow-primary/10 ring-1 ring-white/10">
          <div 
            className="h-full w-full bg-cover bg-center transition-transform duration-700 hover:scale-105"
            style={{ backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuDSqHSEWDZaPzfLG4QoYLTxvicE5deYZTlNw6Yr2K2zoNZHDjb4jSH_-u0mwwznu-9z93PPIGZU7s-7sfNEqQkQvr5gfEm3-Sr-h1IBelRNycJfV7eUZ65_49Revv7ythSghlS8vmUeQwp_GY933WlM-DWezuI4QoS4wQhdmDZ_dPaQtmXj7E49HMQJzp9BpqkIrHSJtSV-7WAYVHSuQPvlg9ziJlxoOc9HXD8GxSPLaC5TOimK612DD2qHc3nI0v9q1zonblRvJqQB')" }}
          ></div>
          <div className="absolute bottom-6 left-6 z-30 flex items-center gap-2 rounded-full bg-white/10 px-4 py-2 backdrop-blur-md border border-white/20 shadow-lg">
            <span className="material-symbols-outlined text-primary text-xl">view_in_ar</span>
            <span className="text-[10px] font-bold uppercase tracking-wider text-white">3D Preview</span>
          </div>
        </div>
      </div>

      <div className="bg-background-dark px-6 pb-12 pt-6 text-center">
        <div className="flex justify-center gap-2 mb-6">
          <div className="h-2 w-8 rounded-full bg-primary shadow-neon"></div>
          <div className="h-2 w-2 rounded-full bg-gray-700"></div>
          <div className="h-2 w-2 rounded-full bg-gray-700"></div>
        </div>
        <h1 className="text-4xl font-bold tracking-tight mb-4">
          Style <span className="text-primary">Reimagined</span>
        </h1>
        <p className="text-gray-400 text-base leading-relaxed mb-8">
          Meet your AI stylist. Generate your lifelike 3D twin and discover outfits curated just for you.
        </p>
        <button 
          onClick={onStart}
          className="w-full h-14 bg-primary rounded-full text-white font-bold text-lg shadow-glow flex items-center justify-center gap-3 active:scale-95 transition-all"
        >
          Create My Avatar
          <span className="material-symbols-outlined">arrow_forward</span>
        </button>
        <button onClick={onSkip} className="mt-6 text-gray-400 font-medium">
          Already have an account? <span className="text-white underline underline-offset-4">Log in</span>
        </button>
      </div>
    </div>
  );
};

export default Onboarding;
