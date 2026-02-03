
import React from 'react';

interface NotificationsProps {
  onBack: () => void;
}

const Notifications: React.FC<NotificationsProps> = ({ onBack }) => {
  const sections = [
    {
      title: 'Styling & Inspiration',
      items: [
        { label: 'Daily Outfit Push', sub: 'Your AI curated look every morning', icon: 'checkroom', checked: true, color: 'text-primary' },
        { label: 'New Trends', sub: 'Viral styles matching your DNA', icon: 'trending_up', checked: true, color: 'text-blue-400' },
        { label: '3D Render Ready', sub: 'Notify when virtual try-on is ready', icon: 'view_in_ar', checked: false, color: 'text-fuchsia-400' }
      ]
    },
    {
      title: 'Shopping & Deals',
      items: [
        { label: 'Sales & Promotions', sub: 'Discounts on brands you love', icon: 'local_offer', checked: false, color: 'text-orange-400' },
        { label: 'Price Drops', sub: 'Alerts for items in your saved list', icon: 'price_check', checked: true, color: 'text-green-400' }
      ]
    }
  ];

  return (
    <div className="min-h-screen bg-background-dark pb-12">
      <header className="p-6 pt-12 flex items-center justify-between sticky top-0 z-50 bg-background-dark/80 backdrop-blur-md">
        <button onClick={onBack} className="size-10 flex items-center justify-center rounded-full hover:bg-white/10"><span className="material-symbols-outlined">arrow_back</span></button>
        <h2 className="text-xl font-bold">Notifications</h2>
        <div className="size-10"></div>
      </header>

      <div className="px-6 mb-8">
        <p className="text-sm text-gray-400 leading-relaxed">
            Control which alerts you receive. We recommend keeping <span className="text-primary font-medium">Daily Outfit</span> enabled for the best experience.
        </p>
      </div>

      <div className="px-5 space-y-8">
        {sections.map(section => (
            <section key={section.title}>
                <h3 className="text-[10px] font-bold uppercase tracking-widest text-gray-500 mb-3 px-2">{section.title}</h3>
                <div className="bg-surface-dark rounded-3xl overflow-hidden border border-white/5 divide-y divide-white/5">
                    {section.items.map(item => (
                        <div key={item.label} className="p-4 flex items-center justify-between">
                            <div className="flex items-center gap-4">
                                <div className={`size-10 rounded-full bg-white/5 flex items-center justify-center ${item.color}`}><span className="material-symbols-outlined text-xl">{item.icon}</span></div>
                                <div className="flex flex-col">
                                    <p className="font-bold">{item.label}</p>
                                    <p className="text-[10px] text-gray-500">{item.sub}</p>
                                </div>
                            </div>
                            <div className={`w-11 h-6 rounded-full p-1 transition-colors ${item.checked ? 'bg-primary' : 'bg-gray-800'}`}>
                                <div className={`size-4 bg-white rounded-full transition-transform ${item.checked ? 'translate-x-5' : ''}`}></div>
                            </div>
                        </div>
                    ))}
                </div>
            </section>
        ))}
      </div>

      <p className="text-center text-[10px] text-gray-600 mt-12">Push notifications are currently enabled in iOS Settings.</p>
    </div>
  );
};

export default Notifications;
