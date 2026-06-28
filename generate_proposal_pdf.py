import os
from fpdf import FPDF

class ProposalPDF(FPDF):
    def header(self):
        # Header banner
        self.set_fill_color(14, 27, 43) # Deep dark blue/navy
        self.rect(0, 0, 210, 30, 'F')
        self.set_y(10)
        self.set_font("helvetica", 'B', 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, text="EXECUTIVE PROPOSAL: URBAN HEAT MITIGATION VIA AI/ML", new_x="LMARGIN", new_y="NEXT", align='C')
        self.set_font("helvetica", 'I', 11)
        self.cell(0, 8, text="High-Novelty Model Architecture & Selection Enhancement Guide", new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", 'I', 9)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, text=f"Page {self.page_no()} | Hackathon Project Selection Document · June 2026", align='C')

def generate_pdf():
    pdf = ProposalPDF('P', 'mm', 'A4')
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    
    # Title Section
    pdf.set_font("helvetica", 'B', 18)
    pdf.set_text_color(14, 27, 43)
    pdf.cell(0, 10, text="Project Selection Pitch: Why This Framework Wins", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", '', 11)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6, text=
        "Hackathon judges evaluating selection rounds look for three things: academic novelty, real-world feasibility, "
        "and rigorous mathematical architecture. This document outlines the cutting-edge architectural advancements "
        "being integrated into our Physics-Informed Neural Network (PINN) and Evolutionary Optimization pipeline to "
        "make it an elite, research-grade framework for smart-city governance."
    )
    pdf.ln(8)

    # Section 1: The 4 High-Novelty Model Enhancements
    pdf.set_font("helvetica", 'B', 14)
    pdf.set_text_color(14, 27, 43)
    pdf.cell(0, 10, text="1. Cutting-Edge Model Enhancements (Architectural Novelty)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(200, 200, 200)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
    pdf.ln(5)

    # Enhancement 1
    pdf.set_font("helvetica", 'B', 12)
    pdf.set_text_color(180, 40, 40) # Muted deep red
    pdf.cell(0, 8, text="Enhancement 1: Multi-Temporal PINN (Diurnal & Nocturnal Physics)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", '', 11)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6, text=
        "- Current Implementation: The V4 PINN trains on a single daytime thermal snapshot (Landsat 8 LST).\n"
        "- The Novel Upgrade: We are incorporating time-dependent thermal inertia into the Surface Energy Balance "
        "(SEB) loss function (G = C_v * dT/dt). By pairing day-night thermal rasters (MODIS/ECOSTRESS), the PINN "
        "learns how dense concrete traps heat during the day and releases it at night.\n"
        "- Selection Appeal: Capturing the Nocturnal Urban Heat Island effect is the holy grail of urban climatology. "
        "Judges will instantly recognize this as a breakthrough over standard static models."
    )
    pdf.ln(6)

    # Enhancement 2
    pdf.set_font("helvetica", 'B', 12)
    pdf.set_text_color(40, 140, 40) # Muted deep green
    pdf.cell(0, 8, text="Enhancement 2: Empirical Blue Space Extraction (Sentinel-2 B11)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", '', 11)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6, text=
        "- Current Implementation: The water index (NDWI) is simulated via random distributions as a placeholder.\n"
        "- The Novel Upgrade: Updating gee_extraction.py to extract Sentinel-2 Band 11 (Shortwave Infrared) and Band 3 "
        "(Green) to compute empirical, verified NDWI. This directly feeds into the Latent Heat Flux (LE) physics equation.\n"
        "- Selection Appeal: Replaces mock proxies with satellite-verified proof of how wetlands act as thermal sinks, "
        "boosting the model R-squared accuracy score above 0.45."
    )
    pdf.ln(6)

    # Enhancement 3
    pdf.set_font("helvetica", 'B', 12)
    pdf.set_text_color(40, 80, 180) # Muted deep blue
    pdf.cell(0, 8, text="Enhancement 3: Unsupervised Local Climate Zone (LCZ) Clustering", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", '', 11)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6, text=
        "- Current Implementation: Spatial zoning is done via a simple median split on building heat (BAH > median).\n"
        "- The Novel Upgrade: Replacing the median split with an unsupervised K-Means Machine Learning clustering "
        "engine operating on [NDVI, Albedo, BAH, LST] to automatically segment the city into official WUDAPT Local Climate Zones.\n"
        "- Selection Appeal: Aligns the framework with international climatology standards (WUDAPT), demonstrating "
        "rigorous data science workflows to technical judges."
    )
    pdf.ln(6)

    # Enhancement 4
    pdf.set_font("helvetica", 'B', 12)
    pdf.set_text_color(140, 90, 40) # Muted bronze/orange
    pdf.cell(0, 8, text="Enhancement 4: NSGA-III Multi-Objective Ward-Level Budgeting", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", '', 11)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6, text=
        "- Current Implementation: NSGA-II evaluates the top 100 hotspots collectively with 2 objectives.\n"
        "- The Novel Upgrade: Moving to pymoo NSGA-III to optimize 3+ competing municipal objectives per ward: "
        "(1) Minimize Surface Temp, (2) Minimize City Implementation Cost, and (3) Maximize Socio-Economic Benefit.\n"
        "- Selection Appeal: Proves the AI is ready for real-world smart-city governance and municipal budget deployment."
    )
    pdf.ln(10)

    # Section 2: Summary Table for Judges
    pdf.set_font("helvetica", 'B', 14)
    pdf.set_text_color(14, 27, 43)
    pdf.cell(0, 10, text="2. Quick Comparison: Standard Submissions vs. Our Novel Framework", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(200, 200, 200)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
    pdf.ln(6)

    # Table Header
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("helvetica", 'B', 11)
    pdf.set_text_color(14, 27, 43)
    pdf.cell(45, 10, text="Feature Area", border=1, align='C', fill=True)
    pdf.cell(70, 10, text="Standard Hackathon Models", border=1, align='C', fill=True)
    pdf.cell(75, 10, text="Our Novel Framework (V4+)", border=1, align='C', fill=True, new_x="LMARGIN", new_y="NEXT")

    # Table Rows
    pdf.set_font("helvetica", '', 10)
    pdf.set_text_color(50, 50, 50)
    
    rows = [
        ("ML Methodology", "Standard Deep Learning / Random Forests", "Physics-Informed Neural Network (PINN)"),
        ("Thermodynamics", "Unbounded (AI can hallucinate -50C)", "Strict Surface Energy Balance (SEB) loss"),
        ("Mitigation Engine", "Trial & error simulation guessing", "NSGA-II/III Genetic Algorithm Pareto front"),
        ("Spatial Zoning", "Homogeneous flat city rules (0.14C drop)", "Kundu 2026 Heterogeneous zoning (3.35C drop)"),
        ("Municipal Reality", "Ignores city budget and density limits", "Enforces ward-level 20% spending constraints")
    ]

    for col1, col2, col3 in rows:
        pdf.cell(45, 10, text=col1, border=1, align='L')
        pdf.cell(70, 10, text=col2, border=1, align='L')
        pdf.cell(75, 10, text=col3, border=1, align='L', new_x="LMARGIN", new_y="NEXT")

    pdf.ln(12)
    pdf.set_font("helvetica", 'I', 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, text="Document prepared for Hackathon Selection Committee · Delhi-NCR Thermal Mitigation Architecture", align='C')

    # Ensure reports directory exists
    os.makedirs('reports', exist_ok=True)
    output_path = os.path.join('reports', 'Urban_Heat_Mitigation_Novelty_Proposal.pdf')
    pdf.output(output_path)
    print(f"PDF successfully generated at: {output_path}")

if __name__ == "__main__":
    generate_pdf()
