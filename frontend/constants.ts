
import { StyleOption, ProductItem, Outfit } from './types';

export const STYLE_OPTIONS: StyleOption[] = [
  {
    id: 'edgy',
    name: 'Edgy',
    image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDGAqFE3_w8YJs5zhq46ftRHiLXnkLW0Oa4YZTD59OWot3Lql89_-XZSE4Bk6q4Egb0Ahhfo_lfSeNjVZQGwS25v-qWl7o9MFe1RAA9MuR4BWaBVRu4JPDlLcmiqZMfg5rCzgx_I9CCCKjpEehk49EhZpSa__RhMJh2SpbPiNpPsXITRTZ6mmaVMZIZLMdkQp_ydMd8anH69pbCilZqfYxJNBFdoRLbKCYt770G8W4qLRE4b4bMrSeegJdAJ1zD4Z0PMeghTbj010Gy',
    highMatch: true
  },
  {
    id: 'elegant',
    name: 'Elegant',
    image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuD24gdrOF3_8B0JhwYI8_Vo4SmuMfZz8e-kPOXpkBW9yi5Sa6PooCTpCQ6VDQ1WIW5Oag_pN8SrIWx9t1XekAuyOoQac3BYE84aVf2cphfqSie1mpnaCahooqlX2qHzc_KrRHM_67HRmNLttZOdHNJ-NJ6Hf5igEZYdfzS0Qx7S3ILRQseBSoGXtmGWNzUe5QSIxrBFUVpC4khr-X1fUfU3MBgdCMGxfnKX4XE7DOJJfKvkf1zBQXPEMWozroMD511Sn9nJpflXlF0V'
  },
  {
    id: 'retro',
    name: 'Retro',
    image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCYz6zBN4dj3Vu6iDkOj7tWoBhYj6CKDsGpQaPphZJpG_igRUJMHWfy5zZGq-_7FjyZ-5kyrxioAQJzHh2Y06Ysx3YHoCq2fTZLzxuJyq6ddysZhShca4S2PbqKubVxwSqr30qm_35_ugdwcNwJ_IMn9HJRrotOh390N6Yw9OY1faRcz2MgCghSx_FDCGkTX2cezt6K4T29hYwp2wLSvQ8qCq9nqJK6rMjmt8GUxcN6a1d036f9QhjFHyzDI_Tjy-gKdElmduFpSCJv'
  },
  {
    id: 'sport',
    name: 'Sport',
    image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBz-iT_l4JEtthSwAN63g3LADbUFytuhRFqqkGka-pQtHmuP0_A20GN4RU6DgyqBQ6KJFGGiGjkNqQ_kmSxLHz2QyIwlF7KiJJU1gj-kesj4ysGLf3Ln4drmIh1p-Ah2LGZRrfOsX78mRl2nWqF3vRoyuKpejwA3YlOYf7z1o69dsZtI0YEvH7UiOlGkzlGyR2HMKBnyAKvxZAP7vWu77RvwvcOGAdOHUGrc7ils8iR_21T0MUi7I75HFhEFAdsYni7cm5BDa0oKmsq'
  }
];

export const MOCK_PRODUCTS: ProductItem[] = [
  { id: '1', name: 'Structured Wool Blazer', brand: 'ACME STUDIOS', price: 295, currency: '$', image: 'https://picsum.photos/400/600?random=1' },
  { id: '2', name: 'Metallic Mini Bag', brand: 'URBAN DRIFT', price: 185, currency: '$', image: 'https://picsum.photos/400/600?random=2' },
  { id: '3', name: 'Runner XT White', brand: 'SPORTIVA', price: 120, currency: '$', image: 'https://picsum.photos/400/600?random=3' },
  { id: '4', name: 'Velvet Slip Dress', brand: 'NOIR', price: 59, currency: '$', image: 'https://picsum.photos/400/600?random=4', lowStock: true },
];

export const MOCK_OUTFITS: Outfit[] = [
  {
    id: 'neon-nights',
    name: 'Neon Nights',
    description: 'Perfect for late night urban exploration.',
    matchScore: 98,
    imageUrl: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDzXA9buoLTOU-GXOtYPQ35OmV1XKRAhutF65wVuuiOiqSxZzbaSNMZD-HdU93_CJVFKzylhi1jVzcWW0GpnFc9SeP_Gr3FZn6GNX0kaoLIyQhz3DK_RaO9-L8lEeQeu-OM9AEe6DdMWP2cR4_w60m-xPB7zyiHKyahdyCMJrxxr8TtUCd9ktsVKZTTx4JeSazRJ-CRhfybqqMnv9_6BQxsebW6ZGoJjIc3zJvCnfN8oMqPzd_Amta6jSMi5y7kB0Ex3ylQ4ipBEuc5',
    createdAt: 'Created yesterday',
    tags: ['Cyberpunk', 'Night Out'],
    items: MOCK_PRODUCTS.slice(0, 2)
  },
  {
    id: 'office-minimal',
    name: 'Office Minimal',
    description: 'Clean lines for a professional setting.',
    matchScore: 85,
    imageUrl: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBue7SrXaBDeerInEJL9cJL7SXeCDWQONNhoAE3xKa0lFaJ4JmizCTZnFBUh4bTrR91GV_uQJTFwuttpZroQIvtvh43aIsUJUNcIuamTHdyJmmr-OqclVVLOHIBdkxWOqGF0xxWBIHIDztaJuxbK0RAq-0XdpAALUK4iAXhX3dm8Bl23VCH26BnZVH22cS1EpagsfAo7ZMJWv1_6dfHlyUOvYL0NKM1m4Qd41mlzO7DEX-q-A276GYiNZlUakrwW0VtsIPWLAyxGxXf',
    createdAt: 'Last worn 2 days ago',
    tags: ['Work', 'Minimalist'],
    items: MOCK_PRODUCTS.slice(2, 4)
  }
];

export const VIBE_TAGS = ['Streetwear', 'Minimalist', 'Y2K', 'Avant-Garde', 'Old Money', 'Cyberpunk', 'Grunge'];
export const SKIN_TONES = ['#F9E4D4', '#EFD2BD', '#E2C0A5', '#C68642', '#8D5524', '#553318', '#311c0f'];
