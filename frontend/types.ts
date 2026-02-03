
export type Occasion = 'Date Night' | 'Beach Outing' | 'Wedding' | 'Office' | 'Gym' | 'Casual' | 'Gala' | 'Travel';

export interface StyleOption {
  id: string;
  name: string;
  image: string;
  highMatch?: boolean;
}

export interface ProductItem {
  id: string;
  name: string;
  brand: string;
  price: number;
  currency: string;
  image: string;
  rating?: number;
  lowStock?: boolean;
}

export interface Outfit {
  id: string;
  name: string;
  description: string;
  matchScore: number;
  items: ProductItem[];
  imageUrl: string;
  createdAt: string;
  tags: string[];
}

export interface UserProfile {
  gender: 'Masculine' | 'Feminine' | 'Unisex';
  height: number;
  weight: number;
  skinTone: string;
  vibe: string[];
  avatarUrl?: string;
}

export type AppScreen = 
  | 'onboarding'
  | 'profile-setup'
  | 'avatar-refine'
  | 'home'
  | 'wardrobe'
  | 'quiz'
  | 'context-setup'
  | 'outfit-details'
  | 'settings'
  | 'notifications'
  | 'orders'
  | 'wishlist';
