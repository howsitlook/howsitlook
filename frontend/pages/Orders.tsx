
import React from 'react';
import { AppScreen } from '../types';

interface OrdersProps {
  onNavigate: (screen: AppScreen) => void;
  onBack: () => void;
}

const Orders: React.FC<OrdersProps> = ({ onNavigate, onBack }) => {
  const orders = [
    { name: 'Cyberpunk Bomber', price: 145, date: 'Oct 24', status: 'Shipped', accessories: '+ 2 accessories', image: 'https://picsum.photos/100/100?random=40', is3D: true },
    { name: 'Neon High-Tops', price: 89.99, date: 'Oct 10', status: 'Delivered', sub: 'Size: 42 • Green', image: 'https://picsum.photos/100/100?random=41', is3D: false },
    { name: 'Holo Visor v2', price: 45, date: 'Sep 28', status: 'Delivered', sub: 'Eyewear', image: 'https://picsum.photos/100/100?random=42', is3D: true }
  ];

  return (
    <div className="min-h-screen bg-background-dark pb-32">
      <header className="p-6 pt-12 flex items-center justify-between sticky top-0 z-50 bg-background-dark/80 backdrop-blur-md">
        <button onClick={onBack} className="size-10 flex items-center justify-center rounded-full hover:bg-white/10"><span className="material-symbols-outlined">arrow_back</span></button>
        <h2 className="text-xl font-bold">Order History</h2>
        <div className="size-10"></div>
      </header>

      <div className="px-6 flex gap-3 mb-8">
        <button className="flex-1 py-2 rounded-full bg-primary text-[10px] font-bold uppercase tracking-widest shadow-neon">All Orders</button>
        <button className="flex-1 py-2 rounded-full bg-surface-dark border border-white/5 text-[10px] font-bold uppercase tracking-widest text-gray-400">Shipped</button>
        <button className="flex-1 py-2 rounded-full bg-surface-dark border border-white/5 text-[10px] font-bold uppercase tracking-widest text-gray-400">Last 30 Days</button>
      </div>

      <div className="px-5 space-y-4">
        {orders.map(order => (
            <div key={order.name} className="bg-surface-dark p-5 rounded-3xl border border-white/5">
                <div className="flex gap-4 mb-6">
                    <div className="size-20 bg-white/5 rounded-full overflow-hidden shrink-0 relative p-1 border border-white/10">
                        <img src={order.image} className="w-full h-full object-cover rounded-full" />
                        {order.is3D && <div className="absolute bottom-0 right-0 bg-black text-[8px] font-bold px-1 py-0.5 rounded-tl border-l border-t border-white/20">3D</div>}
                    </div>
                    <div className="flex-1 min-w-0">
                        <div className="flex justify-between items-start mb-1">
                            <h3 className="font-bold text-base truncate">{order.name}</h3>
                            <span className="text-primary font-bold">${order.price}</span>
                        </div>
                        <p className="text-[10px] text-gray-500 mb-2">{order.accessories || order.sub}</p>
                        <div className="flex items-center gap-2">
                            <span className={`px-2 py-0.5 rounded text-[8px] font-bold uppercase tracking-widest ${order.status === 'Shipped' ? 'bg-green-500/20 text-green-400' : 'bg-gray-800 text-gray-400'}`}>{order.status}</span>
                            <span className="text-[10px] text-gray-500">• {order.date}</span>
                        </div>
                    </div>
                </div>
                <div className="flex gap-3">
                    <button className="flex-1 h-12 rounded-2xl bg-white/5 border border-white/5 text-xs font-bold uppercase tracking-widest flex items-center justify-center gap-2">
                        <span className="material-symbols-outlined text-sm">checkroom</span> {order.status === 'Delivered' ? 'Restyle' : 'Try On'}
                    </button>
                    <button className="flex-1 h-12 rounded-2xl bg-primary text-white text-xs font-bold uppercase tracking-widest shadow-glow">
                        {order.status === 'Shipped' ? 'Track Order' : 'View Details'}
                    </button>
                </div>
            </div>
        ))}
      </div>
    </div>
  );
};

export default Orders;
