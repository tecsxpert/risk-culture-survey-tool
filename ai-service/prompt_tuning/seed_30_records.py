import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.chroma_client import chroma_client

print("Seeding ChromaDB with 30 demo records...")
chroma_client.reset_collection()

DOCUMENTS = [
    # Leadership & Governance (6 docs)
    {
        "id": "demo_001",
        "text": (
            "The board of directors plays a critical role in setting "
            "the tone for risk culture. Board oversight includes "
            "reviewing risk appetite statements and holding management "
            "accountable for risk outcomes."
        ),
        "metadata": {
            "category": "Leadership & Governance",
            "source":   "demo_records",
            "record_id": 1
        }
    },
    {
        "id": "demo_002",
        "text": (
            "Senior leadership must visibly champion risk management "
            "in all communications. When executives discuss risk in "
            "town halls and board meetings, employees follow their "
            "example and take risk processes seriously."
        ),
        "metadata": {
            "category": "Leadership & Governance",
            "source":   "demo_records",
            "record_id": 2
        }
    },
    {
        "id": "demo_003",
        "text": (
            "Risk governance frameworks define how risks are identified "
            "escalated and managed across the organisation. Without "
            "clear governance structures, risk management becomes "
            "inconsistent and ineffective."
        ),
        "metadata": {
            "category": "Leadership & Governance",
            "source":   "demo_records",
            "record_id": 3
        }
    },
    {
        "id": "demo_004",
        "text": (
            "The risk committee should meet at least quarterly to "
            "review the organisation's risk profile. Effective "
            "committees have clear mandates, diverse membership, "
            "and direct reporting lines to the board."
        ),
        "metadata": {
            "category": "Leadership & Governance",
            "source":   "demo_records",
            "record_id": 4
        }
    },
    {
        "id": "demo_005",
        "text": (
            "Tone from the top is the single most important driver "
            "of risk culture. Organisations where leaders model good "
            "risk behaviour consistently outperform those where "
            "leadership is disengaged from risk management."
        ),
        "metadata": {
            "category": "Leadership & Governance",
            "source":   "demo_records",
            "record_id": 5
        }
    },
    {
        "id": "demo_006",
        "text": (
            "Board risk appetite statements must be translated into "
            "operational limits that frontline staff can understand "
            "and apply in their daily decisions."
        ),
        "metadata": {
            "category": "Leadership & Governance",
            "source":   "demo_records",
            "record_id": 6
        }
    },
    # Risk Awareness (4 docs)
    {
        "id": "demo_007",
        "text": (
            "Risk awareness training helps employees understand how "
            "to identify and report risks in their daily work. "
            "Regular training improves overall risk culture scores "
            "significantly across all departments."
        ),
        "metadata": {
            "category": "Risk Awareness",
            "source":   "demo_records",
            "record_id": 7
        }
    },
    {
        "id": "demo_008",
        "text": (
            "Employees with high risk awareness can identify emerging "
            "risks before they escalate into incidents. This early "
            "warning capability is one of the most valuable outcomes "
            "of a strong risk culture programme."
        ),
        "metadata": {
            "category": "Risk Awareness",
            "source":   "demo_records",
            "record_id": 8
        }
    },
    {
        "id": "demo_009",
        "text": (
            "Risk awareness surveys help organisations measure how "
            "well employees understand the risk landscape. Low scores "
            "indicate training gaps that need to be addressed urgently "
            "before they lead to operational failures."
        ),
        "metadata": {
            "category": "Risk Awareness",
            "source":   "demo_records",
            "record_id": 9
        }
    },
    {
        "id": "demo_010",
        "text": (
            "Understanding risk appetite is a key component of risk "
            "awareness. Staff who know the organisation's risk "
            "tolerance make better decisions and escalate appropriately "
            "when risks approach or exceed defined thresholds."
        ),
        "metadata": {
            "category": "Risk Awareness",
            "source":   "demo_records",
            "record_id": 10
        }
    },
    # Communication & Reporting (4 docs)
    {
        "id": "demo_011",
        "text": (
            "Effective risk communication involves clear escalation "
            "pathways so that frontline staff can report risks to "
            "senior management quickly. Delays in communication "
            "allow small risks to become major incidents."
        ),
        "metadata": {
            "category": "Communication & Reporting",
            "source":   "demo_records",
            "record_id": 11
        }
    },
    {
        "id": "demo_012",
        "text": (
            "Risk reports should be clear, concise, and actionable. "
            "Reports that are too long or too technical fail to "
            "reach decision makers in time to prevent adverse outcomes."
        ),
        "metadata": {
            "category": "Communication & Reporting",
            "source":   "demo_records",
            "record_id": 12
        }
    },
    {
        "id": "demo_013",
        "text": (
            "Managers encourage speak-up culture by actively listening "
            "to concerns, providing feedback on reported risks, and "
            "visibly acting on information raised by frontline staff. "
            "Recognition of risk reporters reinforces the behaviour."
        ),
        "metadata": {
            "category": "Communication & Reporting",
            "source":   "demo_records",
            "record_id": 13
        }
    },
    {
        "id": "demo_014",
        "text": (
            "Common barriers to risk communication include complex "
            "risk language, fear of blame, unclear escalation pathways "
            "and lack of feedback from senior management after risks "
            "are reported by frontline employees."
        ),
        "metadata": {
            "category": "Communication & Reporting",
            "source":   "demo_records",
            "record_id": 14
        }
    },
    # Accountability (4 docs)
    {
        "id": "demo_015",
        "text": (
            "Risk accountability requires clear ownership structures "
            "where every risk has a named owner. Signs of poor "
            "accountability include overdue action items, ignored "
            "risk registers, and no consequences for risk failures."
        ),
        "metadata": {
            "category": "Accountability",
            "source":   "demo_records",
            "record_id": 15
        }
    },
    {
        "id": "demo_016",
        "text": (
            "Performance reviews should include risk management "
            "objectives for all staff. Linking risk behaviour to "
            "compensation and promotion decisions creates meaningful "
            "accountability throughout the organisation."
        ),
        "metadata": {
            "category": "Accountability",
            "source":   "demo_records",
            "record_id": 16
        }
    },
    {
        "id": "demo_017",
        "text": (
            "Risk owners must have the authority and resources to "
            "manage their assigned risks effectively. Without proper "
            "empowerment, risk ownership becomes a paper exercise "
            "that adds no real value to the organisation."
        ),
        "metadata": {
            "category": "Accountability",
            "source":   "demo_records",
            "record_id": 17
        }
    },
    {
        "id": "demo_018",
        "text": (
            "Three lines of defence model clarifies accountability "
            "across the organisation. First line owns the risks, "
            "second line provides oversight, and third line provides "
            "independent assurance to the board."
        ),
        "metadata": {
            "category": "Accountability",
            "source":   "demo_records",
            "record_id": 18
        }
    },
    # Training & Competency (4 docs)
    {
        "id": "demo_019",
        "text": (
            "Effective risk training is scenario-based, regularly "
            "updated, and reinforced through ongoing refresher "
            "sessions. Training should be role-specific and measure "
            "knowledge retention through post-training assessments."
        ),
        "metadata": {
            "category": "Training & Competency",
            "source":   "demo_records",
            "record_id": 19
        }
    },
    {
        "id": "demo_020",
        "text": (
            "New employee onboarding must include risk management "
            "training from day one. Early exposure to risk culture "
            "expectations sets the right tone and reduces the time "
            "needed for new staff to become risk-aware."
        ),
        "metadata": {
            "category": "Training & Competency",
            "source":   "demo_records",
            "record_id": 20
        }
    },
    {
        "id": "demo_021",
        "text": (
            "Risk training completion rates are a key indicator of "
            "cultural engagement. Low completion rates suggest that "
            "risk management is not seen as a priority by staff or "
            "their line managers."
        ),
        "metadata": {
            "category": "Training & Competency",
            "source":   "demo_records",
            "record_id": 21
        }
    },
    {
        "id": "demo_022",
        "text": (
            "Specialist risk roles require dedicated competency "
            "frameworks. Risk managers, compliance officers, and "
            "internal auditors need deeper technical knowledge than "
            "general staff risk awareness programmes provide."
        ),
        "metadata": {
            "category": "Training & Competency",
            "source":   "demo_records",
            "record_id": 22
        }
    },
    # Policies & Procedures (3 docs)
    {
        "id": "demo_023",
        "text": (
            "Risk policies must be written in plain language that all "
            "employees can understand and apply. Policies written in "
            "legal or technical language are rarely read and even "
            "more rarely followed by frontline staff."
        ),
        "metadata": {
            "category": "Policies & Procedures",
            "source":   "demo_records",
            "record_id": 23
        }
    },
    {
        "id": "demo_024",
        "text": (
            "Procedure reviews should happen at least annually or "
            "when significant changes occur. Outdated procedures "
            "create compliance gaps and expose the organisation to "
            "unnecessary operational and regulatory risks."
        ),
        "metadata": {
            "category": "Policies & Procedures",
            "source":   "demo_records",
            "record_id": 24
        }
    },
    {
        "id": "demo_025",
        "text": (
            "Policy exceptions must be formally approved and "
            "time-limited. Uncontrolled exceptions undermine the "
            "integrity of the policy framework and create a culture "
            "where bypassing controls becomes normalised."
        ),
        "metadata": {
            "category": "Policies & Procedures",
            "source":   "demo_records",
            "record_id": 25
        }
    },
    # Incident & Near Miss (3 docs)
    {
        "id": "demo_026",
        "text": (
            "Incident reporting rates improve when organisations "
            "establish blame-free reporting cultures. Staff must "
            "feel psychologically safe to report near misses without "
            "fear of punishment or negative consequences."
        ),
        "metadata": {
            "category": "Incident & Near Miss",
            "source":   "demo_records",
            "record_id": 26
        }
    },
    {
        "id": "demo_027",
        "text": (
            "Near miss reporting is one of the most valuable leading "
            "indicators of risk culture health. Organisations that "
            "capture and act on near misses experience significantly "
            "fewer major incidents over time."
        ),
        "metadata": {
            "category": "Incident & Near Miss",
            "source":   "demo_records",
            "record_id": 27
        }
    },
    {
        "id": "demo_028",
        "text": (
            "Lessons learned from incidents must be shared across "
            "the organisation to prevent recurrence. Without a "
            "systematic process for sharing learnings, organisations "
            "repeat the same mistakes repeatedly."
        ),
        "metadata": {
            "category": "Incident & Near Miss",
            "source":   "demo_records",
            "record_id": 28
        }
    },
    # Culture & Behaviour (2 docs)
    {
        "id": "demo_029",
        "text": (
            "Risk culture goes beyond compliance. While compliance "
            "focuses on following rules, risk culture reflects the "
            "genuine attitudes and values that drive behaviour when "
            "nobody is watching or enforcing the rules."
        ),
        "metadata": {
            "category": "Culture & Behaviour",
            "source":   "demo_records",
            "record_id": 29
        }
    },
    {
        "id": "demo_030",
        "text": (
            "Peer behaviour is one of the strongest influences on "
            "individual risk decisions. When senior staff visibly "
            "bypass controls, junior staff normalise the same "
            "behaviour, creating systemic risk culture problems."
        ),
        "metadata": {
            "category": "Culture & Behaviour",
            "source":   "demo_records",
            "record_id": 30
        }
    }
]

chroma_client.add_documents(DOCUMENTS)
print(f"Seeded {chroma_client.count()} documents ✓")
print("Now start Flask: python app.py")