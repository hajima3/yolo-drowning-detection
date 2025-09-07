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
  // Realistic 3D fish-shaped texture with proper body proportions
  texture: 'data:image/svg+xml;base64,' + btoa(`
    <svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <!-- Orange Koi gradient -->
        <radialGradient id="koi1" cx="60%" cy="30%">
          <stop offset="0%" style="stop-color:#FF9933"/>
          <stop offset="40%" style="stop-color:#FFCC66"/>
          <stop offset="80%" style="stop-color:#FFE4B3"/>
          <stop offset="100%" style="stop-color:#FFFFFF"/>
        </radialGradient>
        
        <!-- White Koi with subtle shading -->
        <radialGradient id="koi2" cx="60%" cy="30%">
          <stop offset="0%" style="stop-color:#FFFEF7"/>
          <stop offset="60%" style="stop-color:#F8F8F8"/>
          <stop offset="100%" style="stop-color:#E6E6E6"/>
        </radialGradient>
        
        <!-- Black Koi with metallic sheen -->
        <radialGradient id="koi3" cx="60%" cy="30%">
          <stop offset="0%" style="stop-color:#4A4A4A"/>
          <stop offset="40%" style="stop-color:#2C2C2C"/>
          <stop offset="80%" style="stop-color:#1A1A1A"/>
          <stop offset="100%" style="stop-color:#0F0F0F"/>
        </radialGradient>
        
        <!-- Golden Koi -->
        <radialGradient id="koi4" cx="60%" cy="30%">
          <stop offset="0%" style="stop-color:#FFD700"/>
          <stop offset="40%" style="stop-color:#FFC649"/>
          <stop offset="80%" style="stop-color:#FFEB9C"/>
          <stop offset="100%" style="stop-color:#FFF8DC"/>
        </radialGradient>
        
        <!-- Scale pattern overlay -->
        <pattern id="scales" x="0" y="0" width="8" height="6" patternUnits="userSpaceOnUse">
          <circle cx="4" cy="3" r="2.5" fill="none" stroke="#FFFFFF" stroke-width="0.3" opacity="0.4"/>
        </pattern>
        
        <!-- Fin transparency -->
        <linearGradient id="fins" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#FFFFFF" stop-opacity="0.9"/>
          <stop offset="100%" style="stop-color:#CCCCCC" stop-opacity="0.6"/>
        </linearGradient>
      </defs>
      
      <!-- Row 1: Fish shaped like actual koi -->
      <g transform="translate(0,0)">
        <!-- Orange Koi Fish Body - Proper fish silhouette -->
        <!-- Main body - oval fish shape -->
        <ellipse cx="120" cy="50" rx="70" ry="25" fill="url(#koi1)" stroke="#D2691E" stroke-width="1"/>
        <!-- Head taper -->
        <ellipse cx="180" cy="50" rx="35" ry="20" fill="url(#koi1)" stroke="#D2691E" stroke-width="0.8"/>
        <!-- Tail base -->
        <ellipse cx="60" cy="50" rx="20" ry="15" fill="url(#koi1)"/>
        
        <!-- Caudal (tail) fin - realistic fork shape -->
        <path d="M40 50 L10 35 L20 45 L25 50 L20 55 L10 65 Z" fill="url(#fins)" stroke="#FF8C42" stroke-width="1"/>
        
        <!-- Dorsal fin on top -->
        <path d="M100 25 Q120 15 140 25 Q130 35 110 35 Q100 30 100 25" fill="url(#fins)" stroke="#FF8C42" stroke-width="0.8"/>
        
        <!-- Pectoral fins (side fins) -->
        <ellipse cx="150" cy="40" rx="15" ry="8" fill="url(#fins)" transform="rotate(-20 150 40)" stroke="#FF8C42" stroke-width="0.6"/>
        <ellipse cx="150" cy="60" rx="15" ry="8" fill="url(#fins)" transform="rotate(20 150 60)" stroke="#FF8C42" stroke-width="0.6"/>
        
        <!-- Pelvic fins (bottom) -->
        <ellipse cx="110" cy="70" rx="10" ry="5" fill="url(#fins)" stroke="#FF8C42" stroke-width="0.5"/>
        <ellipse cx="130" cy="70" rx="10" ry="5" fill="url(#fins)" stroke="#FF8C42" stroke-width="0.5"/>
        
        <!-- Anal fin -->
        <path d="M90 65 Q100 75 110 65 Q100 70 90 65" fill="url(#fins)" stroke="#FF8C42" stroke-width="0.5"/>
        
        <!-- Eye -->
        <circle cx="190" cy="45" r="6" fill="white" stroke="#333" stroke-width="1"/>
        <circle cx="191" cy="45" r="4" fill="black"/>
        <circle cx="192" cy="43" r="1.5" fill="white"/>
        
        <!-- Mouth -->
        <ellipse cx="205" cy="52" rx="4" ry="2" fill="#FFB6C1"/>
        
        <!-- Barbels -->
        <line x1="200" y1="55" x2="210" y2="58" stroke="#D2691E" stroke-width="1.5" opacity="0.8"/>
        <line x1="200" y1="49" x2="210" y2="46" stroke="#D2691E" stroke-width="1.5" opacity="0.8"/>
        
        <!-- Scale pattern overlay -->
        <ellipse cx="120" cy="50" rx="65" ry="20" fill="url(#scales)"/>
        
        <!-- Orange markings -->
        <ellipse cx="100" cy="48" rx="15" ry="10" fill="#FF6B35" opacity="0.7"/>
        <ellipse cx="140" cy="52" rx="12" ry="8" fill="#FF4500" opacity="0.6"/>
      </g>
      
      <g transform="translate(200,0)">
        <!-- White Tancho Koi -->
        <ellipse cx="120" cy="50" rx="70" ry="25" fill="url(#koi2)" stroke="#E6E6E6" stroke-width="1"/>
        <ellipse cx="180" cy="50" rx="35" ry="20" fill="url(#koi2)" stroke="#E6E6E6" stroke-width="0.8"/>
        <ellipse cx="60" cy="50" rx="20" ry="15" fill="url(#koi2)"/>
        
        <path d="M40 50 L10 35 L20 45 L25 50 L20 55 L10 65 Z" fill="url(#fins)" stroke="#E6E6E6" stroke-width="1"/>
        <path d="M100 25 Q120 15 140 25 Q130 35 110 35 Q100 30 100 25" fill="url(#fins)" stroke="#E6E6E6" stroke-width="0.8"/>
        <ellipse cx="150" cy="40" rx="15" ry="8" fill="url(#fins)" transform="rotate(-20 150 40)" stroke="#E6E6E6" stroke-width="0.6"/>
        <ellipse cx="150" cy="60" rx="15" ry="8" fill="url(#fins)" transform="rotate(20 150 60)" stroke="#E6E6E6" stroke-width="0.6"/>
        <ellipse cx="110" cy="70" rx="10" ry="5" fill="url(#fins)" stroke="#E6E6E6" stroke-width="0.5"/>
        <ellipse cx="130" cy="70" rx="10" ry="5" fill="url(#fins)" stroke="#E6E6E6" stroke-width="0.5"/>
        <path d="M90 65 Q100 75 110 65 Q100 70 90 65" fill="url(#fins)" stroke="#E6E6E6" stroke-width="0.5"/>
        
        <circle cx="190" cy="45" r="6" fill="white" stroke="#333" stroke-width="1"/>
        <circle cx="191" cy="45" r="4" fill="black"/>
        <circle cx="192" cy="43" r="1.5" fill="white"/>
        <ellipse cx="205" cy="52" rx="4" ry="2" fill="#FFB6C1"/>
        <line x1="200" y1="55" x2="210" y2="58" stroke="#C0C0C0" stroke-width="1.5" opacity="0.8"/>
        <line x1="200" y1="49" x2="210" y2="46" stroke="#C0C0C0" stroke-width="1.5" opacity="0.8"/>
        
        <ellipse cx="120" cy="50" rx="65" ry="20" fill="url(#scales)"/>
        
        <!-- Tancho red spot -->
        <ellipse cx="180" cy="42" rx="8" ry="6" fill="#DC143C"/>
      </g>
      
      <!-- Row 2: More fish varieties -->
      <g transform="translate(0,100)">
        <!-- Black Koi -->
        <ellipse cx="120" cy="50" rx="70" ry="25" fill="url(#koi3)" stroke="#1A1A1A" stroke-width="1"/>
        <ellipse cx="180" cy="50" rx="35" ry="20" fill="url(#koi3)" stroke="#1A1A1A" stroke-width="0.8"/>
        <ellipse cx="60" cy="50" rx="20" ry="15" fill="url(#koi3)"/>
        
        <path d="M40 50 L10 35 L20 45 L25 50 L20 55 L10 65 Z" fill="url(#fins)" stroke="#4A4A4A" stroke-width="1"/>
        <path d="M100 25 Q120 15 140 25 Q130 35 110 35 Q100 30 100 25" fill="url(#fins)" stroke="#4A4A4A" stroke-width="0.8"/>
        <ellipse cx="150" cy="40" rx="15" ry="8" fill="url(#fins)" transform="rotate(-20 150 40)" stroke="#4A4A4A" stroke-width="0.6"/>
        <ellipse cx="150" cy="60" rx="15" ry="8" fill="url(#fins)" transform="rotate(20 150 60)" stroke="#4A4A4A" stroke-width="0.6"/>
        <ellipse cx="110" cy="70" rx="10" ry="5" fill="url(#fins)" stroke="#4A4A4A" stroke-width="0.5"/>
        <ellipse cx="130" cy="70" rx="10" ry="5" fill="url(#fins)" stroke="#4A4A4A" stroke-width="0.5"/>
        <path d="M90 65 Q100 75 110 65 Q100 70 90 65" fill="url(#fins)" stroke="#4A4A4A" stroke-width="0.5"/>
        
        <circle cx="190" cy="45" r="6" fill="white" stroke="#333" stroke-width="1"/>
        <circle cx="191" cy="45" r="4" fill="black"/>
        <circle cx="192" cy="43" r="1.5" fill="white"/>
        <ellipse cx="205" cy="52" rx="4" ry="2" fill="#FFB6C1"/>
        <line x1="200" y1="55" x2="210" y2="58" stroke="#666666" stroke-width="1.5" opacity="0.8"/>
        <line x1="200" y1="49" x2="210" y2="46" stroke="#666666" stroke-width="1.5" opacity="0.8"/>
        
        <ellipse cx="120" cy="50" rx="65" ry="20" fill="url(#scales)"/>
      </g>
      
      <g transform="translate(200,100)">
        <!-- Golden Koi -->
        <ellipse cx="120" cy="50" rx="70" ry="25" fill="url(#koi4)" stroke="#B8860B" stroke-width="1"/>
        <ellipse cx="180" cy="50" rx="35" ry="20" fill="url(#koi4)" stroke="#B8860B" stroke-width="0.8"/>
        <ellipse cx="60" cy="50" rx="20" ry="15" fill="url(#koi4)"/>
        
        <path d="M40 50 L10 35 L20 45 L25 50 L20 55 L10 65 Z" fill="url(#fins)" stroke="#B8860B" stroke-width="1"/>
        <path d="M100 25 Q120 15 140 25 Q130 35 110 35 Q100 30 100 25" fill="url(#fins)" stroke="#B8860B" stroke-width="0.8"/>
        <ellipse cx="150" cy="40" rx="15" ry="8" fill="url(#fins)" transform="rotate(-20 150 40)" stroke="#B8860B" stroke-width="0.6"/>
        <ellipse cx="150" cy="60" rx="15" ry="8" fill="url(#fins)" transform="rotate(20 150 60)" stroke="#B8860B" stroke-width="0.6"/>
        <ellipse cx="110" cy="70" rx="10" ry="5" fill="url(#fins)" stroke="#B8860B" stroke-width="0.5"/>
        <ellipse cx="130" cy="70" rx="10" ry="5" fill="url(#fins)" stroke="#B8860B" stroke-width="0.5"/>
        <path d="M90 65 Q100 75 110 65 Q100 70 90 65" fill="url(#fins)" stroke="#B8860B" stroke-width="0.5"/>
        
        <circle cx="190" cy="45" r="6" fill="white" stroke="#333" stroke-width="1"/>
        <circle cx="191" cy="45" r="4" fill="black"/>
        <circle cx="192" cy="43" r="1.5" fill="white"/>
        <ellipse cx="205" cy="52" rx="4" ry="2" fill="#FFB6C1"/>
        <line x1="200" y1="55" x2="210" y2="58" stroke="#B8860B" stroke-width="1.5" opacity="0.8"/>
        <line x1="200" y1="49" x2="210" y2="46" stroke="#B8860B" stroke-width="1.5" opacity="0.8"/>
        
        <ellipse cx="120" cy="50" rx="65" ry="20" fill="url(#scales)"/>
      </g>
    </svg>
  `),
  textureCount: 4, // 4 realistic koi fish
  wingsScale: [3.5, 1.8, 1.0], // More realistic fish body proportions
  wingsWidthSegments: 32, // Higher detail for smooth curves
  wingsHeightSegments: 24,
  wingsSpeed: 0.2, // Slower, more fish-like movement
  wingsDisplacementScale: 0.5, // Moderate undulation for swimming motion
  noiseCoordScale: 0.004, // Smoother movement patterns
  noiseTimeCoef: 0.0001, // Very slow time changes
  noiseIntensity: 0.002, // Subtle swimming movement
  attractionRadius1: 80, // Natural fish schooling
  attractionRadius2: 140,
  maxVelocity: 0.06 // Gentle swimming speed
})
