import { butterfliesBackground } from 'https://unpkg.com/threejs-toys@0.0.8/build/threejs-toys.module.cdn.min.js'

const pc = butterfliesBackground({
  el: document.getElementById('app'),
  eventsEl: document.body,
  gpgpuSize: 18,
  background: 0x0066AA, // Ocean blue background
  material: 'phong',
  lights: [
    { type: 'ambient', params: [0xffffff, 0.5] },
    { type: 'directional', params: [0xffffff, 1], props: { position: [10, 0, 0] } }
  ],
  materialParams: { transparent: true, alphaTest: 0.5 },
  // Anatomically correct koi fish texture based on your specifications
  texture: 'data:image/svg+xml;base64,' + btoa(`
    <svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <!-- Orange Kohaku Koi -->
        <linearGradient id="koi1" x1="0%" y1="40%" x2="0%" y2="100%">
          <stop offset="0%" style="stop-color:#FF9933"/>
          <stop offset="50%" style="stop-color:#FFCC66"/>
          <stop offset="100%" style="stop-color:#FFFFFF"/>
        </linearGradient>
        
        <!-- White Tancho Koi -->
        <linearGradient id="koi2" x1="0%" y1="40%" x2="0%" y2="100%">
          <stop offset="0%" style="stop-color:#FFFEF7"/>
          <stop offset="100%" style="stop-color:#F8F8F8"/>
        </linearGradient>
        
        <!-- Black Karasu Koi -->
        <linearGradient id="koi3" x1="0%" y1="40%" x2="0%" y2="100%">
          <stop offset="0%" style="stop-color:#2C2C2C"/>
          <stop offset="50%" style="stop-color:#1A1A1A"/>
          <stop offset="100%" style="stop-color:#404040"/>
        </linearGradient>
        
        <!-- Golden Yamabuki Koi -->
        <linearGradient id="koi4" x1="0%" y1="40%" x2="0%" y2="100%">
          <stop offset="0%" style="stop-color:#FFD700"/>
          <stop offset="50%" style="stop-color:#FFC649"/>
          <stop offset="100%" style="stop-color:#FFEB9C"/>
        </linearGradient>
        
        <!-- Blue-gray Asagi Koi -->
        <linearGradient id="koi5" x1="0%" y1="40%" x2="0%" y2="100%">
          <stop offset="0%" style="stop-color:#4A6B8A"/>
          <stop offset="50%" style="stop-color:#6B8FB5"/>
          <stop offset="100%" style="stop-color:#E8F4FD"/>
        </linearGradient>
        
        <!-- Multicolored Sanke Koi -->
        <linearGradient id="koi6" x1="0%" y1="40%" x2="0%" y2="100%">
          <stop offset="0%" style="stop-color:#FFFEF7"/>
          <stop offset="30%" style="stop-color:#FF6B35"/>
          <stop offset="70%" style="stop-color:#2C2C2C"/>
          <stop offset="100%" style="stop-color:#F8F8F8"/>
        </linearGradient>
        
        <!-- Transparent fin material -->
        <linearGradient id="finMaterial" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#FFFFFF" stop-opacity="0.8"/>
          <stop offset="100%" style="stop-color:#E0E0E0" stop-opacity="0.5"/>
        </linearGradient>
        
        <!-- Scale shimmer effect -->
        <radialGradient id="scaleShimmer" cx="30%" cy="20%">
          <stop offset="0%" style="stop-color:#FFFFFF" stop-opacity="0.6"/>
          <stop offset="50%" style="stop-color:#FFD700" stop-opacity="0.3"/>
          <stop offset="100%" style="stop-color:#40E0D0" stop-opacity="0.1"/>
        </radialGradient>
      </defs>
      
      <!-- Row 1: Orange, White, Black Koi -->
      <g transform="translate(0,0)">
        <!-- Orange Kohaku Koi - Following your anatomical specs -->
        
        <!-- Body: Streamlined torpedo shape (5-6x longer than width) -->
        <ellipse cx="120" cy="75" rx="90" ry="18" fill="url(#koi1)" stroke="#D2691E" stroke-width="0.8"/>
        <!-- Body capsule extension -->
        <rect x="30" y="57" width="180" height="36" fill="url(#koi1)" rx="18"/>
        
        <!-- Head: Rounded, slightly wider than body front -->
        <ellipse cx="210" cy="75" rx="25" ry="20" fill="url(#koi1)"/>
        
        <!-- Mouth at tip -->
        <ellipse cx="235" cy="78" rx="5" ry="3" fill="#FFB6C1"/>
        
        <!-- Caudal Fin (Tail): Large, flowing, fan-shaped -->
        <path d="M30 75 L5 50 L10 60 L15 75 L10 90 L5 100 Z" fill="url(#finMaterial)" stroke="#FFAA55" stroke-width="1"/>
        <!-- Secondary tail fin layer -->
        <path d="M25 75 L8 58 L12 68 L15 75 L12 82 L8 92 Z" fill="#FFCC66" opacity="0.7"/>
        
        <!-- Dorsal Fin: Long, thin, triangular when extended -->
        <path d="M80 57 Q100 45 130 50 Q120 57 100 60 Q80 57 80 57" fill="url(#finMaterial)" stroke="#FFAA55" stroke-width="0.8"/>
        
        <!-- Pectoral Fins: Two oval, fan-like fins near head -->
        <ellipse cx="190" cy="60" rx="18" ry="10" fill="url(#finMaterial)" transform="rotate(-30 190 60)" stroke="#FFAA55" stroke-width="0.5"/>
        <ellipse cx="190" cy="90" rx="18" ry="10" fill="url(#finMaterial)" transform="rotate(30 190 90)" stroke="#FFAA55" stroke-width="0.5"/>
        
        <!-- Pelvic Fins: Smaller paired fins under belly -->
        <ellipse cx="150" cy="88" rx="12" ry="6" fill="url(#finMaterial)" transform="rotate(-20 150 88)" stroke="#FFAA55" stroke-width="0.5"/>
        <ellipse cx="140" cy="88" rx="12" ry="6" fill="url(#finMaterial)" transform="rotate(20 140 88)" stroke="#FFAA55" stroke-width="0.5"/>
        
        <!-- Anal Fin: Single triangular fin behind pelvic fins -->
        <path d="M100 93 Q108 98 115 93 Q108 95 100 93" fill="url(#finMaterial)" stroke="#FFAA55" stroke-width="0.5"/>
        
        <!-- Eyes: Round, slightly protruding, on sides of head -->
        <circle cx="220" cy="68" r="5" fill="white" stroke="#333" stroke-width="0.8"/>
        <circle cx="221" cy="68" r="3" fill="black"/>
        <circle cx="222" cy="67" r="1" fill="white"/>
        
        <!-- Barbels (whiskers) near mouth corners -->
        <line x1="230" y1="80" x2="240" y2="83" stroke="#D2691E" stroke-width="1.5" opacity="0.8"/>
        <line x1="230" y1="76" x2="240" y2="73" stroke="#D2691E" stroke-width="1.5" opacity="0.8"/>
        
        <!-- Scale shimmer highlights -->
        <ellipse cx="100" cy="70" rx="15" ry="8" fill="url(#scaleShimmer)"/>
        <ellipse cx="140" cy="75" rx="12" ry="6" fill="url(#scaleShimmer)"/>
        <ellipse cx="170" cy="68" rx="10" ry="5" fill="url(#scaleShimmer)"/>
        
        <!-- Orange markings -->
        <ellipse cx="90" cy="72" rx="12" ry="8" fill="#FF6B35" opacity="0.8"/>
        <ellipse cx="130" cy="78" rx="8" ry="6" fill="#FF4500" opacity="0.7"/>
      </g>
      
      <g transform="translate(0,150)">
        <!-- White Tancho Koi -->
        <ellipse cx="120" cy="75" rx="90" ry="18" fill="url(#koi2)" stroke="#E6E6E6" stroke-width="0.8"/>
        <rect x="30" y="57" width="180" height="36" fill="url(#koi2)" rx="18"/>
        <ellipse cx="210" cy="75" rx="25" ry="20" fill="url(#koi2)"/>
        <ellipse cx="235" cy="78" rx="5" ry="3" fill="#FFB6C1"/>
        
        <!-- All fins with same structure -->
        <path d="M30 75 L5 50 L10 60 L15 75 L10 90 L5 100 Z" fill="url(#finMaterial)" stroke="#E6E6E6" stroke-width="1"/>
        <path d="M25 75 L8 58 L12 68 L15 75 L12 82 L8 92 Z" fill="#F8F8F8" opacity="0.7"/>
        <path d="M80 57 Q100 45 130 50 Q120 57 100 60 Q80 57 80 57" fill="url(#finMaterial)" stroke="#E6E6E6" stroke-width="0.8"/>
        <ellipse cx="190" cy="60" rx="18" ry="10" fill="url(#finMaterial)" transform="rotate(-30 190 60)" stroke="#E6E6E6" stroke-width="0.5"/>
        <ellipse cx="190" cy="90" rx="18" ry="10" fill="url(#finMaterial)" transform="rotate(30 190 90)" stroke="#E6E6E6" stroke-width="0.5"/>
        <ellipse cx="150" cy="88" rx="12" ry="6" fill="url(#finMaterial)" transform="rotate(-20 150 88)" stroke="#E6E6E6" stroke-width="0.5"/>
        <ellipse cx="140" cy="88" rx="12" ry="6" fill="url(#finMaterial)" transform="rotate(20 140 88)" stroke="#E6E6E6" stroke-width="0.5"/>
        <path d="M100 93 Q108 98 115 93 Q108 95 100 93" fill="url(#finMaterial)" stroke="#E6E6E6" stroke-width="0.5"/>
        
        <circle cx="220" cy="68" r="5" fill="white" stroke="#333" stroke-width="0.8"/>
        <circle cx="221" cy="68" r="3" fill="black"/>
        <circle cx="222" cy="67" r="1" fill="white"/>
        <line x1="230" y1="80" x2="240" y2="83" stroke="#C0C0C0" stroke-width="1.5" opacity="0.8"/>
        <line x1="230" y1="76" x2="240" y2="73" stroke="#C0C0C0" stroke-width="1.5" opacity="0.8"/>
        
        <!-- Tancho red spot on head -->
        <ellipse cx="210" cy="68" rx="8" ry="6" fill="#DC143C"/>
        
        <ellipse cx="100" cy="70" rx="15" ry="8" fill="url(#scaleShimmer)"/>
        <ellipse cx="140" cy="75" rx="12" ry="6" fill="url(#scaleShimmer)"/>
        <ellipse cx="170" cy="68" rx="10" ry="5" fill="url(#scaleShimmer)"/>
      </g>
      
      <!-- Additional koi varieties in remaining space following same anatomical structure -->
      <g transform="translate(300,0)">
        <!-- Black Karasu Koi -->
        <ellipse cx="120" cy="75" rx="90" ry="18" fill="url(#koi3)" stroke="#1A1A1A" stroke-width="0.8"/>
        <rect x="30" y="57" width="180" height="36" fill="url(#koi3)" rx="18"/>
        <ellipse cx="210" cy="75" rx="25" ry="20" fill="url(#koi3)"/>
        <ellipse cx="235" cy="78" rx="5" ry="3" fill="#FFB6C1"/>
        
        <path d="M30 75 L5 50 L10 60 L15 75 L10 90 L5 100 Z" fill="url(#finMaterial)" stroke="#1A1A1A" stroke-width="1"/>
        <path d="M25 75 L8 58 L12 68 L15 75 L12 82 L8 92 Z" fill="#2C2C2C" opacity="0.7"/>
        <path d="M80 57 Q100 45 130 50 Q120 57 100 60 Q80 57 80 57" fill="url(#finMaterial)" stroke="#1A1A1A" stroke-width="0.8"/>
        <ellipse cx="190" cy="60" rx="18" ry="10" fill="url(#finMaterial)" transform="rotate(-30 190 60)" stroke="#1A1A1A" stroke-width="0.5"/>
        <ellipse cx="190" cy="90" rx="18" ry="10" fill="url(#finMaterial)" transform="rotate(30 190 90)" stroke="#1A1A1A" stroke-width="0.5"/>
        <ellipse cx="150" cy="88" rx="12" ry="6" fill="url(#finMaterial)" transform="rotate(-20 150 88)" stroke="#1A1A1A" stroke-width="0.5"/>
        <ellipse cx="140" cy="88" rx="12" ry="6" fill="url(#finMaterial)" transform="rotate(20 140 88)" stroke="#1A1A1A" stroke-width="0.5"/>
        <path d="M100 93 Q108 98 115 93 Q108 95 100 93" fill="url(#finMaterial)" stroke="#1A1A1A" stroke-width="0.5"/>
        
        <circle cx="220" cy="68" r="5" fill="white" stroke="#333" stroke-width="0.8"/>
        <circle cx="221" cy="68" r="3" fill="black"/>
        <circle cx="222" cy="67" r="1" fill="white"/>
        <line x1="230" y1="80" x2="240" y2="83" stroke="#4A4A4A" stroke-width="1.5" opacity="0.8"/>
        <line x1="230" y1="76" x2="240" y2="73" stroke="#4A4A4A" stroke-width="1.5" opacity="0.8"/>
        
        <ellipse cx="100" cy="70" rx="15" ry="8" fill="url(#scaleShimmer)"/>
        <ellipse cx="140" cy="75" rx="12" ry="6" fill="url(#scaleShimmer)"/>
      </g>
      
      <g transform="translate(300,150)">
        <!-- Golden Yamabuki Koi -->
        <ellipse cx="120" cy="75" rx="90" ry="18" fill="url(#koi4)" stroke="#B8860B" stroke-width="0.8"/>
        <rect x="30" y="57" width="180" height="36" fill="url(#koi4)" rx="18"/>
        <ellipse cx="210" cy="75" rx="25" ry="20" fill="url(#koi4)"/>
        <ellipse cx="235" cy="78" rx="5" ry="3" fill="#FFB6C1"/>
        
        <path d="M30 75 L5 50 L10 60 L15 75 L10 90 L5 100 Z" fill="url(#finMaterial)" stroke="#B8860B" stroke-width="1"/>
        <path d="M25 75 L8 58 L12 68 L15 75 L12 82 L8 92 Z" fill="#FFD700" opacity="0.7"/>
        <path d="M80 57 Q100 45 130 50 Q120 57 100 60 Q80 57 80 57" fill="url(#finMaterial)" stroke="#B8860B" stroke-width="0.8"/>
        <ellipse cx="190" cy="60" rx="18" ry="10" fill="url(#finMaterial)" transform="rotate(-30 190 60)" stroke="#B8860B" stroke-width="0.5"/>
        <ellipse cx="190" cy="90" rx="18" ry="10" fill="url(#finMaterial)" transform="rotate(30 190 90)" stroke="#B8860B" stroke-width="0.5"/>
        <ellipse cx="150" cy="88" rx="12" ry="6" fill="url(#finMaterial)" transform="rotate(-20 150 88)" stroke="#B8860B" stroke-width="0.5"/>
        <ellipse cx="140" cy="88" rx="12" ry="6" fill="url(#finMaterial)" transform="rotate(20 140 88)" stroke="#B8860B" stroke-width="0.5"/>
        <path d="M100 93 Q108 98 115 93 Q108 95 100 93" fill="url(#finMaterial)" stroke="#B8860B" stroke-width="0.5"/>
        
        <circle cx="220" cy="68" r="5" fill="white" stroke="#333" stroke-width="0.8"/>
        <circle cx="221" cy="68" r="3" fill="black"/>
        <circle cx="222" cy="67" r="1" fill="white"/>
        <line x1="230" y1="80" x2="240" y2="83" stroke="#B8860B" stroke-width="1.5" opacity="0.8"/>
        <line x1="230" y1="76" x2="240" y2="73" stroke="#B8860B" stroke-width="1.5" opacity="0.8"/>
        
        <ellipse cx="100" cy="70" rx="15" ry="8" fill="url(#scaleShimmer)"/>
        <ellipse cx="140" cy="75" rx="12" ry="6" fill="url(#scaleShimmer)"/>
        <ellipse cx="170" cy="68" rx="10" ry="5" fill="url(#scaleShimmer)"/>
      </g>
    </svg>
  `),
  textureCount: 4, // 4 anatomically correct koi varieties
        
        <!-- White koi with orange/red spots (tancho style) -->
        <linearGradient id="koi2" x1="0%" y1="30%" x2="0%" y2="100%">
          <stop offset="0%" style="stop-color:#FFFEF7"/>
          <stop offset="100%" style="stop-color:#F8F8F8"/>
        </linearGradient>
        
        <!-- Black koi (karasu style) -->
        <linearGradient id="koi3" x1="0%" y1="30%" x2="0%" y2="100%">
          <stop offset="0%" style="stop-color:#2C2C2C"/>
          <stop offset="50%" style="stop-color:#1A1A1A"/>
          <stop offset="100%" style="stop-color:#0F0F0F"/>
        </linearGradient>
        
        <!-- Golden yellow koi (yamabuki style) -->
        <linearGradient id="koi4" x1="0%" y1="30%" x2="0%" y2="100%">
          <stop offset="0%" style="stop-color:#FFD700"/>
          <stop offset="50%" style="stop-color:#FFC649"/>
          <stop offset="100%" style="stop-color:#FFEB9C"/>
        </linearGradient>
        
        <!-- Blue-gray koi (asagi style) -->
        <linearGradient id="koi5" x1="0%" y1="30%" x2="0%" y2="100%">
          <stop offset="0%" style="stop-color:#4A6B8A"/>
          <stop offset="50%" style="stop-color:#6B8FB5"/>
          <stop offset="100%" style="stop-color:#E8F4FD"/>
        </linearGradient>
        
        <!-- Multicolored koi (sanke style) -->
        <linearGradient id="koi6" x1="0%" y1="30%" x2="0%" y2="100%">
          <stop offset="0%" style="stop-color:#FFFEF7"/>
          <stop offset="30%" style="stop-color:#FF6B35"/>
          <stop offset="70%" style="stop-color:#2C2C2C"/>
          <stop offset="100%" style="stop-color:#F8F8F8"/>
        </linearGradient>
        
        <!-- Fin material -->
        <linearGradient id="finGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#FFFFFF" stop-opacity="0.9"/>
          <stop offset="100%" style="stop-color:#E0E0E0" stop-opacity="0.7"/>
        </linearGradient>
      </defs>
      
      <!-- Row 1: Orange, White, Black Koi -->
      <g transform="translate(0,0)">
        <!-- Orange Kohaku Koi - streamlined fish body -->
        <ellipse cx="90" cy="64" rx="75" ry="28" fill="url(#koi1)" stroke="#D2691E" stroke-width="1"/>
        <!-- Tapered head -->
        <ellipse cx="140" cy="64" rx="35" ry="22" fill="url(#koi1)"/>
        <!-- Mouth -->
        <ellipse cx="165" cy="67" rx="8" ry="4" fill="#FFB6C1"/>
        <!-- Elegant forked tail -->
        <path d="M10 64 L0 45 L8 50 L12 64 L8 78 L0 83 Z" fill="url(#finGradient)" stroke="#D2691E" stroke-width="0.5"/>
        <!-- Secondary tail fin -->
        <path d="M15 64 L5 52 L10 58 L12 64 L10 70 L5 76 Z" fill="#FF8C42" opacity="0.8"/>
        <!-- Dorsal fin - curved and elegant -->
        <path d="M60 35 Q80 25 100 30 Q90 45 70 40 Q60 35 60 35" fill="url(#finGradient)" stroke="#D2691E" stroke-width="0.5"/>
        <!-- Pectoral fins -->
        <ellipse cx="110" cy="50" rx="15" ry="8" fill="url(#finGradient)" transform="rotate(-25 110 50)"/>
        <ellipse cx="110" cy="78" rx="15" ry="8" fill="url(#finGradient)" transform="rotate(25 110 78)"/>
        <!-- Realistic eye -->
        <circle cx="150" cy="58" r="7" fill="white" stroke="#333" stroke-width="1"/>
        <circle cx="152" cy="58" r="4" fill="black"/>
        <circle cx="153" cy="56" r="1.5" fill="white"/>
        <!-- Koi barbels (whiskers) -->
        <line x1="165" y1="70" x2="175" y2="72" stroke="#D2691E" stroke-width="2" opacity="0.8"/>
        <line x1="165" y1="65" x2="175" y2="62" stroke="#D2691E" stroke-width="2" opacity="0.8"/>
        <!-- Orange spots -->
        <ellipse cx="70" cy="58" rx="12" ry="8" fill="#FF4500" opacity="0.9"/>
        <ellipse cx="100" cy="70" rx="8" ry="6" fill="#FF6B35" opacity="0.8"/>
        <ellipse cx="85" cy="50" rx="6" ry="4" fill="#FF8C42" opacity="0.7"/>
      </g>
      
      <g transform="translate(170,0)">
        <!-- White Tancho Koi -->
        <ellipse cx="90" cy="64" rx="75" ry="28" fill="url(#koi2)" stroke="#E6E6E6" stroke-width="1"/>
        <ellipse cx="140" cy="64" rx="35" ry="22" fill="url(#koi2)"/>
        <ellipse cx="165" cy="67" rx="8" ry="4" fill="#FFB6C1"/>
        <path d="M10 64 L0 45 L8 50 L12 64 L8 78 L0 83 Z" fill="url(#finGradient)" stroke="#E6E6E6" stroke-width="0.5"/>
        <path d="M15 64 L5 52 L10 58 L12 64 L10 70 L5 76 Z" fill="#F8F8F8" opacity="0.8"/>
        <path d="M60 35 Q80 25 100 30 Q90 45 70 40 Q60 35 60 35" fill="url(#finGradient)" stroke="#E6E6E6" stroke-width="0.5"/>
        <ellipse cx="110" cy="50" rx="15" ry="8" fill="url(#finGradient)" transform="rotate(-25 110 50)"/>
        <ellipse cx="110" cy="78" rx="15" ry="8" fill="url(#finGradient)" transform="rotate(25 110 78)"/>
        <circle cx="150" cy="58" r="7" fill="white" stroke="#333" stroke-width="1"/>
        <circle cx="152" cy="58" r="4" fill="black"/>
        <circle cx="153" cy="56" r="1.5" fill="white"/>
        <line x1="165" y1="70" x2="175" y2="72" stroke="#C0C0C0" stroke-width="2" opacity="0.8"/>
        <line x1="165" y1="65" x2="175" y2="62" stroke="#C0C0C0" stroke-width="2" opacity="0.8"/>
        <!-- Red spot on head (tancho marking) -->
        <ellipse cx="140" cy="55" rx="10" ry="8" fill="#DC143C"/>
        <!-- Orange spots -->
        <ellipse cx="80" cy="60" rx="8" ry="6" fill="#FF6B35"/>
        <ellipse cx="105" cy="72" rx="6" ry="4" fill="#FF4500"/>
      </g>
      
      <g transform="translate(340,0)">
        <!-- Black Karasu Koi -->
        <ellipse cx="90" cy="64" rx="75" ry="28" fill="url(#koi3)" stroke="#1A1A1A" stroke-width="1"/>
        <ellipse cx="140" cy="64" rx="35" ry="22" fill="url(#koi3)"/>
        <ellipse cx="165" cy="67" rx="8" ry="4" fill="#FFB6C1"/>
        <path d="M10 64 L0 45 L8 50 L12 64 L8 78 L0 83 Z" fill="url(#finGradient)" stroke="#1A1A1A" stroke-width="0.5"/>
        <path d="M15 64 L5 52 L10 58 L12 64 L10 70 L5 76 Z" fill="#2C2C2C" opacity="0.8"/>
        <path d="M60 35 Q80 25 100 30 Q90 45 70 40 Q60 35 60 35" fill="url(#finGradient)" stroke="#1A1A1A" stroke-width="0.5"/>
        <ellipse cx="110" cy="50" rx="15" ry="8" fill="url(#finGradient)" transform="rotate(-25 110 50)"/>
        <ellipse cx="110" cy="78" rx="15" ry="8" fill="url(#finGradient)" transform="rotate(25 110 78)"/>
        <circle cx="150" cy="58" r="7" fill="white" stroke="#333" stroke-width="1"/>
        <circle cx="152" cy="58" r="4" fill="black"/>
        <circle cx="153" cy="56" r="1.5" fill="white"/>
        <line x1="165" y1="70" x2="175" y2="72" stroke="#4A4A4A" stroke-width="2" opacity="0.8"/>
        <line x1="165" y1="65" x2="175" y2="62" stroke="#4A4A4A" stroke-width="2" opacity="0.8"/>
      </g>
      
      <!-- Row 2: Golden, Blue-Gray, Multicolored Koi -->
      <g transform="translate(0,128)">
        <!-- Golden Yamabuki Koi -->
        <ellipse cx="90" cy="64" rx="75" ry="28" fill="url(#koi4)" stroke="#B8860B" stroke-width="1"/>
        <ellipse cx="140" cy="64" rx="35" ry="22" fill="url(#koi4)"/>
        <ellipse cx="165" cy="67" rx="8" ry="4" fill="#FFB6C1"/>
        <path d="M10 64 L0 45 L8 50 L12 64 L8 78 L0 83 Z" fill="url(#finGradient)" stroke="#B8860B" stroke-width="0.5"/>
        <path d="M15 64 L5 52 L10 58 L12 64 L10 70 L5 76 Z" fill="#FFD700" opacity="0.8"/>
        <path d="M60 35 Q80 25 100 30 Q90 45 70 40 Q60 35 60 35" fill="url(#finGradient)" stroke="#B8860B" stroke-width="0.5"/>
        <ellipse cx="110" cy="50" rx="15" ry="8" fill="url(#finGradient)" transform="rotate(-25 110 50)"/>
        <ellipse cx="110" cy="78" rx="15" ry="8" fill="url(#finGradient)" transform="rotate(25 110 78)"/>
        <circle cx="150" cy="58" r="7" fill="white" stroke="#333" stroke-width="1"/>
        <circle cx="152" cy="58" r="4" fill="black"/>
        <circle cx="153" cy="56" r="1.5" fill="white"/>
        <line x1="165" y1="70" x2="175" y2="72" stroke="#B8860B" stroke-width="2" opacity="0.8"/>
        <line x1="165" y1="65" x2="175" y2="62" stroke="#B8860B" stroke-width="2" opacity="0.8"/>
      </g>
      
      <g transform="translate(170,128)">
        <!-- Blue-Gray Asagi Koi -->
        <ellipse cx="90" cy="64" rx="75" ry="28" fill="url(#koi5)" stroke="#4A6B8A" stroke-width="1"/>
        <ellipse cx="140" cy="64" rx="35" ry="22" fill="url(#koi5)"/>
        <ellipse cx="165" cy="67" rx="8" ry="4" fill="#FFB6C1"/>
        <path d="M10 64 L0 45 L8 50 L12 64 L8 78 L0 83 Z" fill="url(#finGradient)" stroke="#4A6B8A" stroke-width="0.5"/>
        <path d="M15 64 L5 52 L10 58 L12 64 L10 70 L5 76 Z" fill="#6B8FB5" opacity="0.8"/>
        <path d="M60 35 Q80 25 100 30 Q90 45 70 40 Q60 35 60 35" fill="url(#finGradient)" stroke="#4A6B8A" stroke-width="0.5"/>
        <ellipse cx="110" cy="50" rx="15" ry="8" fill="url(#finGradient)" transform="rotate(-25 110 50)"/>
        <ellipse cx="110" cy="78" rx="15" ry="8" fill="url(#finGradient)" transform="rotate(25 110 78)"/>
        <circle cx="150" cy="58" r="7" fill="white" stroke="#333" stroke-width="1"/>
        <circle cx="152" cy="58" r="4" fill="black"/>
        <circle cx="153" cy="56" r="1.5" fill="white"/>
        <line x1="165" y1="70" x2="175" y2="72" stroke="#4A6B8A" stroke-width="2" opacity="0.8"/>
        <line x1="165" y1="65" x2="175" y2="62" stroke="#4A6B8A" stroke-width="2" opacity="0.8"/>
        <!-- Blue scale pattern -->
        <ellipse cx="70" cy="55" rx="8" ry="6" fill="#4A6B8A" opacity="0.7"/>
        <ellipse cx="90" cy="62" rx="6" ry="4" fill="#6B8FB5" opacity="0.6"/>
      </g>
      
      <g transform="translate(340,128)">
        <!-- Multicolored Sanke Koi -->
        <ellipse cx="90" cy="64" rx="75" ry="28" fill="url(#koi6)" stroke="#E6E6E6" stroke-width="1"/>
        <ellipse cx="140" cy="64" rx="35" ry="22" fill="url(#koi6)"/>
        <ellipse cx="165" cy="67" rx="8" ry="4" fill="#FFB6C1"/>
        <path d="M10 64 L0 45 L8 50 L12 64 L8 78 L0 83 Z" fill="url(#finGradient)" stroke="#E6E6E6" stroke-width="0.5"/>
        <path d="M15 64 L5 52 L10 58 L12 64 L10 70 L5 76 Z" fill="#F8F8F8" opacity="0.8"/>
        <path d="M60 35 Q80 25 100 30 Q90 45 70 40 Q60 35 60 35" fill="url(#finGradient)" stroke="#E6E6E6" stroke-width="0.5"/>
        <ellipse cx="110" cy="50" rx="15" ry="8" fill="url(#finGradient)" transform="rotate(-25 110 50)"/>
        <ellipse cx="110" cy="78" rx="15" ry="8" fill="url(#finGradient)" transform="rotate(25 110 78)"/>
        <circle cx="150" cy="58" r="7" fill="white" stroke="#333" stroke-width="1"/>
        <circle cx="152" cy="58" r="4" fill="black"/>
        <circle cx="153" cy="56" r="1.5" fill="white"/>
        <line x1="165" y1="70" x2="175" y2="72" stroke="#C0C0C0" stroke-width="2" opacity="0.8"/>
        <line x1="165" y1="65" x2="175" y2="62" stroke="#C0C0C0" stroke-width="2" opacity="0.8"/>
        <!-- Mixed color patterns -->
        <ellipse cx="75" cy="58" rx="10" ry="7" fill="#FF6B35"/>
        <ellipse cx="95" cy="70" rx="7" ry="5" fill="#2C2C2C"/>
        <ellipse cx="115" cy="55" rx="6" ry="4" fill="#FF4500"/>
        <ellipse cx="125" cy="72" rx="5" ry="3" fill="#1A1A1A"/>
      </g>
    </svg>
  `),
  textureCount: 6, // 6 different koi varieties
  wingsScale: [3.2, 1.4, 0.8], // More fish-like proportions - longer body, narrower width
  wingsWidthSegments: 24, // More detailed geometry for fish shape
  wingsHeightSegments: 18,
  wingsSpeed: 0.3, // Slow, graceful fish swimming motion
  wingsDisplacementScale: 0.4, // Subtle fin movement like real fish
  noiseCoordScale: 0.006, // Smooth, realistic fish movement
  noiseTimeCoef: 0.0002, // Slow time changes for natural swimming
  noiseIntensity: 0.001, // Very subtle undulation
  attractionRadius1: 100, // Fish schooling behavior
  attractionRadius2: 160,
  maxVelocity: 0.05 // Calm, graceful koi swimming speed
})
