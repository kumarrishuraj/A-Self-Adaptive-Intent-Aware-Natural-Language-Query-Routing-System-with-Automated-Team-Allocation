/**
 * Frontend Logic for Nexus AI Intent Classification Landing Page
 */

document.addEventListener('DOMContentLoaded', () => {

    /* --- 1. Intersection Observer for Scroll Animations --- */
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target); // Optional: stop observing once animated
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    animatedElements.forEach(el => observer.observe(el));


    /* --- 2. Live Demo Mock API Logic --- */
    const demoForm = document.getElementById('demoForm');
    const queryInput = document.getElementById('queryInput');
    const submitBtn = document.getElementById('submitBtn');
    
    // Result UI elements
    const emptyState = document.querySelector('.empty-state');
    const resultDisplay = document.getElementById('resultDisplay');
    const scanningAnim = document.getElementById('scanningAnim');
    const resultData = document.getElementById('resultData');
    
    // Output spans
    const resIntent = document.getElementById('resIntent');
    const resConfidence = document.getElementById('resConfidence');
    const resTeam = document.getElementById('resTeam');
    const resTicket = document.getElementById('resTicket');

    // Mock dictionaries to simulate NLP categorization
    const mockIntents = [
        { keywords: ['password', 'reset', 'login', 'access', 'locked'], intent: 'CREDENTIAL_ISSUE', team: '<i class="fa-solid fa-server"></i> IT Security', prefix: 'SEC-' },
        { keywords: ['leave', 'sick', 'vacation', 'pto', 'absence'], intent: 'LEAVE_REQUEST', team: '<i class="fa-solid fa-users"></i> HR Operations', prefix: 'HR-' },
        { keywords: ['laptop', 'screen', 'keyboard', 'mouse', 'hardware'], intent: 'HARDWARE_REPAIR', team: '<i class="fa-solid fa-laptop"></i> IT Hardware', prefix: 'HDW-' },
        { keywords: ['salary', 'pay', 'deposit', 'tax', 'invoice'], intent: 'PAYROLL_INQUIRY', team: '<i class="fa-solid fa-file-invoice-dollar"></i> Finance', prefix: 'FIN-' }
    ];

    demoForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const queryText = queryInput.value.trim();
        if(!queryText) return;

        // UI Reset & Loading State
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Processing...';
        
        emptyState.style.display = 'none';
        resultDisplay.style.display = 'block';
        scanningAnim.style.display = 'block';
        resultData.style.display = 'none';
        
        // Remove animation classes to re-trigger them when shown
        const rows = resultData.querySelectorAll('.res-row');
        rows.forEach(row => {
            row.style.animation = 'none';
            row.offsetHeight; // trigger reflow
            row.style.animation = null; 
        });

        // Simulate API latency (e.g., fetch request waiting time)
        setTimeout(() => {
            // Simulated backend processing logic
            const analysis = analyzeQuery(queryText);
            
            // Populate data
            resIntent.textContent = analysis.intent;
            resConfidence.textContent = analysis.confidence + '%';
            resTeam.innerHTML = analysis.team;
            resTicket.textContent = analysis.ticketId;
            
            // Switch UI states
            scanningAnim.style.display = 'none';
            resultData.style.display = 'block';
            
            // Revert button
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> Analyze & Route';
            
        }, 1500); // 1.5s delay to represent processing
    });

    /**
     * Mocks a backend intent classification ML inference
     */
    function analyzeQuery(text) {
        text = text.toLowerCase();
        let matchedCategory = null;

        // Simple keyword matching heuristic to simulate ML model output
        for (const cat of mockIntents) {
            const matchCount = cat.keywords.filter(kw => text.includes(kw)).length;
            if (matchCount > 0) {
                matchedCategory = cat;
                break;
            }
        }

        // Default fallback if no keywords match
        if (!matchedCategory) {
            matchedCategory = {
                intent: 'GENERAL_INQUIRY',
                team: '<i class="fa-solid fa-headset"></i> L1 Support Desk',
                prefix: 'GEN-'
            };
        }

        // Generate mock data for visualization
        const confidenceScore = (Math.random() * (99.8 - 85.0) + 85.0).toFixed(1);
        const randomId = Math.floor(10000 + Math.random() * 90000);

        return {
            intent: matchedCategory.intent,
            team: matchedCategory.team,
            confidence: confidenceScore,
            ticketId: matchedCategory.prefix + randomId
        };
    }

    /* --- 3. Example Filler helper --- */
    // Attaching to window so inline onclick handlers in HTML can access it
    window.fillExample = function(text) {
        queryInput.value = text;
        queryInput.focus();
    };

    /* --- 4. Navbar Scrolled Effect (Optional enhancement) --- */
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.5)';
            navbar.style.background = 'rgba(11, 15, 25, 0.9)';
        } else {
            navbar.style.boxShadow = 'none';
            navbar.style.background = 'var(--glass-bg)';
        }
    });
});


