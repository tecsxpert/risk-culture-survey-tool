import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.chroma_client import chroma_client

print("Seeding ChromaDB...")
chroma_client.reset_collection()
chroma_client.add_documents([
    {"id": "w2_001", "text": "The board of directors plays a critical role in setting the tone for risk culture. Board oversight includes reviewing risk appetite statements and holding management accountable for risk outcomes.", "metadata": {"category": "Leadership & Governance", "source": "risk_framework_v2"}},
    {"id": "w2_002", "text": "Incident reporting rates improve when organisations establish blame-free reporting cultures. Staff must feel psychologically safe to report near misses without fear of punishment or negative consequences.", "metadata": {"category": "Incident & Near Miss", "source": "risk_framework_v2"}},
    {"id": "w2_003", "text": "Risk accountability requires clear ownership structures where every risk has a named owner. Signs of poor accountability include overdue action items, ignored risk registers, and no consequences for risk failures.", "metadata": {"category": "Accountability", "source": "risk_framework_v2"}},
    {"id": "w2_004", "text": "Risk appetite statements must be communicated clearly to all levels of the organisation. Effective communication includes translating technical risk language into simple terms that frontline staff understand.", "metadata": {"category": "Communication & Reporting", "source": "risk_framework_v2"}},
    {"id": "w2_005", "text": "Effective risk training is scenario-based, regularly updated, and reinforced through ongoing refresher sessions. Training should be role-specific and measure knowledge retention through assessments.", "metadata": {"category": "Training & Competency", "source": "risk_framework_v2"}},
    {"id": "w2_006", "text": "Peer behaviour is one of the strongest influences on individual risk decisions. When senior staff visibly bypass controls, junior staff normalise the same behaviour, creating systemic risk culture problems.", "metadata": {"category": "Culture & Behaviour", "source": "risk_framework_v2"}},
    {"id": "w2_007", "text": "Risk culture goes beyond compliance. While compliance focuses on following rules, risk culture reflects the genuine attitudes and values that drive behaviour when nobody is watching or enforcing the rules.", "metadata": {"category": "Culture & Behaviour", "source": "risk_framework_v2"}},
    {"id": "w2_008", "text": "Managers encourage speak-up culture by actively listening to concerns, providing feedback on reported risks, and visibly acting on information raised by frontline staff. Recognition of risk reporters reinforces the behaviour.", "metadata": {"category": "Communication & Reporting", "source": "risk_framework_v2"}},
    {"id": "w2_009", "text": "Common barriers to risk communication include complex risk language, fear of blame, unclear escalation pathways, and lack of feedback from senior management after risks are reported.", "metadata": {"category": "Communication & Reporting", "source": "risk_framework_v2"}},
    {"id": "w2_010", "text": "Risk culture improvement is measured through regular surveys, incident reporting trends, audit findings, and behavioural indicators such as near miss reporting rates and training completion scores.", "metadata": {"category": "Risk Awareness", "source": "risk_framework_v2"}},
])
print(f"Done — {chroma_client.count()} documents seeded ✓")