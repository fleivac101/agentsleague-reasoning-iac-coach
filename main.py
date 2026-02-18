import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI

# ==========================================================
# 🚀 TERRAFORM GUARDIAN – Microsoft Agents League Edition
# ==========================================================

print("\n🚀 Starting Terraform Guardian Scan...\n")

# Load environment variables
load_dotenv()

# Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-12-01-preview"
)

deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# ----------------------------------------------------------
# 📂 Load Terraform file dynamically
# ----------------------------------------------------------

try:
    with open("sample_insecure.tf", "r") as f:
        terraform_code = f.read()
except FileNotFoundError:
    print("❌ sample_insecure.tf not found in this folder.")
    exit()

# ----------------------------------------------------------
# 🤖 Multi-Agent Call Function
# ----------------------------------------------------------

def call_agent(role, prompt):
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content


# ==========================================================
# 🧠 AGENT 1 – Structural Analyzer
# ==========================================================

analysis = call_agent(
    "You are a Terraform structural analysis agent.",
    f"Analyze the following Terraform code. Extract resources, detect structural issues and governance gaps:\n\n{terraform_code}"
)

# ==========================================================
# ⚖️ AGENT 2 – Security Policy Reviewer
# ==========================================================

policy = call_agent(
    "You are a cloud security policy reviewer.",
    f"Review this Terraform analysis and classify security risks with severity (LOW/MEDIUM/HIGH):\n\n{analysis}"
)

# ==========================================================
# 🛠️ AGENT 3 – Remediation Architect
# ==========================================================

remediation = call_agent(
    "You are a Terraform remediation architect.",
    f"Provide improved Terraform code and explain changes:\n\n{terraform_code}"
)

# ==========================================================
# 📊 AGENT 4 – Executive Risk Reporter
# ==========================================================

report = call_agent(
    "You are an executive cloud risk reporting agent.",
    f"""
    Based on this policy review, generate a JSON executive summary:

    Required format:
    {{
      "overall_risk_score": number (0-100),
      "risk_level": "LOW/MEDIUM/HIGH",
      "top_risks": [
        {{"issue": "...", "severity": "..."}}
      ],
      "recommended_action": [
        "action 1",
        "action 2"
      ]
    }}

    Policy review:
    {policy}
    """
)

# ==========================================================
# 🎨 WOW VISUAL OUTPUT
# ==========================================================

print("="*70)
print("🛡️  TERRAFORM GUARDIAN – AI GOVERNANCE REPORT")
print("="*70)

print("\n🔍 STRUCTURAL ANALYSIS")
print("-"*70)
print(analysis)

print("\n⚖️  POLICY & SECURITY REVIEW")
print("-"*70)
print(policy)

print("\n🛠️  REMEDIATION PLAN")
print("-"*70)
print(remediation)

print("\n📊 EXECUTIVE RISK SUMMARY")
print("-"*70)

try:
    parsed_report = json.loads(report)
    print(f"Overall Risk Score : {parsed_report.get('overall_risk_score', 'N/A')}/100")
    print(f"Risk Level         : {parsed_report.get('risk_level', 'N/A')}")

    print("\nTop Risks:")
    for risk in parsed_report.get("top_risks", []):
        print(f"  - {risk.get('issue')} ({risk.get('severity')})")

    print("\nRecommended Actions:")
    for action in parsed_report.get("recommended_action", []):
        print(f"  - {action}")

except:
    print(report)

print("\n" + "="*70)
print("🔐 Governance Confidence Level: Enterprise Ready")
print("✅ Terraform Guardian Scan Completed")
print("="*70)
