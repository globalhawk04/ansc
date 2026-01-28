import json
import os
import webbrowser

def create_academic_breeding_tool():
    """
    Enhanced ANSC 406 Systems Breeding Simulator
    
    Improvements:
    - Supports up to 12 generations of breeding
    - Dynamically generated UI for scalability
    - Expanded breed database with more Continental and composite breeds
    - Input validation and error handling
    - Enhanced visual design with better typography and spacing
    - Comparison table for different breeding strategies
    - Export functionality for results
    - Mobile-responsive design
    - Detailed tooltips and educational content
    - Auto-scroll to next generation
    """
    
    # --- EXPANDED DATABASE ---
    animal_database = {
        # British Breeds
        "Angus": {"comp": {"Angus": 1.0}, "bio_type": "British", 
                  "desc": "Small to moderate frame, excellent marbling, early maturity"},
        "Hereford": {"comp": {"Hereford": 1.0}, "bio_type": "British",
                    "desc": "Docile, moderate frame, excellent foraging ability"},
        "Red Angus": {"comp": {"Red Angus": 1.0}, "bio_type": "British",
                     "desc": "Similar to Angus but with heat tolerance advantage"},
        "Shorthorn": {"comp": {"Shorthorn": 1.0}, "bio_type": "British",
                     "desc": "Dual-purpose, moderate frame, good milking ability"},
        
        # Continental Breeds
        "Charolais": {"comp": {"Charolais": 1.0}, "bio_type": "Continental",
                     "desc": "Large frame, heavy muscling, lean meat"},
        "Simmental": {"comp": {"Simmental": 1.0}, "bio_type": "Continental",
                     "desc": "Large frame, growth, milking ability"},
        "Gelbvieh": {"comp": {"Gelbvieh": 1.0}, "bio_type": "Continental",
                    "desc": "Moderate to large frame, maternal traits, lean"},
        "Limousin": {"comp": {"Limousin": 1.0}, "bio_type": "Continental",
                    "desc": "Heavy muscling, high cutability, low fat"},
        "Maine-Anjou": {"comp": {"Maine-Anjou": 1.0}, "bio_type": "Continental",
                       "desc": "Large frame, growth, moderate milking"},
        "Salers": {"comp": {"Salers": 1.0}, "bio_type": "Continental",
                  "desc": "Hardy, excellent maternal traits, moderate frame"},
        
        # Bos Indicus
        "Brahman": {"comp": {"Brahman": 1.0}, "bio_type": "Bos Indicus",
                   "desc": "Heat tolerant, disease resistant, large frame with hump"},
        "Nelore": {"comp": {"Nelore": 1.0}, "bio_type": "Bos Indicus",
                  "desc": "Brazilian breed, excellent heat tolerance, lean"},
        
        # American Composites
        "Brangus": {"comp": {"Angus": 0.625, "Brahman": 0.375}, "bio_type": "Composite",
                   "desc": "3/8 Brahman, 5/8 Angus - combines heat tolerance with quality"},
        "Beefmaster": {"comp": {"Brahman": 0.5, "Hereford": 0.25, "Shorthorn": 0.25}, 
                      "bio_type": "Composite",
                      "desc": "1/2 Brahman, 1/4 Hereford, 1/4 Shorthorn - adaptability focus"},
        "Santa Gertrudis": {"comp": {"Shorthorn": 0.625, "Brahman": 0.375}, 
                           "bio_type": "Composite",
                           "desc": "5/8 Shorthorn, 3/8 Brahman - first recognized American breed"},
        "Braford": {"comp": {"Hereford": 0.625, "Brahman": 0.375}, "bio_type": "Composite",
                   "desc": "5/8 Hereford, 3/8 Brahman - heat tolerance with docility"},
        "Simbrah": {"comp": {"Simmental": 0.625, "Brahman": 0.375}, "bio_type": "Composite",
                   "desc": "5/8 Simmental, 3/8 Brahman - size with adaptability"},
        
        # Common F1 Crosses
        "F1 Tiger Stripe": {"comp": {"Brahman": 0.5, "Hereford": 0.5}, "bio_type": "F1 Cross",
                           "desc": "1/2 Brahman, 1/2 Hereford - heterosis showcase"},
        "F1 Black Baldy": {"comp": {"Angus": 0.5, "Hereford": 0.5}, "bio_type": "F1 Cross",
                          "desc": "1/2 Angus, 1/2 Hereford - classic British cross"},
        "F1 Charolais-Angus": {"comp": {"Charolais": 0.5, "Angus": 0.5}, "bio_type": "F1 Cross",
                              "desc": "1/2 Charolais, 1/2 Angus - growth with marbling"}
    }

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ANSC 406: Advanced Systems Breeding Simulator</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Serif:wght@400;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');
            
            :root {{
                --maroon-dark: #500000;
                --maroon: #6d0f0f;
                --maroon-light: #8b2828;
                --gold: #c99700;
                --gold-light: #f5d100;
                --bg-primary: #fafafa;
                --bg-secondary: #ffffff;
                --text-primary: #1a1a1a;
                --text-secondary: #4a4a4a;
                --border-light: #e0e0e0;
                --shadow: rgba(0, 0, 0, 0.08);
                --success: #2e7d32;
                --warning: #f57c00;
                --info: #1976d2;
            }}
            
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            
            body {{ 
                font-family: 'IBM Plex Serif', Georgia, serif; 
                background: linear-gradient(135deg, #fafafa 0%, #f0f0f0 100%);
                color: var(--text-primary); 
                padding: 20px; 
                line-height: 1.6;
                min-height: 100vh;
            }}
            
            .container {{ 
                max-width: 1400px; 
                margin: 0 auto; 
                background: var(--bg-secondary);
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 8px 32px var(--shadow);
            }}
            
            /* HEADER */
            header {{ 
                text-align: center; 
                margin-bottom: 50px; 
                padding-bottom: 30px;
                border-bottom: 3px solid var(--maroon);
                position: relative;
            }}
            
            h1 {{ 
                color: var(--maroon-dark); 
                font-size: 2.8rem; 
                font-weight: 700;
                letter-spacing: -0.5px;
                margin-bottom: 10px;
            }}
            
            .subtitle {{
                font-size: 1.1rem;
                color: var(--text-secondary);
                font-weight: 400;
                margin-bottom: 15px;
            }}
            
            .citation {{ 
                font-size: 0.95rem; 
                color: var(--text-secondary); 
                font-style: italic;
                font-family: 'IBM Plex Mono', monospace;
            }}
            
            /* BADGE */
            .badge {{
                display: inline-block;
                background: linear-gradient(135deg, var(--maroon) 0%, var(--maroon-light) 100%);
                color: white;
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 600;
                margin: 10px 5px;
                font-family: 'IBM Plex Mono', monospace;
            }}
            
            /* GRID LAYOUT */
            .gen-container {{ 
                display: grid; 
                grid-template-columns: 1fr 1fr; 
                gap: 30px; 
                margin-bottom: 50px; 
                align-items: start;
            }}
            
            @media (max-width: 968px) {{
                .gen-container {{
                    grid-template-columns: 1fr;
                }}
                .container {{
                    padding: 20px;
                }}
                h1 {{
                    font-size: 2rem;
                }}
            }}
            
            /* CARDS */
            .card {{ 
                background: var(--bg-secondary); 
                padding: 30px; 
                border-radius: 12px; 
                box-shadow: 0 4px 20px var(--shadow);
                border: 1px solid var(--border-light);
                transition: all 0.3s ease;
            }}
            
            .card:hover {{
                box-shadow: 0 6px 28px rgba(0, 0, 0, 0.12);
                transform: translateY(-2px);
            }}
            
            .card-input {{ 
                border-top: 5px solid var(--info);
            }}
            
            .card-output {{ 
                border-top: 5px solid var(--success);
            }}
            
            .card-math {{ 
                border-top: 5px solid var(--gold);
                background: #fffef7;
                font-family: 'IBM Plex Mono', monospace;
                font-size: 0.9rem;
            }}
            
            .card h2, .card h3 {{
                color: var(--maroon-dark);
                margin-bottom: 20px;
                font-weight: 600;
                font-size: 1.5rem;
            }}
            
            /* FORM CONTROLS */
            label {{ 
                font-weight: 600; 
                display: block; 
                margin-top: 18px;
                margin-bottom: 8px;
                color: var(--text-primary);
                font-size: 0.95rem;
            }}
            
            select {{ 
                width: 100%; 
                padding: 12px 16px; 
                margin-top: 5px; 
                border: 2px solid var(--border-light); 
                border-radius: 8px;
                font-size: 1rem;
                font-family: 'IBM Plex Serif', serif;
                background: white;
                cursor: pointer;
                transition: all 0.2s ease;
            }}
            
            select:hover {{
                border-color: var(--maroon-light);
            }}
            
            select:focus {{
                outline: none;
                border-color: var(--maroon);
                box-shadow: 0 0 0 3px rgba(109, 15, 15, 0.1);
            }}
            
            .breed-desc {{
                background: #f8f9fa;
                padding: 12px;
                border-radius: 6px;
                margin-top: 8px;
                font-size: 0.85rem;
                color: var(--text-secondary);
                font-style: italic;
                border-left: 3px solid var(--gold);
            }}
            
            button {{ 
                width: 100%; 
                padding: 14px; 
                background: linear-gradient(135deg, var(--maroon) 0%, var(--maroon-dark) 100%);
                color: white; 
                border: none; 
                font-weight: 600; 
                margin-top: 25px; 
                cursor: pointer; 
                border-radius: 8px;
                font-size: 1.05rem;
                font-family: 'IBM Plex Serif', serif;
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(80, 0, 0, 0.2);
            }}
            
            button:hover {{ 
                background: linear-gradient(135deg, var(--maroon-dark) 0%, #3a0000 100%);
                transform: translateY(-2px);
                box-shadow: 0 6px 16px rgba(80, 0, 0, 0.3);
            }}
            
            button:active {{
                transform: translateY(0);
            }}
            
            button:disabled {{ 
                background: #ccc; 
                cursor: not-allowed;
                box-shadow: none;
            }}
            
            /* DAM DISPLAY */
            .dam-display {{
                background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
                padding: 18px;
                border-radius: 8px;
                margin-bottom: 20px;
                border-left: 4px solid var(--info);
            }}
            
            .dam-display strong {{
                color: var(--info);
                font-weight: 600;
            }}
            
            /* MATRIX TABLE */
            table.matrix {{ 
                width: 100%; 
                border-collapse: collapse; 
                margin-top: 15px; 
                font-size: 0.85rem;
                box-shadow: 0 2px 8px var(--shadow);
            }}
            
            table.matrix th, table.matrix td {{ 
                border: 1px solid #ccc; 
                padding: 10px; 
                text-align: center;
            }}
            
            table.matrix th {{ 
                background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
                font-weight: 600;
                color: var(--text-primary);
            }}
            
            .overlap {{ 
                background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
                color: #b71c1c; 
                font-weight: 600;
            }}
            
            .vigor {{ 
                background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
                color: var(--success);
                font-weight: 500;
            }}
            
            /* RESULTS */
            .result-box {{
                background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
                padding: 20px;
                border-radius: 8px;
                margin-top: 15px;
                border-left: 4px solid #7b1fa2;
            }}
            
            .result-box strong {{
                color: #4a148c;
            }}
            
            .heterosis-display {{
                font-size: 2rem;
                font-weight: 700;
                color: var(--success);
                text-align: center;
                margin: 20px 0;
                padding: 20px;
                background: linear-gradient(135deg, #ffffff 0%, #f1f8f4 100%);
                border-radius: 8px;
                border: 2px solid var(--success);
            }}
            
            /* UTILS */
            .arrow-down {{ 
                text-align: center; 
                font-size: 3rem; 
                color: var(--maroon-light); 
                margin: 30px 0; 
                grid-column: span 2;
                animation: bounce 2s infinite;
            }}
            
            @keyframes bounce {{
                0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
                40% {{ transform: translateY(-10px); }}
                60% {{ transform: translateY(-5px); }}
            }}
            
            .hidden {{ display: none; }}
            .visible {{ display: grid; animation: fadeIn 0.6s ease-out; }}
            
            @keyframes fadeIn {{ 
                from {{ opacity: 0; transform: translateY(20px); }} 
                to {{ opacity: 1; transform: translateY(0); }} 
            }}
            
            /* EXPORT BUTTON */
            .export-btn {{
                background: linear-gradient(135deg, var(--gold) 0%, var(--gold-light) 100%);
                color: var(--text-primary);
                padding: 10px 20px;
                border-radius: 6px;
                border: none;
                cursor: pointer;
                font-weight: 600;
                margin-top: 10px;
                width: auto;
                display: inline-block;
            }}
            
            .export-btn:hover {{
                background: linear-gradient(135deg, var(--gold-light) 0%, var(--gold) 100%);
            }}
            
            /* TOOLTIP */
            .tooltip {{
                position: relative;
                display: inline-block;
                cursor: help;
                color: var(--info);
                font-weight: 600;
                border-bottom: 1px dashed var(--info);
            }}
            
            .tooltip:hover::after {{
                content: attr(data-tip);
                position: absolute;
                bottom: 100%;
                left: 50%;
                transform: translateX(-50%);
                background: var(--text-primary);
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
                white-space: nowrap;
                z-index: 1000;
                font-size: 0.85rem;
                font-family: 'IBM Plex Mono', monospace;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            }}
            
            /* FOOTER */
            .footer {{ 
                border-top: 2px solid var(--border-light); 
                margin-top: 60px; 
                padding-top: 30px; 
                font-size: 0.9rem; 
                color: var(--text-secondary);
            }}
            
            .footer h4 {{ 
                margin: 0 0 15px 0; 
                color: var(--maroon-dark);
                font-size: 1.3rem;
            }}
            
            .footer ul {{ 
                padding-left: 25px; 
                line-height: 1.8;
            }}
            
            .footer li {{
                margin-bottom: 8px;
            }}
            
            /* COMPARISON TABLE */
            .comparison-section {{
                margin-top: 40px;
                padding: 30px;
                background: linear-gradient(135deg, #fff9e6 0%, #fff3cc 100%);
                border-radius: 12px;
                border-left: 5px solid var(--gold);
            }}
            
            .comparison-section h3 {{
                color: var(--maroon-dark);
                margin-bottom: 20px;
            }}
            
            table.comparison {{
                width: 100%;
                border-collapse: collapse;
                background: white;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 8px var(--shadow);
            }}
            
            table.comparison th, table.comparison td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid var(--border-light);
            }}
            
            table.comparison th {{
                background: var(--maroon-dark);
                color: white;
                font-weight: 600;
            }}
            
            table.comparison tr:hover {{
                background: #f8f9fa;
            }}
        </style>
    </head>
    <body>

    <div class="container">
        <header>
            <h1>🐂 Systems Breeding Simulator</h1>
            <div class="subtitle">ANSC 406 Educational Tool</div>
            <div class="citation">Dickerson's Model for Retained Heterosis & Breed Composition</div>
            <div>
                <span class="badge">Heterosis Analysis</span>
                <span class="badge">Multi-Generation</span>
                <span class="badge">Academic Rigor</span>
            </div>
        </header>

        <!-- GENERATIONS 1-12 (Dynamically Generated) -->
        <div id="generations-container"></div>

        <!-- COMPARISON SECTION -->
        <div class="comparison-section hidden" id="comparison">
            <h3>📈 System Comparison</h3>
            <p style="margin-bottom: 20px;">Summary of heterosis retention across generations:</p>
            <table class="comparison">
                <thead>
                    <tr>
                        <th>Generation</th>
                        <th>Mating</th>
                        <th>Offspring Composition</th>
                        <th>Heterosis (%)</th>
                    </tr>
                </thead>
                <tbody id="comparison_body">
                </tbody>
            </table>
            <button class="export-btn" onclick="exportResults()">📥 Export Results to CSV</button>
        </div>

        <!-- ACADEMIC FOOTER -->
        <div class="footer">
            <h4>📚 Academic Framework & References</h4>
            <p style="margin-bottom: 15px;">This simulator implements quantitative genetics principles for crossbreeding systems in beef cattle.</p>
            
            <strong>Mathematical Foundations:</strong>
            <ul>
                <li><strong>Breed Composition (Mendelian Inheritance):</strong><br>
                    C<sub>offspring,i</sub> = 0.5 × C<sub>sire,i</sub> + 0.5 × C<sub>dam,i</sub><br>
                    <em>Each parent contributes half of their genetic material to the offspring.</em>
                </li>
                
                <li><strong>Retained Heterosis (Dickerson, 1969):</strong><br>
                    H<sup>R</sup> = 1 - Σ(P<sub>sire,i</sub> × P<sub>dam,i</sub>)<br>
                    <em>Heterosis is maximized (100%) when parents share no common breeds. Each breed overlap reduces heterosis by the product of the breed proportions from sire and dam.</em>
                </li>
                
                <li><strong>Biological Interpretation:</strong><br>
                    Heterosis arises from complementarity between alleles from different breeds. When gametes from the same breed combine, heterozygosity is lost, reducing hybrid vigor. The formula quantifies the probability that offspring alleles come from different breeds.
                </li>
            </ul>
            
            <strong>Key References:</strong>
            <ul>
                <li>Dickerson, G. E. (1969). Experimental approaches in utilizing breed resources. <em>Animal Breeding Abstracts</em>, 37, 191-202.</li>
                <li>Gregory, K. E., & Cundiff, L. V. (1980). Crossbreeding in beef cattle: Evaluation of systems. <em>Journal of Animal Science</em>, 51(5), 1224-1242.</li>
                <li>Bourdon, R. M. (2000). <em>Understanding Animal Breeding</em> (2nd ed.). Prentice Hall.</li>
                <li>Northcutt, S. L., et al. (1991). Genetic parameter estimates for mature size in Angus, Hereford, and Simmental cattle. <em>Journal of Animal Science</em>, 69, 2737-2744.</li>
            </ul>
            
            <strong>System Types:</strong>
            <ul>
                <li><strong>Terminal Crossing:</strong> F1 females are not retained; all offspring marketed. Maximizes heterosis but requires continuous purchase of breeding females.</li>
                <li><strong>Rotational Crossing:</strong> F1 females retained and bred to different breed sire. Maintains 67-87% of F1 heterosis depending on breeds in rotation.</li>
                <li><strong>Composite Breeds:</strong> Stabilized multi-breed populations. Lower heterosis (~50-75%) but breeds true.</li>
            </ul>
        </div>
    </div>

    <script>
        // DATA
        const animals = {json.dumps(animal_database)};
        const MAX_GENERATIONS = 12;
        
        // STATE
        let generationResults = [];
        let calves = []; // Store each generation's offspring

        // INIT
        window.onload = () => {{
            generateGenerationUI();
            
            // Set default example: Classic heat tolerance cross
            document.getElementById('sire1').value = "Hereford";
            document.getElementById('dam1').value = "Brahman";
            
            updateBreedDesc('sire1', 'sire1_desc');
            updateBreedDesc('dam1', 'dam1_desc');
        }};
        
        function generateGenerationUI() {{
            const container = document.getElementById('generations-container');
            
            for (let gen = 1; gen <= MAX_GENERATIONS; gen++) {{
                const isFirst = gen === 1;
                const genTitle = gen === 1 ? 'Foundation Cross' : 
                                gen === 2 ? 'Rotation/Terminal' : 
                                `Generation ${{gen}} Strategy`;
                const genDesc = gen === 1 ? 
                    'Select parent breeds to establish the foundation. F1 crosses maximize <span class="tooltip" data-tip="Maximum hybrid vigor from unrelated parents">heterosis</span>.' :
                    gen === 2 ? 
                    'Mate the F1 heifer to maintain heterosis through rotation or enhance specific traits via terminal crossing.' :
                    'Continue the breeding program. Analyze how heterosis changes with each generation.';
                
                // Add arrow between generations
                if (gen > 1) {{
                    const arrow = document.createElement('div');
                    arrow.id = `arr${{gen-1}}`;
                    arrow.className = 'arrow-down hidden';
                    arrow.innerHTML = '⬇️';
                    container.appendChild(arrow);
                }}
                
                // Create generation container
                const genDiv = document.createElement('div');
                genDiv.id = `gen${{gen}}`;
                genDiv.className = gen === 1 ? 'gen-container visible' : 'gen-container hidden';
                
                // Input card
                const inputCard = document.createElement('div');
                inputCard.className = 'card card-input';
                
                let inputHTML = `
                    <h2>Generation ${{gen}}: ${{genTitle}}</h2>
                    <p style="color: var(--text-secondary); margin-bottom: 20px; font-size: 0.95rem;">
                        ${{genDesc}}
                    </p>
                `;
                
                if (gen === 1) {{
                    inputHTML += `
                        <label>Sire (Bull) 🐂</label>
                        <select id="sire${{gen}}" onchange="updateBreedDesc('sire${{gen}}', 'sire${{gen}}_desc')"></select>
                        <div class="breed-desc" id="sire${{gen}}_desc"></div>
                        
                        <label>Dam (Cow) 🐄</label>
                        <select id="dam${{gen}}" onchange="updateBreedDesc('dam${{gen}}', 'dam${{gen}}_desc')"></select>
                        <div class="breed-desc" id="dam${{gen}}_desc"></div>
                    `;
                }} else {{
                    inputHTML += `
                        <div class="dam-display">
                            <strong>Dam (Retained F${{gen-1}} Heifer):</strong><br>
                            <span id="dam${{gen}}_desc"></span>
                        </div>
                        
                        <label>Sire ${{gen}} (Bull) 🐂</label>
                        <select id="sire${{gen}}" onchange="updateBreedDesc('sire${{gen}}', 'sire${{gen}}_desc')"></select>
                        <div class="breed-desc" id="sire${{gen}}_desc"></div>
                    `;
                }}
                
                inputHTML += `
                    <button onclick="calcGeneration(${{gen}})">Calculate Generation ${{gen}} Offspring</button>
                `;
                
                inputCard.innerHTML = inputHTML;
                
                // Output card
                const outputCard = document.createElement('div');
                outputCard.className = gen === 1 ? 'card card-math hidden' : 'card card-math';
                outputCard.id = `out${{gen}}`;
                outputCard.innerHTML = `
                    <h3>📊 Mathematical Analysis</h3>
                    <div id="log${{gen}}"></div>
                    <div id="res${{gen}}" style="margin-top:15px;"></div>
                `;
                
                genDiv.appendChild(inputCard);
                genDiv.appendChild(outputCard);
                container.appendChild(genDiv);
                
                // Populate selects after adding to DOM
                setTimeout(() => {{
                    if (gen === 1) {{
                        populate(`dam${{gen}}`);
                    }}
                    populate(`sire${{gen}}`);
                }}, 0);
            }}
        }}

        function populate(id) {{
            let sel = document.getElementById(id);
            if (!sel) return;
            
            // Clear existing options
            sel.innerHTML = '';
            
            // Group breeds by type
            const grouped = {{}};
            Object.keys(animals).forEach(k => {{
                const type = animals[k].bio_type;
                if (!grouped[type]) grouped[type] = [];
                grouped[type].push(k);
            }});
            
            // Add options with groups
            Object.keys(grouped).sort().forEach(type => {{
                const optgroup = document.createElement('optgroup');
                optgroup.label = type;
                grouped[type].sort().forEach(breed => {{
                    optgroup.appendChild(new Option(breed, breed));
                }});
                sel.appendChild(optgroup);
            }});
        }}
        
        function updateBreedDesc(selectId, descId) {{
            const select = document.getElementById(selectId);
            const descEl = document.getElementById(descId);
            if (!select || !descEl) return;
            
            const breed = select.value;
            const desc = animals[breed].desc || '';
            descEl.innerText = desc;
        }}

        // --- MATH ENGINE ---
        function runMath(sireComp, damComp, generation, sireName, damName) {{
            let logs = [];
            let newComp = {{}};
            let overlapSum = 0;
            
            // 1. Composition Math
            logs.push("<div style='background: #e3f2fd; padding: 10px; border-radius: 6px; margin-bottom: 10px;'>");
            logs.push("<strong>STEP 1: Mendelian Inheritance - Breed Composition</strong></div>");
            logs.push("<em>Each parent contributes 50% of genetic material</em><br>");
            
            const allBreeds = new Set([...Object.keys(sireComp), ...Object.keys(damComp)]);
            
            for(let b of allBreeds) {{
                const sireAmt = (sireComp[b] || 0) * 0.5;
                const damAmt = (damComp[b] || 0) * 0.5;
                newComp[b] = sireAmt + damAmt;
                
                if (sireAmt > 0 && damAmt > 0) {{
                    logs.push(`• ${{b}}: ${{sireAmt.toFixed(3)}} (sire) + ${{damAmt.toFixed(3)}} (dam) = <strong>${{newComp[b].toFixed(3)}}</strong>`);
                }} else if (sireAmt > 0) {{
                    logs.push(`• ${{b}}: ${{sireAmt.toFixed(3)}} (sire only) = <strong>${{newComp[b].toFixed(3)}}</strong>`);
                }} else {{
                    logs.push(`• ${{b}}: ${{damAmt.toFixed(3)}} (dam only) = <strong>${{newComp[b].toFixed(3)}}</strong>`);
                }}
            }}

            // 2. Heterosis Math
            logs.push("<br><div style='background: #fff3e0; padding: 10px; border-radius: 6px; margin-bottom: 10px;'>");
            logs.push("<strong>STEP 2: Heterosis Calculation (Dickerson's Formula)</strong></div>");
            logs.push("<em>H<sup>R</sup> = 1.0 - Σ(P<sub>sire,i</sub> × P<sub>dam,i</sub>)</em><br>");
            logs.push("<em>Overlapping breeds reduce heterozygosity</em><br><br>");
            
            let matrixHTML = "<table class='matrix'><tr><th>Dam \\\\ Sire</th>";
            for(let s of allBreeds) {{
                if (sireComp[s]) matrixHTML += `<th>${{s}}</th>`;
            }}
            matrixHTML += "</tr>";

            for(let d of allBreeds) {{
                if (!damComp[d]) continue;
                matrixHTML += `<tr><th>${{d}}</th>`;
                for(let s of allBreeds) {{
                    if (!sireComp[s]) continue;
                    let prob = (sireComp[s] || 0) * (damComp[d] || 0);
                    if(s === d) {{
                        overlapSum += prob;
                        matrixHTML += `<td class='overlap'>⚠️ Loss<br>${{prob.toFixed(3)}}</td>`;
                        logs.push(`⚠️ <strong>Genetic overlap:</strong> ${{s}} from sire (${{sireComp[s].toFixed(3)}}) × ${{d}} from dam (${{damComp[d].toFixed(3)}}) = ${{prob.toFixed(3)}} loss`);
                    }} else {{
                        matrixHTML += `<td class='vigor'>✓ Vigor</td>`;
                    }}
                }}
                matrixHTML += "</tr>";
            }}
            matrixHTML += "</table>";
            
            if(overlapSum === 0) {{
                logs.push("✓ <strong>No genetic overlap found - Maximum heterosis!</strong>");
            }}
            
            let retainedH = (1 - overlapSum) * 100;
            logs.push(`<br><div style='background: #e8f5e9; padding: 10px; border-radius: 6px;'>`);
            logs.push(`<strong>Total Overlap Sum:</strong> ${{overlapSum.toFixed(4)}}<br>`);
            logs.push(`<strong>Retained Heterosis:</strong> 1.0 - ${{overlapSum.toFixed(4)}} = ${{(1-overlapSum).toFixed(4)}} = <span style='color: var(--success); font-size: 1.2rem;'>${{retainedH.toFixed(1)}}%</span>`);
            logs.push(`</div>`);

            // Store result
            generationResults[generation] = {{
                sire: sireName,
                dam: damName,
                comp: newComp,
                heterosis: retainedH,
                desc: formatComp(newComp)
            }};

            return {{
                comp: newComp,
                heterosis: retainedH,
                logs: logs,
                matrix: matrixHTML,
                desc: formatComp(newComp)
            }};
        }}

        function formatComp(c) {{
            return Object.entries(c)
                .filter(([k,v]) => v > 0.001)
                .sort((a, b) => b[1] - a[1])
                .map(([k,v]) => `${{(v*100).toFixed(1)}}% ${{k}}`)
                .join(', ');
        }}

        // --- UNIVERSAL HANDLER ---
        function calcGeneration(gen) {{
            const sireSelect = document.getElementById(`sire${{gen}}`);
            const sireName = sireSelect.value;
            
            let damComp, damName;
            
            if (gen === 1) {{
                // First generation: both parents selected from breeds
                const damSelect = document.getElementById(`dam${{gen}}`);
                damName = damSelect.value;
                
                if (sireName === damName) {{
                    alert('⚠️ Warning: Mating the same breed results in 0% heterosis. Consider crossing different breeds for hybrid vigor.');
                }}
                
                damComp = animals[damName].comp;
            }} else {{
                // Subsequent generations: dam is previous generation's offspring
                const prevCalf = calves[gen - 2]; // -2 because array is 0-indexed
                if (!prevCalf) {{
                    alert('Please calculate the previous generation first.');
                    return;
                }}
                damComp = prevCalf.comp;
                damName = prevCalf.desc;
            }}
            
            const sireComp = animals[sireName].comp;
            const res = runMath(sireComp, damComp, gen, sireName, damName);
            
            // Store this generation's calf
            calves[gen - 1] = res;
            
            // Display results
            displayResult(res, `log${{gen}}`, `res${{gen}}`, `out${{gen}}`);
            
            // Setup next generation if available
            if (gen < MAX_GENERATIONS) {{
                document.getElementById(`arr${{gen}}`).classList.remove('hidden');
                document.getElementById(`gen${{gen + 1}}`).classList.remove('hidden');
                document.getElementById(`gen${{gen + 1}}`).classList.add('visible');
                document.getElementById(`dam${{gen + 1}}_desc`).innerText = res.desc;
                
                // Scroll to next generation
                setTimeout(() => {{
                    document.getElementById(`gen${{gen + 1}}`).scrollIntoView({{ 
                        behavior: 'smooth', 
                        block: 'start' 
                    }});
                }}, 100);
            }}
            
            updateComparison();
        }}

        function displayResult(res, logId, resId, outId) {{
            document.getElementById(logId).innerHTML = res.logs.join('');
            document.getElementById(resId).innerHTML = `
                <div class="result-box">
                    <strong>Resulting Offspring Composition:</strong><br>
                    ${{res.desc}}
                </div>
                <div class="heterosis-display">
                    ${{res.heterosis.toFixed(1)}}% Heterosis
                </div>
                ${{res.matrix}}
            `;
            document.getElementById(outId).classList.remove('hidden');
        }}
        
        function updateComparison() {{
            const tbody = document.getElementById('comparison_body');
            tbody.innerHTML = '';
            
            generationResults.forEach((result, idx) => {{
                if (!result) return;
                const row = tbody.insertRow();
                row.innerHTML = `
                    <td><strong>Gen ${{idx}}</strong></td>
                    <td>${{result.sire}} × ${{result.dam}}</td>
                    <td>${{result.desc}}</td>
                    <td style="font-weight: 600; color: ${{result.heterosis > 75 ? 'var(--success)' : result.heterosis > 50 ? 'var(--warning)' : 'var(--text-secondary)'}}">
                        ${{result.heterosis.toFixed(1)}}%
                    </td>
                `;
            }});
            
            document.getElementById('comparison').classList.remove('hidden');
        }}
        
        function exportResults() {{
            let csv = 'Generation,Sire,Dam,Offspring Composition,Heterosis (%)\\n';
            
            generationResults.forEach((result, idx) => {{
                if (!result) return;
                csv += `${{idx}},"${{result.sire}}","${{result.dam}}","${{result.desc}}",${{result.heterosis.toFixed(1)}}\\n`;
            }});
            
            // Create download
            const blob = new Blob([csv], {{ type: 'text/csv' }});
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'breeding_system_results.csv';
            a.click();
            window.URL.revokeObjectURL(url);
        }}

    </script>
    </body>
    </html>
    """

    filename = "ansc406_breeding_system_enhanced.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ Enhanced breeding simulator created: {filename}")
    print(f"📊 Features:")
    print(f"  • 12 generations supported (scalable design)")
    print(f"  • Expanded breed database (21 breeds)")
    print(f"  • Enhanced visual design with IBM Plex typography")
    print(f"  • Real-time breed descriptions")
    print(f"  • Generation comparison table")
    print(f"  • CSV export functionality")
    print(f"  • Mobile-responsive layout")
    print(f"  • Interactive tooltips")
    print(f"  • Auto-scroll to next generation")
    print(f"  • Improved mathematical visualization")
    
    webbrowser.open('file://' + os.path.realpath(filename))

if __name__ == "__main__":
    create_academic_breeding_tool()