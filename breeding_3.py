import json

def create_three_gen_tool():
    # --- EXPANDED DATABASE ---
    animal_database = {
        # --- PUREBREDS - British ---
        "Angus": { "comp": {"Angus": 1.0}, "bio_type": "British" },
        "Hereford": { "comp": {"Hereford": 1.0}, "bio_type": "British" },
        "Red Angus": { "comp": {"Red Angus": 1.0}, "bio_type": "British" },
        "Shorthorn": { "comp": {"Shorthorn": 1.0}, "bio_type": "British" },
        
        # --- PUREBREDS - Continental ---
        "Charolais": { "comp": {"Charolais": 1.0}, "bio_type": "Continental" },
        "Simmental": { "comp": {"Simmental": 1.0}, "bio_type": "Continental" },
        "Limousin": { "comp": {"Limousin": 1.0}, "bio_type": "Continental" },
        "Gelbvieh": { "comp": {"Gelbvieh": 1.0}, "bio_type": "Continental" },
        
        # --- PUREBREDS - Bos Indicus ---
        "Brahman": { "comp": {"Brahman": 1.0}, "bio_type": "Bos Indicus" },
        "Brangus": { "comp": {"Angus": 0.625, "Brahman": 0.375}, "bio_type": "Bos Indicus Cross" },
        
        # --- PUREBREDS - Dairy ---
        "Holstein": { "comp": {"Holstein": 1.0}, "bio_type": "Dairy" },
        
        # --- COMMON F1s (Starting points) ---
        "F1 Tiger Stripe": { "comp": {"Brahman": 0.5, "Hereford": 0.5}, "bio_type": "Bos Indicus Cross" },
        "F1 Black Baldy": { "comp": {"Angus": 0.5, "Hereford": 0.5}, "bio_type": "British Cross" },
        "F1 Braford": { "comp": {"Brahman": 0.5, "Hereford": 0.5}, "bio_type": "Bos Indicus Cross" }
    }

    breed_groups = {
        "Angus": "British", 
        "Hereford": "British", 
        "Red Angus": "British",
        "Shorthorn": "British",
        "Charolais": "Continental", 
        "Simmental": "Continental",
        "Limousin": "Continental",
        "Gelbvieh": "Continental",
        "Brahman": "Bos Indicus",
        "Holstein": "Dairy"
    }

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>3-Generation Breeding Simulator</title>
        <style>
            :root {{ 
                --maroon: #500000; 
                --gold: #e6b31e; 
                --gray: #f4f4f4;
                --gen1-color: #2196F3;
                --gen2-color: #9C27B0;
                --gen3-color: #FF9800;
            }}
            
            * {{ box-sizing: border-box; }}
            
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #e9e9e9 0%, #d4d4d4 100%);
                padding: 20px; 
                margin: 0;
            }}
            
            .container {{ 
                max-width: 1200px; 
                margin: 0 auto; 
            }}
            
            h1 {{ 
                color: var(--maroon); 
                text-align: center; 
                border-bottom: 4px solid var(--maroon); 
                padding-bottom: 10px;
                margin-bottom: 10px;
                font-size: 2em;
            }}
            
            .subtitle {{
                text-align: center;
                color: #666;
                margin-bottom: 30px;
                font-size: 1.05em;
            }}
            
            /* Generation Sections */
            .generation-block {{
                background: white;
                border-radius: 12px;
                padding: 25px;
                margin-bottom: 25px;
                box-shadow: 0 6px 15px rgba(0,0,0,0.12);
                border-left: 12px solid #ccc;
                transition: all 0.4s ease;
            }}
            
            .generation-block:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            }}
            
            .gen-1 {{ border-left-color: var(--gen1-color); }}
            .gen-2 {{ border-left-color: var(--gen2-color); }}
            .gen-3 {{ border-left-color: var(--gen3-color); }}

            .gen-header {{ 
                display: flex; 
                justify-content: space-between; 
                align-items: center; 
                margin-bottom: 15px; 
            }}
            
            .gen-title {{ 
                font-size: 1.6em; 
                font-weight: bold; 
                color: #333; 
            }}
            
            .gen-badge {{
                background: #f0f0f0;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.85em;
                font-weight: bold;
                color: #666;
            }}
            
            .gen-1 .gen-badge {{ background: #e3f2fd; color: var(--gen1-color); }}
            .gen-2 .gen-badge {{ background: #f3e5f5; color: var(--gen2-color); }}
            .gen-3 .gen-badge {{ background: #fff3e0; color: var(--gen3-color); }}
            
            .gen-description {{
                font-style: italic;
                color: #666;
                margin-bottom: 15px;
                padding: 10px;
                background: #f9f9f9;
                border-radius: 5px;
            }}
            
            .controls {{ 
                display: grid;
                grid-template-columns: 1fr 1fr auto;
                gap: 20px; 
                background: #f9f9f9; 
                padding: 20px; 
                border-radius: 8px; 
                align-items: flex-end; 
            }}
            
            .control-group {{ 
                flex: 1; 
            }}
            
            label {{ 
                display: block; 
                font-weight: bold; 
                margin-bottom: 8px; 
                font-size: 0.95em; 
                color: #555; 
            }}
            
            select {{ 
                width: 100%; 
                padding: 12px; 
                border: 2px solid #ddd; 
                border-radius: 6px;
                font-size: 1em;
                background: white;
                transition: border-color 0.3s;
            }}
            
            select:focus {{
                outline: none;
                border-color: var(--maroon);
            }}
            
            button {{ 
                padding: 14px 30px; 
                background: var(--maroon); 
                color: white; 
                border: none; 
                font-weight: bold; 
                cursor: pointer; 
                border-radius: 6px;
                font-size: 1em;
                transition: all 0.3s ease;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            }}
            
            button:hover {{ 
                background: #300000;
                transform: translateY(-1px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }}
            
            button:active {{
                transform: translateY(0);
            }}
            
            button:disabled {{ 
                background: #ccc; 
                cursor: not-allowed;
                transform: none;
                box-shadow: none;
            }}

            /* Results Grid */
            .results-grid {{ 
                display: grid; 
                grid-template-columns: 1.2fr 1fr; 
                gap: 25px; 
                margin-top: 25px; 
                padding-top: 25px; 
                border-top: 2px dashed #ddd; 
            }}
            
            /* Matrix Table */
            table.matrix {{ 
                width: 100%; 
                border-collapse: collapse; 
                font-size: 0.9em;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            
            table.matrix th, table.matrix td {{ 
                border: 1px solid #999; 
                padding: 10px; 
                text-align: center; 
            }}
            
            table.matrix th {{ 
                background: #e0e0e0;
                font-weight: bold;
            }}
            
            .overlap {{ 
                background: #ffcdd2; 
                color: #b71c1c;
                font-weight: bold;
            }}
            
            .vigor {{ 
                background: #c8e6c9; 
                color: #2e7d32;
                font-weight: 600;
            }}
            
            .heterosis-display {{
                background: #e8f5e9;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #4caf50;
                margin-top: 15px;
            }}
            
            .heterosis-display strong {{
                font-size: 1.2em;
                color: #2e7d32;
            }}

            /* Info Tags */
            .tag {{ 
                display: inline-block; 
                padding: 5px 12px; 
                border-radius: 5px; 
                font-size: 0.85em; 
                color: white; 
                margin-right: 8px;
                margin-bottom: 8px;
                font-weight: 600;
            }}
            
            .tag-env {{ background: #2e7d32; }}
            .tag-sys {{ background: #ef6c00; }}
            .tag-het {{ background: #1976d2; }}

            .arrow-down {{ 
                text-align: center; 
                font-size: 2.5em; 
                color: #bbb; 
                margin: -15px 0 15px 0;
                animation: bounce 2s infinite;
            }}
            
            @keyframes bounce {{
                0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
                40% {{ transform: translateY(-10px); }}
                60% {{ transform: translateY(-5px); }}
            }}
            
            .hidden {{ 
                display: none; 
                opacity: 0; 
            }}
            
            .visible {{ 
                display: block; 
                opacity: 1; 
                animation: fadeIn 0.6s ease-out; 
            }}
            
            @keyframes fadeIn {{ 
                from {{ 
                    opacity: 0; 
                    transform: translateY(20px); 
                }} 
                to {{ 
                    opacity: 1; 
                    transform: translateY(0); 
                }} 
            }}

            .cow-card {{ 
                background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
                padding: 15px; 
                border-radius: 8px; 
                font-weight: bold; 
                text-align: center; 
                border: 2px solid #2196F3; 
                color: #0d47a1;
                min-height: 50px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            
            .info-section {{
                background: #fff9e6;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 15px;
                border-left: 4px solid var(--gold);
            }}
            
            .info-section h3 {{
                margin-top: 0;
                color: #555;
            }}
            
            .info-section ul {{
                list-style: none;
                padding: 0;
                margin: 10px 0 0 0;
            }}
            
            .info-section li {{
                margin-bottom: 8px;
                padding-left: 20px;
                position: relative;
            }}
            
            .info-section li:before {{
                content: "▸";
                position: absolute;
                left: 0;
                color: var(--maroon);
                font-weight: bold;
            }}
            
            @media (max-width: 768px) {{
                .controls {{
                    grid-template-columns: 1fr;
                }}
                
                .results-grid {{
                    grid-template-columns: 1fr;
                }}
                
                h1 {{
                    font-size: 1.5em;
                }}
            }}
        </style>
    </head>
    <body>

    <div class="container">
        <h1>🐄 ANSC 406: 3-Generation Breeding System</h1>
        <p class="subtitle">Design a multi-generational breeding system. Watch how composition and heterosis change as you retain daughters and continue breeding.</p>

        <!-- GENERATION 1 -->
        <div class="generation-block gen-1" id="block1">
            <div class="gen-header">
                <span class="gen-title">Generation 1: Foundation Cross</span>
                <span class="gen-badge">F1</span>
            </div>
            <div class="gen-description">
                Select your foundation sire and dam. This first cross establishes your base genetics and initial heterosis.
            </div>
            <div class="controls">
                <div class="control-group">
                    <label>🐂 Select Sire 1 (Bull)</label>
                    <select id="sire1"></select>
                </div>
                <div class="control-group">
                    <label>🐄 Select Dam 1 (Cow)</label>
                    <select id="dam1"></select>
                </div>
                <button onclick="calcGen1()">Breed Generation 1</button>
            </div>
            <div id="result1" class="results-grid hidden"></div>
        </div>

        <div id="arrow1" class="arrow-down hidden">⬇</div>

        <!-- GENERATION 2 -->
        <div class="generation-block gen-2 hidden" id="block2">
            <div class="gen-header">
                <span class="gen-title">Generation 2: Replacement Female</span>
                <span class="gen-badge">F2</span>
            </div>
            <div class="gen-description">
                You've retained a daughter from Generation 1 as a replacement female. Select a bull to breed to this F1 heifer.
            </div>
            <div class="controls">
                <div class="control-group">
                    <label>🐂 Select Sire 2 (Bull)</label>
                    <select id="sire2"></select>
                </div>
                <div class="control-group">
                    <label>🐄 Dam 2 (F1 Heifer from Gen 1)</label>
                    <div id="dam2-display" class="cow-card">Waiting for Gen 1 breeding...</div>
                </div>
                <button onclick="calcGen2()">Breed Generation 2</button>
            </div>
            <div id="result2" class="results-grid hidden"></div>
        </div>

        <div id="arrow2" class="arrow-down hidden">⬇</div>

        <!-- GENERATION 3 -->
        <div class="generation-block gen-3 hidden" id="block3">
            <div class="gen-header">
                <span class="gen-title">Generation 3: Terminal Cross</span>
                <span class="gen-badge">F3</span>
            </div>
            <div class="gen-description">
                You've retained a granddaughter from Generation 2. This is often where producers use a terminal sire for maximum growth and carcass traits.
            </div>
            <div class="controls">
                <div class="control-group">
                    <label>🐂 Select Sire 3 (Bull)</label>
                    <select id="sire3"></select>
                </div>
                <div class="control-group">
                    <label>🐄 Dam 3 (F2 Heifer from Gen 2)</label>
                    <div id="dam3-display" class="cow-card">Waiting for Gen 2 breeding...</div>
                </div>
                <button onclick="calcGen3()">Breed Generation 3</button>
            </div>
            <div id="result3" class="results-grid hidden"></div>
        </div>

    </div>

    <script>
        // --- DATA ---
        const animals = {json.dumps(animal_database)};
        const groups = {json.dumps(breed_groups)};

        // --- STATE VARIABLES ---
        let calf1 = null; // Result of Gen 1 (becomes Dam 2)
        let calf2 = null; // Result of Gen 2 (becomes Dam 3)

        // --- INITIALIZATION ---
        window.onload = function() {{
            populateDropdown('sire1');
            populateDropdown('dam1');
            populateDropdown('sire2');
            populateDropdown('sire3');
            
            // Set smart defaults for classic Tiger Stripe scenario
            document.getElementById('sire1').value = "Hereford";
            document.getElementById('dam1').value = "Brahman";
        }};

        function populateDropdown(id) {{
            const sel = document.getElementById(id);
            const sortedNames = Object.keys(animals).sort();
            
            for(let name of sortedNames) {{
                sel.add(new Option(name, name));
            }}
        }}

        // --- CORE BREEDING LOGIC ---

        function calculateBreeding(sireComp, damComp) {{
            // 1. Calculate New Composition (50% from each parent)
            let newComp = {{}};
            let totalBio = {{ "British": 0, "Continental": 0, "Bos Indicus": 0, "Dairy": 0 }};

            // Add Sire contribution (50%)
            for(let breed in sireComp) {{
                let contribution = sireComp[breed] * 0.5;
                newComp[breed] = (newComp[breed] || 0) + contribution;
                let group = groups[breed] || "British";
                totalBio[group] = (totalBio[group] || 0) + contribution;
            }}
            
            // Add Dam contribution (50%)
            for(let breed in damComp) {{
                let contribution = damComp[breed] * 0.5;
                newComp[breed] = (newComp[breed] || 0) + contribution;
                let group = groups[breed] || "British";
                totalBio[group] = (totalBio[group] || 0) + contribution;
            }}

            // 2. Calculate Heterosis using Genetic Matrix
            let overlap = 0;
            let matrix = '<table class="matrix"><thead><tr><th>Dam ↓ \\ Sire →</th>';
            
            for(let s in sireComp) {{
                matrix += `<th>${{s}}<br><small>${{(sireComp[s]*100).toFixed(0)}}%</small></th>`;
            }}
            matrix += '</tr></thead><tbody>';

            for(let d in damComp) {{
                matrix += `<tr><th>${{d}}<br><small>${{(damComp[d]*100).toFixed(0)}}%</small></th>`;
                for(let s in sireComp) {{
                    let probability = sireComp[s] * damComp[d];
                    if(s === d) {{
                        overlap += probability;
                        matrix += `<td class="overlap">Overlap<br>−${{(probability*100).toFixed(1)}}%</td>`;
                    }} else {{
                        matrix += `<td class="vigor">Hybrid<br>Vigor</td>`;
                    }}
                }}
                matrix += '</tr>';
            }}
            matrix += '</tbody></table>';
            
            // Heterosis = 100% - overlap
            let heterosis = (1 - overlap) * 100;

            // 3. Generate System Recommendations
            let recs = [];
            let indicus = totalBio["Bos Indicus"] * 100;
            let continental = totalBio["Continental"] * 100;
            let british = totalBio["British"] * 100;

            // Environmental Adaptation
            if(indicus >= 37.5) {{
                recs.push("<span class='tag tag-env'>Hot/Humid Adapted</span> Excellent for Gulf Coast and Southern environments.");
            }} else if(indicus >= 12.5) {{
                recs.push("<span class='tag tag-env'>Moderate Climate</span> Good for transition zones, some heat tolerance.");
            }} else {{
                recs.push("<span class='tag tag-env'>Temperate Climate</span> Best suited for Northern/Midwest regions.");
            }}

            // Production System
            if(continental >= 50) {{
                recs.push("<span class='tag tag-sys'>Terminal Sire</span> High growth and lean meat. Use for slaughter calves.");
            }} else if(indicus >= 12.5 && indicus <= 50) {{
                recs.push("<span class='tag tag-sys'>Maternal/Replacement</span> Excellent for replacement females. Good efficiency.");
            }} else if(british >= 75) {{
                recs.push("<span class='tag tag-sys'>British Base</span> Good for moderate growth and marbling.");
            }} else {{
                recs.push("<span class='tag tag-sys'>Balanced System</span> General-purpose commercial production.");
            }}

            // Heterosis assessment
            if(heterosis >= 75) {{
                recs.push("<span class='tag tag-het'>Maximum Heterosis</span> F1 level hybrid vigor retained.");
            }} else if(heterosis >= 50) {{
                recs.push("<span class='tag tag-het'>Good Heterosis</span> Strong hybrid vigor maintained.");
            }} else if(heterosis >= 25) {{
                recs.push("<span class='tag tag-het'>Moderate Heterosis</span> Some hybrid vigor present.");
            }} else {{
                recs.push("<span class='tag tag-het'>Low Heterosis</span> Limited hybrid vigor. Consider outcross.");
            }}

            return {{ 
                comp: newComp, 
                heterosis: heterosis, 
                matrix: matrix, 
                recs: recs,
                desc: formatComp(newComp),
                bioType: totalBio
            }};
        }}

        function formatComp(comp) {{
            let arr = [];
            for(let breed in comp) {{
                if(comp[breed] > 0.01) {{
                    arr.push(`${{(comp[breed]*100).toFixed(1)}}% ${{breed}}`);
                }}
            }}
            return arr.join(" + ");
        }}

        // --- UI RENDERING ---

        function renderOutput(result, divId, genNum) {{
            const div = document.getElementById(divId);
            
            // Build biotype summary
            let bioSummary = '';
            for(let type in result.bioType) {{
                let pct = result.bioType[type] * 100;
                if(pct > 0) {{
                    bioSummary += `<div><strong>${{type}}:</strong> ${{pct.toFixed(1)}}%</div>`;
                }}
            }}
            
            div.innerHTML = `
                <div>
                    <h3 style="margin-top:0; color:#555;">Genetic Matrix</h3>
                    ${{result.matrix}}
                    <div class="heterosis-display">
                        <strong>Retained Heterosis: ${{result.heterosis.toFixed(1)}}%</strong>
                        <div style="margin-top:5px; font-size:0.9em; color:#555;">
                            (100% = maximum F1 hybrid vigor)
                        </div>
                    </div>
                </div>
                <div>
                    <div class="info-section">
                        <h3>Calf Profile</h3>
                        <p style="font-size:1.05em; margin:10px 0;"><strong>Breed Composition:</strong><br>${{result.desc}}</p>
                        <div style="margin-top:15px; font-size:0.95em;">
                            <strong>Biological Type:</strong>
                            ${{bioSummary}}
                        </div>
                    </div>
                    
                    <div class="info-section">
                        <h3>System Recommendations</h3>
                        <ul style="list-style:none; padding:0; margin:0;">
                            ${{result.recs.map(r => `<li style="margin-bottom:8px;">${{r}}</li>`).join('')}}
                        </ul>
                    </div>
                </div>
            `;
            
            div.classList.remove('hidden');
            div.classList.add('visible');
        }}

        // --- GENERATION CALCULATIONS ---

        function calcGen1() {{
            const sireName = document.getElementById('sire1').value;
            const damName = document.getElementById('dam1').value;
            
            if(!sireName || !damName) {{
                alert('Please select both a sire and dam.');
                return;
            }}
            
            // Calculate breeding
            const result = calculateBreeding(animals[sireName].comp, animals[damName].comp);
            
            // Save state for next generation
            calf1 = result; // This calf becomes Dam 2

            // Render results
            renderOutput(result, 'result1', 1);

            // Unlock Generation 2
            document.getElementById('arrow1').classList.remove('hidden');
            document.getElementById('block2').classList.remove('hidden');
            document.getElementById('block2').classList.add('visible');
            document.getElementById('dam2-display').innerHTML = `<strong>F1 Heifer</strong><br>${{result.desc}}`;
        }}

        function calcGen2() {{
            if(!calf1) {{
                alert('Please complete Generation 1 first.');
                return;
            }}
            
            const sireName = document.getElementById('sire2').value;
            
            if(!sireName) {{
                alert('Please select a sire.');
                return;
            }}
            
            // Calculate breeding (Sire 2 × F1 Daughter)
            const result = calculateBreeding(animals[sireName].comp, calf1.comp);
            
            // Save state for next generation
            calf2 = result; // This calf becomes Dam 3
            
            // Render results
            renderOutput(result, 'result2', 2);

            // Unlock Generation 3
            document.getElementById('arrow2').classList.remove('hidden');
            document.getElementById('block3').classList.remove('hidden');
            document.getElementById('block3').classList.add('visible');
            document.getElementById('dam3-display').innerHTML = `<strong>F2 Heifer</strong><br>${{result.desc}}`;
        }}

        function calcGen3() {{
            if(!calf2) {{
                alert('Please complete Generation 2 first.');
                return;
            }}
            
            const sireName = document.getElementById('sire3').value;
            
            if(!sireName) {{
                alert('Please select a sire.');
                return;
            }}
            
            // Calculate breeding (Sire 3 × F2 Granddaughter)
            const result = calculateBreeding(animals[sireName].comp, calf2.comp);
            
            // Render results
            renderOutput(result, 'result3', 3);
        }}

    </script>
    </body>
    </html>
    """

    filename = "3_gen_breeding_tool.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✓ File created: {filename}")
    print(f"✓ Enhanced with:")
    print(f"  - Expanded breed database (11 purebreds + 3 F1s)")
    print(f"  - Improved UI/UX with better styling")
    print(f"  - Enhanced heterosis calculations and display")
    print(f"  - Biological type breakdown")
    print(f"  - Better system recommendations")
    print(f"  - Mobile responsive design")
    print(f"  - Input validation")
    return filename

if __name__ == "__main__":
    create_three_gen_tool()