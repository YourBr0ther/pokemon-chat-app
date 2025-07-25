// PokeChat Service Worker
const CACHE_NAME = 'pokechat-v1.2.0';
const DATA_CACHE_NAME = 'pokechat-data-v1.2.0';

// Core app files to cache for offline functionality
const urlsToCache = [
  '/',
  '/chat',
  '/pokedex', 
  '/import',
  '/static/css/style.css',
  '/static/js/common.js',
  '/static/js/chat.js',
  '/static/js/pokedex.js',
  '/static/js/import.js',
  '/static/manifest.json',
  '/static/icon.png',
  '/static/favicon.ico'
];

// Pokemon sprites for popular Pokemon
const popularPokemonSprites = [
  'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png',   // Bulbasaur
  'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png',   // Charmander
  'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png',   // Squirtle
  'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png',  // Pikachu
  'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/150.png', // Mewtwo
  'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/151.png', // Mew
  'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/249.png', // Lugia
  'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/250.png'  // Ho-Oh
];

// Background sync configuration
const BACKGROUND_SYNC_TAG = 'pokechat-background-sync';
const MESSAGE_SYNC_TAG = 'pokechat-message-sync';

// Offline data storage
let offlineQueue = [];
let offlineTeamData = null;
let offlineChatHistory = new Map();

// Install event - cache resources with improved strategy
self.addEventListener('install', event => {
  console.log('PokeChat Service Worker: Installing...');
  event.waitUntil(
    Promise.all([
      // Cache core app shell
      caches.open(CACHE_NAME).then(cache => {
        console.log('PokeChat Service Worker: Caching app shell');
        return cache.addAll(urlsToCache);
      }),
      // Pre-cache popular Pokemon sprites
      caches.open(IMAGE_CACHE_NAME).then(cache => {
        console.log('PokeChat Service Worker: Pre-caching popular Pokemon sprites');
        return cache.addAll(popularPokemonSprites.slice(0, 4)); // Cache first 4 to avoid install delay
      })
    ]).then(() => {
      console.log('PokeChat Service Worker: Installed successfully');
      // Show install notification to user
      self.registration.showNotification('PokeChat Ready!', {
        body: 'PokeChat is now available offline. Your Pokemon are always with you!',
        icon: '/static/icons/icon-192x192.png',
        badge: '/static/icons/icon-72x72.png',
        tag: 'install-success',
        requireInteraction: false,
        silent: true
      });
      return self.skipWaiting();
    })
  );
});

// Activate event - clean up old caches and claim clients
self.addEventListener('activate', event => {
  console.log('PokeChat Service Worker: Activating...');
  event.waitUntil(
    Promise.all([
      // Clean up old caches
      caches.keys().then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => {
            if (![CACHE_NAME, DATA_CACHE_NAME, IMAGE_CACHE_NAME].includes(cacheName)) {
              console.log('PokeChat Service Worker: Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      }),
      // Initialize offline data structures
      initializeOfflineData()
    ]).then(() => {
      console.log('PokeChat Service Worker: Activated');
      return self.clients.claim();
    })
  );
});

// Initialize offline data storage
async function initializeOfflineData() {
  try {
    // Try to load existing offline data
    const existingData = await getStoredData('offline-team-data');
    if (existingData) {
      offlineTeamData = existingData;
    }
    
    const existingQueue = await getStoredData('offline-queue');
    if (existingQueue) {
      offlineQueue = existingQueue;
    }
  } catch (error) {
    console.log('PokeChat Service Worker: No existing offline data found');
  }
}

// Helper function to get stored data
async function getStoredData(key) {
  if ('indexedDB' in self) {
    // Use IndexedDB for larger data storage
    return new Promise((resolve, reject) => {
      const request = indexedDB.open('PokeChat', 1);
      request.onsuccess = () => {
        const db = request.result;
        const transaction = db.transaction(['offline'], 'readonly');
        const store = transaction.objectStore('offline');
        const getRequest = store.get(key);
        getRequest.onsuccess = () => resolve(getRequest.result?.data);
        getRequest.onerror = () => reject(getRequest.error);
      };
      request.onerror = () => reject(request.error);
    });
  }
  return null;
}

// Advanced fetch event with multiple caching strategies
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  
  // Handle API requests
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(handleApiRequest(event.request));
    return;
  }
  
  // Handle image requests (Pokemon sprites)
  if (event.request.destination === 'image' || url.href.includes('sprites')) {
    event.respondWith(handleImageRequest(event.request));
    return;
  }
  
  // Handle navigation requests
  if (event.request.mode === 'navigate') {
    event.respondWith(handleNavigationRequest(event.request));
    return;
  }
  
  // Handle static assets (CSS, JS)
  if (url.pathname.startsWith('/static/')) {
    event.respondWith(handleStaticAssetRequest(event.request));
    return;
  }
  
  // Default handling for other requests
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
      .catch(() => {
        console.log('PokeChat Service Worker: Request failed and no cache available');
        return new Response('Offline - content not available', { status: 503 });
      })
  );
});

// Handle API requests with network-first strategy and offline queue
async function handleApiRequest(request) {
  try {
    const response = await fetch(request);
    
    // Cache successful API responses
    if (response.ok) {
      const cache = await caches.open(DATA_CACHE_NAME);
      cache.put(request, response.clone());
    }
    
    return response;
  } catch (error) {
    console.log('PokeChat Service Worker: API request failed, checking cache');
    
    // Try to serve from cache
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // If POST request failed, add to offline queue
    if (request.method === 'POST') {
      const requestData = await request.clone().json().catch(() => null);
      if (requestData) {
        offlineQueue.push({
          url: request.url,
          method: request.method,
          data: requestData,
          timestamp: Date.now()
        });
        
        // Store offline queue persistently
        await storeData('offline-queue', offlineQueue);
        
        return new Response(JSON.stringify({
          success: false,
          queued: true,
          message: 'Request queued for when you\'re back online'
        }), {
          status: 202,
          headers: { 'Content-Type': 'application/json' }
        });
      }
    }
    
    return new Response(JSON.stringify({
      error: 'Offline - please check your connection'
    }), {
      status: 503,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Handle image requests with cache-first strategy
async function handleImageRequest(request) {
  const cachedResponse = await caches.match(request);
  if (cachedResponse) {
    return cachedResponse;
  }
  
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(IMAGE_CACHE_NAME);
      cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    // Return placeholder image for offline Pokemon sprites
    return new Response(await generatePlaceholderImage(), {
      headers: { 'Content-Type': 'image/svg+xml' }
    });
  }
}

// Handle navigation requests with app shell
async function handleNavigationRequest(request) {
  try {
    const response = await fetch(request);
    return response;
  } catch (error) {
    // Serve cached version of the page or app shell
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Fallback to app shell
    return caches.match('/');
  }
}

// Handle static assets with cache-first strategy
async function handleStaticAssetRequest(request) {
  const cachedResponse = await caches.match(request);
  if (cachedResponse) {
    return cachedResponse;
  }
  
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    return new Response('Asset not available offline', { status: 503 });
  }
}

// Generate placeholder image for offline Pokemon sprites
async function generatePlaceholderImage() {
  return `<svg width="96" height="96" xmlns="http://www.w3.org/2000/svg">
    <rect width="96" height="96" fill="#334155" rx="8"/>
    <text x="48" y="35" text-anchor="middle" fill="#64748b" font-family="Arial" font-size="10">Pokemon</text>
    <text x="48" y="50" text-anchor="middle" fill="#64748b" font-family="Arial" font-size="8">Offline</text>
    <circle cx="48" cy="65" r="8" fill="#64748b"/>
  </svg>`;
}

// Store data persistently
async function storeData(key, data) {
  if ('indexedDB' in self) {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open('PokeChat', 1);
      request.onupgradeneeded = () => {
        const db = request.result;
        if (!db.objectStoreNames.contains('offline')) {
          db.createObjectStore('offline', { keyPath: 'id' });
        }
      };
      request.onsuccess = () => {
        const db = request.result;
        const transaction = db.transaction(['offline'], 'readwrite');
        const store = transaction.objectStore('offline');
        store.put({ id: key, data: data });
        transaction.oncomplete = () => resolve();
        transaction.onerror = () => reject(transaction.error);
      };
      request.onerror = () => reject(request.error);
    });
  }
}

// Enhanced background sync for failed API requests
self.addEventListener('sync', event => {
  console.log('PokeChat Service Worker: Background sync triggered with tag:', event.tag);
  
  if (event.tag === BACKGROUND_SYNC_TAG) {
    event.waitUntil(processOfflineQueue());
  } else if (event.tag === MESSAGE_SYNC_TAG) {
    event.waitUntil(syncChatMessages());
  }
});

// Process offline queue when back online
async function processOfflineQueue() {
  console.log('PokeChat Service Worker: Processing offline queue');
  
  if (offlineQueue.length === 0) {
    return;
  }
  
  const failedRequests = [];
  
  for (const queuedRequest of offlineQueue) {
    try {
      const response = await fetch(queuedRequest.url, {
        method: queuedRequest.method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(queuedRequest.data)
      });
      
      if (response.ok) {
        console.log('PokeChat Service Worker: Successfully synced queued request');
      } else {
        failedRequests.push(queuedRequest);
      }
    } catch (error) {
      console.log('PokeChat Service Worker: Failed to sync request:', error);
      failedRequests.push(queuedRequest);
    }
  }
  
  // Update queue with only failed requests
  offlineQueue = failedRequests;
  await storeData('offline-queue', offlineQueue);
  
  // Notify user of sync results
  if (failedRequests.length === 0) {
    self.registration.showNotification('PokeChat Synced!', {
      body: 'All your offline actions have been synchronized.',
      icon: '/static/icons/icon-192x192.png',
      tag: 'sync-success',
      requireInteraction: false
    });
  }
}

// Sync chat messages
async function syncChatMessages() {
  console.log('PokeChat Service Worker: Syncing chat messages');
  
  // Notify connected clients about sync
  const clients = await self.clients.matchAll();
  clients.forEach(client => {
    client.postMessage({
      type: 'SYNC_COMPLETE',
      data: { syncType: 'messages' }
    });
  });
}

// Enhanced push notifications with Pokemon-themed content
self.addEventListener('push', event => {
  console.log('PokeChat Service Worker: Push notification received');
  
  let notificationData = {
    title: 'PokeChat',
    body: 'You have a new message from your Pokemon!',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/icon-72x72.png'
  };
  
  if (event.data) {
    try {
      const data = event.data.json();
      notificationData = {
        ...notificationData,
        title: data.title || `Message from ${data.pokemon || 'Pokemon'}`,
        body: data.body || data.message || 'Your Pokemon wants to chat with you!',
        tag: `pokemon-${data.pokemonId || 'general'}`,
        data: {
          pokemonId: data.pokemonId,
          url: data.url || `/chat${data.pokemonId ? `?pokemon=${data.pokemonId}` : ''}`,
          timestamp: Date.now()
        },
        actions: [
          {
            action: 'reply',
            title: '💬 Reply',
            icon: '/static/icons/icon-96x96.png'
          },
          {
            action: 'view',
            title: '👀 View Chat',
            icon: '/static/icons/icon-96x96.png'
          }
        ],
        vibrate: [200, 100, 200],
        requireInteraction: true
      };
      
      // Add Pokemon-specific styling
      if (data.pokemon) {
        notificationData.body = `${data.pokemon} says: "${data.message || 'Hello trainer!'}"`;
      }
      
    } catch (error) {
      console.log('PokeChat Service Worker: Error parsing push data:', error);
    }
  }
  
  event.waitUntil(
    self.registration.showNotification(notificationData.title, notificationData)
  );
});

// Handle notification interactions
self.addEventListener('notificationclick', event => {
  console.log('PokeChat Service Worker: Notification clicked');
  
  event.notification.close();
  
  const notificationData = event.notification.data || {};
  const action = event.action;
  
  let urlToOpen = '/chat';
  
  if (notificationData.url) {
    urlToOpen = notificationData.url;
  } else if (notificationData.pokemonId) {
    urlToOpen = `/chat?pokemon=${notificationData.pokemonId}`;
  }
  
  if (action === 'reply') {
    // Open chat page for quick reply
    urlToOpen = urlToOpen + (urlToOpen.includes('?') ? '&' : '?') + 'action=reply';
  } else if (action === 'view') {
    // Just open the chat page
    urlToOpen = urlToOpen;
  }
  
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true })
      .then(clientList => {
        // Check if app is already open
        for (const client of clientList) {
          if (client.url.includes('/chat') && 'focus' in client) {
            client.focus();
            client.postMessage({
              type: 'NOTIFICATION_CLICK',
              action: action,
              data: notificationData
            });
            return;
          }
        }
        
        // Open new window/tab if not already open
        if (clients.openWindow) {
          return clients.openWindow(urlToOpen);
        }
      })
  );
});

// Handle notification close
self.addEventListener('notificationclose', event => {
  console.log('PokeChat Service Worker: Notification closed');
  
  // Track notification engagement analytics if needed
  const notificationData = event.notification.data || {};
  if (notificationData.pokemonId) {
    console.log(`Notification for Pokemon ${notificationData.pokemonId} was dismissed`);
  }
});

// Message handling for communication with main app
self.addEventListener('message', event => {
  console.log('PokeChat Service Worker: Message received:', event.data);
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  } else if (event.data && event.data.type === 'GET_VERSION') {
    event.ports[0].postMessage({ version: CACHE_NAME });
  } else if (event.data && event.data.type === 'SYNC_REQUEST') {
    // Trigger background sync
    self.registration.sync.register(BACKGROUND_SYNC_TAG);
  }
});