"""Contact service — generates pre-filled email drafts for recruiters."""

import urllib.parse

EMAIL = "chabanenarymane@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/narymane-chabane/"


def get_contact_context() -> dict:
    """Generate contact info with mailto link."""

    subject = "Opportunité professionnelle — Prise de contact"
    body = """Bonjour Narymane,

J'ai découvert votre profil via votre chatbot AskNarymane et je souhaiterais échanger avec vous au sujet d'une opportunité professionnelle.

[Décrivez brièvement le poste ou le projet]

Cordialement,
[Votre nom]
[Votre entreprise]"""

    mailto = f"mailto:{EMAIL}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"

    context = f"""[Contact — Narymane Chabane]

Pour contacter Narymane, voici les options :

1. **Email** : [{EMAIL}]({mailto})
   → Cliquez pour ouvrir un brouillon pré-rempli dans votre client mail

2. **LinkedIn** : [{LINKEDIN}]({LINKEDIN})

IMPORTANT: Always include the clickable mailto link and LinkedIn link in your response. Encourage the recruiter to use the email link which opens a pre-filled draft."""

    return {
        "context": context,
        "sources": ["contact:email", "contact:linkedin"],
    }
