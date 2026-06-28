import os
from fpdf import FPDF

class TrueNoveltyPDF(FPDF):
    def header(self):
        self.set_fill_color(24, 43, 49) # Rich dark slate/teal
        self.rect(0, 0, 210, 32, 'F')
        self.set_y(10)
        self.set_font("helvetica", 'B', 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, text="EXECUTIVE PITCH: NEXT-GEN THERMAL MITIGATION", new_x="LMARGIN", new_y="NEXT", align='C')
        self.set_font("helvetica", 'I', 11)
        self.cell(0, 8, text="True Breakthrough Novelty Beyond Standard Project Roadmaps", new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(16)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", 'I', 9)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, text=f"Page {self.page_no()} | Advanced Selection Committee Document - June 2026", align='C')

def generate_pdf():
    pdf = TrueNoveltyPDF('P', 'mm', 'A4')
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    
    # Title Section
    pdf.set_font("helvetica", 'B', 18)
    pdf.set_text_color(24, 43, 49)
    pdf.cell(0, 10, text="Elite Selection Pitch: Unmentioned Innovations", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", '', 11)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6, text=
        "To win a highly competitive hackathon selection round, a proposal must go beyond standard roadmap features "
        "like seasonal training or basic REST APIs. This document presents four brand-new, highly advanced architectural "
        "innovations that bridge aerospace fluid dynamics, material degradation physics, humanitarian equity, "
        "and multi-agent AI wargaming - establishing an indisputable edge for selection."
    )
    pdf.ln(8)

    # Section 1: The 4 Brand-New Innovations
    pdf.set_font("helvetica", 'B', 14)
    pdf.set_text_color(24, 43, 49)
    pdf.cell(0, 10, text="1. Brand-New Architectural Innovations (Unrivaled Novelty)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(200, 200, 200)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
    pdf.ln(5)

    # Innovation 1
    pdf.set_font("helvetica", 'B', 12)
    pdf.set_text_color(180, 50, 50) # Muted deep red
    pdf.cell(0, 8, text="Innovation 1: PINN-CFD Horizontal Wind & Street Canyon Advection", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", '', 11)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6, text=
        "- The Baseline Limitation: Current PINN models use a 1D vertical Surface Energy Balance (SEB) equation for each "
        "pixel independently, entirely ignoring wind patterns and urban ventilation.\n"
        "- The True Novelty: We integrate the Navier-Stokes fluid dynamics equations into the PINN loss function alongside "
        "the SEB. This models horizontal thermal advection - calculating how wind breezes carry heat from hot industrial parks "
        "into cooler residential neighborhoods through street canyons.\n"
        "- Selection Appeal: Moving from a 1D vertical balance to a 3D thermodynamic wind-flow model bridges AI with "
        "advanced aerospace computational fluid dynamics (CFD)."
    )
    pdf.ln(6)

    # Innovation 2
    pdf.set_font("helvetica", 'B', 12)
    pdf.set_text_color(40, 140, 100) # Muted teal/green
    pdf.cell(0, 8, text="Innovation 2: Real-World Albedo Degradation & Dust Decay Modeling", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", '', 11)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6, text=
        "- The Baseline Limitation: Standard optimizers assume that once a roof is painted white (Albedo 0.65), it stays "
        "perfectly clean and reflective forever.\n"
        "- The True Novelty: We incorporate an empirical Albedo Decay Function into the optimization constraints. In cities "
        "like Delhi, severe dust storms and pollution degrade reflective white roofs by 30-50% within 12 months. Our new model "
        "optimizes for maintenance-weighted cooling leverage, recommending materials that resist dust accumulation.\n"
        "- Selection Appeal: Proves your team understands the gritty reality of Indian municipal environments (dust and pollution) "
        "rather than living in a theoretical AI bubble."
    )
    pdf.ln(6)

    # Innovation 3
    pdf.set_font("helvetica", 'B', 12)
    pdf.set_text_color(40, 90, 180) # Muted deep blue
    pdf.cell(0, 8, text="Innovation 3: Socio-Economic Vulnerability Index (SEVI) Integration", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", '', 11)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6, text=
        "- The Baseline Limitation: Current algorithms treat every 30m pixel identically based purely on physical temperature. "
        "It cannot distinguish between an empty commercial warehouse and a high-density, low-income informal settlement.\n"
        "- The True Novelty: We inject a geospatial Socio-Economic Vulnerability Index (SEVI) layer (combining population density, "
        "income census data, and hospital proximity) directly into the genetic algorithm's objective function. The AI prioritizes "
        "cooling interventions in vulnerable, high-density neighborhoods over empty commercial rooftops.\n"
        "- Selection Appeal: Turns a purely technical math problem into a highly compelling humanitarian and smart-governance "
        "solution, solving Urban Thermal Inequity."
    )
    pdf.ln(6)

    # Innovation 4
    pdf.set_font("helvetica", 'B', 12)
    pdf.set_text_color(150, 90, 30) # Muted bronze
    pdf.cell(0, 8, text="Innovation 4: Multi-Agent Municipal Wargaming (AI Debate Consensus)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", '', 11)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6, text=
        "- The Baseline Limitation: Standard roadmaps propose a single AI chatbot agent that gives static recommendations.\n"
        "- The True Novelty: We build an autonomous Multi-Agent Municipal Wargaming System where three distinct AI personas "
        "debate each other in real-time: (1) The Mayor AI (pushes for green parks), (2) The Budget Auditor AI (strictly vetoes "
        "expensive plans), and (3) The Chief Climatologist AI (defends thermodynamic laws). The final cooling policy is the "
        "result of an automated consensus debate.\n"
        "- Selection Appeal: Multi-agent debate frameworks (like AutoGen/CrewAI) represent the absolute state-of-the-art in "
        "generative AI right now."
    )
    pdf.ln(10)

    # Section 2: Comparison Table
    pdf.set_font("helvetica", 'B', 14)
    pdf.set_text_color(24, 43, 49)
    pdf.cell(0, 10, text="2. Architectural Evolution: Repository Roadmap vs. Our True Novelty", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(200, 200, 200)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
    pdf.ln(6)

    # Table Header
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("helvetica", 'B', 10)
    pdf.set_text_color(24, 43, 49)
    pdf.cell(42, 10, text="Domain", border=1, align='C', fill=True)
    pdf.cell(73, 10, text="Existing Git Roadmap (Liza's Repo)", border=1, align='C', fill=True)
    pdf.cell(75, 10, text="Our True Advanced Novelty", border=1, align='C', fill=True, new_x="LMARGIN", new_y="NEXT")

    # Table Rows
    pdf.set_font("helvetica", '', 10)
    pdf.set_text_color(50, 50, 50)
    
    rows = [
        ("Physics Engine", "1D Vertical SEB (Independent pixels)", "3D PINN-CFD (Horizontal wind & advection)"),
        ("Material Lifespan", "Static perfect reflectivity (Albedo 0.65)", "Dynamic Albedo decay (Dust & soot aging)"),
        ("Optimization Goal", "Pure temperature drop (Ignores population)", "Socio-Economic Vulnerability Index (SEVI)"),
        ("Agentic AI", "Single LangChain assistant per ward", "Multi-Agent Wargaming (Debate consensus)")
    ]

    for col1, col2, col3 in rows:
        pdf.cell(42, 10, text=col1, border=1, align='L')
        pdf.cell(73, 10, text=col2, border=1, align='L')
        pdf.cell(75, 10, text=col3, border=1, align='L', new_x="LMARGIN", new_y="NEXT")

    pdf.ln(12)
    pdf.set_font("helvetica", 'I', 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, text="Document prepared for Hackathon Selection Committee - True Next-Gen Innovations", align='C')

    # Ensure reports directory exists
    os.makedirs('reports', exist_ok=True)
    output_path = os.path.join('reports', 'True_Advanced_Novelty_Proposal.pdf')
    pdf.output(output_path)
    print(f"PDF successfully generated at: {output_path}")

if __name__ == "__main__":
    generate_pdf()
