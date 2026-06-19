 # ---- Proteção de dados do Cliente ---

import re
import logging

class PII_Redactor:
    """
    detecta e mascara PII (Personally Identifiable Information) 
    para proteção de dados (LGPD) e segurança no envio para LLMs.
    """
    
    def __init__(self):
        # Regex simplificados para detecção básica (será melhorado com NLP, posteriormente )
        self.regex_patterns = {
            # CPF (com ou sem pontuação)
            "cpf": re.compile(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b'),
            # Número de Cartão de Crédito (simplificado 16 dígitos)
            "credit_card": re.compile(r'\b(?:\d{4}[ -]?){3}\d{4}\b'),
            # E-mail (básico)
            "email": re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            # Telefone Celular (BR - simplificado)
            "phone": re.compile(r'\b(?:\(?\d{2}\)?\s?)?9\d{4}-?\d{4}\b')
        }

    def redact_text(self, text: str) -> str:
        """
        Substitui PIIs detectados por [DADO MASCARADO: TIPO]
        para proteção dos dados do cliente.
        """
        redacted_text = text
        redactions_found = []

        for pii_type, pattern in self.regex_patterns.items():
            matches = pattern.findall(redacted_text)
            if matches:
                redactions_found.append(f"{pii_type} ({len(matches)})")
                # Substitui as ocorrências pelo placeholder
                redacted_text = pattern.sub(f"[DADO MASCARADO: {pii_type.upper()}]", redacted_text)

        if redactions_found:
            logging.info(f"Dados sensíveis anonimizados antes do processamento: {', '.join(redactions_found)}")
        
        return redacted_text

# Instancia globalmente para reuso em todas as chamadas
redactor = PII_Redactor()