import { butterfliesBackground } from 'https://unpkg.com/threejs-toys@0.0.8/build/threejs-toys.module.cdn.min.js'

// Initialize 3D swimming koi fish with proper fish movement and 3D geometry
const koiSystem = butterfliesBackground({
  el: document.getElementById('app'),
  eventsEl: document.body,
  gpgpuSize: 12, // Fewer fish for better performance and realism
  background: 0x001133, // Deep water blue
  material: 'phong', // Phong material for better 3D appearance
  lights: [
    { type: 'ambient', params: [0x4488BB, 0.6] }, // Underwater ambient lighting
    { type: 'directional', params: [0x88DDFF, 0.8], props: { position: [10, 20, 10] } }, // Sunlight from above
    { type: 'point', params: [0xFFFFFF, 0.4], props: { position: [0, 10, 0] } } // Underwater point light
  ],
  materialParams: { 
    transparent: true, 
    alphaTest: 0.3,
    shininess: 80, // Wet fish shininess
    specular: 0x99CCFF // Specular highlights like fish scales
  },
  
  // 3D Fish texture designed for depth and volume
  texture: 'data:image/svg+xml;base64,' + btoa(`
    <svg width="200" height="80" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <!-- Orange Koi body with 3D shading -->
        <radialGradient id="orangeKoi" cx="35%" cy="40%">
          <stop offset="0%" style="stop-color:#FF7733"/>
          <stop offset="30%" style="stop-color:#FF9955"/>
          <stop offset="70%" style="stop-color:#FFBB77"/>
          <stop offset="100%" style="stop-color:#FFDDAA"/>
        </radialGradient>
        
        <!-- White Koi with depth -->
        <radialGradient id="whiteKoi" cx="35%" cy="40%">
          <stop offset="0%" style="stop-color:#FFFFFF"/>
          <stop offset="50%" style="stop-color:#F8F8F8"/>
          <stop offset="100%" style="stop-color:#E8E8E8"/>
        </radialGradient>
        
        <!-- Fin material with transparency -->
        <linearGradient id="finGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#FFFFFF" stop-opacity="0.9"/>
          <stop offset="100%" style="stop-color:#CCDDEE" stop-opacity="0.6"/>
        </linearGradient>
        
        <!-- Scale texture for 3D effect -->
        <pattern id="scalePattern" x="0" y="0" width="4" height="3" patternUnits="userSpaceOnUse">
          <circle cx="2" cy="1.5" r="1" fill="none" stroke="#FFFFFF" stroke-width="0.2" opacity="0.4"/>
        </pattern>
      </defs>
      
      <!-- Fish 1: Orange Koi with 3D body shape -->
      <g transform="translate(0,0)">
        <!-- Main body - elongated for 3D effect -->
        <ellipse cx="100" cy="40" rx="60" ry="20" fill="url(#orangeKoi)" stroke="#DD5522" stroke-width="1"/>
        
        <!-- Head section with taper -->
        <ellipse cx="150" cy="40" rx="25" ry="16" fill="url(#orangeKoi)" stroke="#DD5522" stroke-width="0.8"/>
        
        <!-- Tail body section -->
        <ellipse cx="50" cy="40" rx="15" ry="14" fill="url(#orangeKoi)"/>
        
        <!-- Caudal (tail) fin - flowing -->
        <path d="M35 40 L15 28 L20 36 L25 40 L20 44 L15 52 Z" fill="url(#finGrad)" stroke="#FF8844" stroke-width="1"/>
        
        <!-- Dorsal fin on top -->
        <path d="M80 20 Q95 12 110 18 Q100 24 85 26 Q80 22 80 20" fill="url(#finGrad)" stroke="#FF8844" stroke-width="0.8"/>
        
        <!-- Pectoral fins (side fins) for 3D effect -->
        <ellipse cx="130" cy="32" rx="12" ry="8" fill="url(#finGrad)" transform="rotate(-20 130 32)" stroke="#FF8844" stroke-width="0.6"/>
        <ellipse cx="130" cy="48" rx="12" ry="8" fill="url(#finGrad)" transform="rotate(20 130 48)" stroke="#FF8844" stroke-width="0.6"/>
        
        <!-- Pelvic fins -->
        <ellipse cx="110" cy="52" rx="8" ry="5" fill="url(#finGrad)" stroke="#FF8844" stroke-width="0.5"/>
        <ellipse cx="90" cy="52" rx="8" ry="5" fill="url(#finGrad)" stroke="#FF8844" stroke-width="0.5"/>
        
        <!-- Eye with 3D appearance -->
        <circle cx="160" cy="36" r="5" fill="white" stroke="#333" stroke-width="0.8"/>
        <circle cx="161" cy="36" r="3" fill="black"/>
        <circle cx="162" cy="35" r="1" fill="white"/>
        
        <!-- Mouth -->
        <ellipse cx="175" cy="42" rx="4" ry="2" fill="#FFB6C1"/>
        
        <!-- Scale pattern for texture -->
        <ellipse cx="100" cy="40" rx="55" ry="15" fill="url(#scalePattern)"/>
        
        <!-- Highlight for 3D volume -->
        <ellipse cx="90" cy="35" rx="20" ry="6" fill="#FFFFFF" opacity="0.3"/>
      </g>
      
      <!-- Fish 2: White Koi for variety -->
      <g transform="translate(0,20)" opacity="0.95">
        <ellipse cx="100" cy="40" rx="55" ry="18" fill="url(#whiteKoi)" stroke="#DDDDDD" stroke-width="0.8"/>
        <ellipse cx="145" cy="40" rx="22" ry="14" fill="url(#whiteKoi)" stroke="#DDDDDD" stroke-width="0.6"/>
        <ellipse cx="55" cy="40" rx="12" ry="12" fill="url(#whiteKoi)"/>
        
        <!-- Red tancho spot -->
        <ellipse cx="145" cy="36" rx="6" ry="4" fill="#DD2222"/>
        
        <!-- Fins -->
        <path d="M43 40 L25 30 L28 38 L32 40 L28 42 L25 50 Z" fill="url(#finGrad)" stroke="#DDDDDD" stroke-width="0.8"/>
        <path d="M78 24 Q90 18 100 22 Q92 26 82 28 Q78 25 78 24" fill="url(#finGrad)" stroke="#DDDDDD" stroke-width="0.6"/>
        
        <circle cx="155" cy="37" r="4" fill="white" stroke="#333" stroke-width="0.6"/>
        <circle cx="156" cy="37" r="2.5" fill="black"/>
        <ellipse cx="167" cy="41" rx="3" ry="1.5" fill="#FFB6C1"/>
        
        <ellipse cx="100" cy="40" rx="50" ry="13" fill="url(#scalePattern)"/>
        <ellipse cx="92" cy="36" rx="18" ry="5" fill="#FFFFFF" opacity="0.2"/>
      </g>
    </svg>
  `),
  textureCount: 2, // Two fish variants for performance
  
  // 3D Fish body proportions (not flat butterfly wings)
  wingsScale: [3.0, 1.0, 0.5], // Length, width, thickness - creates proper fish volume
  wingsWidthSegments: 16, // Enough segments for smooth fish curves
  wingsHeightSegments: 10,
  
  // SWIMMING motion parameters (not flying)
  wingsSpeed: 0.08, // Very slow, graceful swimming motion
  wingsDisplacementScale: 0.15, // Gentle body undulation like real fish swimming
  
  // Fish swimming patterns (horizontal movement, not vertical flying)
  noiseCoordScale: 0.001, // Extremely smooth movement - fish glide gracefully
  noiseTimeCoef: 0.00005, // Very slow time progression for calm underwater movement
  noiseIntensity: 0.0005, // Minimal random movement - fish swim purposefully
  
  // Underwater schooling behavior
  attractionRadius1: 80, // Close schooling distance
  attractionRadius2: 150, // Loose group formation
  maxVelocity: 0.025, // Slow, realistic swimming speed
  
  // Fish-specific 3D rotation
  wingsRotation: 0.3, // Gentle body rotation while swimming
  wingsBeat: 0.05, // Very subtle fin movement (not wing flapping)
  
  // 3D underwater environment
  cameraPosition: [0, 0, 200], // Camera position for underwater view
  cameraTarget: [0, 0, 0],
  
  // Fish depth and layering
  zRange: 100, // Swimming depth variation in the water column
  
  // Custom fish swimming behavior
  customUpdate: (mesh, i) => {
    // Add gentle vertical bobbing like real fish
    mesh.position.y += Math.sin(Date.now() * 0.0008 + i) * 0.02;
    
    // Add subtle side-to-side movement
    mesh.position.x += Math.cos(Date.now() * 0.0006 + i * 2) * 0.01;
    
    // Gentle rotation around fish's central axis
    mesh.rotation.z += Math.sin(Date.now() * 0.0004 + i) * 0.008;
    
    // Fish-like forward swimming motion
    mesh.rotation.y = Math.atan2(mesh.userData.velocity.x, mesh.userData.velocity.z) || 0;
  }
});

// Export the system for potential controls
window.koiSystem = koiSystem;
