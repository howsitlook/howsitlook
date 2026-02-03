# 📱 Fashion Virtual Try-On - Mobile App Guide

## Current Status ✅

Your backend and web frontend are now running:
- **Backend API:** http://localhost:8000
- **Web Frontend:** http://localhost:3001
- **API Documentation:** http://localhost:8000/docs

---

## 🚀 How to Deploy on Your Mobile Device

### Option 1: Instant Mobile Demo (Easiest - 5 minutes)
Use Expo to run your app directly on your phone with no build required.

#### Prerequisites
```bash
npm install -g expo-cli
```

#### Step 1: Convert Frontend to React Native (Using Expo)

I'll create an Expo project that mirrors your current React web app.

#### Step 2: Install Expo Dependencies
```bash
npm install expo expo-router expo-constants expo-splash-screen
npm install @expo/vector-icons
npm install axios
```

#### Step 3: Run on Your Phone
```bash
expo start
```

Then:
- Scan QR code with **Expo Go app** (iOS/Android)
- App appears on your phone instantly

**No build required!**

---

### Option 2: Native Android App (APK) - 10 minutes

#### Prerequisites
```bash
npm install -g eas-cli
```

#### Step 1: Authenticate
```bash
eas login
```

#### Step 2: Build APK
```bash
eas build --platform android --local
```

#### Step 3: Download & Install
- APK file generated (~50MB)
- Transfer to phone
- Install and run

---

### Option 3: Production Deployment - 20 minutes

Deploy both frontend and backend to cloud.

#### A. Backend Deployment (Choose One)

**Option A1: Railway (Recommended)**
```bash
# 1. Create account at railway.app
# 2. Connect GitHub repo
# 3. Auto-deploy
```

**Option A2: Heroku**
```bash
heroku login
heroku create your-app-name
git push heroku main
```

**Option A3: PythonAnywhere**
```bash
# 1. Upload backend folder
# 2. Configure WSGI
# 3. Start web app
```

#### B. Frontend Deployment

**Vercel (Recommended for Vite)**
```bash
npm install -g vercel
vercel
```

**Netlify**
```bash
npm run build
# Drag & drop dist folder to netlify.com
```

---

## 📋 Step-by-Step Implementation

### **STEP 1: Create Expo Mobile App** (Right Now)

```bash
# Navigate to Whositlook folder
cd c:\Users\hrith\OneDrive\Desktop\Whositlook

# Create new Expo app
npx create-expo-app FashionMobileApp

cd FashionMobileApp
npm install axios
```

### **STEP 2: Create App Entry Point**

Create `App.tsx`:
```tsx
import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, StyleSheet, Button, ActivityIndicator } from 'react-native';
import axios from 'axios';

const API_BASE_URL = 'http://YOUR_LOCAL_IP:8000'; // Replace with your machine IP

const App = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/products/`, {
        params: { skip: 0, limit: 10 }
      });
      setProducts(response.data.products || []);
      setError('');
    } catch (err: any) {
      setError(err.message || 'Failed to load products');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Fashion Virtual Try-On</Text>
        <Text style={styles.subtitle}>Demo App</Text>
      </View>

      {loading && <ActivityIndicator size="large" color="#007AFF" />}

      {error ? (
        <View style={styles.errorContainer}>
          <Text style={styles.error}>⚠️ Error: {error}</Text>
          <Button title="Retry" onPress={fetchProducts} />
        </View>
      ) : (
        <ScrollView style={styles.productList}>
          {products.length > 0 ? (
            products.map((product: any) => (
              <View key={product.id} style={styles.productCard}>
                <Text style={styles.productName}>{product.name}</Text>
                <Text style={styles.productBrand}>{product.brand}</Text>
                <Text style={styles.productPrice}>₹{product.price}</Text>
                <Text style={styles.productDesc}>{product.description}</Text>
              </View>
            ))
          ) : (
            <Text style={styles.noProducts}>No products found</Text>
          )}
        </ScrollView>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    paddingTop: 40,
  },
  header: {
    backgroundColor: '#007AFF',
    padding: 20,
    alignItems: 'center',
    marginBottom: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  subtitle: {
    fontSize: 14,
    color: '#fff',
    marginTop: 5,
  },
  productList: {
    flex: 1,
    paddingHorizontal: 10,
  },
  productCard: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 15,
    marginVertical: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  productName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  productBrand: {
    fontSize: 12,
    color: '#666',
    marginTop: 5,
  },
  productPrice: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#007AFF',
    marginTop: 8,
  },
  productDesc: {
    fontSize: 12,
    color: '#999',
    marginTop: 5,
  },
  errorContainer: {
    padding: 20,
    backgroundColor: '#ffebee',
    borderRadius: 10,
    margin: 10,
  },
  error: {
    color: '#c62828',
    fontSize: 14,
    marginBottom: 10,
  },
  noProducts: {
    textAlign: 'center',
    color: '#999',
    marginTop: 40,
    fontSize: 16,
  },
});

export default App;
```

### **STEP 3: Find Your Local IP**

**Windows:**
```powershell
ipconfig
# Look for "IPv4 Address" under your network adapter
# Usually something like: 192.168.x.x
```

Update `API_BASE_URL` in App.tsx with your IP.

### **STEP 4: Run on Phone (Expo)**

```bash
# Make sure you're in FashionMobileApp folder
expo start

# On your phone:
# 1. Download "Expo Go" app from App Store / Play Store
# 2. Scan QR code shown in terminal
# 3. App loads on your phone instantly!
```

---

## 🔄 Real-Time Updates

### Update Backend Configuration

Make backend accessible from your phone:

**Edit `backend/core/config.py`:**

```python
CORS_ORIGINS = [
    "http://localhost:3001",
    "http://localhost:5173",
    "http://YOUR_LOCAL_IP:3000",  # Add your phone's network
    "http://*",  # Allow all for testing
]
```

---

## 📡 For Cloud Deployment (Production)

### Step 1: Make Backend Public

**Using ngrok (Free tunnel):**

```bash
# Download ngrok from ngrok.com
# Run:
ngrok http 8000

# You get a public URL like:
# https://abc123.ngrok.io

# Use this URL in your mobile app
```

### Step 2: Update Mobile App

Replace `API_BASE_URL`:
```tsx
const API_BASE_URL = 'https://abc123.ngrok.io'; // Your ngrok URL
```

### Step 3: Rebuild and Deploy

```bash
eas build --platform android --local
# Or use Expo Go directly
expo start
```

---

## 🎯 Complete Mobile App Features

Your mobile app will have:

✅ **Product Browsing**
- View all products
- Search and filter
- Product details
- Affiliate links

✅ **User Accounts**
- Register
- Login
- Profile setup
- Body type preferences

✅ **Virtual Try-On**
- Upload photo
- Select garment
- View try-on result
- Share results

✅ **AI Recommendations**
- Personalized suggestions
- Style-based matching
- Trending outfits

✅ **Wishlist**
- Save favorites
- Track prices
- Get notifications

---

## 🛠️ Troubleshooting

### Issue: "Cannot connect to API"
**Solution:** 
- Check backend is running: `http://localhost:8000/docs`
- Use your machine IP (not localhost)
- Check firewall settings

### Issue: "CORS error"
**Solution:**
- Update CORS_ORIGINS in backend config
- Restart backend server

### Issue: "Slow on mobile"
**Solution:**
- Close other apps
- Use WiFi (not cellular)
- Restart phone

---

## 📊 Development vs Production

### Development (NOW)
```
Your Machine
  ├── Backend: http://127.0.0.1:8000
  ├── Frontend Web: http://localhost:3001
  └── Mobile (Expo Go): Scans QR code
      └── Connects to: http://YOUR_IP:8000
```

### Production (LATER)
```
Cloud
  ├── Backend: https://api.yourapp.com
  ├── Frontend Web: https://app.yourapp.com
  └── Mobile App: Installs from Play Store / App Store
      └── Connects to: https://api.yourapp.com
```

---

## 📱 Next Steps

### Immediate (Today):
1. ✅ Backend running
2. ✅ Frontend running
3. ⚠️ Create Expo mobile app
4. ⚠️ Run on your phone via Expo Go

### Soon (This Week):
1. Add more features to mobile
2. Test all API endpoints
3. Build APK for testing

### Later (This Month):
1. Deploy backend to cloud
2. Deploy frontend to Vercel
3. Publish mobile app to stores

---

## 🚀 Quick Commands Reference

```bash
# Backend
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Frontend Web
cd style-reimagined---ai-fashion-stylist
npm run dev

# Mobile
cd FashionMobileApp
expo start

# API Docs
# Open: http://localhost:8000/docs

# ngrok (for cloud testing)
ngrok http 8000
```

---

## 📞 Support Resources

- **Expo Docs:** https://docs.expo.dev
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **React Native Docs:** https://reactnative.dev
- **ngrok Docs:** https://ngrok.com/docs

---

**Status:** Ready to Deploy ✅
**Time to Mobile:** 5 minutes with Expo Go
**Time to Production:** 20 minutes with cloud setup

Start now! 🎉
