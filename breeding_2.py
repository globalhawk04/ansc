import json

def create_expert_tool():
    # --- DATABASE WITH BIOLOGICAL TYPES ---
    animal_database = {
        # --- PUREBREDS ---
        "Angus": {
            "comp": {"Angus": 1.0},
            "bio_type": {"Angus": "British"},
            "desc": "Maternal, Marbling"
        },
        "Hereford": {
            "comp": {"Hereford": 1.0},
            "bio_type": {"Hereford": "British"},
            "desc": "Hardy, Forage Efficient"
        },
        "Brahman": {
            "comp": {"Brahman": 1.0},
            "bio_type": {"Brahman": "Bos Indicus"},
            "desc": "Heat Tolerance, Insect Resistance"
        },
        "Charolais": {
            "comp": {"Charolais": 1.0},
            "bio_type": {"Charolais": "Continental"},
            "desc": "Terminal Growth, Lean Yield"
        },
        
        # --- F1 CROSSES ---
        "F1 Tiger Stripe": {
            "comp": {"Brahman": 0.5, "Hereford": 0.5},
            "bio_type": {"Brahman": "Bos Indicus", "Hereford": "British"},
            "desc": "Max Heterosis, Hardy Maternal"
        },
        "F1 Black Baldy": {
            "comp": {"Angus": 0.5, "Hereford": 0.5},
            "bio_type": {"Angus": "British", "Hereford": "British"},
            "desc": "Standard commercial female"
        },

        # --- COMPOSITES ---
        "Brangus": {
            "comp": {"Angus": 0.625, "Brahman": 0.375},
            "bio_type": {"Angus": "British", "Brahman": "Bos Indicus"},
            "desc": "Heat tolerant Angus"
        },
        "Beefmaster": {
            "comp": {"Brahman": 0.5, "Hereford": 0.25, "Shorthorn": 0.25},
            "bio_type": {"Brahman": "Bos Indicus", "Hereford": "British", "Shorthorn": "British"},
            "desc": "The 'Six Essentials' breed"
        }
    }

    breed_groups = {
        "Angus": "British", "Hereford": "British", "Shorthorn": "British",
        "Charolais": "Continental", "Simmental": "Continental",
        "Brahman": "Bos Indicus"
    }

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ANSC 406: Systems Matcher</title>
        <style>
            :root {{ --maroon: #500000; --bg: #fdfdfd; }}
            body {{ font-family: 'Segoe UI', Tahoma, sans-serif; background: #eee; padding: 20px; }}
            .container {{ max-width: 1100px; margin: 0 auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
            
            h1 {{ color: var(--maroon); border-bottom: 3px solid var(--maroon); padding-bottom: 10px; }}
            h2 {{ color: #333; margin-top: 0; }}
            
            .controls {{ display: flex; gap: 20px; background: #f4f4f4; padding: 20px; border-radius: 8px; }}
            .control-box {{ flex: 1; }}
            select {{ width: 100%; padding: 10px; margin-top: 5px; border-radius: 4px; border: 1px solid #ccc; }}
            
            button {{ width: 100%; padding: 15px; margin-top: 20px; background: var(--maroon); color: white; border: none; font-size: 1.1em; font-weight: bold; cursor: pointer; border-radius: 4px; }}
            button:hover {{ background: #300000; }}

            /* Results Grid */
            .results-area {{ display: none; margin-top: 30px; }}
            .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
            
            /* Card Styling */
            .card {{ background: #fff; border: 1px solid #ddd; padding: 20px; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
            .full-width {{ grid-column: span 2; }}
            .rec-box {{ background: #e3f2fd; border-left: 5px solid #2196f3; }}
            .math-box {{ background: #fffde7; border-left: 5px solid #fbc02d; font-family: 'Courier New', monospace; }}

            /* Matrix Styles (The Punnett Square) */
            table.matrix {{ width: 100%; border-collapse: collapse; font-size: 0.9em; margin-top: 10px; }}
            td, th {{ border: 2px solid #555; padding: 10px; text-align: center; vertical-align: top; }}
            th {{ background: #ddd; }}
            
            /* Matrix Colors */
            .bad {{ background: #ffcdd2; color: #b71c1c; }} /* Overlap */
            .good {{ background: #c8e6c9; color: #2e7d32; }} /* Vigor */
            
            .cell-math {{ display: block; font-size: 0.75em; color: #555; margin-top: 5px; font-style: italic; }}
            .cell-result {{ font-weight: bold; font-size: 1.1em; }}

            ul.checklist {{ list-style-type: none; padding: 0; }}
            ul.checklist li {{ padding: 8px 0; border-bottom: 1px solid #eee; }}
            
            .tag {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; margin-left: 5px; color: white; }}
            .tag-env {{ background: #2e7d32; }}
            .tag-mgt {{ background: #f57f17; }}
        </style>
    </head>
    <body>

    <div class="container">
        <h1>ANSC 406: Breed Composition & Environment Matcher</h1>
        <p>Select a Sire and Dam. The system will generate the Genetic Square and show the math.</p>

        <div class="controls">
            <div class="control-box">
                <label><strong>Sire (Bull)</strong></label>
                <select id="sireSelect"></select>
            </div>
            <div class="control-box">
                <label><strong>Dam (Cow)</strong></label>
                <select id="damSelect"></select>
            </div>
        </div>

        <button onclick="runSimulation()">Analyze Breeding Scenario</button>

        <div id="results" class="results-area">
            
            <div class="grid">
                
                <!-- VISUAL: THE PUNNETT SQUARE MATRIX -->
                <div class="card full-width">
                    <h2>1. Genetic Interaction Square (Heterosis Check)</h2>
                    <p>This grid checks for genetic overlap. <span style="background:#c8e6c9; padding:0 5px;">Green</span> = Hybrid Vigor. <span style="background:#ffcdd2; padding:0 5px;">Red</span> = Overlap (Loss of Vigor).</p>
                    <div id="matrixContainer"></div>
                </div>

                <!-- MATH: STEP BY STEP -->
                <div class="card math-box full-width">
                    <h3>2. Calculation Breakdown</h3>
                    <div id="mathLog"></div>
                    <div style="margin-top: 15px; border-top: 1px dashed #999; padding-top:10px;">
                        <strong>Final Retained Heterosis: </strong> <span id="finalScore" style="font-size:1.5em; font-weight:bold;"></span>
                    </div>
                </div>

                <!-- COMPOSITION -->
                <div class="card">
                    <h3>3. Calf Composition</h3>
                    <p><em>(0.5 x Sire) + (0.5 x Dam)</em></p>
                    <div id="compList"></div>
                </div>

                <!-- RECOMMENDATIONS -->
                <div class="card rec-box">
                    <h3>4. System Suitability</h3>
                    <ul id="recList" class="checklist"></ul>
                </div>

            </div>
        </div>
    </div>

    <script>
        const animals = {json.dumps(animal_database)};
        const breedGroups = {json.dumps(breed_groups)};

        window.onload = function() {{
            const sireSel = document.getElementById('sireSelect');
            const damSel = document.getElementById('damSelect');
            for(let name in animals) {{
                sireSel.add(new Option(name, name));
                damSel.add(new Option(name, name));
            }}
            sireSel.value = "Charolais";
            damSel.value = "F1 Tiger Stripe";
        }};

        function runSimulation() {{
            const sireName = document.getElementById('sireSelect').value;
            const damName = document.getElementById('damSelect').value;
            const sire = animals[sireName];
            const dam = animals[damName];

            // --- 1. CALCULATE COMPOSITION ---
            let calfComp = {{}};
            let bioTypes = {{ "British": 0, "Continental": 0, "Bos Indicus": 0 }};

            function addComp(sourceComp, factor) {{
                for(let breed in sourceComp) {{
                    let amt = sourceComp[breed] * factor;
                    calfComp[breed] = (calfComp[breed] || 0) + amt;
                    let group = breedGroups[breed] || "British"; 
                    bioTypes[group] += amt;
                }}
            }}

            addComp(sire.comp, 0.5);
            addComp(dam.comp, 0.5);

            // --- 2. GENERATE MATRIX & MATH ---
            let overlapSum = 0;
            let mathLogHtml = "<ul style='margin:0; padding-left:20px;'>";
            
            // Start Table
            let matrixHtml = '<table class="matrix"><thead><tr><th>Dam \\ Sire</th>';
            
            // Create Header Row (Sire Breeds)
            for (let sBreed in sire.comp) {{
                matrixHtml += `<th>${{sBreed}}<br><small>${{sire.comp[sBreed]*100}}%</small></th>`;
            }}
            matrixHtml += '</tr></thead><tbody>';

            // Create Rows (Dam Breeds)
            for (let dBreed in dam.comp) {{
                matrixHtml += `<tr><th>${{dBreed}}<br><small>${{dam.comp[dBreed]*100}}%</small></th>`;
                
                for (let sBreed in sire.comp) {{
                    // CALCULATION LOGIC FOR THE CELL
                    let sVal = sire.comp[sBreed];
                    let dVal = dam.comp[dBreed];
                    let prob = sVal * dVal;
                    
                    let cellClass = "good";
                    let cellText = "Vigor";
                    
                    if (sBreed === dBreed) {{
                        cellClass = "bad";
                        cellText = "Overlap";
                        overlapSum += prob;
                        // Add to Math Log
                        mathLogHtml += `<li>Found genetic overlap in <strong>${{sBreed}}</strong>: Sire(${{sVal}}) x Dam(${{dVal}}) = ${{prob.toFixed(4)}}</li>`;
                    }}

                    // Fill Cell
                    matrixHtml += `<td class="${{cellClass}}">
                        <span class="cell-result">${{cellText}}</span>
                        <span class="cell-math">${{sVal}} x ${{dVal}} = ${{prob.toFixed(4)}}</span>
                    </td>`;
                }}
                matrixHtml += '</tr>';
            }}
            matrixHtml += '</tbody></table>';

            // Final Math
            let finalHeterosis = (1 - overlapSum) * 100;
            
            if(overlapSum === 0) {{
                mathLogHtml += "<li>No genetic overlaps found.</li>";
            }}
            mathLogHtml += "</ul>";
            mathLogHtml += `<p><strong>Formula:</strong> 1.0 - Sum of Overlaps (${{overlapSum.toFixed(4)}}) = <strong>${{(1-overlapSum).toFixed(4)}}</strong></p>`;


            // --- 3. LOGIC GENERATOR (RECOMMENDATIONS) ---
            let recs = [];
            let indicusPct = bioTypes["Bos Indicus"] * 100;
            let contPct = bioTypes["Continental"] * 100;

            // Environmental Logic
            if (indicusPct >= 25) {{
                recs.push("<strong>Environment:</strong> Suitable for Hot/Humid Climates (Gulf Coast).");
            }} else {{
                recs.push("<strong>Environment:</strong> Suitable for Temperate Climates (Midwest/North). Avoid extreme heat.");
            }}

            // Management Logic
            if (contPct >= 50) {{
                recs.push("<strong>Management:</strong> Terminal System. High growth potential implies higher feed inputs. Sell calves at weaning/yearling.");
            }} else if (indicusPct > 0 && indicusPct < 50) {{
                recs.push("<strong>Management:</strong> Excellent Maternal Replacement. Use these females to build a cow herd (Tiger Stripe / Brangus type).");
            }} else {{
                recs.push("<strong>Management:</strong> General Purpose / British Maternal.");
            }}

            // Heterosis Logic
            if (finalHeterosis === 100) {{
                recs.push("<strong>Strategy:</strong> 100% Heterosis achieved. Maximizes health and growth.");
            }} else if (finalHeterosis < 50) {{
                recs.push("<strong>Warning:</strong> Low Heterosis. You are inbreeding significantly. Ensure purebreds are high quality.");
            }}

            // --- RENDER ---
            document.getElementById('results').style.display = 'block';
            document.getElementById('matrixContainer').innerHTML = matrixHtml;
            document.getElementById('mathLog').innerHTML = mathLogHtml;
            document.getElementById('finalScore').innerText = finalHeterosis.toFixed(1) + "%";
            
            // Comp List
            let compHtml = '<ul class="checklist">';
            for(let b in calfComp) {{
                if(calfComp[b] > 0) compHtml += `<li>${{b}}: <strong>${{(calfComp[b]*100).toFixed(1)}}%</strong></li>`;
            }}
            compHtml += '</ul>';
            document.getElementById('compList').innerHTML = compHtml;

            // Rec List
            let recHtml = '';
            recs.forEach(r => recHtml += `<li>${{r}}</li>`);
            document.getElementById('recList').innerHTML = recHtml;
        }}
    </script>
    </body>
    </html>
    """

    filename = "aggie_breeding_expert.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"File created: {filename}")

if __name__ == "__main__":
    create_expert_tool()