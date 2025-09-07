import * as THREE from 'https://unpkg.com/three@0.157.0/build/three.module.js';

// Create 3D swimming koi fish with realistic movement
class SwimmingKoiFish {
  constructor() {
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    this.fish = [];
    this.clock = new THREE.Clock();
    
    this.init();
    this.createFish();
    this.animate();
  }
  
  init() {
    // Set up renderer
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setClearColor(0x001144, 1); // Deep underwater blue
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    document.getElementById('app').appendChild(this.renderer.domElement);
    
    // Set up camera - move back to see fish better
    this.camera.position.set(0, 2, 20); // Further back and slightly above
    this.camera.lookAt(0, 0, 0);
    
    // Create underwater lighting
    const ambientLight = new THREE.AmbientLight(0x4488bb, 0.8); // Brighter ambient light
    this.scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0x88ddff, 1.2); // Brighter directional
    directionalLight.position.set(10, 10, 5);
    directionalLight.castShadow = true;
    this.scene.add(directionalLight);
    
    // Add mouse controls
    this.addControls();
    
    // Handle window resize
    window.addEventListener('resize', () => this.onWindowResize());
  }
  
  createFishGeometry() {
    // Create realistic koi fish following the detailed specifications
    const fishGroup = new THREE.Group();
    
    // 1. BODY - CapsuleGeometry for smooth torpedo shape
    const bodyGeometry = new THREE.CapsuleGeometry(0.45, 2.2, 4, 32);
    bodyGeometry.scale(1, 1.2, 1); // Widen belly slightly
    
    const bodyMaterial = new THREE.MeshStandardMaterial({
      color: 0xffffff, // White base for koi patterns
      roughness: 0.6,
      metalness: 0.1,
      emissive: 0xff5500,
      emissiveIntensity: 0.05 // Subtle mythical glow
    });
    
    const fishBody = new THREE.Mesh(bodyGeometry, bodyMaterial);
    fishGroup.add(fishBody);
    
    // 2. HEAD - SphereGeometry merged with body front
    const headGeometry = new THREE.SphereGeometry(0.5, 32, 32);
    const headMaterial = new THREE.MeshStandardMaterial({
      color: 0xffffff,
      roughness: 0.6,
      metalness: 0.1
    });
    
    const head = new THREE.Mesh(headGeometry, headMaterial);
    head.position.set(1.6, 0, 0); // Position at front of body
    fishGroup.add(head);
    
    // MOUTH - Small circular opening
    const mouthGeometry = new THREE.CircleGeometry(0.15, 16);
    const mouthMaterial = new THREE.MeshStandardMaterial({
      color: 0x330000,
      roughness: 0.8
    });
    
    const mouth = new THREE.Mesh(mouthGeometry, mouthMaterial);
    mouth.position.set(2.0, -0.1, 0);
    mouth.rotation.y = Math.PI / 2;
    fishGroup.add(mouth);
    
    // BARBELS (Whiskers) - Thin cylinders at mouth corners
    const barbelGeometry = new THREE.CylinderGeometry(0.02, 0.02, 0.3, 8);
    const barbelMaterial = new THREE.MeshStandardMaterial({
      color: 0xffaa88,
      roughness: 0.7
    });
    
    // Upper barbels
    const barbel1 = new THREE.Mesh(barbelGeometry, barbelMaterial);
    barbel1.position.set(1.9, 0.1, 0.2);
    barbel1.rotation.z = Math.PI / 6;
    fishGroup.add(barbel1);
    
    const barbel2 = new THREE.Mesh(barbelGeometry, barbelMaterial);
    barbel2.position.set(1.9, 0.1, -0.2);
    barbel2.rotation.z = -Math.PI / 6;
    fishGroup.add(barbel2);
    
    // Lower barbels
    const barbel3 = new THREE.Mesh(barbelGeometry, barbelMaterial);
    barbel3.position.set(1.95, -0.05, 0.15);
    barbel3.rotation.z = Math.PI / 8;
    barbel3.rotation.x = Math.PI / 8;
    fishGroup.add(barbel3);
    
    const barbel4 = new THREE.Mesh(barbelGeometry, barbelMaterial);
    barbel4.position.set(1.95, -0.05, -0.15);
    barbel4.rotation.z = -Math.PI / 8;
    barbel4.rotation.x = -Math.PI / 8;
    fishGroup.add(barbel4);
    
    // 3. EYES - Spherical with reflective sheen
    const eyeGeometry = new THREE.SphereGeometry(0.08, 16, 16);
    const eyeMaterial = new THREE.MeshStandardMaterial({
      color: 0x000000,
      roughness: 0.3,
      emissive: 0x222222,
      emissiveIntensity: 0.1
    });
    
    const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    leftEye.position.set(1.7, 0.35, 0.35);
    fishGroup.add(leftEye);
    
    const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    rightEye.position.set(1.7, 0.35, -0.35);
    fishGroup.add(rightEye);
    
    // 4. TAIL (Caudal Fin) - Large fan shape
    const tailGeometry = new THREE.PlaneGeometry(1.2, 1.8, 32, 32);
    const tailMaterial = new THREE.MeshStandardMaterial({
      color: 0xffaa55,
      transparent: true,
      opacity: 0.8,
      emissive: 0xffaa55,
      emissiveIntensity: 0.6,
      side: THREE.DoubleSide
    });
    
    const tailFin = new THREE.Mesh(tailGeometry, tailMaterial);
    tailFin.position.set(-1.8, 0, 0);
    tailFin.rotation.y = Math.PI / 2;
    fishGroup.add(tailFin);
    
    // 5. DORSAL FIN (Top) - Long fin along spine
    const dorsalGeometry = new THREE.PlaneGeometry(0.3, 1.0, 16, 16);
    const dorsalMaterial = new THREE.MeshStandardMaterial({
      color: 0xff7744,
      transparent: true,
      opacity: 0.7,
      emissive: 0xff3300,
      emissiveIntensity: 0.3,
      side: THREE.DoubleSide
    });
    
    const dorsalFin = new THREE.Mesh(dorsalGeometry, dorsalMaterial);
    dorsalFin.position.set(0.2, 0.7, 0);
    dorsalFin.rotation.z = Math.PI / 2;
    fishGroup.add(dorsalFin);
    
    // 6. PECTORAL FINS (Sides, near head) - Pair of side fins
    const pectoralGeometry = new THREE.PlaneGeometry(0.5, 0.35, 16, 16);
    const pectoralMaterial = new THREE.MeshStandardMaterial({
      color: 0xffaa77,
      transparent: true,
      opacity: 0.7,
      emissive: 0xff5522,
      emissiveIntensity: 0.2,
      side: THREE.DoubleSide
    });
    
    const leftPectoral = new THREE.Mesh(pectoralGeometry, pectoralMaterial);
    leftPectoral.position.set(1.2, -0.1, 0.6);
    leftPectoral.rotation.y = Math.PI / 6;
    leftPectoral.rotation.z = -Math.PI / 8;
    fishGroup.add(leftPectoral);
    
    const rightPectoral = new THREE.Mesh(pectoralGeometry, pectoralMaterial);
    rightPectoral.position.set(1.2, -0.1, -0.6);
    rightPectoral.rotation.y = -Math.PI / 6;
    rightPectoral.rotation.z = Math.PI / 8;
    fishGroup.add(rightPectoral);
    
    // 7. PELVIC FINS (Bottom Mid-Body) - Belly fins
    const pelvicGeometry = new THREE.PlaneGeometry(0.3, 0.25, 12, 12);
    const pelvicMaterial = new THREE.MeshStandardMaterial({
      color: 0xff8855,
      transparent: true,
      opacity: 0.6,
      side: THREE.DoubleSide
    });
    
    const leftPelvic = new THREE.Mesh(pelvicGeometry, pelvicMaterial);
    leftPelvic.position.set(0.5, -0.6, 0.3);
    leftPelvic.rotation.x = Math.PI / 2;
    fishGroup.add(leftPelvic);
    
    const rightPelvic = new THREE.Mesh(pelvicGeometry, pelvicMaterial);
    rightPelvic.position.set(0.5, -0.6, -0.3);
    rightPelvic.rotation.x = Math.PI / 2;
    fishGroup.add(rightPelvic);
    
    // 8. ANAL FIN (Bottom Rear) - Stabilization fin
    const analGeometry = new THREE.PlaneGeometry(0.4, 0.3, 12, 12);
    const analMaterial = new THREE.MeshStandardMaterial({
      color: 0xff6633,
      transparent: true,
      opacity: 0.7,
      side: THREE.DoubleSide
    });
    
    const analFin = new THREE.Mesh(analGeometry, analMaterial);
    analFin.position.set(-0.5, -0.5, 0);
    analFin.rotation.x = Math.PI / 2;
    fishGroup.add(analFin);
    
    // Store references for animation
    fishGroup.userData = {
      body: fishBody,
      tail: tailFin,
      dorsal: dorsalFin,
      pectorals: [leftPectoral, rightPectoral],
      pelvics: [leftPelvic, rightPelvic],
      anal: analFin,
      barbels: [barbel1, barbel2, barbel3, barbel4]
    };
    
    return fishGroup;
  }
  
  createFish() {
    // Create realistic koi with proper color varieties
    const koiVarieties = [
      {
        name: 'Kohaku',
        body: 0xffffff, // White base
        pattern: 0xff3300, // Red patches
        fins: 0xff6644,
        emissive: 0xff2200
      },
      {
        name: 'Sanke',
        body: 0xffffff, // White base
        pattern: 0xff2200, // Red patches with black
        fins: 0xff4422,
        emissive: 0xff1100
      },
      {
        name: 'Showa',
        body: 0x222222, // Black base
        pattern: 0xff3300, // Red and white patches
        fins: 0xff5533,
        emissive: 0xff3300
      },
      {
        name: 'Mythical',
        body: 0xffffff, // White base
        pattern: 0x00ffff, // Cyan glowing
        fins: 0x44aaff,
        emissive: 0x0088ff
      }
    ];
    
    for (let i = 0; i < 4; i++) {
      const fish = this.createFishGeometry();
      const variety = koiVarieties[i];
      
      // Apply color variety to body and head
      if (fish.userData.body) {
        fish.userData.body.material.color.setHex(variety.body);
        fish.userData.body.material.emissive.setHex(variety.emissive);
      }
      
      // Update fin colors
      if (fish.userData.tail) {
        fish.userData.tail.material.color.setHex(variety.fins);
        fish.userData.tail.material.emissive.setHex(variety.emissive);
      }
      
      if (fish.userData.dorsal) {
        fish.userData.dorsal.material.color.setHex(variety.fins);
        fish.userData.dorsal.material.emissive.setHex(variety.emissive);
      }
      
      fish.userData.pectorals.forEach(fin => {
        fin.material.color.setHex(variety.fins);
        fin.material.emissive.setHex(variety.emissive);
      });
      
      // Position fish clearly
      fish.position.set(
        (i - 1.5) * 3, // Spread horizontally
        0, // Center level
        (Math.random() - 0.5) * 4 // Some depth variation
      );
      
      // Swimming properties with realistic animation references
      fish.userData.swimSpeed = 0.02 + Math.random() * 0.01;
      fish.userData.swimTime = 0;
      fish.userData.targetRotation = 0;
      fish.userData.variety = variety.name;
      
      this.fish.push(fish);
      this.scene.add(fish);
      
      console.log(`${variety.name} koi created at position:`, fish.position);
    }
    
    console.log(`Total realistic koi created: ${this.fish.length}`);
  }
  
  updateFishSwimming() {
    const time = this.clock.getElapsedTime();
    
    this.fish.forEach((fish, index) => {
      const userData = fish.userData;
      userData.swimTime += 0.02;
      
      // BODY ANIMATION - Whole body sways side-to-side
      if (userData.body) {
        userData.body.rotation.y = Math.sin(time * 2 + index) * 0.15;
      }
      
      // TAIL ANIMATION - Faster oscillation than body
      if (userData.tail) {
        userData.tail.rotation.y = Math.sin(time * 6 + index) * 0.6;
      }
      
      // DORSAL FIN - Gentle flutter synced with swimming
      if (userData.dorsal) {
        userData.dorsal.rotation.z = Math.sin(time * 3 + index) * 0.1;
      }
      
      // PECTORAL FINS - Flap back and forth for stability
      userData.pectorals.forEach((fin, finIndex) => {
        fin.rotation.z = Math.sin(time * 4 + index + finIndex * Math.PI) * 0.3;
      });
      
      // PELVIC FINS - Small flutters in sync with pectorals
      userData.pelvics.forEach((fin, finIndex) => {
        fin.rotation.x = Math.sin(time * 4 + index + finIndex * Math.PI) * 0.2;
      });
      
      // ANAL FIN - Minor stabilization oscillation
      if (userData.anal) {
        userData.anal.rotation.x = Math.sin(time * 2.5 + index) * 0.1;
      }
      
      // BARBELS - Gentle movement with water current
      userData.barbels.forEach((barbel, barbelIndex) => {
        barbel.rotation.z += Math.sin(time * 1.5 + barbelIndex) * 0.02;
        barbel.rotation.x += Math.cos(time * 1.2 + barbelIndex) * 0.01;
      });
      
      // FORWARD SWIMMING MOTION
      const swimDirection = new THREE.Vector3(
        Math.cos(fish.rotation.y), 
        0, 
        Math.sin(fish.rotation.y)
      );
      
      // Move fish forward at steady pace
      fish.position.add(swimDirection.multiplyScalar(userData.swimSpeed));
      
      // Gentle vertical movement for natural buoyancy
      fish.position.y += Math.sin(time * 0.5 + index) * 0.002;
      
      // Occasional direction changes
      if (Math.random() < 0.008) {
        userData.targetRotation += (Math.random() - 0.5) * 0.4;
      }
      
      // Smooth turning
      const rotationDiff = userData.targetRotation - fish.rotation.y;
      fish.rotation.y += rotationDiff * 0.02;
      
      // Boundary checking - turn around at edges
      if (Math.abs(fish.position.x) > 12) {
        userData.targetRotation = Math.atan2(-fish.position.z, -fish.position.x);
      }
      if (Math.abs(fish.position.z) > 12) {
        userData.targetRotation = Math.atan2(-fish.position.z, -fish.position.x);
      }
      if (Math.abs(fish.position.y) > 4) {
        fish.position.y *= 0.95;
      }
    });
  }
  
  addControls() {
    let isMouseDown = false;
    let mouseX = 0;
    let mouseY = 0;
    
    this.renderer.domElement.addEventListener('mousedown', (event) => {
      isMouseDown = true;
      mouseX = event.clientX;
      mouseY = event.clientY;
    });
    
    this.renderer.domElement.addEventListener('mouseup', () => {
      isMouseDown = false;
    });
    
    this.renderer.domElement.addEventListener('mousemove', (event) => {
      if (isMouseDown) {
        const deltaX = event.clientX - mouseX;
        const deltaY = event.clientY - mouseY;
        
        this.camera.position.x += deltaX * 0.01;
        this.camera.position.y -= deltaY * 0.01;
        
        mouseX = event.clientX;
        mouseY = event.clientY;
      }
    });
    
    // Zoom with mouse wheel
    this.renderer.domElement.addEventListener('wheel', (event) => {
      this.camera.position.z += event.deltaY * 0.01;
      this.camera.position.z = Math.max(5, Math.min(50, this.camera.position.z));
    });
  }
  
  onWindowResize() {
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
  }
  
  animate() {
    requestAnimationFrame(() => this.animate());
    
    this.updateFishSwimming();
    this.renderer.render(this.scene, this.camera);
  }
}

// Initialize the swimming koi system
new SwimmingKoiFish();
