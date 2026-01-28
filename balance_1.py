import webbrowser
import os

def create_advanced_rumen_simulation():
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Rumen Associative Effects Model (TAMU RNS Logic)</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f7f6; padding: 20px; color: #2c3e50; }
        .container { max-width: 1300px; margin: 0 auto; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.08); }
        
        /* TAMU Maroon Header */
        header { border-bottom: 3px solid #500000; padding-bottom: 15px; margin-bottom: 25px; }
        h1 { color: #500000; margin: 0; }
        .subtitle { font-style: italic; color: #7f8c8d; margin-top: 5px; }

        .layout { display: grid; grid-template-columns: 350px 1fr; gap: 30px; }
        
        /* Feed Controls */
        .feed-panel { background: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #e9ecef; }
        .feed-group { margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px dashed #ced4da; }
        .feed-group:last-child { border-bottom: none; }
        label { display: flex; justify-content: space-between; font-weight: 600; font-size: 0.9rem; margin-bottom: 5px; }
        .chem-tag { font-size: 0.75rem; color: #666; display: block; margin-top: 3px; }
        input[type="range"] { width: 100%; accent-color: #500000; cursor: pointer; }

        /* Chemistry Dashboard */
        .dashboard { display: flex; flex-direction: column; gap: 20px; }
        
        .chem-meters { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; }
        .meter { background: #ecf0f1; padding: 10px; border-radius: 6px; text-align: center; }
        .meter-val { font-size: 1.3rem; font-weight: bold; color: #2980b9; }
        .meter-lbl { font-size: 0.8rem; text-transform: uppercase; color: #7f8c8d; }

        /* Mechanism Box */
        .mechanism-box { background: #eef2f3; padding: 15px; border-radius: 8px; border-left: 5px solid #27ae60; font-size: 0.9rem; min-height: 80px; }
        .mech-title { font-weight: bold; color: #2c3e50; margin-bottom: 5px; }
        .neg-text { color: #c0392b; font-weight: bold; }
        .pos-text { color: #27ae60; font-weight: bold; }

        .charts-area { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; height: 300px; }

        .citation { margin-top: 30px; font-size: 0.75rem; color: #95a5a6; border-top: 1px solid #eee; padding-top: 10px; }
    </style>
</head>
<body>

<div class="container">
    <header>
        <h1>Bio-Chemical Interaction Model</h1>
        <div class="subtitle">Simulating Associative Effects via Chemical Composition (TAMU RNS / NASEM Logic)</div>
    </header>

    <div class="layout">
        <!-- LEFT: FEED INPUTS -->
        <div class="feed-panel">
            <h3 style="margin-top:0; color:#500000;">Ration Composition (kg DM)</h3>
            
            <div class="feed-group">
                <label>Low Quality Grass Hay <span id="val_hay">0.0 kg</span></label>
                <input type="range" id="hay" min="0" max="10" step="0.5" value="8.0" oninput="updateModel()">
                <span class="chem-tag">High NDF (65%), Low CP (6%). The base fiber.</span>
            </div>

            <div class="feed-group">
                <label>Rolled Corn <span id="val_corn">0.0 kg</span></label>
                <input type="range" id="corn" min="0" max="10" step="0.5" value="0.0" oninput="updateModel()">
                <span class="chem-tag">High Starch (72%), Low NDF. The pH depressor.</span>
            </div>

            <div class="feed-group">
                <label>Soybean Meal (SBM) <span id="val_sbm">0.0 kg</span></label>
                <input type="range" id="sbm" min="0" max="3" step="0.1" value="0.0" oninput="updateModel()">
                <span class="chem-tag">High CP (48%), RDP Source. The Nitrogen donor.</span>
            </div>

            <div class="feed-group">
                <label>Alfalfa Hay <span id="val_alf">0.0 kg</span></label>
                <input type="range" id="alf" min="0" max="5" step="0.5" value="0.0" oninput="updateModel()">
                <span class="chem-tag">Mod CP (17%), High Buffer Capacity. The stabilizer.</span>
            </div>

            <div class="feed-group">
                <label>DDGS (Distillers) <span id="val_ddgs">0.0 kg</span></label>
                <input type="range" id="ddgs" min="0" max="5" step="0.5" value="0.0" oninput="updateModel()">
                <span class="chem-tag">High Energy, Mod Protein. Fiber & protein source.</span>
            </div>
        </div>

        <!-- RIGHT: CHEMICAL DASHBOARD -->
        <div class="dashboard">
            
            <!-- Chemical Meters -->
            <div class="chem-meters">
                <div class="meter">
                    <div class="meter-val" id="disp_cp">0%</div>
                    <div class="meter-lbl">Crude Protein</div>
                </div>
                <div class="meter">
                    <div class="meter-val" id="disp_ndf">0%</div>
                    <div class="meter-lbl">Total NDF</div>
                </div>
                <div class="meter">
                    <div class="meter-val" id="disp_starch">0%</div>
                    <div class="meter-lbl">Starch</div>
                </div>
                <div class="meter">
                    <div class="meter-val" id="disp_ph" style="color:#500000">0.0</div>
                    <div class="meter-lbl">Predicted pH</div>
                </div>
            </div>

            <!-- Logic Explanation -->
            <div class="mechanism-box" id="mech_box">
                <div class="mech-title">Interaction Logic:</div>
                <span id="mech_text">Adjust feeds to see chemical interactions.</span>
            </div>

            <!-- Charts -->
            <div class="charts-area">
                <canvas id="energyChart"></canvas>
                <canvas id="microbeChart"></canvas>
            </div>

        </div>
    </div>

    <div class="citation">
        <strong>Biological Basis:</strong>
        <ul>
            <li><strong>Feed Chemistry:</strong> Values derived from NASEM (2016) Beef Cattle Nutrient Requirements and NRC (2001) Dairy.</li>
            <li><strong>pH Calculation:</strong> Simplified from CNCPS equations relating starch fermentation rate vs. physically effective NDF (peNDF).</li>
            <li><strong>Associative Effects:</strong> 
                <br><em>Negative:</em> Low pH (< 6.0) severely inhibits cellulolytic bacteria (Fibrobacter succinogenes, Ruminococcus spp.). Starch fermentation produces VFA faster than saliva can buffer.
                <br><em>Positive:</em> CP < 8% creates N limitation for microbial protein synthesis. Adding RDP (rumen degradable protein) removes this bottleneck and enhances fiber digestion.
            </li>
            <li><strong>References:</strong> Tedeschi & Fox (2020) TAMU Ruminant Nutrition System; Klopfenstein et al. (2001) protein supplementation effects; Russell & Strobel (1989) cellulolytic bacteria pH requirements.</li>
        </ul>
    </div>
</div>

<script>
    // --- FEED LIBRARY (Source: NASEM 2016, NRC 2001) ---
    // Values are in % DM - CORRECTED VALUES
    const feeds = {
        hay:  { name: "Grass Hay",  cp: 6.0,  ndf: 65.0, starch: 1.0,  tdn: 52.0, peNDF: 55.0 },
        corn: { name: "Rolled Corn",cp: 9.0,  ndf: 9.0,  starch: 72.0, tdn: 88.0, peNDF: 2.0 },
        sbm:  { name: "SBM",        cp: 48.0, ndf: 12.0, starch: 2.0,  tdn: 84.0, peNDF: 3.0 },  
        alf:  { name: "Alfalfa",    cp: 17.0, ndf: 42.0, starch: 2.0,  tdn: 58.0, peNDF: 35.0 },  
        ddgs: { name: "DDGS",       cp: 30.0, ndf: 35.0, starch: 5.0,  tdn: 82.0, peNDF: 15.0 }   
    };

    let energyChart = null;
    let microbeChart = null;

    function updateModel() {
        // 1. Get Inputs
        const kg_hay  = parseFloat(document.getElementById('hay').value);
        const kg_corn = parseFloat(document.getElementById('corn').value);
        const kg_sbm  = parseFloat(document.getElementById('sbm').value);
        const kg_alf  = parseFloat(document.getElementById('alf').value);
        const kg_ddgs = parseFloat(document.getElementById('ddgs').value);

        // Update Labels
        document.getElementById('val_hay').innerText = kg_hay + " kg";
        document.getElementById('val_corn').innerText = kg_corn + " kg";
        document.getElementById('val_sbm').innerText = kg_sbm + " kg";
        document.getElementById('val_alf').innerText = kg_alf + " kg";
        document.getElementById('val_ddgs').innerText = kg_ddgs + " kg";

        const total_dm = kg_hay + kg_corn + kg_sbm + kg_alf + kg_ddgs;
        if(total_dm <= 0) return;

        // 2. Calculate Aggregate Chemistry
        function getChem(nutrient) {
            let total_g = (kg_hay * feeds.hay[nutrient]) +
                          (kg_corn * feeds.corn[nutrient]) +
                          (kg_sbm  * feeds.sbm[nutrient]) +
                          (kg_alf  * feeds.alf[nutrient]) +
                          (kg_ddgs * feeds.ddgs[nutrient]);
            return total_g / total_dm;
        }

        const diet_cp = getChem('cp');
        const diet_ndf = getChem('ndf');
        const diet_starch = getChem('starch');
        const diet_base_tdn = getChem('tdn');
        const diet_peNDF = getChem('peNDF');

        // 3. Simulate Rumen pH - IMPROVED MODEL
        // Base pH starts at 6.8 for forage-only diet
        // Starch fermentation produces VFA (primarily propionate) -> pH drops
        // peNDF stimulates rumination -> saliva production -> buffering
        
        let base_ph = 6.8;
        
        // pH depression from starch (more accurate coefficient)
        let ph_drop_starch = (diet_starch * 0.028);  
        
        // pH buffering from peNDF (stimulates rumination and salivation)
        let ph_lift_peNDF = (diet_peNDF * 0.012);  
        
        // Calculate base pH
        let pred_ph = base_ph - ph_drop_starch + ph_lift_peNDF;
        
        // Alfalfa buffering bonus (cation exchange capacity - K, Ca, Mg)
        let alf_proportion = kg_alf / total_dm;
        if(alf_proportion > 0) pred_ph += alf_proportion * 0.18;  

        // Clamp pH to physiologically realistic range
        if(pred_ph > 7.0) pred_ph = 7.0;
        if(pred_ph < 5.3) pred_ph = 5.3;  

        // 4. Calculate Associative Effects (The Interaction)

        let fiber_bug_health = 100; // % Efficiency
        let starch_bug_health = 100;
        let messages = [];

        // --- A. The Nitrogen Effect (Positive Associative Effect) ---
        // Critical threshold is around 7-8% CP for microbial protein synthesis
        if(diet_cp < 8.0) {  
            let deficit = 8.0 - diet_cp;
            let crash = deficit * 18;  
            fiber_bug_health -= crash;
            messages.push(`<span class="neg-text">NITROGEN LIMITATION:</span> Diet CP is ${diet_cp.toFixed(1)}%. Microbial N limits fiber digestion.`);
        } else {
             // Positive synergy when protein supplementation helps low-quality forage
             if (kg_hay > 5 && (kg_sbm > 0.3 || kg_alf > 1.0)) {
                 messages.push(`<span class="pos-text">PROTEIN SYNERGY:</span> RDP supplementation enhancing forage fiber digestion.`);
             }
        }

        // --- B. The pH Effect (Negative Associative Effect) ---
        // Cellulolytic bacteria (F. succinogenes, R. albus) are pH-sensitive
        
        if(pred_ph < 6.0) {
            let acidity = 6.0 - pred_ph;
            let burn = acidity * 70;  
            if(burn > 70) burn = 70;  
            fiber_bug_health -= burn;
            messages.push(`<span class="neg-text">SUBACUTE ACIDOSIS:</span> pH ${pred_ph.toFixed(2)} severely inhibits cellulolytic bacteria.`);
        } else if(pred_ph < 6.2) {
            let mild_acidity = 6.2 - pred_ph;
            let mild_burn = mild_acidity * 35;
            fiber_bug_health -= mild_burn;
            messages.push(`<span class="neg-text">MILD ACIDOSIS:</span> pH ${pred_ph.toFixed(2)} beginning to reduce fiber digestion.`);
        }

        // Warning for very low pH (clinical acidosis risk)
        if(pred_ph < 5.6) {
            messages.push(`<span class="neg-text">⚠ ACUTE ACIDOSIS RISK:</span> This diet poses serious health risks.`);
        }

        // Clamp health values
        if(fiber_bug_health < 0) fiber_bug_health = 0;
        if(fiber_bug_health > 100) fiber_bug_health = 100;

        // --- C. Realized Energy Calculation ---
        // More sophisticated partitioning of energy sources
        
        // Estimate digestibility depression on NDF
        // NDF typically contributes 30-50% of TDN in forage-based diets
        let ndf_contribution = diet_ndf * 0.45;  // Assume 45% digestibility at optimal conditions
        let ndf_energy = ndf_contribution * (fiber_bug_health / 100);
        
        // Starch and other NSC (non-structural carbs) are less affected by these factors
        let non_fiber_energy = diet_base_tdn - ndf_contribution;
        
        // Minor reduction in starch digestion at very low pH (< 5.5)
        if(pred_ph < 5.5) {
            non_fiber_energy *= 0.95;  // 5% reduction for extreme acidosis
        }
        
        let realized_tdn = non_fiber_energy + ndf_energy;

        // Total TDN Mass
        let expected_mass = total_dm * (diet_base_tdn/100);
        let realized_mass = total_dm * (realized_tdn/100);

        // 5. Update UI
        document.getElementById('disp_cp').innerText = diet_cp.toFixed(1) + "%";
        document.getElementById('disp_ndf').innerText = diet_ndf.toFixed(1) + "%";
        document.getElementById('disp_starch').innerText = diet_starch.toFixed(1) + "%";
        document.getElementById('disp_ph').innerText = pred_ph.toFixed(2);

        if(messages.length === 0) messages.push("Diet is well-balanced. Interactions are neutral to slightly positive.");
        document.getElementById('mech_text').innerHTML = messages.join("<br>");

        // 6. Charts
        updateCharts(expected_mass, realized_mass, fiber_bug_health, starch_bug_health);
    }

    function updateCharts(exp, real, fibHealth, starchHealth) {
        // ENERGY CHART
        const ctx1 = document.getElementById('energyChart').getContext('2d');
        if(energyChart) energyChart.destroy();
        
        let color = "#34495e";
        let percent_change = ((real - exp) / exp) * 100;
        
        if (percent_change < -2) color = "#c0392b";  // Negative associative effect
        if (percent_change > 2) color = "#27ae60";   // Positive associative effect

        energyChart = new Chart(ctx1, {
            type: 'bar',
            data: {
                labels: ['Total Diet Energy (TDN kg)'],
                datasets: [
                    { label: 'Expected (Additive)', data: [exp], backgroundColor: '#95a5a6' },
                    { label: 'Realized (with interactions)', data: [real], backgroundColor: color }
                ]
            },
            options: {
                plugins: { 
                    title: { display: true, text: 'Associative Effect on Energy' },
                    legend: { display: true }
                },
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true, title: { display: true, text: 'TDN (kg)' } }
                }
            }
        });

        // MICROBE CHART
        const ctx2 = document.getElementById('microbeChart').getContext('2d');
        if(microbeChart) microbeChart.destroy();

        microbeChart = new Chart(ctx2, {
            type: 'doughnut',
            data: {
                labels: ['Active Cellulolytic Bacteria', 'Inhibited/Inactive'],
                datasets: [{
                    data: [fibHealth, 100-fibHealth],
                    backgroundColor: ['#27ae60', '#e74c3c']
                }]
            },
            options: {
                plugins: { 
                    title: { display: true, text: 'Fiber Digester Activity (%)' },
                    legend: { display: true, position: 'bottom' }
                },
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    // Initialize on page load
    updateModel();

</script>
</body>
</html>
    """
    
    with open("advanced_rumen_sim.html", "w", encoding='utf-8') as f:
        f.write(html_content)
    
    webbrowser.open('file://' + os.path.realpath("advanced_rumen_sim.html"))

if __name__ == "__main__":
    create_advanced_rumen_simulation()