// Beautiful 2D Koi Fish System with High Detail and Smooth Animation
class DetailedKoi2D {
    constructor() {
        this.canvas = document.getElementById('fishCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        
        this.fish = [];
        this.fishCount = 8;
        this.particles = []; // For bubbles and water effects
        
        this.init();
        this.createFish();
        this.animate();
    }
    
    init() {
        // Set up canvas styles
        this.canvas.style.background = 'linear-gradient(180deg, #001144 0%, #003366 50%, #002244 100%)';
        
        // Add mouse interaction
        this.addMouseControls();
        
        // Handle window resize
        window.addEventListener('resize', () => this.handleResize());
    }
    
    createFish() {
        for (let i = 0; i < this.fishCount; i++) {
            this.fish.push({
                // Position and movement
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 2,
                vy: (Math.random() - 0.5) * 1,
                rotation: Math.random() * Math.PI * 2,
                
                // Fish properties
                size: 40 + Math.random() * 30,
                species: this.getRandomSpecies(),
                
                // Animation properties
                swimPhase: Math.random() * Math.PI * 2,
                tailSwing: 0,
                finFlap: 0,
                bodyWave: 0,
                
                // Behavior
                speed: 0.5 + Math.random() * 1.5,
                turnSpeed: 0.02 + Math.random() * 0.03,
                
                // Eye tracking
                eyeX: 0,
                eyeY: 0,
                
                // Hover effects
                isHovered: false,
                hoverScale: 1,
                hoverBrightness: 1
            });
        }
    }
    
    getRandomSpecies() {
        const species = [
            // Traditional Koi
            {
                name: 'Kohaku',
                bodyColor: '#FFFFFF',
                patternColor: '#FF4444',
                finColor: '#FFEEEE',
                eyeColor: '#000000',
                patterns: ['spots', 'stripes']
            },
            {
                name: 'Sanke',
                bodyColor: '#FFFFFF',
                patternColor: '#FF3333',
                accentColor: '#222222',
                finColor: '#FFEEEE',
                eyeColor: '#000000',
                patterns: ['mixed']
            },
            {
                name: 'Showa',
                bodyColor: '#333333',
                patternColor: '#FF4444',
                accentColor: '#FFFFFF',
                finColor: '#DDDDDD',
                eyeColor: '#000000',
                patterns: ['bold']
            },
            {
                name: 'Ogon',
                bodyColor: '#FFD700',
                patternColor: '#FFEE99',
                finColor: '#FFDD77',
                eyeColor: '#000000',
                patterns: ['solid'],
                metallic: true
            },
            // New colorful varieties
            {
                name: 'Asagi',
                bodyColor: '#6699BB',
                patternColor: '#FFFFFF',
                accentColor: '#FF6666',
                finColor: '#99BBDD',
                eyeColor: '#000000',
                patterns: ['scales']
            },
            {
                name: 'Shusui',
                bodyColor: '#4477AA',
                patternColor: '#FFAAAA',
                accentColor: '#FFFFFF',
                finColor: '#6699CC',
                eyeColor: '#000000',
                patterns: ['dorsal_line']
            },
            {
                name: 'Bekko',
                bodyColor: '#FFDD88',
                patternColor: '#333333',
                finColor: '#FFCC77',
                eyeColor: '#000000',
                patterns: ['spots']
            },
            {
                name: 'Utsurimono',
                bodyColor: '#222222',
                patternColor: '#FFDD00',
                finColor: '#444444',
                eyeColor: '#000000',
                patterns: ['bold']
            },
            {
                name: 'Koromo',
                bodyColor: '#FFFFFF',
                patternColor: '#BB4444',
                accentColor: '#444466',
                finColor: '#FFDDDD',
                eyeColor: '#000000',
                patterns: ['overlay']
            },
            {
                name: 'Goshiki',
                bodyColor: '#EEEEFF',
                patternColor: '#6644AA',
                accentColor: '#AA4466',
                finColor: '#CCCCFF',
                eyeColor: '#000000',
                patterns: ['mixed']
            },
            {
                name: 'Tancho',
                bodyColor: '#FFFFFF',
                patternColor: '#FF0000',
                finColor: '#FFFFFF',
                eyeColor: '#000000',
                patterns: ['head_spot']
            },
            {
                name: 'Kujaku',
                bodyColor: '#DDDDDD',
                patternColor: '#AA6633',
                accentColor: '#66AA88',
                finColor: '#CCDDCC',
                eyeColor: '#000000',
                patterns: ['peacock'],
                metallic: true
            },
            // Mystic varieties
            {
                name: 'Aurora',
                bodyColor: '#E6E6FA',
                patternColor: '#9966FF',
                accentColor: '#66FFCC',
                finColor: '#DDDDFF',
                eyeColor: '#000000',
                patterns: ['aurora'],
                iridescent: true
            },
            {
                name: 'Sakura',
                bodyColor: '#FFE4E6',
                patternColor: '#FF69B4',
                accentColor: '#FFFFFF',
                finColor: '#FFCCDD',
                eyeColor: '#000000',
                patterns: ['cherry_blossom']
            },
            {
                name: 'Ocean',
                bodyColor: '#87CEEB',
                patternColor: '#4169E1',
                accentColor: '#FFFFFF',
                finColor: '#B0E0E6',
                eyeColor: '#000000',
                patterns: ['waves']
            }
        ];
        
        return species[Math.floor(Math.random() * species.length)];
    }
    
    drawDetailedFish(fish) {
        const ctx = this.ctx;
        
        ctx.save();
        ctx.translate(fish.x, fish.y);
        ctx.rotate(fish.rotation);
        
        // Apply hover effects
        if (fish.isHovered) {
            ctx.scale(fish.hoverScale, fish.hoverScale);
            ctx.filter = `brightness(${fish.hoverBrightness}) saturate(1.5)`;
        }
        
        const size = fish.size;
        const species = fish.species;
        
        // Update animation phases
        fish.swimPhase += 0.08 * fish.speed;
        fish.tailSwing = Math.sin(fish.swimPhase) * 0.3;
        fish.finFlap = Math.sin(fish.swimPhase * 1.5) * 0.2;
        fish.bodyWave = Math.sin(fish.swimPhase * 0.8) * 0.1;
        
        // Update hover effects smoothly
        if (fish.isHovered) {
            fish.hoverScale = Math.min(1.2, fish.hoverScale + 0.02);
            fish.hoverBrightness = Math.min(1.4, fish.hoverBrightness + 0.02);
        } else {
            fish.hoverScale = Math.max(1, fish.hoverScale - 0.02);
            fish.hoverBrightness = Math.max(1, fish.hoverBrightness - 0.02);
        }
        
        // Draw body shadow (depth effect)
        ctx.save();
        ctx.translate(3, 3);
        ctx.scale(0.9, 0.9);
        ctx.globalAlpha = 0.3;
        this.drawFishBody(size, '#000000');
        ctx.restore();
        
        // Draw main body
        this.drawFishBody(size, species.bodyColor);
        
        // Draw patterns
        this.drawFishPatterns(fish, size, species);
        
        // Draw fins
        this.drawFins(fish, size, species);
        
        // Draw head details
        this.drawHeadDetails(fish, size, species);
        
        // Draw eyes
        this.drawEyes(fish, size, species);
        
        // Draw body highlights (wet effect)
        this.drawBodyHighlights(size, species);
        
        ctx.restore();
    }
    
    drawFishBody(size, color) {
        const ctx = this.ctx;
        
        // Main torpedo-shaped body
        ctx.beginPath();
        ctx.fillStyle = color;
        
        // Create smooth fish body shape
        ctx.moveTo(-size * 0.8, 0);
        ctx.bezierCurveTo(-size * 0.8, -size * 0.4, -size * 0.2, -size * 0.5, size * 0.3, -size * 0.3);
        ctx.bezierCurveTo(size * 0.8, -size * 0.2, size * 0.9, 0, size * 0.8, 0);
        ctx.bezierCurveTo(size * 0.9, 0, size * 0.8, size * 0.2, size * 0.3, size * 0.3);
        ctx.bezierCurveTo(-size * 0.2, size * 0.5, -size * 0.8, size * 0.4, -size * 0.8, 0);
        
        ctx.fill();
        
        // Add body outline
        ctx.strokeStyle = 'rgba(0, 0, 0, 0.3)';
        ctx.lineWidth = 1;
        ctx.stroke();
    }
    
    drawFishPatterns(fish, size, species) {
        const ctx = this.ctx;
        
        if (species.patterns.includes('spots')) {
            // Draw koi spots
            ctx.fillStyle = species.patternColor;
            this.drawSpotPattern(size, 3 + Math.floor(Math.random() * 3));
        }
        
        if (species.patterns.includes('stripes')) {
            // Draw stripe patterns
            ctx.fillStyle = species.patternColor;
            this.drawStripePattern(size);
        }
        
        if (species.patterns.includes('mixed')) {
            // Draw mixed Sanke pattern
            ctx.fillStyle = species.patternColor;
            this.drawSpotPattern(size, 2);
            ctx.fillStyle = species.accentColor;
            this.drawAccentMarks(size);
        }
        
        if (species.patterns.includes('scales')) {
            // Draw Asagi scale pattern
            ctx.fillStyle = species.patternColor;
            this.drawScalePattern(size);
        }
        
        if (species.patterns.includes('dorsal_line')) {
            // Draw Shusui dorsal line
            ctx.fillStyle = species.accentColor;
            this.drawDorsalLine(size);
        }
        
        if (species.patterns.includes('overlay')) {
            // Draw Koromo overlay pattern
            ctx.fillStyle = species.accentColor;
            this.drawOverlayPattern(size);
        }
        
        if (species.patterns.includes('head_spot')) {
            // Draw Tancho head spot
            ctx.fillStyle = species.patternColor;
            this.drawHeadSpot(size);
        }
        
        if (species.patterns.includes('peacock')) {
            // Draw Kujaku peacock pattern
            this.drawPeacockPattern(size, species);
        }
        
        if (species.patterns.includes('aurora')) {
            // Draw Aurora mystical pattern
            this.drawAuroraPattern(size, species);
        }
        
        if (species.patterns.includes('cherry_blossom')) {
            // Draw Sakura cherry blossom pattern
            this.drawCherryBlossomPattern(size, species);
        }
        
        if (species.patterns.includes('waves')) {
            // Draw Ocean wave pattern
            this.drawWavePattern(size, species);
        }
    }
    
    drawSpotPattern(size, spotCount) {
        const ctx = this.ctx;
        
        for (let i = 0; i < spotCount; i++) {
            const x = (Math.random() - 0.5) * size * 1.2;
            const y = (Math.random() - 0.5) * size * 0.6;
            const spotSize = size * (0.1 + Math.random() * 0.15);
            
            ctx.beginPath();
            ctx.ellipse(x, y, spotSize, spotSize * 0.8, 0, 0, Math.PI * 2);
            ctx.fill();
        }
    }
    
    drawStripePattern(size) {
        const ctx = this.ctx;
        
        for (let i = 0; i < 3; i++) {
            const x = -size * 0.6 + (i * size * 0.4);
            ctx.beginPath();
            ctx.moveTo(x, -size * 0.3);
            ctx.bezierCurveTo(x + size * 0.1, -size * 0.1, x + size * 0.1, size * 0.1, x, size * 0.3);
            ctx.lineWidth = size * 0.08;
            ctx.stroke();
        }
    }
    
    drawBoldPattern(size) {
        const ctx = this.ctx;
        
        // Large contrasting areas
        ctx.beginPath();
        ctx.moveTo(-size * 0.3, -size * 0.4);
        ctx.bezierCurveTo(size * 0.2, -size * 0.3, size * 0.4, size * 0.1, -size * 0.1, size * 0.4);
        ctx.bezierCurveTo(-size * 0.5, size * 0.2, -size * 0.6, -size * 0.1, -size * 0.3, -size * 0.4);
        ctx.fill();
    }
    
    drawScalePattern(size) {
        const ctx = this.ctx;
        
        // Asagi blue-grey scale pattern
        for (let i = 0; i < 20; i++) {
            const x = (Math.random() - 0.5) * size * 1.2;
            const y = (Math.random() - 0.5) * size * 0.6;
            
            ctx.save();
            ctx.translate(x, y);
            ctx.scale(0.8, 1.2);
            ctx.beginPath();
            ctx.arc(0, 0, size * 0.04, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        }
    }
    
    drawDorsalLine(size) {
        const ctx = this.ctx;
        
        // Shusui dorsal line pattern
        ctx.beginPath();
        ctx.moveTo(-size * 0.8, 0);
        ctx.bezierCurveTo(-size * 0.4, -size * 0.1, size * 0.4, -size * 0.1, size * 0.8, 0);
        ctx.lineWidth = size * 0.1;
        ctx.stroke();
    }
    
    drawOverlayPattern(size) {
        const ctx = this.ctx;
        
        // Koromo overlay effect
        ctx.globalAlpha = 0.7;
        for (let i = 0; i < 3; i++) {
            const x = (Math.random() - 0.5) * size * 0.8;
            const y = (Math.random() - 0.5) * size * 0.4;
            
            ctx.beginPath();
            ctx.arc(x, y, size * 0.15, 0, Math.PI * 2);
            ctx.fill();
        }
        ctx.globalAlpha = 1;
    }
    
    drawHeadSpot(size) {
        const ctx = this.ctx;
        
        // Tancho head spot
        ctx.beginPath();
        ctx.arc(size * 0.4, -size * 0.1, size * 0.2, 0, Math.PI * 2);
        ctx.fill();
    }
    
    drawPeacockPattern(size, species) {
        const ctx = this.ctx;
        
        // Kujaku peacock-like pattern
        const gradient = ctx.createRadialGradient(0, 0, 0, 0, 0, size);
        gradient.addColorStop(0, species.patternColor);
        gradient.addColorStop(0.5, species.accentColor);
        gradient.addColorStop(1, species.bodyColor);
        
        ctx.fillStyle = gradient;
        ctx.globalAlpha = 0.6;
        ctx.beginPath();
        ctx.arc(0, 0, size * 0.6, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
    }
    
    drawAuroraPattern(size, species) {
        const ctx = this.ctx;
        
        // Aurora mystical pattern
        const gradient = ctx.createLinearGradient(-size, -size * 0.5, size, size * 0.5);
        gradient.addColorStop(0, species.patternColor);
        gradient.addColorStop(0.3, species.accentColor);
        gradient.addColorStop(0.6, species.patternColor);
        gradient.addColorStop(1, species.accentColor);
        
        ctx.fillStyle = gradient;
        ctx.globalAlpha = 0.8;
        
        // Flowing aurora shapes
        ctx.beginPath();
        ctx.moveTo(-size * 0.6, -size * 0.2);
        ctx.bezierCurveTo(-size * 0.2, -size * 0.4, size * 0.2, size * 0.4, size * 0.6, size * 0.2);
        ctx.bezierCurveTo(size * 0.4, size * 0.1, -size * 0.4, -size * 0.1, -size * 0.6, -size * 0.2);
        ctx.fill();
        ctx.globalAlpha = 1;
    }
    
    drawCherryBlossomPattern(size, species) {
        const ctx = this.ctx;
        
        // Sakura cherry blossom pattern
        ctx.fillStyle = species.patternColor;
        
        for (let i = 0; i < 5; i++) {
            const x = (Math.random() - 0.5) * size * 1.0;
            const y = (Math.random() - 0.5) * size * 0.6;
            
            // Draw 5-petal cherry blossom
            ctx.save();
            ctx.translate(x, y);
            
            for (let petal = 0; petal < 5; petal++) {
                ctx.rotate(Math.PI * 2 / 5);
                ctx.beginPath();
                ctx.ellipse(0, -size * 0.08, size * 0.04, size * 0.08, 0, 0, Math.PI * 2);
                ctx.fill();
            }
            ctx.restore();
        }
    }
    
    drawWavePattern(size, species) {
        const ctx = this.ctx;
        
        // Ocean wave pattern
        ctx.strokeStyle = species.patternColor;
        ctx.lineWidth = size * 0.03;
        
        for (let i = 0; i < 4; i++) {
            const y = -size * 0.3 + (i * size * 0.2);
            ctx.beginPath();
            ctx.moveTo(-size * 0.8, y);
            
            for (let x = -size * 0.8; x < size * 0.8; x += size * 0.2) {
                const waveY = y + Math.sin(x / (size * 0.1)) * size * 0.05;
                ctx.lineTo(x, waveY);
            }
            ctx.stroke();
        }
    }
    
    drawAccentMarks(size) {
        const ctx = this.ctx;
        
        // Small black accent marks for Sanke
        for (let i = 0; i < 2; i++) {
            const x = (Math.random() - 0.5) * size * 0.8;
            const y = (Math.random() - 0.5) * size * 0.4;
            
            ctx.beginPath();
            ctx.rect(x, y, size * 0.05, size * 0.08);
            ctx.fill();
        }
    }
    
    drawFins(fish, size, species) {
        const ctx = this.ctx;
        
        ctx.fillStyle = species.finColor;
        ctx.strokeStyle = 'rgba(0, 0, 0, 0.2)';
        ctx.lineWidth = 1;
        
        // Pectoral fins (side fins)
        ctx.save();
        ctx.rotate(fish.finFlap);
        this.drawPectoralFin(size, 0.3, -0.3); // Left
        this.drawPectoralFin(size, 0.3, 0.3);  // Right
        ctx.restore();
        
        // Dorsal fin (top)
        ctx.save();
        ctx.translate(0, -size * 0.5);
        ctx.rotate(fish.bodyWave);
        this.drawDorsalFin(size);
        ctx.restore();
        
        // Tail fin
        ctx.save();
        ctx.translate(-size * 0.8, 0);
        ctx.rotate(fish.tailSwing);
        this.drawTailFin(size);
        ctx.restore();
        
        // Anal fin (bottom)
        ctx.save();
        ctx.translate(size * 0.2, size * 0.4);
        ctx.rotate(-fish.bodyWave * 0.5);
        this.drawAnalFin(size);
        ctx.restore();
    }
    
    drawPectoralFin(size, offsetX, offsetY) {
        const ctx = this.ctx;
        
        ctx.save();
        ctx.translate(size * offsetX, size * offsetY);
        
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.bezierCurveTo(size * 0.2, -size * 0.1, size * 0.3, size * 0.1, size * 0.15, size * 0.2);
        ctx.bezierCurveTo(size * 0.1, size * 0.15, size * 0.05, size * 0.05, 0, 0);
        ctx.fill();
        ctx.stroke();
        
        ctx.restore();
    }
    
    drawDorsalFin(size) {
        const ctx = this.ctx;
        
        ctx.beginPath();
        ctx.moveTo(-size * 0.2, 0);
        ctx.bezierCurveTo(-size * 0.1, -size * 0.3, size * 0.1, -size * 0.3, size * 0.2, 0);
        ctx.bezierCurveTo(size * 0.1, size * 0.05, -size * 0.1, size * 0.05, -size * 0.2, 0);
        ctx.fill();
        ctx.stroke();
    }
    
    drawTailFin(size) {
        const ctx = this.ctx;
        
        ctx.beginPath();
        // Upper tail lobe
        ctx.moveTo(0, 0);
        ctx.bezierCurveTo(-size * 0.3, -size * 0.4, -size * 0.5, -size * 0.3, -size * 0.4, -size * 0.1);
        ctx.bezierCurveTo(-size * 0.3, -size * 0.05, -size * 0.1, -size * 0.02, 0, 0);
        
        // Lower tail lobe
        ctx.moveTo(0, 0);
        ctx.bezierCurveTo(-size * 0.3, size * 0.4, -size * 0.5, size * 0.3, -size * 0.4, size * 0.1);
        ctx.bezierCurveTo(-size * 0.3, size * 0.05, -size * 0.1, size * 0.02, 0, 0);
        
        ctx.fill();
        ctx.stroke();
    }
    
    drawAnalFin(size) {
        const ctx = this.ctx;
        
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.bezierCurveTo(size * 0.1, size * 0.1, size * 0.2, size * 0.05, size * 0.15, -size * 0.05);
        ctx.bezierCurveTo(size * 0.1, -size * 0.02, size * 0.05, 0, 0, 0);
        ctx.fill();
        ctx.stroke();
    }
    
    drawHeadDetails(fish, size, species) {
        const ctx = this.ctx;
        
        // Mouth
        ctx.fillStyle = 'rgba(100, 50, 50, 0.8)';
        ctx.beginPath();
        ctx.ellipse(size * 0.7, 0, size * 0.08, size * 0.04, 0, 0, Math.PI * 2);
        ctx.fill();
        
        // Barbels (whiskers)
        ctx.strokeStyle = species.bodyColor;
        ctx.lineWidth = size * 0.02;
        
        // Upper barbels
        ctx.beginPath();
        ctx.moveTo(size * 0.6, -size * 0.1);
        ctx.bezierCurveTo(size * 0.8, -size * 0.15, size * 0.85, -size * 0.05, size * 0.75, size * 0.05);
        ctx.stroke();
        
        ctx.beginPath();
        ctx.moveTo(size * 0.6, size * 0.1);
        ctx.bezierCurveTo(size * 0.8, size * 0.15, size * 0.85, size * 0.05, size * 0.75, -size * 0.05);
        ctx.stroke();
    }
    
    drawEyes(fish, size, species) {
        const ctx = this.ctx;
        
        const eyeSize = size * 0.12;
        const eyeX = size * 0.5;
        const eyeY = -size * 0.15;
        
        // Eye whites
        ctx.fillStyle = '#FFFFFF';
        ctx.beginPath();
        ctx.ellipse(eyeX, eyeY, eyeSize, eyeSize, 0, 0, Math.PI * 2);
        ctx.fill();
        
        // Eye outline
        ctx.strokeStyle = 'rgba(0, 0, 0, 0.3)';
        ctx.lineWidth = 1;
        ctx.stroke();
        
        // Pupil
        ctx.fillStyle = species.eyeColor;
        ctx.beginPath();
        ctx.ellipse(eyeX + fish.eyeX, eyeY + fish.eyeY, eyeSize * 0.6, eyeSize * 0.6, 0, 0, Math.PI * 2);
        ctx.fill();
        
        // Eye shine
        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
        ctx.beginPath();
        ctx.ellipse(eyeX + fish.eyeX - eyeSize * 0.2, eyeY + fish.eyeY - eyeSize * 0.2, eyeSize * 0.2, eyeSize * 0.2, 0, 0, Math.PI * 2);
        ctx.fill();
    }
    
    drawBodyHighlights(size, species) {
        const ctx = this.ctx;
        
        // Wet shine effect
        const gradient = ctx.createLinearGradient(0, -size * 0.3, 0, size * 0.3);
        gradient.addColorStop(0, 'rgba(255, 255, 255, 0.3)');
        gradient.addColorStop(0.3, 'rgba(255, 255, 255, 0.1)');
        gradient.addColorStop(0.7, 'rgba(255, 255, 255, 0.05)');
        gradient.addColorStop(1, 'rgba(255, 255, 255, 0.15)');
        
        ctx.fillStyle = gradient;
        
        ctx.beginPath();
        ctx.moveTo(-size * 0.6, -size * 0.2);
        ctx.bezierCurveTo(size * 0.2, -size * 0.3, size * 0.5, -size * 0.1, size * 0.6, 0);
        ctx.bezierCurveTo(size * 0.5, size * 0.1, size * 0.2, size * 0.3, -size * 0.6, size * 0.2);
        ctx.bezierCurveTo(-size * 0.7, 0, -size * 0.6, -size * 0.2, -size * 0.6, -size * 0.2);
        ctx.fill();
        
        // Metallic effect for Ogon
        if (species.metallic) {
            const metalGradient = ctx.createRadialGradient(0, 0, 0, 0, 0, size);
            metalGradient.addColorStop(0, 'rgba(255, 255, 255, 0.4)');
            metalGradient.addColorStop(0.5, 'rgba(255, 255, 255, 0.1)');
            metalGradient.addColorStop(1, 'rgba(255, 255, 255, 0)');
            
            ctx.fillStyle = metalGradient;
            ctx.beginPath();
            ctx.ellipse(0, 0, size * 0.8, size * 0.4, 0, 0, Math.PI * 2);
            ctx.fill();
        }
    }
    
    updateFish() {
        this.fish.forEach(fish => {
            // Update swimming movement
            fish.x += fish.vx * fish.speed;
            fish.y += fish.vy * fish.speed;
            
            // Add natural swimming undulation
            fish.y += Math.sin(fish.swimPhase) * 0.5;
            
            // Boundary wrapping
            if (fish.x > this.canvas.width + 50) fish.x = -50;
            if (fish.x < -50) fish.x = this.canvas.width + 50;
            if (fish.y > this.canvas.height + 50) fish.y = -50;
            if (fish.y < -50) fish.y = this.canvas.height + 50;
            
            // Update rotation to follow movement
            fish.rotation = Math.atan2(fish.vy, fish.vx);
            
            // Random direction changes
            if (Math.random() < 0.02) {
                fish.vx += (Math.random() - 0.5) * 0.5;
                fish.vy += (Math.random() - 0.5) * 0.5;
                
                // Limit speed
                const speed = Math.sqrt(fish.vx * fish.vx + fish.vy * fish.vy);
                if (speed > 3) {
                    fish.vx = (fish.vx / speed) * 3;
                    fish.vy = (fish.vy / speed) * 3;
                }
            }
        });
    }
    
    createBubbles() {
        // Add water bubbles occasionally
        if (Math.random() < 0.1) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: this.canvas.height + 10,
                size: 2 + Math.random() * 4,
                vy: -1 - Math.random() * 2,
                life: 1.0,
                decay: 0.005 + Math.random() * 0.01
            });
        }
    }
    
    updateParticles() {
        this.particles.forEach((particle, index) => {
            particle.y += particle.vy;
            particle.life -= particle.decay;
            
            // Remove dead particles
            if (particle.life <= 0 || particle.y < -10) {
                this.particles.splice(index, 1);
            }
        });
    }
    
    drawParticles() {
        const ctx = this.ctx;
        
        this.particles.forEach(particle => {
            ctx.save();
            ctx.globalAlpha = particle.life * 0.6;
            ctx.fillStyle = '#88DDFF';
            
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            ctx.fill();
            
            // Bubble shine
            ctx.fillStyle = '#FFFFFF';
            ctx.beginPath();
            ctx.arc(particle.x - particle.size * 0.3, particle.y - particle.size * 0.3, particle.size * 0.3, 0, Math.PI * 2);
            ctx.fill();
            
            ctx.restore();
        });
    }
    
    addMouseControls() {
        this.canvas.addEventListener('mousemove', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;
            
            // Fish are attracted to mouse and check for hover
            this.fish.forEach(fish => {
                const dx = mouseX - fish.x;
                const dy = mouseY - fish.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                // Hover detection (like butterfly effect)
                fish.isHovered = distance < fish.size * 1.5;
                
                if (distance < 200) {
                    fish.vx += dx * 0.00005;
                    fish.vy += dy * 0.00005;
                }
                
                // Eye tracking
                if (distance < 100) {
                    fish.eyeX = (dx / distance) * fish.size * 0.02;
                    fish.eyeY = (dy / distance) * fish.size * 0.02;
                } else {
                    fish.eyeX *= 0.95;
                    fish.eyeY *= 0.95;
                }
            });
        });
        
        // Reset hover when mouse leaves canvas
        this.canvas.addEventListener('mouseleave', () => {
            this.fish.forEach(fish => {
                fish.isHovered = false;
            });
        });
    }
    
    handleResize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    animate() {
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Update and draw everything
        this.updateFish();
        this.createBubbles();
        this.updateParticles();
        
        // Draw all fish
        this.fish.forEach(fish => this.drawDetailedFish(fish));
        
        // Draw particles
        this.drawParticles();
        
        // Continue animation
        requestAnimationFrame(() => this.animate());
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    new DetailedKoi2D();
});

export default DetailedKoi2D;
