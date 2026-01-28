import os
import webbrowser

def create_final_simulation():
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
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        
        /* Header */
        header { border-bottom: 2px solid #3498db; padding-bottom: 20px; margin-bottom: 30px; }
        h1 { color: #2c3e50; margin: 0; }
        .subtitle { font-size: 1.1rem; color: #7f8c8d; margin-top: 5px; }

        /* Layout */
        .grid { display: grid; grid-template-columns: 1fr 2fr; gap: 40px; }
        
        /* Controls */
        .controls { background: #f8f9fa; padding: 25px; border-radius: 8px; border: 1px solid #e9ecef; height: fit-content; }
        .control-group { margin-bottom: 20px; }
        label { display: block; font-weight: bold; margin-bottom: 5px; font-size: 0.95rem; color: #2c3e50; }
        input[type="range"] { width: 100%; cursor: pointer; accent-color: #3498db; }
        .value-display { float: right; color: #3498db; font-weight: bold; font-family: monospace; font-size: 1rem; }
        .sub-label { font-size: 0.8rem; color: #7f8c8d; display: block; margin-top: 4px; font-style: italic; line-height: 1.4; }
        hr { border: 0; border-top: 1px solid #ddd; margin: 20px 0; }
        
        /* Results & KPIs */
        .results { display: flex; flex-direction: column; gap: 25px; }
        
        .warning-box { background: #fff3cd; border-left: 5px solid #ffc107; padding: 15px; border-radius: 4px; display: none; margin-bottom: 20px; }
        .warning-text { color: #856404; font-size: 0.9rem; line-height: 1.5; }
        .warning-box.critical { background: #f8d7da; border-left-color: #dc3545; }
        .warning-box.critical .warning-text { color: #721c24; }

        .kpi-box { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }
        .kpi { background: #ecf0f1; padding: 15px; border-radius: 6px; text-align: center; border: 1px solid #dee2e6; }
        .kpi h3 { margin: 0 0 5px 0; font-size: 0.85rem; text-transform: uppercase; color: #7f8c8d; letter-spacing: 0.5px; }
        .kpi .num { font-size: 1.5rem; font-weight: bold; color: #2c3e50; }
        .kpi .unit { font-size: 0.8rem; color: #95a5a6; }
        .highlight .num { color: #e74c3c; }

        /* Equation Box */
        .equation-section { background-color: #eef9f9; border: 1px solid #b2dfdb; padding: 20px; border-radius: 8px; }
        .math-step { font-family: 'Courier New', Courier, monospace; margin-bottom: 10px; border-bottom: 1px dashed #b2dfdb; padding-bottom: 5px; font-size: 0.9rem; }
        .math-step:last-child { border-bottom: none; }
        .math-var { color: #d35400; font-weight: bold; }
        .math-res { color: #009688; font-weight: bold; }
        
        .chart-container { position: relative; height: 250px; }
        
        /* References Section */
        .references { margin-top: 50px; border-top: 1px solid #eee; padding-top: 20px; }
        .references h3 { font-size: 1.1rem; color: #2c3e50; margin-bottom: 15px; }
        .ref-list { list-style-type: none; padding: 0; font-size: 0.85rem; color: #555; }
        .ref-list li { margin-bottom: 12px; padding-left: 20px; text-indent: -20px; line-height: 1.5; }
        .ref-list strong { color: #333; }
        .ref-note { display: inline-block; background: #e8f4f8; font-size: 0.75rem; padding: 2px 6px; border-radius: 4px; margin-left: 8px; color: #0c5460; }
    </style>
</head>
<body>

<div class="container">
    <header>
        <h1>🔬 Sulfide Detoxification Energetics Model</h1>
        <div class="subtitle">Estimating the Metabolic Cost of H₂S Oxidation in Beef Cattle</div>
    </header>
    
    <div class="grid">
        <!-- Controls -->
        <div class="controls">
            <h3 style="margin-top:0;">Animal & Diet Parameters</h3>
            
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
                <span class="sub-label">Recommended max: 0.40% (NASEM 2016). DDGS typically 0.7-1.0%.</span>
            </div>
            <div class="control-group">
                <label>Water Sulfate (mg/L) <span id="val_waterS" class="value-display"></span></label>
                <input type="range" id="waterS" min="0" max="4000" step="100" value="2000" oninput="updateModel()">
                <span class="sub-label">300 mg/L (Most of East/Central Texas, 300 – 1,000 mg/L (Common in Gulf Coast & Southern High Plains), 1,000 mg/L (Common in West Texas / Pecos Valley) https://www.twdb.texas.gov/groundwater/aquifer/index.asp.</span>
            </div>
            <div class="control-group">
                <label>Water Intake <span id="val_waterIn" class="value-display"></span></label>
                <input type="range" id="waterIn" min="20" max="100" step="5" value="50" oninput="updateModel()">
                <span class="sub-label">Typically 2-4× DMI, varies with temperature and diet.</span>
            </div>

            <hr>
            <label style="color:#7f8c8d; text-transform:uppercase; font-size:0.8rem; letter-spacing:1px; margin-bottom:15px;">Physiological Parameters</label>

            <div class="control-group">
                <label>Rumen Reduction Rate <span id="val_reduction" class="value-display"></span></label>
                <input type="range" id="reduction" min="30" max="90" step="5" value="70" oninput="updateModel()">
                <span class="sub-label">% of dietary SO₄²⁻ reduced to H₂S by sulfate-reducing bacteria. Higher with fermentable carbs (H₂ donors). Range: 30-90%.</span>
            </div>

            <div class="control-group">
                <label>H₂S Absorption Rate <span id="val_abs" class="value-display"></span></label>
                <input type="range" id="abs" min="30" max="80" step="5" value="60" oninput="updateModel()">
                <span class="sub-label">% of rumen H₂S absorbed across epithelium. Depends on pH (pKa≈7.0) and partial pressure. Range: 40-80%.</span>
            </div>

            <div class="control-group">
                <label>Mitochondrial Oxidation Efficiency <span id="val_ox" class="value-display"></span></label>
                <input type="range" id="ox" min="70" max="100" step="1" value="95" oninput="updateModel()">
                <span class="sub-label">% of absorbed H₂S completely oxidized to SO₄²⁻ via SQR pathway. Remainder detoxified via alternative routes. Default: 95%.</span>
            </div>
        </div>

        <!-- Results -->
        <div class="results">
            <div class="warning-box" id="warning-box">
                <strong>⚠ Sulfur Toxicity Risk</strong><br>
                <span id="warning-text" class="warning-text"></span>
            </div>

            <div class="kpi-box">
                <div class="kpi">
                    <h3>Total S Intake</h3>
                    <div class="num" id="res_totalS">0</div>
                    <div class="unit">g S/day</div>
                </div>
                <div class="kpi">
                    <h3>Rumen H₂S Produced</h3>
                    <div class="num" id="res_rumen">0</div>
                    <div class="unit">g S/day</div>
                </div>
                <div class="kpi">
                    <h3>Absorbed H₂S</h3>
                    <div class="num" id="res_absorbed">0</div>
                    <div class="unit">g S/day</div>
                </div>
                <div class="kpi">
                    <h3>O₂ Consumed</h3>
                    <div class="num" id="res_o2">0</div>
                    <div class="unit">L O₂/day</div>
                </div>
                <div class="kpi">
                    <h3>Heat Produced</h3>
                    <div class="num" id="res_heat_raw">0</div>
                    <div class="unit">Mcal/day</div>
                </div>
                <div class="kpi highlight">
                    <h3>NE Cost</h3>
                    <div class="num" id="res_heat">0</div>
                    <div class="unit">Mcal NEm/day</div>
                </div>
                <div class="kpi">
                    <h3>Base NEm</h3>
                    <div class="num" id="res_base">0</div>
                    <div class="unit">Mcal/day</div>
                </div>
                <div class="kpi">
                    <h3>Total NEm</h3>
                    <div class="num" id="res_total">0</div>
                    <div class="unit">Mcal/day</div>
                </div>
                <div class="kpi highlight">
                    <h3>% Increase</h3>
                    <div class="num" id="res_pct">0</div>
                    <div class="unit">NEm increase</div>
                </div>
            </div>

            <div class="chart-container">
                <canvas id="energyChart"></canvas>
            </div>

            <div class="equation-section">
                <h4 style="margin-top:0; color:#009688;">Stoichiometric Calculation Path</h4>
                <div id="equation-display"></div>
            </div>
        </div>
    </div>

    <!-- References -->
    <div class="references">
        <h3>Scientific References & Model Basis</h3>
        <ul class="ref-list">
            <li>
                <strong>Hildebrandt, T. M., & Grieshaber, M. K. (2008).</strong> Three enzymatic activities catalyze the oxidation of sulfide to thiosulfate in mammalian and invertebrate mitochondria. <em>FEBS Journal</em>, 275(13), 3352-3361.
                <span class="ref-note">Mitochondrial sulfide oxidation pathway (SQR → SO → TST)</span>
            </li>
            <li>
                <strong>Brouwer, E. (1965).</strong> Report of Sub-committee on Constants and Factors. <em>EAAP Publication</em>, 11, 441-443.
                <span class="ref-note">Oxygen caloric equivalent: 4.89 kcal/L O₂</span>
            </li>
            <li>
                <strong>Gould, D. H., et al. (1997).</strong> Sulfide-induced polioencephalomalacia in cattle. <em>Veterinary and Human Toxicology</em>, 39(2), 69-75.
                <span class="ref-note">H₂S absorption kinetics, pH effects (pKa ≈ 7.0)</span>
            </li>
            <li>
                <strong>Kung, L., et al. (1998).</strong> Rumen microbial degradation of added taurine and urea. <em>Journal of Dairy Science</em>, 81(9), 2374-2382.
                <span class="ref-note">Sulfate reduction rates: 30-90% depending on H₂ availability</span>
            </li>
            <li>
                <strong>Drewnoski, M. E., & Hansen, S. L. (2014).</strong> High-sulfur in beef cattle diets: a review. <em>Journal of Animal Science</em>, 92(9), 3763-3780.
                <span class="ref-note">Comprehensive review of sulfur toxicity mechanisms</span>
            </li>
            <li>
                <strong>Loneragan, G. H., et al. (2001).</strong> The magnitude and pattern of ruminal hydrogen sulfide production. <em>Journal of Veterinary Diagnostic Investigation</em>, 13(4), 310-317.
                <span class="ref-note">Clinical thresholds: Total S > 0.4% of diet, water SO₄ > 2000 mg/L</span>
            </li>
            <li>
                <strong>NASEM. (2016).</strong> <em>Nutrient Requirements of Beef Cattle</em> (8th rev. ed.). Washington, DC: The National Academies Press.
                <span class="ref-note">Base NEm equation: 0.077 × BW^0.75 Mcal/day</span>
            </li>
        </ul>
        
        <div style="margin-top:25px; padding:15px; background:#f8f9fa; border-left:4px solid #3498db; border-radius:4px;">
            <strong style="color:#2c3e50;">Model Assumptions:</strong>
            <ul style="margin:10px 0 0 20px; font-size:0.85rem; color:#555;">
                <li>Stoichiometry: H₂S + 2O₂ → SO₄²⁻ + 2H⁺ (complete oxidation pathway)</li>
                <li>This is a COST, not energy yield - no ATP captured from sulfide oxidation</li>
                <li>Heat-to-NE conversion: Heat ÷ 0.70 = NE cost (accounts for 30% metabolic inefficiency)</li>
                <li>Model represents steady-state conditions (not acute toxicity episodes)</li>
            </ul>
        </div>
    </div>
</div>

<script>
    // Physical Constants (Literature Values)
    const MW_S = 32.065;        // g/mol (IUPAC 2021)
    const MW_SO4 = 96.066;      // g/mol (calculated)
    const S_IN_SO4 = MW_S / MW_SO4; // 0.3337
    const MOL_VOL = 22.4;       // L/mol at STP
    const KCAL_PER_L_O2 = 4.89; // Brouwer (1965)
    const NEM_COEFF = 0.077;    // NASEM (2016) - Mcal/kg BW^0.75
    const HEAT_TO_NE = 0.70;    // Metabolic efficiency factor

    let myChart = null;

    function updateModel() {
        // 1. GET INPUTS
        const bw = parseFloat(document.getElementById('bw').value);
        const dmi = parseFloat(document.getElementById('dmi').value);
        const feedS_pct = parseFloat(document.getElementById('feedS').value);
        const waterS_conc = parseFloat(document.getElementById('waterS').value);
        const waterIn = parseFloat(document.getElementById('waterIn').value);
        const red_pct = parseFloat(document.getElementById('reduction').value);
        const abs_pct = parseFloat(document.getElementById('abs').value);
        const ox_pct = parseFloat(document.getElementById('ox').value);

        // 2. CALCULATE SULFUR FLOW
        // Step 1: Total Intake (as elemental S)
        const feedS_g = dmi * (feedS_pct / 100) * 1000;
        const waterSulfate_g = waterIn * (waterS_conc / 1000);
        const waterS_g = waterSulfate_g * S_IN_SO4;
        const totalS_g = feedS_g + waterS_g;
        const totalS_dmi_pct = (totalS_g / (dmi * 1000)) * 100;

        // Step 2: Rumen Reduction (SO₄²⁻ → H₂S by sulfate-reducing bacteria)
        const rumenH2S_g = totalS_g * (red_pct / 100);

        // Step 3: Absorption (H₂S crosses rumen epithelium)
        const absorbedH2S_g = rumenH2S_g * (abs_pct / 100);

        // Step 4: Hepatic/Mitochondrial Oxidation (H₂S → SO₄²⁻)
        const oxidizedS_g = absorbedH2S_g * (ox_pct / 100);

        // 3. STOICHIOMETRY: H₂S + 2O₂ → SO₄²⁻
        const mols_S = oxidizedS_g / MW_S;
        const mols_O2 = mols_S * 2; // 2 moles O₂ per mole S
        const liters_O2 = mols_O2 * MOL_VOL;
        
        // 4. ENERGETICS
        // Heat production from O₂ consumption
        const heat_kcal = liters_O2 * KCAL_PER_L_O2;
        const heat_mcal_raw = heat_kcal / 1000;
        
        // Net Energy cost (accounting for metabolic inefficiency)
        const ne_cost_mcal = heat_mcal_raw / HEAT_TO_NE;

        // Base Maintenance (NASEM 2016)
        const mbw = Math.pow(bw, 0.75);
        const base_nem = NEM_COEFF * mbw;
        
        // Total requirement
        const total_nem = base_nem + ne_cost_mcal;
        const pct_increase = (ne_cost_mcal / base_nem) * 100;

        // 5. UPDATE UI VALUES
        document.getElementById('val_bw').innerText = bw + " kg (" + (bw * 2.205).toFixed(0) + " lb)";
        document.getElementById('val_dmi').innerText = dmi + " kg (" + (dmi * 2.205).toFixed(1) + " lb)";
        document.getElementById('val_feedS').innerText = feedS_pct.toFixed(2) + "%";
        document.getElementById('val_waterS').innerText = waterS_conc + " mg/L";
        document.getElementById('val_waterIn').innerText = waterIn + " L (" + (waterIn * 0.264).toFixed(1) + " gal)";
        document.getElementById('val_reduction').innerText = red_pct + "%";
        document.getElementById('val_abs').innerText = abs_pct + "%";
        document.getElementById('val_ox').innerText = ox_pct + "%";

        // Update KPIs
        document.getElementById('res_totalS').innerText = totalS_g.toFixed(1);
        document.getElementById('res_rumen').innerText = rumenH2S_g.toFixed(1);
        document.getElementById('res_absorbed').innerText = absorbedH2S_g.toFixed(2);
        document.getElementById('res_o2').innerText = liters_O2.toFixed(1);
        document.getElementById('res_heat_raw').innerText = heat_mcal_raw.toFixed(3);
        document.getElementById('res_heat').innerText = ne_cost_mcal.toFixed(3);
        document.getElementById('res_base').innerText = base_nem.toFixed(2);
        document.getElementById('res_total').innerText = total_nem.toFixed(2);
        document.getElementById('res_pct').innerText = "+" + pct_increase.toFixed(1) + "%";

        // 6. TOXICITY WARNINGS (NASEM Guidelines)
        const warnBox = document.getElementById('warning-box');
        let warnings = [];
        let isCritical = false;
        
        if(totalS_dmi_pct > 0.50) {
            warnings.push(`<strong>CRITICAL:</strong> Total dietary S is ${totalS_dmi_pct.toFixed(2)}% (max: 0.40%). High risk of polioencephalomalacia (PEM).`);
            isCritical = true;
        } else if(totalS_dmi_pct > 0.40) {
            warnings.push(`<strong>WARNING:</strong> Total dietary S is ${totalS_dmi_pct.toFixed(2)}% (exceeds 0.40% threshold). Increased PEM risk.`);
        }
        
        if(waterS_conc > 3000) {
            warnings.push(`<strong>CRITICAL:</strong> Water sulfate is ${waterS_conc} mg/L. Severe toxicity risk - find alternative water source.`);
            isCritical = true;
        } else if(waterS_conc > 2000) {
            warnings.push(`<strong>WARNING:</strong> Water sulfate is ${waterS_conc} mg/L (recommended max: 500 mg/L). High risk zone.`);
        }
        
        if(absorbedH2S_g > 40) {
            warnings.push(`<strong>WARNING:</strong> Absorbed H₂S burden is ${absorbedH2S_g.toFixed(1)} g/day - very high detoxification load.`);
        }
        
        if(warnings.length > 0) {
            warnBox.style.display = 'block';
            warnBox.className = 'warning-box' + (isCritical ? ' critical' : '');
            document.getElementById('warning-text').innerHTML = warnings.join("<br><br>");
        } else {
            warnBox.style.display = 'none';
        }

        // 7. EQUATION DISPLAY
        const eqHTML = `
            <div class="math-step">
                <strong>Step 1 - Total Intake:</strong> 
                Feed: ${feedS_g.toFixed(1)}g + Water: ${waterS_g.toFixed(1)}g = 
                <span class="math-res">${totalS_g.toFixed(1)} g S/day</span> 
                (${totalS_dmi_pct.toFixed(2)}% of DMI)
            </div>
            <div class="math-step">
                <strong>Step 2 - Rumen Reduction:</strong> 
                ${totalS_g.toFixed(1)} g × ${red_pct}% = 
                <span class="math-res">${rumenH2S_g.toFixed(1)} g H₂S produced</span>
            </div>
            <div class="math-step">
                <strong>Step 3 - Absorption:</strong> 
                ${rumenH2S_g.toFixed(1)} g × ${abs_pct}% = 
                <span class="math-res">${absorbedH2S_g.toFixed(2)} g H₂S absorbed</span>
            </div>
            <div class="math-step">
                <strong>Step 4 - Oxidation:</strong> 
                ${absorbedH2S_g.toFixed(2)} g × ${ox_pct}% = 
                <span class="math-res">${oxidizedS_g.toFixed(2)} g oxidized to SO₄²⁻</span>
            </div>
            <div class="math-step">
                <strong>Step 5 - O₂ Demand:</strong> 
                (${oxidizedS_g.toFixed(2)} g ÷ 32.065) × 2 mol O₂/mol S × 22.4 L/mol = 
                <span class="math-res">${liters_O2.toFixed(1)} L O₂/day</span>
            </div>
            <div class="math-step">
                <strong>Step 6 - Heat Production:</strong> 
                ${liters_O2.toFixed(1)} L × 4.89 kcal/L = 
                <span class="math-res">${heat_mcal_raw.toFixed(3)} Mcal heat/day</span>
            </div>
            <div class="math-step">
                <strong>Step 7 - NE Cost:</strong> 
                ${heat_mcal_raw.toFixed(3)} Mcal ÷ 0.70 (efficiency) = 
                <span class="math-res">${ne_cost_mcal.toFixed(3)} Mcal NEm/day</span>
                (+${pct_increase.toFixed(1)}% maintenance requirement)
            </div>
        `;
        document.getElementById('equation-display').innerHTML = eqHTML;

        updateChart(base_nem, ne_cost_mcal, totalS_dmi_pct);
    }

    function updateChart(base, cost, sulfur_pct) {
        const ctx = document.getElementById('energyChart').getContext('2d');
        if (myChart) myChart.destroy();

        const total = base + cost;
        const pct = ((cost / base) * 100).toFixed(1);
        
        let titleColor = '#2c3e50';
        if(sulfur_pct > 0.50) titleColor = '#c0392b';
        else if(sulfur_pct > 0.40) titleColor = '#f39c12';

        myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Baseline NEm', 'NEm with S-Tax'],
                datasets: [
                    { 
                        label: 'Base Maintenance (NASEM)', 
                        data: [base, base], 
                        backgroundColor: '#3498db', 
                        stack: '1' 
                    },
                    { 
                        label: `Sulfide Detox Cost (+${pct}%)`, 
                        data: [0, cost], 
                        backgroundColor: '#e74c3c', 
                        stack: '1' 
                    }
                ]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Net Energy for Maintenance (Mcal/day)',
                        color: titleColor,
                        font: { size: 14, weight: 'bold' }
                    },
                    legend: { position: 'bottom' },
                    tooltip: {
                        callbacks: {
                            footer: function(items) {
                                return `Total NEm Required: ${total.toFixed(2)} Mcal/day`;
                            }
                        }
                    }
                },
                scales: { 
                    x: { 
                        stacked: true, 
                        title: { display: true, text: 'Energy (Mcal/day)' } 
                    }, 
                    y: { stacked: true } 
                }
            }
        });
    }

    // Initialize on load
    updateModel();
</script>
</body>
</html>
    """
    
    filename = "sulfur_model_final_corrected.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✓ Final Sulfur Model created successfully!")
    print("\n✓ All Corrections Applied:")
    print("  - Complete 4-step physiological pathway")
    print("  - Separate reduction, absorption, and oxidation parameters")
    print("  - NE conversion factor (÷ 0.70 for metabolic efficiency)")
    print("  - 9 KPIs showing complete energy flow")
    print("  - Enhanced toxicity warnings (2 severity levels)")
    print("  - 7-step calculation display")
    print("  - Comprehensive scientific references")
    print("  - Imperial unit conversions for US ranchers")
    print("  - Color-coded chart based on S toxicity risk")
    
    webbrowser.open('file://' + os.path.realpath(filename))

if __name__ == "__main__":
    create_final_simulation()