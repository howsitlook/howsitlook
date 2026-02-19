
import React, { useState, useEffect } from 'react';
import { AppScreen, UserProfile, Occasion, Outfit, ProductItem } from './types';
import Onboarding from './pages/Onboarding';
import ProfileSetup from './pages/ProfileSetup';
import Home from './pages/Home';
import Wardrobe from './pages/Wardrobe';
import StyleQuiz from './pages/StyleQuiz';
import ContextSetup from './pages/ContextSetup';
import OutfitDetails from './pages/OutfitDetails';
import Settings from './pages/Settings';
import Notifications from './pages/Notifications';
import Orders from './pages/Orders';
import AvatarRefine from './pages/AvatarRefine';
import Wishlist from './pages/Wishlist';
import { MOCK_OUTFITS } from './constants';

const App: React.FC = () => {
  const [currentScreen, setCurrentScreen] = useState<AppScreen>('onboarding');
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [selectedOccasion, setSelectedOccasion] = useState<Occasion>('Date Night');
  const [selectedOutfit, setSelectedOutfit] = useState<Outfit>(MOCK_OUTFITS[0]);
  const [favorites, setFavorites] = useState<string[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);

  const navigateTo = (screen: AppScreen) => {
    setCurrentScreen(screen);
    window.scrollTo(0, 0);
  };

  const toggleFavorite = (itemId: string) => {
    setFavorites(prev => 
      prev.includes(itemId) ? prev.filter(id => id !== itemId) : [...prev, itemId]
    );
  };

  const handleGenerateSequence = () => {
    setIsGenerating(true);
    // Simulate AI computing time
    setTimeout(() => {
      setIsGenerating(false);
      navigateTo('home');
    }, 2500);
  };

  const renderScreen = () => {
    if (isGenerating) {
      return (
        <div className="h-screen flex flex-col items-center justify-center bg-background-dark p-8 text-center">
          <div className="relative mb-8">
            <div className="size-24 rounded-full border-4 border-primary/20 border-t-primary animate-spin"></div>
            <span className="material-symbols-outlined absolute inset-0 flex items-center justify-center text-primary text-4xl animate-pulse">auto_awesome</span>
          </div>
          <h2 className="text-2xl font-bold mb-2">Analyzing Style DNA</h2>
          <p className="text-gray-400 text-sm animate-pulse">Consulting virtual trends and local weather...</p>
        </div>
      );
    }

    switch (currentScreen) {
      case 'onboarding':
        return <Onboarding onStart={() => navigateTo('profile-setup')} onSkip={() => navigateTo('home')} />;
      case 'profile-setup':
        return <ProfileSetup onComplete={(profile) => {
          setUserProfile(profile);
          navigateTo('avatar-refine');
        }} onBack={() => navigateTo('onboarding')} />;
      case 'avatar-refine':
        return <AvatarRefine onConfirm={() => navigateTo('home')} onBack={() => navigateTo('profile-setup')} />;
      case 'home':
        return <Home 
          onNavigate={navigateTo} 
          onViewDetails={(outfit) => {
            setSelectedOutfit(outfit);
            navigateTo('outfit-details');
          }} 
          favorites={favorites}
          toggleFavorite={toggleFavorite}
        />;
      case 'wardrobe':
        return <Wardrobe onNavigate={navigateTo} onViewDetails={(outfit) => {
            setSelectedOutfit(outfit);
            navigateTo('outfit-details');
          }} />;
      case 'quiz':
        return <StyleQuiz onBack={() => navigateTo('home')} onNext={() => navigateTo('context-setup')} />;
      case 'context-setup':
        return <ContextSetup 
          onBack={() => navigateTo('quiz')} 
          onGenerate={handleGenerateSequence}
          selectedOccasion={selectedOccasion}
          setSelectedOccasion={setSelectedOccasion}
        />;
      case 'outfit-details':
        return <OutfitDetails 
          outfit={selectedOutfit} 
          onBack={() => navigateTo('home')} 
          isFavorited={favorites.includes(selectedOutfit.id)}
          toggleFavorite={() => toggleFavorite(selectedOutfit.id)}
        />;
      case 'settings':
        return <Settings onNavigate={navigateTo} onBack={() => navigateTo('home')} />;
      case 'notifications':
        return <Notifications onBack={() => navigateTo('settings')} />;
      case 'orders':
        return <Orders onNavigate={navigateTo} onBack={() => navigateTo('settings')} />;
      case 'wishlist':
        return <Wishlist onBack={() => navigateTo('home')} favorites={favorites} toggleFavorite={toggleFavorite} />;
      default:
        return <Home onNavigate={navigateTo} onViewDetails={setSelectedOutfit} favorites={favorites} toggleFavorite={toggleFavorite} />;
    }
  };

  return (
    <div className="min-h-screen bg-background-dark mx-auto relative shadow-2xl overflow-x-hidden no-scrollbar w-full max-w-screen-lg px-4 sm:px-6 lg:px-8">
      {renderScreen()}
    </div>
  );
};

export default App;
