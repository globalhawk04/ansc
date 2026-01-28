import json

def create_advanced_tool():
    # --- DATABASE: DEFINING BREEDS BY COMPOSITION ---
    # format: { "BreedName": { "Composition": {"Angus": 0.5, "Hereford": 0.5}, "Type": "..." } }
    
    animal_database = {
        # --- PUREBREDS ---
        "Angus": {
            "comp": {"Angus": 1.0},
            "type": "British",
            "desc": "Maternal, Marbling"
        },
        "Hereford": {
            "comp": {"Hereford": 1.0},
            "type": "British",
            "desc": "Hardy, Forage Efficient"
        },
        "Brahman": {
            "comp": {"Brahman": 1.0},
            "type": "Bos Indicus",
            "desc": "Heat Tolerance, Insect Resistance"
        },
        "Charolais": {
            "comp": {"Charolais": 1.0},
            "type": "Continental",
            "desc": "Terminal Growth, Lean Yield"
        },
        
        # --- COMMON F1 CROSSES (The "Maternal" Cows) ---
        "F1 Tiger Stripe": {
            "comp": {"Brahman": 0.5, "Hereford": 0.5},
            "type": "F1 Cross",
            "desc": "The 'Queen of the South'. Max Heterosis, hardy."
        },
        "F1 Black Baldy": {
            "comp": {"Angus": 0.5, "Hereford": 0.5},
            "type": "F1 Cross",
            "desc": "Standard commercial female. Good milk/marbling."
        },
        "F1 Braford (1st Gen)": {
            "comp": {"Brahman": 0.5, "Hereford": 0.5}, 
            "type": "F1 Cross",
            "desc": "Similar to Tiger Stripe but usually specific branding."
        },

        # --- COMPOSITES (Stabilized Mixes) ---
        "Brangus": {
            "comp": {"Angus": 0.625, "Brahman": 0.375}, # 5/8, 3/8
            "type": "American Composite",
            "desc": "Heat tolerant Angus."
        },
        "Beefmaster": {
            "comp": {"Brahman": 0.5, "Hereford": 0.25, "Shorthorn": 0.25},
            "type": "American Composite",
            "desc": "The 'Six Essentials' breed."
        },
        "Santa Gertrudis": {
            "comp": {"Brahman": 0.375, "Shorthorn": 0.625},
            "type": "American Composite",
            "desc": "First American breed. Hardy."
        }
    }

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Advanced Heterosis Calculator</title>
        <style>
            :root {{ --maroon: #500000; --light: #f4f4f4; }}
            body {{ font-family: sans-serif; background: var(--light); padding: 20px; }}
            .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
            
            h1 {{ color: var(--maroon); border-bottom: 2px solid var(--maroon); }}
            .control-panel {{ display: flex; gap: 20px; padding: 20px; background: #eee; border-radius: 8px; }}
            .control-group {{ flex: 1; }}
            select {{ width: 100%; padding: 8px; margin-top: 5px; }}
            
            button {{ width: 100%; padding: 15px; background: var(--maroon); color: white; border: none; font-size: 1.2em; cursor: pointer; margin-top: 20px; }}
            button:hover {{ background: #300000; }}

            .results-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }}
            .box {{ border: 1px solid #ccc; padding: 15px; border-radius: 5px; }}
            .box h3 {{ margin-top: 0; color: #444; }}

            /* Matrix Table Styling */
            table.matrix {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9em; }}
            table.matrix th, table.matrix td {{ border: 1px solid #aaa; padding: 8px; text-align: center; }}
            table.matrix th {{ background: #ddd; }}
            .overlap {{ background-color: #ffcdd2; color: #b71c1c; font-weight: bold; }} /* Bad (Overlap) */
            .vigor {{ background-color: #c8e6c9; color: #1b5e20; }} /* Good (Heterosis) */

            .bar-container {{ width: 100%; background: #ddd; height: 20px; border-radius: 10px; overflow: hidden; display: flex; margin-top: 5px; }}
            .bar-segment {{ height: 100%; text-align: center; color: white; font-size: 12px; line-height: 20px; }}
        </style>
    </head>
    <body>

    <div class="container">
        <h1>Advanced Heterosis & Composition Calculator</h1>
        <p>Select parents (including F1s and Composites) to calculate Retained Heterosis based on genetic overlap.</p>

        <div class="control-panel">
            <div class="control-group">
                <label><strong>Select Sire (Bull)</strong></label>
                <select id="sireSelect"></select>
                <p id="sireDesc" style="font-size:0.8em; color: #666;"></p>
            </div>
            <div class="control-group">
                <label><strong>Select Dam (Cow)</strong></label>
                <select id="damSelect"></select>
                <p id="damDesc" style="font-size:0.8em; color: #666;"></p>
            </div>
        </div>

        <button onclick="calculate()">Run Genetic Scenario</button>

        <div id="results" style="display:none;">
            
            <!-- Top Row: Composition Visuals -->
            <div class="results-grid">
                <div class="box">
                    <h3>Calf Breed Composition</h3>
                    <div id="calfCompBar" class="bar-container"></div>
                    <ul id="calfCompList" style="margin-top:10px; font-size:0.9em;"></ul>
                </div>
                <div class="box" id="heterosisBox">
                    <h3>Heterosis Calculation</h3>
                    <h1 id="heterosisValue" style="text-align:center; font-size: 3em; margin: 10px 0;"></h1>
                    <p id="heterosisExplanation" style="text-align:center;"></p>
                </div>
            </div>

            <!-- Bottom Row: The Matrix -->
            <div class="box" style="margin-top:20px;">
                <h3>Genetic Overlap Matrix (The Math)</h3>
                <p>This grid checks for overlap. <span style="background:#ffcdd2; padding:2px 5px;">Red</span> means genetic overlap (loss of vigor). <span style="background:#c8e6c9; padding:2px 5px;">Green</span> means unique pairing (gain of vigor).</p>
                <div id="matrixContainer"></div>
            </div>

        </div>
    </div>

    <script>
        const animals = {json.dumps(animal_database)};
        const colors = {{
            "Angus": "#000000", "Hereford": "#D2691E", "Brahman": "#A9A9A9", 
            "Charolais": "#F5DEB3", "Shorthorn": "#B22222"
        }};

        // Initialize Dropdowns
        window.onload = function() {{
            const sireSel = document.getElementById('sireSelect');
            const damSel = document.getElementById('damSelect');
            
            for (let name in animals) {{
                let opt = new Option(name, name);
                sireSel.add(opt.cloneNode(true));
                damSel.add(opt.cloneNode(true));
            }}
            
            // Set defaults to interesting cross
            sireSel.value = "Charolais";
            damSel.value = "F1 Tiger Stripe";
        }};

        function calculate() {{
            const sireName = document.getElementById('sireSelect').value;
            const damName = document.getElementById('damSelect').value;
            const sire = animals[sireName];
            const dam = animals[damName];

            // 1. Calculate Calf Composition
            let calfComp = {{}};
            // Add half of sire
            for (let breed in sire.comp) {{
                calfComp[breed] = (calfComp[breed] || 0) + (sire.comp[breed] / 2);
            }}
            // Add half of dam
            for (let breed in dam.comp) {{
                calfComp[breed] = (calfComp[breed] || 0) + (dam.comp[breed] / 2);
            }}

            // 2. Calculate Heterosis (1 - Sum of Overlaps)
            let overlapSum = 0;
            let matrixHtml = '<table class="matrix"><thead><tr><th>Dam \\ Sire</th>';

            // Create Table Headers (Sire Breeds)
            for (let sBreed in sire.comp) {{
                matrixHtml += `<th>${{sBreed}} (${{sire.comp[sBreed]*100}}%)</th>`;
            }}
            matrixHtml += '</tr></thead><tbody>';

            // Create Table Rows (Dam Breeds)
            for (let dBreed in dam.comp) {{
                matrixHtml += `<tr><th>${{dBreed}} (${{dam.comp[dBreed]*100}}%)</th>`;
                
                for (let sBreed in sire.comp) {{
                    let isOverlap = (sBreed === dBreed);
                    let probability = sire.comp[sBreed] * dam.comp[dBreed];
                    
                    if (isOverlap) {{
                        overlapSum += probability; // Add to overlap sum
                        matrixHtml += `<td class="overlap">Overlap<br>-${{(probability*100).toFixed(1)}}%</td>`;
                    }} else {{
                        matrixHtml += `<td class="vigor">Vigor<br>+${{(probability*100).toFixed(1)}}%</td>`;
                    }}
                }}
                matrixHtml += '</tr>';
            }}
            matrixHtml += '</tbody></table>';

            let retainedHeterosis = (1 - overlapSum) * 100;

            // 3. Render Results
            document.getElementById('results').style.display = 'block';
            document.getElementById('matrixContainer').innerHTML = matrixHtml;
            
            // Render Heterosis Score
            const hVal = document.getElementById('heterosisValue');
            hVal.innerText = retainedHeterosis.toFixed(1) + "%";
            if(retainedHeterosis === 100) hVal.style.color = "green";
            else if(retainedHeterosis >= 50) hVal.style.color = "orange";
            else hVal.style.color = "red";

            document.getElementById('heterosisExplanation').innerHTML = 
                `Based on breed overlap, this mating retains <strong>${{retainedHeterosis.toFixed(1)}}%</strong> of maximum possible hybrid vigor.`;

            // Render Composition Bar
            const bar = document.getElementById('calfCompBar');
            const list = document.getElementById('calfCompList');
            bar.innerHTML = '';
            list.innerHTML = '';

            for (let breed in calfComp) {{
                let pct = calfComp[breed] * 100;
                if(pct > 0) {{
                    // Visual Bar
                    let seg = document.createElement('div');
                    seg.className = 'bar-segment';
                    seg.style.width = pct + '%';
                    seg.style.backgroundColor = colors[breed] || '#555';
                    seg.innerText = breed;
                    bar.appendChild(seg);

                    // List Item
                    let li = document.createElement('li');
                    li.innerText = `${{breed}}: ${{pct.toFixed(1)}}%`;
                    list.appendChild(li);
                }}
            }}
        }}
    </script>
    </body>
    </html>
    """

    filename = "advanced_breeding_tool.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"File created: {filename}")

if __name__ == "__main__":
    create_advanced_tool()