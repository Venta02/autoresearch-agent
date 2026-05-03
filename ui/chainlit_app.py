"""
AutoResearch Agent - Chainlit Web UI

Beautiful AI-native chat interface with:
- Live streaming responses
- Tool execution visualization
- Source citations
- Action buttons
- Modern theme

Run:
    chainlit run ui/chainlit_app.py -w
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import chainlit as cl
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from agents import ResearchAgent
from core.config import GEMINI_MODEL


# ============================================
# Welcome Messages & Starters
# ============================================

WELCOME_MESSAGE = """# Welcome to AutoResearch Agent

I'm your **AI-powered research assistant** that can autonomously research any topic using multiple tools.

**What I can do:**
- Plan research strategies
- Search the web (Tavily AI)
- Read and analyze full pages
- Synthesize comprehensive reports
- Generate PDF documents
- Provide source citations

**How to use:**
1. Click a sample query below, or
2. Type your own research question

Let's start researching!
"""


# ============================================
# Starter Suggestions
# ============================================

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="AI Agent Trends 2026",
            message="What are the latest trends in AI agents and autonomous systems in 2026?",
            icon="/public/icons/robot.svg",
        ),
        cl.Starter(
            label="Quantum Computing",
            message="What are the recent breakthroughs in quantum computing and their practical applications?",
            icon="/public/icons/atom.svg",
        ),
        cl.Starter(
            label="Climate Solutions",
            message="What are the most promising climate change adaptation and mitigation strategies?",
            icon="/public/icons/leaf.svg",
        ),
        cl.Starter(
            label="LLM Best Practices",
            message="What are the best practices for fine-tuning and deploying large language models?",
            icon="/public/icons/brain.svg",
        ),
    ]


# ============================================
# Chat Profile (for selecting modes)
# ============================================

@cl.set_chat_profiles
async def chat_profiles():
    return [
        cl.ChatProfile(
            name="Quick Research",
            markdown_description="**Fast research** with 3 iterations max. Best for simple queries.",
            icon="https://cdn-icons-png.flaticon.com/512/2920/2920308.png",
        ),
        cl.ChatProfile(
            name="Deep Research",
            markdown_description="**Thorough research** with 5+ iterations. Best for complex topics.",
            icon="https://cdn-icons-png.flaticon.com/512/2917/2917995.png",
        ),
        cl.ChatProfile(
            name="Academic Mode",
            markdown_description="**Scholarly research** with formal citations and structured reports.",
            icon="https://cdn-icons-png.flaticon.com/512/3145/3145765.png",
        ),
    ]


# ============================================
# On Chat Start
# ============================================

@cl.on_chat_start
async def on_chat_start():
    """Initialize agent when chat starts."""
    
    # Get selected chat profile
    chat_profile = cl.user_session.get("chat_profile") or "Quick Research"
    
    # Initialize agent
    msg = cl.Message(content="Initializing AutoResearch Agent...")
    await msg.send()
    
    try:
        agent = ResearchAgent()
        cl.user_session.set("agent", agent)
        cl.user_session.set("chat_profile", chat_profile)
        cl.user_session.set("research_count", 0)
        
        await msg.remove()
        
        # Send welcome message
        welcome_msg = cl.Message(
            content=f"""# AutoResearch Agent Ready

**Mode:** {chat_profile}
**Model:** Gemini {GEMINI_MODEL}
**Tools:** Web Search, Web Fetch, Summarizer, PDF Generator

Click a starter above or type your research question to begin.""",
            author="System",
        )
        await welcome_msg.send()
        
    except Exception as e:
        error_msg = cl.Message(
            content=f"""# Initialization Failed

Error: {str(e)}

**Setup checklist:**
1. Copy `.env.example` to `.env`
2. Add `GEMINI_API_KEY` (https://aistudio.google.com)
3. Add `TAVILY_API_KEY` (https://app.tavily.com)
4. Run: `pip install -r requirements.txt`

Then restart the app.""",
            author="System",
        )
        await error_msg.send()


# ============================================
# On Message Handler
# ============================================

@cl.on_message
async def on_message(message: cl.Message):
    """Handle user messages with full research pipeline visualization."""
    
    agent: ResearchAgent = cl.user_session.get("agent")
    if not agent:
        await cl.Message(content="Agent not initialized. Please refresh.").send()
        return
    
    query = message.content
    research_count = cl.user_session.get("research_count", 0) + 1
    cl.user_session.set("research_count", research_count)
    
    # Step 1: Planning
    async with cl.Step(name="Planning Research", type="tool") as step:
        step.input = query
        step.output = "Creating research strategy..."
        
        # Show planning visually
        await step.update()
    
    # Step 2: Run research (with progress visualization)
    research_msg = cl.Message(content="", author="AutoResearch")
    await research_msg.send()
    
    # Visual progress
    progress_steps = [
        "Analyzing query and planning research approach...",
        "Searching credible sources...",
        "Reading and analyzing content...",
        "Cross-referencing information...",
        "Synthesizing findings...",
    ]
    
    try:
        # Show progress steps
        progress_text = ""
        for i, step_text in enumerate(progress_steps, 1):
            progress_text += f"**Step {i}:** {step_text}\n\n"
            research_msg.content = progress_text + "\n*Working...*"
            await research_msg.update()
        
        # Run actual research
        async with cl.Step(name="Executing Research", type="tool") as step:
            step.input = query
            
            result = agent.research(query)
            
            step.output = f"Research complete! Found {len(result['sources'])} sources"
            await step.update()
        
        # Step 3: Display final report
        await research_msg.remove()
        
        # Show research plan (collapsible)
        if result.get("plan"):
            async with cl.Step(name="Research Plan", type="run") as step:
                step.output = result["plan"]
        
        # Main report
        report_msg = cl.Message(
            content=result["report"],
            author="AutoResearch",
            elements=[]
        )
        
        # Add sources as elements
        if result.get("sources"):
            sources_text = "## Sources\n\n"
            for i, source in enumerate(result["sources"], 1):
                title = source.get("title", "Untitled")
                url = source.get("url", "")
                if url:
                    sources_text += f"{i}. [{title}]({url})\n"
                else:
                    sources_text += f"{i}. {title}\n"
            
            report_msg.content += "\n\n" + sources_text
        
        # Add metrics
        report_msg.content += f"\n\n---\n"
        report_msg.content += f"**Iterations:** {result.get('iterations', 0)} | "
        report_msg.content += f"**Sources:** {len(result.get('sources', []))} | "
        report_msg.content += f"**Research #{research_count}**"
        
        await report_msg.send()
        
        # Action buttons
        actions = [
            cl.Action(
                name="generate_pdf",
                value=result["report"],
                label="Generate PDF Report",
                description="Export as PDF",
            ),
            cl.Action(
                name="follow_up",
                value=query,
                label="Ask Follow-up",
                description="Continue researching",
            ),
            cl.Action(
                name="new_research",
                value="reset",
                label="New Research",
                description="Start fresh",
            ),
        ]
        
        await cl.Message(
            content="**What would you like to do next?**",
            actions=actions,
            author="System",
        ).send()
        
    except Exception as e:
        await research_msg.remove()
        error_msg = cl.Message(
            content=f"""## Research Failed

**Error:** {str(e)}

**Possible causes:**
- API quota exceeded (Gemini: 250/day, Tavily: 1000/month)
- Network connectivity issues
- Invalid API keys

Try again in a moment, or check your `.env` configuration.""",
            author="System",
        )
        await error_msg.send()


# ============================================
# Action Handlers
# ============================================

@cl.action_callback("generate_pdf")
async def generate_pdf_action(action: cl.Action):
    """Generate PDF from research report."""
    from tools.pdf_generator import generate_pdf_report
    
    async with cl.Step(name="Generating PDF Report", type="tool") as step:
        try:
            result = generate_pdf_report.invoke({
                "title": "AutoResearch Report",
                "content": action.value,
            })
            
            if result.get("status") == "success":
                file_path = result["file_path"]
                step.output = f"PDF generated: {result['filename']}"
                
                # Send file as element
                pdf_element = cl.File(
                    name=result["filename"],
                    path=file_path,
                    display="inline",
                )
                
                await cl.Message(
                    content=f"PDF report generated successfully!\n\nFile size: {result['size_bytes']} bytes",
                    elements=[pdf_element],
                    author="System",
                ).send()
            else:
                step.output = f"Error: {result.get('error')}"
                await cl.Message(
                    content=f"Failed to generate PDF: {result.get('error')}",
                    author="System",
                ).send()
        except Exception as e:
            await cl.Message(
                content=f"Error generating PDF: {str(e)}",
                author="System",
            ).send()


@cl.action_callback("follow_up")
async def follow_up_action(action: cl.Action):
    """Suggest follow-up questions."""
    
    suggestions = [
        f"Tell me more about the most promising aspect of {action.value}",
        f"What are the challenges and limitations related to {action.value}?",
        f"What are the future predictions for {action.value}?",
    ]
    
    suggestions_text = "**Follow-up suggestions:**\n\n"
    for i, suggestion in enumerate(suggestions, 1):
        suggestions_text += f"{i}. {suggestion}\n"
    suggestions_text += "\nOr ask your own follow-up question!"
    
    await cl.Message(
        content=suggestions_text,
        author="System",
    ).send()


@cl.action_callback("new_research")
async def new_research_action(action: cl.Action):
    """Reset for new research."""
    cl.user_session.set("research_count", 0)
    
    await cl.Message(
        content="Ready for new research! What would you like to investigate?",
        author="System",
    ).send()


# ============================================
# On Stop
# ============================================

@cl.on_stop
async def on_stop():
    """Clean up when chat stops."""
    print("Research session ended")
