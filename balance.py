import webbrowser
import os

def create_rumen_simulation():
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TAMU-Based Rumen Associative Effects Simulator</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; padding: 20px; color: #333; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h1 { color: #500000; border-bottom: 2px solid #500000; padding-bottom: 10px; } /* TAMU Maroon */
        .subtitle { font-size: 0.9rem; color: #666; margin-top: -10px; margin-bottom: 20px; font-style: italic; }
        
        .dashboard { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
        .controls { background: #f9f9f9; padding: 20px; border-radius: 8px; border: 1px solid #ddd; }
        .monitor { background: #fff; }
        
        .slider-group { margin-bottom: 25px; }
        label { display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 5px; }
        input[type="range"] { width: 100%; cursor: pointer; accent-color: #500000; }
        .feed-desc { font-size: 0.8rem; color: #777; margin-top: 2px; }

        .meters { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px; }
        .meter-box { text-align: center; padding: 10px; border-radius: 6px; background: #eee; border: 1px solid #ccc; }
        .meter-val { font-size: 1.4rem; font-weight: bold; }
        .meter-label { font-size: 0.85rem; color: #555; }
        
        .warning-positive { color: #27ae60; font-weight: bold; }
        .warning-negative { color: #c0392b; font-weight: bold; }
        .status-box { padding: 15px; border-radius: 8px; margin-top: 20px; font-size: 0.95rem; line-height: 1.5; background: #e8f4f8; border-left: 5px solid #2980b9; }

        .citation { margin-top: 40px; font-size: 0.75rem; color: #999; border-top: 1px solid #eee; padding-top: 10px; }
    </style>
</head>
<body>

<div class="container">
    <h1>Rumen Associative Effects Simulator</h1>
    <div class="subtitle">Based on concepts from the Texas A&M Ruminant Nutrition System (Tedeschi & Fox)</div>

    <div class="dashboard">
        <!-- CONTROLS -->
        <div class="controls">
            <h3>Diet Formulation (kg DM/day)</h3>
            
            <!-- Feed 1: Low Quality Forage -->
            <div class="slider-group">
                <label>Low Quality Forage (Wheat Straw) <span id="val_forage">5.0 kg</span></label>
                <input type="range" id="forage" min="0" max="10" step="0.5" value="5.0" oninput="updateModel()">
                <div class="feed-desc">High Fiber (NDF), Low Protein. Requires N for digestion.</div>
            </div>

            <!-- Feed 2: Rapidly Fermentable Starch -->
            <div class="slider-group">
                <label>Corn (Starch Source) <span id="val_corn">0.0 kg</span></label>
                <input type="range" id="corn" min="0" max="8" step="0.5" value="0.0" oninput="updateModel()">
                <div class="feed-desc">High Energy. Lowers pH. The source of Negative Effects.</div>
            </div>

            <!-- Feed 3: RDP Source -->
            <div class="slider-group">
                <label>Protein Supplement (SBM/Urea mix) <span id="val_prot">0.0 kg</span></label>
                <input type="range" id="prot" min="0" max="2" step="0.1" value="0.0" oninput="updateModel()">
                <div class="feed-desc">Provides Ammonia (NH3) for fiber bugs. The source of Positive Effects.</div>
            </div>
            
            <div class="status-box" id="mechanism_readout">
                Adjust sliders to see effects.
            </div>
        </div>

        <!-- VISUALIZATION -->
        <div class="monitor">
            <div class="meters">
                <div class="meter-box">
                    <div class="meter-label">Predicted Rumen pH</div>
                    <div class="meter-val" id="disp_ph">6.8</div>
                    <div id="ph_status" style="font-size:0.8rem">-</div>
                </div>
                <div class="meter-box">
                    <div class="meter-label">Ammonia Balance</div>
                    <div class="meter-val" id="disp_nh3">Deficient</div>
                    <div id="nh3_status" style="font-size:0.8rem">Bugs Starving</div>
                </div>
            </div>

            <canvas id="effectChart"></canvas>
            <p style="text-align:center; font-size:0.9rem; color:#666;">
                <span style="color:#bdc3c7">■ Expected (Additive)</span> vs 
                <span style="color:#500000">■ Realized (Biological)</span>
            </p>
        </div>
    </div>

    <div class="citation">
        <strong>Sources & Logic:</strong>
        <ul>
            <li><strong>Negative Effect Logic:</strong> Based on pH depression inhibiting cellulolytic bacteria ($K_d$ reduction). See: <em>Tedeschi, L. O., & Fox, D. G. (2020). The Ruminant Nutrition System.</em> & <em>Dixon & Stock (1987).</em></li>
            <li><strong>Positive Effect Logic:</strong> Based on Nitrogen limiting kinetics (Relief of N bottleneck). See: <em>Klopfenstein et al. (University of Nebraska)</em> and TAMU models on RDP requirements.</li>
            <li><strong>Disclaimer:</strong> This is a simplified educational simulation for ANSC 602. It uses simplified coefficients to demonstrate trends and is not a clinical ration balancer.</li>
        </ul>
    </div>
</div>

<script>
    let myChart = null;

    function updateModel() {
        // 1. GET INPUTS
        const forage = parseFloat(document.getElementById('forage').value);
        const corn = parseFloat(document.getElementById('corn').value);
        const prot = parseFloat(document.getElementById('prot').value);

        // Update Labels
        document.getElementById('val_forage').innerText = forage + " kg";
        document.getElementById('val_corn').innerText = corn + " kg";
        document.getElementById('val_prot').innerText = prot + " kg";

        // 2. DEFINE FEED SPECS (Simplified for Simulation)
        // Energy values in TDN (Total Digestible Nutrients) %
        const forage_tdn_base = 45; // Low quality straw
        const corn_tdn = 88;        // High energy
        const prot_tdn = 80;        // Supplement

        // Nitrogen/Protein content (CP %)
        const forage_cp = 4;        // Very low
        const corn_cp = 9;          // Low
        const prot_cp = 45;         // High

        // 3. CALCULATE "ADDITIVE" (EXPECTED) ENERGY
        // This is simple math: (Kg * Energy) + (Kg * Energy)...
        // This assumes no biological interaction.
        let total_dm = forage + corn + prot;
        if (total_dm === 0) total_dm = 0.1; // Avoid divide by zero

        const expected_tdn_mass = (forage * (forage_tdn_base/100)) + 
                                  (corn * (corn_tdn/100)) + 
                                  (prot * (prot_tdn/100));

        // 4. SIMULATE RUMEN ECOLOGY (The Associative Effects)
        
        // A. pH Calculation (The Starch Effect)
        // Base pH is 6.8. Corn drops it. Forage buffers it (saliva).
        // Logic: Starch drives pH down. NDF (Forage) drives pH up (chewing/saliva).
        let ph_stress = (corn * 0.25) - (forage * 0.05);
        let rumen_ph = 6.8 - ph_stress;
        if (rumen_ph < 5.5) rumen_ph = 5.5; // Floor
        if (rumen_ph > 7.0) rumen_ph = 7.0; // Ceiling

        // B. Calculate Nitrogen Balance (The Ammonia Effect)
        // Fiber bugs need N. 
        // Logic: Calculate total CP intake vs Total Energy intake ratio.
        const total_cp_mass = (forage * forage_cp/100) + (corn * corn_cp/100) + (prot * prot_cp/100);
        // Simplified rule: Bugs need ~10-12% CP in diet to digest fiber maximally.
        const cp_percent = (total_cp_mass / total_dm) * 100;
        
        
        // 5. APPLY ASSOCIATIVE EFFECTS TO FORAGE DIGESTIBILITY
        
        let forage_tdn_real = forage_tdn_base;
        let messages = [];

        // --- POSITIVE EFFECT CHECK (Nitrogen) ---
        // If CP < 7%, fiber digestion crashes (Nitrogen Starvation).
        // If we add protein, we recover this.
        let n_factor = 1.0;
        if (cp_percent < 6.0) {
            n_factor = 0.6; // Severe crash (40% loss of fiber energy)
            messages.push("<span class='warning-negative'>NEGATIVE: Nitrogen Starvation.</span> Forage $K_d$ stalled.");
        } else if (cp_percent < 9.0) {
            n_factor = 0.6 + ((cp_percent - 6.0) / 3.0) * 0.4; // Linear recovery
            if (prot > 0) messages.push("<span class='warning-positive'>POSITIVE:</span> Protein addition is unlocking forage energy.");
        } else {
            n_factor = 1.05; // Slight synergy at optimal N
        }

        // --- NEGATIVE EFFECT CHECK (pH / Starch) ---
        // If pH < 6.2, cellulolytic bacteria are inhibited.
        let ph_factor = 1.0;
        if (rumen_ph < 6.2) {
            // Linear drop from 6.2 down to 5.8
            let drop = (6.2 - rumen_ph) * 1.5; 
            if (drop > 0.5) drop = 0.5; // Cap damage at 50%
            ph_factor = 1.0 - drop;
            messages.push("<span class='warning-negative'>NEGATIVE:</span> Low pH is killing fiber digesters ($K_d$ crash).");
        }

        // Apply factors to Forage ONLY (Corn/Protein are digested fine usually)
        // We use the lower of the two factors (Liebig's Law of the Minimum)
        // Actually, they compound.
        
        let combined_factor = n_factor * ph_factor;
        forage_tdn_real = forage_tdn_base * combined_factor;

        // 6. CALCULATE REALIZED ENERGY
        const realized_tdn_mass = (forage * (forage_tdn_real/100)) + 
                                  (corn * (corn_tdn/100)) + 
                                  (prot * (prot_tdn/100));

        // 7. UI UPDATES
        document.getElementById('disp_ph').innerText = rumen_ph.toFixed(2);
        
        // pH Color
        const ph_el = document.getElementById('disp_ph');
        if (rumen_ph < 6.0) ph_el.style.color = "#c0392b";
        else if (rumen_ph < 6.2) ph_el.style.color = "#d35400";
        else ph_el.style.color = "#27ae60";

        // NH3 Status
        const nh3_el = document.getElementById('disp_nh3');
        if (cp_percent < 7.0) { nh3_el.innerText = "Deficient"; nh3_el.style.color="#c0392b"; }
        else if (cp_percent < 10.0) { nh3_el.innerText = "Sub-Optimal"; nh3_el.style.color="#f39c12"; }
        else { nh3_el.innerText = "Sufficient"; nh3_el.style.color="#27ae60"; }

        // Messages
        if (messages.length === 0) messages.push("System Balanced. Additive assumptions hold.");
        document.getElementById('mechanism_readout').innerHTML = messages.join("<br>");

        updateChart(expected_tdn_mass, realized_tdn_mass);
    }

    function updateChart(expected, realized) {
        const ctx = document.getElementById('effectChart').getContext('2d');
        if (myChart) myChart.destroy();

        // Determine Associative Effect Type
        let diff = realized - expected;
        let color = "#34495e";
        if (diff < -0.1) color = "#c0392b"; // Red for negative
        if (diff > 0.1) color = "#27ae60"; // Green for positive

        myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Total Diet Energy (TDN kg)'],
                datasets: [
                    {
                        label: 'Expected (Additive)',
                        data: [expected],
                        backgroundColor: '#bdc3c7',
                        barPercentage: 0.6
                    },
                    {
                        label: 'Realized (Biological)',
                        data: [realized],
                        backgroundColor: color,
                        barPercentage: 0.6
                    }
                ]
            },
            options: {
                indexAxis: 'y',
                scales: { x: { beginAtZero: true } },
                plugins: {
                    title: { display: true, text: 'The Associative Effect Gap' }
                }
            }
        });
    }

    // Init
    updateModel();

</script>
</body>
</html>
    """
    
    with open("rumen_model.html", "w", encoding='utf-8') as f:
        f.write(html_content)
    
    # Automatically open the file in the browser
    webbrowser.open('file://' + os.path.realpath("rumen_model.html"))
    print("Simulation generated: rumen_model.html")

if __name__ == "__main__":
    create_rumen_simulation()
