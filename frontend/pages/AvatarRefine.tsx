
import React from 'react';

interface AvatarRefineProps {
  onConfirm: () => void;
  onBack: () => void;
}

const AvatarRefine: React.FC<AvatarRefineProps> = ({ onConfirm, onBack }) => {
  return (
    <div className="h-screen bg-background-dark flex flex-col overflow-hidden">
      <div className="p-6 pt-12 flex items-center justify-between sticky top-0 z-50">
        <button onClick={onBack} className="size-10 flex items-center justify-center rounded-full bg-white/5"><span className="material-symbols-outlined">arrow_back</span></button>
        <h2 className="text-lg font-bold">Your Digital Twin</h2>
        <button onClick={onBack} className="text-primary text-sm font-bold">Reset</button>
      </div>

      <div className="flex-1 relative flex flex-col items-center justify-center">
        <div className="absolute inset-0 flex items-center justify-center opacity-30">
            <div className="w-64 h-64 rounded-full bg-primary blur-[120px]"></div>
        </div>
        
        <div 
          className="w-full h-full bg-center bg-contain bg-no-repeat"
          style={{ 
            backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuCJt28O4TAQpZKe1T_4xByMsntckAiJWvFZBmUGadwc2QA-Mygd4a4-GhaNUG4_iL6y7yDJouh-nzodwTTgs7rTzwvlO_SfOk-l0XPG5jyNXGQroGs4JLxaKbl0-6t7c3IrQE2VX88XjLLw8r5HqL8x1vQKZ_Z-Kpv1CJGrRNDvr3-H_UMxOc16mW_sNGLUPoKm11Ur_tMzA4HjGxIQbsoJLsaqmSZ5oWC08dkxN6m2n0NgS68MYTg86s4MKtBhN0b4gE0kJsE2FjMQ')",
            maskImage: "linear-gradient(to bottom, black 80%, transparent 100%)",
            WebkitMaskImage: "linear-gradient(to bottom, black 80%, transparent 100%)"
          }}
        ></div>

        <div className="absolute top-24 left-6 right-6 flex justify-between pointer-events-none opacity-70">
            <div className="bg-surface-dark/40 backdrop-blur-md px-3 py-1 rounded-full border border-white/10 text-[10px] font-bold text-white">Height: 175cm</div>
            <div className="bg-surface-dark/40 backdrop-blur-md px-3 py-1 rounded-full border border-white/10 text-[10px] font-bold text-white">Size: M</div>
        </div>

        <div className="absolute bottom-40 flex flex-col items-center gap-4 w-full">
            <div className="bg-black/20 px-4 py-1.5 rounded-full backdrop-blur-md border border-white/10 text-[10px] text-white/60 font-medium flex items-center gap-2">
                <span className="material-symbols-outlined text-sm">360</span> Swipe to rotate • Pinch to zoom
            </div>
            <div className="flex gap-3">
                <button className="px-4 py-2 bg-primary rounded-full text-[10px] font-bold uppercase tracking-wider flex items-center gap-2 shadow-neon">
                    <span className="material-symbols-outlined text-[16px]">wb_sunny</span> Studio
                </button>
                <button className="px-4 py-2 bg-surface-dark border border-white/10 rounded-full text-[10px] font-bold uppercase tracking-wider text-gray-400 flex items-center gap-2">
                    <span className="material-symbols-outlined text-[16px]">partly_cloudy_day</span> Daylight
                </button>
            </div>
        </div>
      </div>

      <div className="bg-background-dark p-6 border-t border-gray-800">
        <div className="flex justify-between items-center mb-4">
            <h3 className="font-bold">Refine Attributes</h3>
            <span className="text-primary text-[10px] font-bold uppercase tracking-widest">Step 2/3</span>
        </div>
        <div className="flex gap-4 overflow-x-auto no-scrollbar pb-4">
            {['Body', 'Face', 'Hair', 'Skin'].map((attr, idx) => (
                <div key={attr} className="flex flex-col items-center gap-2 min-w-[72px]">
                    <div className={`size-[72px] rounded-full p-0.5 ${idx === 0 ? 'bg-gradient-to-tr from-primary to-fuchsia-400' : 'bg-surface-dark'}`}>
                        <div className="w-full h-full rounded-full bg-cover bg-center border-2 border-background-dark" style={{ backgroundImage: `url('https://picsum.photos/100/100?random=${idx + 20}')` }}></div>
                    </div>
                    <span className={`text-[10px] font-bold ${idx === 0 ? 'text-primary' : 'text-gray-500'}`}>{attr}</span>
                </div>
            ))}
        </div>
        <button onClick={onConfirm} className="w-full h-14 bg-primary rounded-full font-bold text-lg shadow-glow flex items-center justify-center gap-2 active:scale-95 transition-all">
            Confirm Avatar <span className="material-symbols-outlined">arrow_forward</span>
        </button>
      </div>
    </div>
  );
};

export default AvatarRefine;
