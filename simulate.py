import os

def create_simulation_file():
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
        .grid { display: grid; grid-template-columns: 1fr 2fr; gap: 30px; margin-top: 20px; }
        .controls { background: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #e9ecef; }
        .control-group { margin-bottom: 20px; }
        label { display: block; font-weight: bold; margin-bottom: 5px; }
        input[type="range"] { width: 100%; }
        .value-display { float: right; color: #3498db; font-weight: bold; }
        .results { display: flex; flex-direction: column; gap: 20px; }
        .kpi-box { display: flex; justify-content: space-between; gap: 15px; }
        .kpi { flex: 1; background: #ecf0f1; padding: 15px; border-radius: 6px; text-align: center; }
        .kpi h3 { margin: 0 0 10px 0; font-size: 0.9rem; color: #7f8c8d; }
        .kpi .num { font-size: 1.5rem; font-weight: bold; color: #2c3e50; }
        .kpi .unit { font-size: 0.8rem; color: #95a5a6; }
        .highlight { color: #e74c3c !important; }
        .footer { margin-top: 40px; font-size: 0.8rem; color: #95a5a6; text-align: center; border-top: 1px solid #eee; padding-top: 20px; }
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
                <label>Steer Body Weight (kg) <span id="val_bw" class="value-display">400</span></label>
                <input type="range" id="bw" min="200" max="700" step="10" value="400" oninput="updateModel()">
            </div>

            <div class="control-group">
                <label>Dry Matter Intake (kg/d) <span id="val_dmi" class="value-display">10</span></label>
                <input type="range" id="dmi" min="5" max="15" step="0.5" value="10" oninput="updateModel()">
            </div>

            <div class="control-group">
                <label>Dietary Sulfur (% DM) <span id="val_feedS" class="value-display">0.50</span></label>
                <input type="range" id="feedS" min="0.1" max="1.0" step="0.05" value="0.50" oninput="updateModel()">
            </div>

            <div class="control-group">
                <label>Water Sulfate (mg/L) <span id="val_waterS" class="value-display">2000</span></label>
                <input type="range" id="waterS" min="0" max="5000" step="100" value="2000" oninput="updateModel()">
            </div>

            <div class="control-group">
                <label>Water Intake (L/d) <span id="val_waterIn" class="value-display">50</span></label>
                <input type="range" id="waterIn" min="20" max="80" step="5" value="50" oninput="updateModel()">
            </div>

            <div class="control-group">
                <label>Absorption Efficiency (%) <span id="val_abs" class="value-display">50</span></label>
                <input type="range" id="abs" min="20" max="80" step="5" value="50" oninput="updateModel()">
                <small style="color:#7f8c8d">Fraction of ruminal sulfide absorbed into portal blood.</small>
            </div>
        </div>

        <!-- Results Section -->
        <div class="results">
            <!-- KPIs -->
            <div class="kpi-box">
                <div class="kpi">
                    <h3>Total Sulfur Intake</h3>
                    <div class="num" id="res_totalS">0</div>
                    <div class="unit">g/day</div>
                </div>
                <div class="kpi">
                    <h3>O2 Consumption</h3>
                    <div class="num" id="res_o2">0</div>
                    <div class="unit">L/day</div>
                </div>
                <div class="kpi">
                    <h3>Sulfide Heat (Tax)</h3>
                    <div class="num highlight" id="res_sCost">0</div>
                    <div class="unit">Mcal/day</div>
                </div>
                <div class="kpi">
                    <h3>% Increase in NEm</h3>
                    <div class="num highlight" id="res_pct">0</div>
                    <div class="unit">%</div>
                </div>
            </div>

            <!-- Charts -->
            <canvas id="energyChart" width="400" height="200"></canvas>
            
        </div>
    </div>

    <div class="footer">
        <strong>ANSC 602: Energetics in Biological Systems</strong> | Student: Justin Houck | January 2026<br>
        Model assumes stoichiometry: H₂S + 2 O₂ → SO₄²⁻ + 2 H⁺ | Caloric Equivalent: 4.89 kcal/L O₂
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

    let myChart = null;

    function updateModel() {
        // 1. Get Inputs
        const bw = parseFloat(document.getElementById('bw').value);
        const dmi = parseFloat(document.getElementById('dmi').value);
        const feedS_pct = parseFloat(document.getElementById('feedS').value);
        const waterS_conc = parseFloat(document.getElementById('waterS').value);
        const waterIn = parseFloat(document.getElementById('waterIn').value);
        const abs_pct = parseFloat(document.getElementById('abs').value);

        // Update Text Labels
        document.getElementById('val_bw').innerText = bw;
        document.getElementById('val_dmi').innerText = dmi;
        document.getElementById('val_feedS').innerText = feedS_pct.toFixed(2);
        document.getElementById('val_waterS').innerText = waterS_conc;
        document.getElementById('val_waterIn').innerText = waterIn;
        document.getElementById('val_abs').innerText = abs_pct;

        // 2. Calculations
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

        // Oxygen Requirement (2 mol O2 per 1 mol S)
        const mols_O2 = mols_S * 2;
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

        // 3. Update UI
        document.getElementById('res_totalS').innerText = totalS_g.toFixed(1);
        document.getElementById('res_o2').innerText = liters_O2.toFixed(1);
        document.getElementById('res_sCost').innerText = heat_mcal.toFixed(3);
        document.getElementById('res_pct').innerText = "+" + pct_increase.toFixed(2);

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
                labels: ['Standard NEm Requirement', 'Sulfide-Adjusted NEm'],
                datasets: [
                    {
                        label: 'Base Maintenance (Mcal)',
                        data: [base, base],
                        backgroundColor: '#3498db',
                        stack: 'Stack 0',
                    },
                    {
                        label: 'Sulfide Detox Cost (Mcal)',
                        data: [0, tax], // Only add to the second bar
                        backgroundColor: '#e74c3c',
                        stack: 'Stack 0',
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Impact of Sulfide Detoxification on Total Maintenance Energy'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + context.raw.toFixed(3) + ' Mcal';
                            }
                        }
                    }
                },
                scales: {
                    x: { stacked: true },
                    y: { 
                        stacked: true,
                        title: { display: true, text: 'Energy (Mcal/day)' }
                    }
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
    
    filename = "sulfur_simulation.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Success! '{filename}' has been created in this directory.")
    print("Open this file in your web browser to view the simulation.")

if __name__ == "__main__":
    create_simulation_file()
