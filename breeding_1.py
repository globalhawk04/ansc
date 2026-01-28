import json

def create_expert_tool():
    # --- DATABASE WITH BIOLOGICAL TYPES ---
    # We add 'bio_type' to categorize breeds for the logic engine
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

    # Map breeds to their larger biological group for analysis
    # This helps the logic decide "British" vs "Continental" vs "Indicus"
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
            .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
            
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
            .card {{ background: #fff; border: 1px solid #ddd; padding: 15px; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
            
            .rec-box {{ grid-column: span 2; background: #e3f2fd; border-left: 5px solid #2196f3; }}
            
            ul.checklist {{ list-style-type: none; padding: 0; }}
            ul.checklist li {{ padding: 5px 0; border-bottom: 1px solid #ddd; }}
            ul.checklist li:last-child {{ border-bottom: none; }}
            
            .tag {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; margin-left: 5px; color: white; }}
            .tag-env {{ background: #2e7d32; }}
            .tag-mgt {{ background: #f57f17; }}

            /* Matrix Styles */
            table.matrix {{ width: 100%; border-collapse: collapse; font-size: 0.9em; margin-top: 10px; }}
            td, th {{ border: 1px solid #ccc; padding: 6px; text-align: center; }}
            th {{ background: #eee; }}
            .bad {{ background: #ffcdd2; color: #b71c1c; }}
            .good {{ background: #c8e6c9; color: #2e7d32; }}
        </style>
    </head>
    <body>

    <div class="container">
        <h1>ANSC 406: Breed Composition & Environment Matcher</h1>
        <p>Select a Sire and Dam. The system will calculate the calf's composition and tell you where it belongs.</p>

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
            
            <!-- Analysis Report -->
            <div class="grid">
                <!-- Box 1: Composition -->
                <div class="card">
                    <h2>1. Calf Composition</h2>
                    <div id="compList"></div>
                    <hr>
                    <p><strong>Retained Heterosis:</strong> <span id="heterosisDisplay" style="font-weight:bold; font-size:1.2em;"></span></p>
                </div>

                <!-- Box 2: Overlap Matrix -->
                <div class="card">
                    <h2>2. Genetic Overlap</h2>
                    <div id="matrixContainer"></div>
                </div>

                <!-- Box 3: Recommendations (Spans full width) -->
                <div class="card rec-box">
                    <h2>3. System Suitability Report</h2>
                    <p>Based on the biological type of this calf, here is the best fit:</p>
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

            // --- CALCULATE COMPOSITION ---
            let calfComp = {{}};
            let bioTypes = {{ "British": 0, "Continental": 0, "Bos Indicus": 0 }};

            // Helper to add composition
            function addComp(sourceComp, factor) {{
                for(let breed in sourceComp) {{
                    let amt = sourceComp[breed] * factor;
                    calfComp[breed] = (calfComp[breed] || 0) + amt;
                    
                    // Add to biological group total
                    let group = breedGroups[breed] || "British"; // Default to British if unknown
                    bioTypes[group] += amt;
                }}
            }}

            addComp(sire.comp, 0.5);
            addComp(dam.comp, 0.5);

            // --- CALCULATE HETEROSIS (The Math) ---
            let overlapSum = 0;
            let matrixHtml = '<table class="matrix"><thead><tr><th>Dam \\ Sire</th>';
            for (let sBreed in sire.comp) matrixHtml += `<th>${{sBreed}}</th>`;
            matrixHtml += '</tr></thead><tbody>';

            for (let dBreed in dam.comp) {{
                matrixHtml += `<tr><th>${{dBreed}}</th>`;
                for (let sBreed in sire.comp) {{
                    if (sBreed === dBreed) {{
                        let prob = sire.comp[sBreed] * dam.comp[dBreed];
                        overlapSum += prob;
                        matrixHtml += `<td class="bad">Overlap<br>-${{(prob*100).toFixed(0)}}%</td>`;
                    }} else {{
                        matrixHtml += `<td class="good">Vigor</td>`;
                    }}
                }}
                matrixHtml += '</tr>';
            }}
            matrixHtml += '</tbody></table>';
            let finalHeterosis = (1 - overlapSum) * 100;

            // --- GENERATE RECOMMENDATIONS (The Logic) ---
            let recs = [];
            
            // 1. Environmental Fit (Based on Bos Indicus)
            let indicusPct = bioTypes["Bos Indicus"] * 100;
            if (indicusPct >= 20 && indicusPct <= 50) {{
                recs.push("<strong>Perfect for Gulf Coast / South:</strong> Has enough Brahman influence (20-50%) for heat resistance without sacrificing too much meat quality. <span class='tag tag-env'>Environment</span>");
            }} else if (indicusPct > 50) {{
                recs.push("<strong>Strictly Tropical:</strong> High Brahman content (>50%). Good for extreme heat/humidity, but will likely suffer price discounts at feedlots (meat tenderness issues). <span class='tag tag-env'>Environment</span>");
            }} else {{
                recs.push("<strong>Temperate / Northern US:</strong> Low heat tolerance. Best for Midwest, Plains, or mild climates. Will suffer in South Texas summers. <span class='tag tag-env'>Environment</span>");
            }}

            // 2. Management Fit (Based on Continental vs British)
            let contPct = bioTypes["Continental"] * 100;
            let britPct = bioTypes["British"] * 100;

            if (contPct >= 40) {{
                recs.push("<strong>Terminal System Candidate:</strong> High Continental influence means high growth rates and lean yield. Best suited for feedlots with high energy rations. Not ideal as a replacement cow (high feed maintenance). <span class='tag tag-mgt'>Management</span>");
            }} else if (britPct >= 60) {{
                recs.push("<strong>Quality Grade Target:</strong> High British influence (Angus/Hereford). Suited for 'Grid Pricing' where marbling pays a premium. Good maternal potential if kept. <span class='tag tag-mgt'>Management</span>");
            }} else {{
                recs.push("<strong>Balanced / General Purpose:</strong> Good mix of growth and quality. Flexible marketing options. <span class='tag tag-mgt'>Management</span>");
            }}

            // 3. Heterosis Note
            if (finalHeterosis >= 90) {{
                 recs.push("<strong>Max Hybrid Vigor:</strong> This pairing has high heterosis. Expect high survivability, immune system function, and growth bumps over the average of the parents. <span class='tag tag-mgt'>Performance</span>");
            }} else if (finalHeterosis <= 50) {{
                 recs.push("<strong>Low Heterosis Warning:</strong> Significant genetic overlap. You are losing the 'free lunch' of crossbreeding. Ensure the purebred genetics used are superior to make up for this. <span class='tag tag-mgt'>Performance</span>");
            }}

            // --- RENDER UI ---
            document.getElementById('results').style.display = 'block';
            document.getElementById('matrixContainer').innerHTML = matrixHtml;
            document.getElementById('heterosisDisplay').innerText = finalHeterosis.toFixed(1) + "%";
            
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