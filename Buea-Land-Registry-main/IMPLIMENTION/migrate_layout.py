import os
import re

props_path = r"c:\Users\HP\Desktop\IMPLIMENTION\my-properties.html"
reg_path = r"c:\Users\HP\Desktop\IMPLIMENTION\LandRegistrationPage.html"

with open(props_path, "r", encoding="utf-8") as f:
    props_html = f.read()

with open(reg_path, "r", encoding="utf-8") as f:
    reg_html = f.read()

# 1. Header structural layout from my-properties
head_match = re.search(r"([\s\S]*?)<main class=\"main-content\">", props_html)
header_html = head_match.group(1) + '<main class="main-content">\n'

# 2. Scripts and map initializers from LandRegistration
scripts_match = re.search(r"(<!-- Leaflet JS for maps -->[\s\S]*?)</body>", reg_html)
scripts_html = scripts_match.group(1) + "\n</body>\n</html>"

# 3. Form CSS from LandRegistration
css_match = re.search(r"(/\* ========== PAGE HEADER ========== \*/[\s\S]*?)</style>", reg_html)
if css_match:
    form_css = css_match.group(1)
    header_html = header_html.replace("</style>", f"\n{form_css}\n    </style>")

# 4. Form HTML from LandRegistration
form_match = re.search(r"(<div class=\"page-header\" data-aos=\"fade-down\">[\s\S]*?)</main>", reg_html)
form_html = form_match.group(1) + "</main>\n        </div>\n    </div>\n"

# 5. Fix navigation active states
header_html = header_html.replace('href="my-properties.html" class="active"', 'href="my-properties.html"')
header_html = header_html.replace('href="LandRegistrationPage.html"', 'href="LandRegistrationPage.html" class="active"')

# 6. Add new Owner & Value fields
new_fields = """
                    <!-- Section 2: Owner & Value -->
                    <div class="form-section">
                        <div class="section-title">
                            <div class="step-number">2</div>
                            <h3>Owner & Value Declaration</h3>
                            <p>Step 2 of 5</p>
                        </div>
                        <div class="form-grid">
                            <div class="form-group full-width">
                                <label class="form-label">
                                    <i class="fas fa-user-tag"></i> Current Owner <span class="required">*</span>
                                </label>
                                <div class="input-wrapper">
                                    <i class="fas fa-user"></i>
                                    <input type="text" id="ownerName" placeholder="Owner Name" required>
                                </div>
                            </div>
                            <div class="form-group full-width">
                                <label class="form-label">
                                    <i class="fas fa-money-bill-wave"></i> Declared Value <span class="required">*</span>
                                </label>
                                <div class="input-wrapper">
                                    <i class="fas fa-coins"></i>
                                    <input type="text" id="declaredValue" placeholder="e.g. 15,000,000 FCFA" required>
                                </div>
                            </div>
                        </div>
                    </div>
"""
form_html = form_html.replace('<!-- Section 2: GPS Coordinates -->', new_fields + '\n                    <!-- Section 3: GPS Coordinates -->')

# Update step numbers
form_html = form_html.replace('Step 2 of 4', 'Step 3 of 5')
form_html = form_html.replace('<div class="step-number">2</div>', '<div class="step-number">3</div>', 1)

form_html = form_html.replace('Step 3 of 4', 'Step 4 of 5')
form_html = form_html.replace('<div class="step-number">3</div>', '<div class="step-number">4</div>', 1)

form_html = form_html.replace('Step 4 of 4', 'Step 5 of 5')
form_html = form_html.replace('<div class="step-number">4</div>', '<div class="step-number">5</div>', 1)

# Write output
res = header_html + form_html + scripts_html

with open(reg_path, "w", encoding="utf-8") as f:
    f.write(res)

print("Migration successful")
