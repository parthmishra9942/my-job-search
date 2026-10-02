import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

output_dir = r"C:\Users\parth\.gemini\antigravity-cli\brain\4bee6099-ee90-43d3-a590-76a48053dbb2\diagrams"
os.makedirs(output_dir, exist_ok=True)

# Styling palette
PRIMARY = "#14327D"      # Deep Navy
SECONDARY = "#2980B9"    # Blue Accent
SUCCESS = "#27AE60"      # Green Accent
WARNING = "#E67E22"      # Orange Accent
DANGER = "#C0392B"       # Red Accent
BG_LIGHT = "#F8F9FA"     # Light Grey
BORDER = "#BDC3C7"       # Border Grey
TEXT_DARK = "#2C3E50"    # Dark Charcoal

# ==============================================================================
# Diagram 1: Manual vs. TravelBrain Workflow
# ==============================================================================
def create_diagram_1():
    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    # Title
    ax.text(50, 95, "Manual Fragmented Trip Planning vs. TravelBrain Single-Request Engine", 
            fontsize=15, fontweight="bold", ha="center", color=PRIMARY)

    # Box 1: Manual Planning (Left)
    rect1 = patches.FancyBboxPatch((4, 8), 44, 80, boxstyle="round,pad=1.5", 
                                   linewidth=2, edgecolor=DANGER, facecolor="#FDEDEC")
    ax.add_patch(rect1)
    ax.text(26, 84, "CONVENTIONAL MANUAL WORKFLOW (High Cognitive Friction)", 
            fontsize=10.5, fontweight="bold", color=DANGER, ha="center")

    steps_manual = [
        ("1. Flight Portals", "Google Flights / Skyscanner (Form parameters, filters)"),
        ("2. Hotel Portals", "Booking.com / Airbnb (Neighborhood, tariff checks)"),
        ("3. Weather Services", "AccuWeather / OpenWeather (Manual packing check)"),
        ("4. Travel Blogs / TripAdvisor", "Research attractions & dining options"),
        ("5. Spreadsheets & Notes", "Manual copy-paste, reconciling dates & times"),
        ("6. Calculator", "Manual FX conversions, budgeting & reconciliation")
    ]
    y = 73
    for title, desc in steps_manual:
        box = patches.FancyBboxPatch((8, y-4), 36, 7.5, boxstyle="round,pad=0.5", 
                                     linewidth=1, edgecolor="#E6B0AA", facecolor="white")
        ax.add_patch(box)
        ax.text(10, y+0.8, title, fontsize=9, fontweight="bold", color=TEXT_DARK)
        ax.text(10, y-2.2, desc, fontsize=7.5, color="#5D6D7E")
        if y > 25:
            ax.annotate("", xy=(26, y-5), xytext=(26, y-3.8),
                        arrowprops=dict(arrowstyle="->", color=DANGER, lw=1.2))
        y -= 10.5

    ax.text(26, 12, "Result: 45–90 Mins Effort | Context Switching | Human Errors", 
            fontsize=9, fontweight="bold", color=DANGER, ha="center")

    # Box 2: TravelBrain (Right)
    rect2 = patches.FancyBboxPatch((52, 8), 44, 80, boxstyle="round,pad=1.5", 
                                   linewidth=2, edgecolor=SUCCESS, facecolor="#EAFAF1")
    ax.add_patch(rect2)
    ax.text(74, 84, "TRAVELBRAIN AUTONOMOUS MULTI-AGENT PIPELINE", 
            fontsize=10.5, fontweight="bold", color=SUCCESS, ha="center")

    # Single Request
    box_req = patches.FancyBboxPatch((56, 68), 36, 10, boxstyle="round,pad=0.8", 
                                     linewidth=1.5, edgecolor=SECONDARY, facecolor="#EBF5FB")
    ax.add_patch(box_req)
    ax.text(74, 74.5, "Single Natural-Language User Query", fontsize=9.5, fontweight="bold", color=PRIMARY, ha="center")
    ax.text(74, 70.5, "\"Plan a 5-day cultural trip to Rome for 2 with $1500 budget\"", 
            fontsize=8, style="italic", color="#2C3E50", ha="center")

    ax.annotate("", xy=(74, 61), xytext=(74, 68),
                arrowprops=dict(arrowstyle="->", color=SECONDARY, lw=2))

    # Engine Box
    box_engine = patches.FancyBboxPatch((56, 33), 36, 27, boxstyle="round,pad=0.8", 
                                        linewidth=1.5, edgecolor=PRIMARY, facecolor="white")
    ax.add_patch(box_engine)
    ax.text(74, 56, "TravelBrain Autonomous Engine (LangGraph + MCP)", fontsize=9.5, fontweight="bold", color=PRIMARY, ha="center")
    
    agent_pills = [
        "[Flight Agent] (AviationStack MCP)",
        "[Hotel Agent] (Tavily Remote MCP)",
        "[Weather Agent] (OpenWeather Local MCP)",
        "[Itinerary Agent] (Groq LPU LLM)",
        "[Final Agent] (7-Section Synthesizer)"
    ]
    y_p = 50.5
    for pill in agent_pills:
        ax.text(58, y_p, pill, fontsize=8, color=TEXT_DARK)
        y_p -= 4

    ax.annotate("", xy=(74, 25), xytext=(74, 33),
                arrowprops=dict(arrowstyle="->", color=SUCCESS, lw=2))

    # Result Box
    box_res = patches.FancyBboxPatch((56, 12), 36, 12, boxstyle="round,pad=0.8", 
                                     linewidth=1.5, edgecolor=SUCCESS, facecolor="#D4EFDF")
    ax.add_patch(box_res)
    ax.text(74, 20.5, "Unified Personalized Travel Plan", fontsize=9.5, fontweight="bold", color=SUCCESS, ha="center")
    ax.text(74, 15.5, "Flight Guide + Hotel Research + Weather Forecast +\nDay-by-Day Itinerary + Budget Breakdown", 
            fontsize=7.5, color=TEXT_DARK, ha="center")

    out_path = os.path.join(output_dir, "fig1_workflow_comparison.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Created:", out_path)

# ==============================================================================
# Diagram 2: RAG vs. Multi-Agent Engine
# ==============================================================================
def create_diagram_2():
    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    ax.text(50, 95, "Architectural Comparison: Traditional Vector-DB RAG vs. TravelBrain Multi-Agent Engine", 
            fontsize=13.5, fontweight="bold", ha="center", color=PRIMARY)

    # Left: Traditional RAG
    box_rag = patches.FancyBboxPatch((4, 8), 44, 80, boxstyle="round,pad=1.5", 
                                     linewidth=2, edgecolor=WARNING, facecolor="#FEF9E7")
    ax.add_patch(box_rag)
    ax.text(26, 84, "TRADITIONAL VECTOR RAG PIPELINE", fontsize=11, fontweight="bold", color=WARNING, ha="center")
    
    rag_steps = [
        ("1. User Query", "Natural language question", "#F9E79F"),
        ("2. Embedding Model", "Converts query into dense vector", "#FADBD8"),
        ("3. Vector Database (Static Chunks)", "Cosine similarity search over static corpus", "#D5F5E3"),
        ("4. Context Chunk Retrieval", "Top-K text chunks retrieved from static storage", "#D6EAF8"),
        ("5. Single LLM Prompt Injection", "LLM answers using retrieved text chunks", "#E8DAEF"),
        ("6. Static Text Generation", "Incapable of live external API queries", "#EDBB99")
    ]
    y = 73
    for title, desc, col in rag_steps:
        p = patches.FancyBboxPatch((8, y-4), 36, 7, boxstyle="round,pad=0.5", 
                                   linewidth=1, edgecolor="#BFC9CA", facecolor="white")
        ax.add_patch(p)
        ax.text(10, y+0.5, title, fontsize=8.5, fontweight="bold", color=TEXT_DARK)
        ax.text(10, y-2.5, desc, fontsize=7.2, color="#566573")
        if y > 25:
            ax.annotate("", xy=(26, y-5), xytext=(26, y-4),
                        arrowprops=dict(arrowstyle="->", color=WARNING, lw=1.2))
        y -= 10.5

    ax.text(26, 11, "Limitation: Cannot query live flights, hotel vacancies, or weather!", 
            fontsize=8, fontweight="bold", color=DANGER, ha="center")

    # Right: Multi-Agent
    box_ma = patches.FancyBboxPatch((52, 8), 44, 80, boxstyle="round,pad=1.5", 
                                    linewidth=2, edgecolor=SECONDARY, facecolor="#EBF5FB")
    ax.add_patch(box_ma)
    ax.text(74, 84, "TRAVELBRAIN MULTI-AGENT + MCP ARCHITECTURE", fontsize=11, fontweight="bold", color=SECONDARY, ha="center")

    ma_steps = [
        ("1. Travel Intent Ingestion", "NLU destination & budget extraction via FastAPI", "#D6EAF8"),
        ("2. LangGraph State Machine", "Orchestrates shared state across specialized nodes", "#D5F5E3"),
        ("3. Standardized MCP Tool Layer", "AviationStack, Tavily, OpenWeather (Live APIs)", "#FCF3CF"),
        ("4. Domain-Specialized Agents", "Flight, Hotel, Weather, Itinerary, Final", "#E8DAEF"),
        ("5. High-Speed Groq Inference", "LPU-accelerated multi-step reasoning & planning", "#FADBD8"),
        ("6. PostgreSQL State Persistence", "Thread checkpoints allow fault-tolerant resumption", "#D4EFDF")
    ]
    y = 73
    for title, desc, col in ma_steps:
        p = patches.FancyBboxPatch((56, y-4), 36, 7, boxstyle="round,pad=0.5", 
                                   linewidth=1, edgecolor=SECONDARY, facecolor="white")
        ax.add_patch(p)
        ax.text(58, y+0.5, title, fontsize=8.5, fontweight="bold", color=PRIMARY)
        ax.text(58, y-2.5, desc, fontsize=7.2, color="#566573")
        if y > 25:
            ax.annotate("", xy=(74, y-5), xytext=(74, y-4),
                        arrowprops=dict(arrowstyle="->", color=SECONDARY, lw=1.2))
        y -= 10.5

    ax.text(74, 11, "Advantage: Dynamic live data, tool isolation, and stateful persistence!", 
            fontsize=8, fontweight="bold", color=SUCCESS, ha="center")

    out_path = os.path.join(output_dir, "fig2_rag_vs_multiagent.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Created:", out_path)

# ==============================================================================
# Diagram 3: 5-Layer Master Architecture
# ==============================================================================
def create_diagram_3():
    fig, ax = plt.subplots(figsize=(12, 8.5), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    ax.text(50, 97, "TravelBrain: Comprehensive 5-Layer System Architecture", 
            fontsize=15, fontweight="bold", ha="center", color=PRIMARY)

    layers = [
        ("Layer 1: Presentation Tier (Client)", 
         "HTML5 / Tailwind CSS / Reactive JavaScript (templates/index.html) | Jinja2 Dashboard", 
         "#EAECEE", 83, 10),
        ("Layer 2: API Gateway & Application Server", 
         "FastAPI ASGI Application (app.py) | Routes: POST /api/travel, GET /api/config, GET /health", 
         "#D6EAF8", 68, 10),
        ("Layer 3: Orchestration & State Machine", 
         "LangGraph StateGraph Runner (runner.py) | Immutable TravelState Container (state.py)", 
         "#D5F5E3", 53, 10),
        ("Layer 4: Specialized Multi-Agent & Reasoning Tier", 
         "Flight Agent  •  Hotel Agent  •  Weather Agent  •  Itinerary Agent  •  Final Agent\n(Groq LPU Inference Cloud — ChatGroq: openai/gpt-oss-20b)", 
         "#FEF9E7", 34, 14),
        ("Layer 5: Tool Integration & Persistence Tier", 
         "MCP Layer (AviationStack stdio + Tavily Remote HTTP + Weather local)  |  PostgreSQL Checkpointer", 
         "#FADBD8", 15, 14)
    ]

    for title, desc, bg, y_pos, h in layers:
        rect = patches.FancyBboxPatch((8, y_pos), 84, h, boxstyle="round,pad=1", 
                                      linewidth=1.8, edgecolor=PRIMARY, facecolor=bg)
        ax.add_patch(rect)
        ax.text(12, y_pos + h - 3.5, title, fontsize=10.5, fontweight="bold", color=PRIMARY)
        ax.text(12, y_pos + 2.5, desc, fontsize=8.5, color=TEXT_DARK)

    # Vertical connectors
    y_arrows = [83, 68, 53, 34]
    for y_a in y_arrows:
        ax.annotate("", xy=(50, y_a), xytext=(50, y_a + 5),
                    arrowprops=dict(arrowstyle="<->", color=PRIMARY, lw=2))

    ax.text(50, 5, "Database Checkpoint: PostgreSQL stores LangGraph state blobs keyed by thread_id", 
            fontsize=8.5, style="italic", ha="center", color="#7F8C8D")

    out_path = os.path.join(output_dir, "fig3_master_architecture.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Created:", out_path)

# ==============================================================================
# Diagram 4: LangGraph Sequential Control Flow & State Transitions
# ==============================================================================
def create_diagram_4():
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    ax.text(50, 94, "LangGraph Sequential Control Flow & State Transition Pipeline", 
            fontsize=14, fontweight="bold", ha="center", color=PRIMARY)

    nodes = [
        ("START", "Input Ingestion", 5, 50, 12, 18, "#D5D8DC"),
        ("Flight Agent", "AviationStack MCP\n+ Groq LLM", 21, 50, 14, 22, "#D6EAF8"),
        ("Hotel Agent", "Tavily Search MCP\n(Web Research)", 39, 50, 14, 22, "#D5F5E3"),
        ("Weather Agent", "NLU Extraction\n+ OpenWeather MCP", 57, 50, 14, 22, "#FCF3CF"),
        ("Itinerary Agent", "Groq LPU Synthesis\n(Day-by-Day)", 75, 50, 14, 22, "#E8DAEF"),
        ("Final Agent", "7-Section Plan\nCompiler", 93, 50, 12, 22, "#FADBD8")
    ]

    for title, subtitle, cx, cy, w, h, bg in nodes:
        rect = patches.FancyBboxPatch((cx - w/2, cy - h/2), w, h, boxstyle="round,pad=0.8", 
                                      linewidth=1.5, edgecolor=PRIMARY, facecolor=bg)
        ax.add_patch(rect)
        ax.text(cx, cy + 3.5, title, fontsize=9.5, fontweight="bold", color=PRIMARY, ha="center")
        ax.text(cx, cy - 3.5, subtitle, fontsize=7.2, color=TEXT_DARK, ha="center")

    # Connectors
    xs = [11, 28, 46, 64, 82]
    for x in xs:
        ax.annotate("", xy=(x + 4, 50), xytext=(x, 50),
                    arrowprops=dict(arrowstyle="->", color=PRIMARY, lw=2.2))

    # Shared State container underneath
    rect_state = patches.FancyBboxPatch((10, 8), 80, 18, boxstyle="round,pad=1", 
                                        linewidth=1.8, edgecolor=SECONDARY, facecolor="#F4F6F6")
    ax.add_patch(rect_state)
    ax.text(50, 20.5, "SHARED MEMORY CONTAINER: TravelState (Thread ID Keyed)", 
            fontsize=10, fontweight="bold", color=SECONDARY, ha="center")
    ax.text(50, 13, "messages [ ]  •  user_query  •  flight_results  •  hotel_results  •  weather_results  •  itinerary  •  llm_calls", 
            fontsize=8, color=TEXT_DARK, ha="center")

    # Dotted connectors to shared state
    for cx in [21, 39, 57, 75, 93]:
        ax.annotate("", xy=(cx, 26), xytext=(cx, 39),
                    arrowprops=dict(arrowstyle="<->", linestyle="--", color=SECONDARY, lw=1.2))

    out_path = os.path.join(output_dir, "fig4_langgraph_flow.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Created:", out_path)

# ==============================================================================
# Diagram 5: Model Context Protocol (MCP) Integration Topology
# ==============================================================================
def create_diagram_5():
    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    ax.text(50, 95, "Model Context Protocol (MCP) Standardized Tool Integration Topology", 
            fontsize=14, fontweight="bold", ha="center", color=PRIMARY)

    # Core App (Left)
    box_app = patches.FancyBboxPatch((6, 25), 26, 50, boxstyle="round,pad=1", 
                                     linewidth=2, edgecolor=PRIMARY, facecolor="#EBF5FB")
    ax.add_patch(box_app)
    ax.text(19, 68, "TravelBrain Core", fontsize=11, fontweight="bold", color=PRIMARY, ha="center")
    ax.text(19, 61, "FastAPI Backend\n+\nLangGraph Agents\n(Flight, Hotel, Weather)", 
            fontsize=8.5, color=TEXT_DARK, ha="center")

    box_client = patches.FancyBboxPatch((8, 30), 22, 15, boxstyle="round,pad=0.8", 
                                        linewidth=1.2, edgecolor=SECONDARY, facecolor="white")
    ax.add_patch(box_client)
    ax.text(19, 39, "LangChain MCP Client", fontsize=9, fontweight="bold", color=SECONDARY, ha="center")
    ax.text(19, 33, "JSON-RPC Protocol Client", fontsize=7.5, color="#7F8C8D", ha="center")

    # MCP Servers (Right)
    servers = [
        ("AviationStack MCP Server", "Transport: Local stdio process (uvx)", "Tool: list_airports, list_airlines", 72, "#D4EFDF"),
        ("Tavily Remote MCP Server", "Transport: Remote HTTP / SSE", "Tool: tavily_search (Live Web)", 50, "#FCF3CF"),
        ("Custom Weather MCP Server", "Transport: Local stdio (weather_server.py)", "Tool: get_current_weather, get_forecast", 28, "#E8DAEF")
    ]

    for title, trans, tools, y_s, bg in servers:
        box_s = patches.FancyBboxPatch((50, y_s-7), 44, 16, boxstyle="round,pad=0.8", 
                                       linewidth=1.5, edgecolor=PRIMARY, facecolor=bg)
        ax.add_patch(box_s)
        ax.text(52, y_s + 5.5, title, fontsize=9.5, fontweight="bold", color=PRIMARY)
        ax.text(52, y_s + 0.5, trans, fontsize=8, color=TEXT_DARK)
        ax.text(52, y_s - 4.5, tools, fontsize=8, style="italic", color="#2C3E50")

        # Bidirectional arrows
        ax.annotate("", xy=(50, y_s + 1), xytext=(32, 40),
                    arrowprops=dict(arrowstyle="<->", color=PRIMARY, lw=1.8))

    out_path = os.path.join(output_dir, "fig5_mcp_topology.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Created:", out_path)

if __name__ == "__main__":
    create_diagram_1()
    create_diagram_2()
    create_diagram_3()
    create_diagram_4()
    create_diagram_5()
    print("All 5 Capstone diagrams generated successfully.")
