import os

def create_advanced_simulation():
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sulfide Detoxification Energetics Model</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f9; color: #333; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        h2 { font-size: 1.2rem; color: #7f8c8d; margin-top: 0; }
        
        /* Layout */
        .grid { display: grid; grid-template-columns: 1fr 2fr; gap: 30px; margin-top: 20px; }
        
        /* Controls */
        .controls { background: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #e9ecef; }
        .control-group { margin-bottom: 20px; }
        label { display: block; font-weight: bold; margin-bottom: 5px; font-size: 0.95rem; }
        input[type="range"] { width: 100%; cursor: pointer; }
        .value-display { float: right; color: #3498db; font-weight: bold; font-family: monospace; font-size: 1rem; }
        .sub-label { font-size: 0.75rem; color: #95a5a6; display: block; margin-top: 2px; }
        
        /* Results */
        .results { display: flex; flex-direction: column; gap: 20px; }
        .kpi-box { display: flex; justify-content: space-between; gap: 15px; }
        .kpi { flex: 1; background: #ecf0f1; padding: 15px; border-radius: 6px; text-align: center; }
        .kpi h3 { margin: 0 0 10px 0; font-size: 0.9rem; color: #7f8c8d; }
        .kpi .num { font-size: 1.4rem; font-weight: bold; color: #2c3e50; }
        .kpi .unit { font-size: 0.8rem; color: #95a5a6; }
        .highlight { color: #e74c3c !important; }

        /* Live Equation Box */
        .equation-section { margin-top: 30px; background-color: #e8f6f3; border: 1px solid #a2d9ce; padding: 20px; border-radius: 8px; }
        .math-step { font-family: 'Courier New', Courier, monospace; margin-bottom: 8px; border-bottom: 1px dashed #d1f2eb; padding-bottom: 4px; }
        .math-var { color: #d35400; font-weight: bold; }
        .math-res { color: #27ae60; font-weight: bold; }
        .imp { color: #7f8c8d; font-size: 0.9em; font-weight: normal; }

        /* Citations */
        .citations { margin-top: 40px; font-size: 0.85rem; color: #7f8c8d; border-top: 1px solid #eee; padding-top: 20px; }
        .citations ul { padding-left: 20px; }
        .citations li { margin-bottom: 5px; }
    </style>
</head>
<body>

<div class="container">
    <h1>The Sulfur Tax: Bio-Energetic Simulation</h1>
    <h2>Projected Maintenance Cost of Sulfide Detoxification (SQR Pathway)</h2>
    
    <div class="grid">
        <!-- Controls Section -->
        <div class="controls">
            <h3>Input Parameters</h3>
            
            <div class="control-group">
                <label>Steer Body Weight <span id="val_bw" class="value-display"></span></label>
                <input type="range" id="bw" min="200" max="700" step="10" value="400" oninput="updateModel()">
            </div>

            <div class="control-group">
                <label>Dry Matter Intake <span id="val_dmi" class="value-display"></span></label>
                <input type="range" id="dmi" min="5" max="15" step="0.5" value="10" oninput="updateModel()">
            </div>

            <div class="control-group">
                <label>Dietary Sulfur (% DM) <span id="val_feedS" class="value-display"></span></label>
                <input type="range" id="feedS" min="0.1" max="1.0" step="0.05" value="0.50" oninput="updateModel()">
            </div>

            <div class="control-group">
                <label>Water Sulfate (mg/L) <span id="val_waterS" class="value-display"></span></label>
                <input type="range" id="waterS" min="0" max="5000" step="100" value="2000" oninput="updateModel()">
            </div>

            <div class="control-group">
                <label>Water Intake <span id="val_waterIn" class="value-display"></span></label>
                <input type="range" id="waterIn" min="20" max="100" step="5" value="50" oninput="updateModel()">
            </div>

            <div class="control-group">
                <label>Absorption Efficiency <span id="val_abs" class="value-display"></span></label>
                <input type="range" id="abs" min="20" max="80" step="5" value="50" oninput="updateModel()">
            </div>

            <!-- NEW CONTROL -->
            <div class="control-group">
                <label>Fraction of Absorbed Sulfide Oxidized to Sulfate <span id="val_ox" class="value-display"></span></label>
                <input type="range" id="ox" min="50" max="100" step="5" value="100" oninput="updateModel()">
                <span class="sub-label">The fraction of absorbed sulfide flux that proceeds through complete mitochondrial oxidation to sulfate, rather than alternative sulfur handling pathways.</span>
            </div>
        </div>

        <!-- Results Section -->
        <div class="results">
            <!-- KPIs -->
            <div class="kpi-box">
                <div class="kpi">
                    <h3>Total S Intake</h3>
                    <div class="num" id="res_totalS">0</div>
                    <div class="unit">grams/day</div>
                </div>
                <div class="kpi">
                    <h3>O2 Cost</h3>
                    <div class="num" id="res_o2">0</div>
                    <div class="unit">Liters/day</div>
                </div>
                <div class="kpi">
                    <h3>Sulfide Tax</h3>
                    <div class="num highlight" id="res_sCost">0</div>
                    <div class="unit">Mcal/day</div>
                </div>
                <div class="kpi">
                    <h3>% Increase NEm</h3>
                    <div class="num highlight" id="res_pct">0</div>
                    <div class="unit">%</div>
                </div>
            </div>

            <!-- Charts -->
            <canvas id="energyChart" width="400" height="200"></canvas>
            
        </div>
    </div>

    <!-- Live Equation Display -->
    <div class="equation-section">
        <h3 style="margin-top:0; color:#16a085;">Live Stoichiometric Calculation:</h3>
        <div id="equation-display"></div>
    </div>

    <div class="citations">
        <strong>Model Basis & Citations:</strong>
        <ul>
            <li><strong>Stoichiometry (H₂S + 2O₂ → SO₄):</strong> Bouillaud, F., & Blachier, F. (2011). Mitochondrial oxidation of sulfide. <em>ARS.</em></li>
            <li><strong>Caloric Equivalent (4.89 kcal/L O₂):</strong> Brouwer, E. (1965). Report of Sub-committee on Constants and Factors. <em>EAAP.</em></li>
            <li><strong>Absorption Range (30-60%):</strong> Drewnoski, M. E., & Hansen, S. L. (2014). High-sulfur in beef cattle diets. <em>J. Anim. Sci.</em></li>
            <li><strong>Base NEm Equation:</strong> Tedeschi, L. O., & Fox, D. G. (2020). <em>The Ruminant Nutrition System.</em></li>
        </ul>
    </div>
</div>

<script>
    // Constants
    const MW_S = 32.06; // g/mol
    const MW_SO4 = 96.06; // g/mol
    const S_IN_SO4 = MW_S / MW_SO4; // ~0.333
    const MOL_VOL = 22.4; // L/mol gas at STP
    const KCAL_PER_L_O2 = 4.89; // Brouwer, 1965
    const NEM_COEFF = 0.077; // Mcal/kg BW^0.75
    
    // Conversion Factors
    const KG_TO_LB = 2.20462;
    const L_TO_GAL = 0.264172;

    let myChart = null;

    function updateModel() {
        // 1. Get Inputs
        const bw = parseFloat(document.getElementById('bw').value);
        const dmi = parseFloat(document.getElementById('dmi').value);
        const feedS_pct = parseFloat(document.getElementById('feedS').value);
        const waterS_conc = parseFloat(document.getElementById('waterS').value);
        const waterIn = parseFloat(document.getElementById('waterIn').value);
        const abs_pct = parseFloat(document.getElementById('abs').value);
        const ox_pct = parseFloat(document.getElementById('ox').value); // NEW

        // 2. Calculations
        // Conversions for Display
        const bw_lb = (bw * KG_TO_LB).toFixed(0);
        const dmi_lb = (dmi * KG_TO_LB).toFixed(1);
        const waterIn_gal = (waterIn * L_TO_GAL).toFixed(1);

        // Feed Sulfur
        const feedS_g = dmi * (feedS_pct / 100) * 1000;
        
        // Water Sulfur (Sulfate -> Sulfur)
        const waterSulfate_g = waterIn * (waterS_conc / 1000);
        const waterS_g = waterSulfate_g * S_IN_SO4;

        // Total Intake
        const totalS_g = feedS_g + waterS_g;

        // Absorbed Sulfur
        const absorbedS_g = totalS_g * (abs_pct / 100);

        // Moles of Sulfur
        const mols_S = absorbedS_g / MW_S;

        // Oxygen Requirement (2 mol O2 per 1 mol S) * OXIDATION FACTOR
        const ox_factor = ox_pct / 100;
        const mols_O2 = mols_S * 2 * ox_factor;
        const liters_O2 = mols_O2 * MOL_VOL;

        // Heat Production
        const heat_kcal = liters_O2 * KCAL_PER_L_O2;
        const heat_mcal = heat_kcal / 1000;

        // Base NEm
        const mbw = Math.pow(bw, 0.75);
        const base_nem = NEM_COEFF * mbw;

        // Total NEm
        const total_nem = base_nem + heat_mcal;
        const pct_increase = (heat_mcal / base_nem) * 100;

        // 3. Update Text Labels
        document.getElementById('val_bw').innerText = `${bw} kg (${bw_lb} lb)`;
        document.getElementById('val_dmi').innerText = `${dmi} kg (${dmi_lb} lb)`;
        document.getElementById('val_feedS').innerText = `${feedS_pct.toFixed(2)} %`;
        document.getElementById('val_waterS').innerText = `${waterS_conc} mg/L`;
        document.getElementById('val_waterIn').innerText = `${waterIn} L (${waterIn_gal} gal)`;
        document.getElementById('val_abs').innerText = `${abs_pct} %`;
        document.getElementById('val_ox').innerText = `${ox_pct} %`; // NEW

        // 4. Update KPIs
        document.getElementById('res_totalS').innerText = totalS_g.toFixed(1);
        document.getElementById('res_o2').innerText = liters_O2.toFixed(1);
        document.getElementById('res_sCost').innerText = heat_mcal.toFixed(3);
        document.getElementById('res_pct').innerText = "+" + pct_increase.toFixed(2);

        // 5. Update Equation Box (Showing Oxidation Factor)
        const eqHTML = `
            <div class="math-step">
                <strong>1. Total Sulfur Intake:</strong> 
                (<span class="math-var">${dmi}</span> kg <span class="imp">[${dmi_lb} lb]</span> Feed × <span class="math-var">${feedS_pct}</span>%) + 
                (<span class="math-var">${waterIn}</span> L <span class="imp">[${waterIn_gal} gal]</span> Water × <span class="math-var">${waterS_conc}</span> mg/L × 0.333) = 
                <span class="math-res">${totalS_g.toFixed(1)} g S/day</span>
            </div>
            <div class="math-step">
                <strong>2. Absorbed S:</strong> 
                <span class="math-res">${totalS_g.toFixed(1)}</span> g × <span class="math-var">${abs_pct/100}</span> (Abs Coeff) = 
                <span class="math-res">${absorbedS_g.toFixed(1)} g S</span>
            </div>
            <div class="math-step">
                <strong>3. O₂ Demand:</strong> 
                (<span class="math-res">${absorbedS_g.toFixed(1)}</span> g / 32.06) × 2 mol O₂ × <span class="math-var">${ox_factor}</span> (Ox. Factor) = 
                <span class="math-res">${mols_O2.toFixed(2)} mol O₂</span>
            </div>
            <div class="math-step">
                <strong>4. Heat Production:</strong> 
                <span class="math-res">${mols_O2.toFixed(2)}</span> mol × 22.4 L/mol × 4.89 kcal/L = 
                <span class="math-res">${heat_mcal.toFixed(3)} Mcal/day</span>
            </div>
        `;
        document.getElementById('equation-display').innerHTML = eqHTML;

        updateChart(base_nem, heat_mcal);
    }

    function updateChart(base, tax) {
        const ctx = document.getElementById('energyChart').getContext('2d');
        
        if (myChart) {
            myChart.destroy();
        }

        myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Base NEm Requirement', 'Sulfide-Adjusted NEm'],
                datasets: [
                    {
                        label: 'Standard Maintenance',
                        data: [base, base],
                        backgroundColor: '#3498db',
                        stack: 'Stack 0',
                    },
                    {
                        label: 'Sulfide Detox Cost',
                        data: [0, tax], 
                        backgroundColor: '#e74c3c',
                        stack: 'Stack 0',
                    }
                ]
            },
            options: {
                responsive: true,
                indexAxis: 'y',
                plugins: {
                    title: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + context.raw.toFixed(3) + ' Mcal';
                            }
                        }
                    }
                },
                scales: {
                    x: { stacked: true, title: {display:true, text: 'Energy (Mcal/day)'} },
                    y: { stacked: true }
                }
            }
        });
    }

    // Initialize
    updateModel();

</script>
</body>
</html>
    """
    
    filename = "sulfur_simulation_advanced.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Success! '{filename}' has been created.")
    print("Open this file to see the advanced model with Oxidation Completeness adjustment.")

if __name__ == "__main__":
    create_advanced_simulation()