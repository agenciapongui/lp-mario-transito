import json, re, html, urllib.parse, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ======= DADOS DO CLIENTE (editar aqui) =======
BASE  = 'https://lp.mariojunioradvocacia.com.br/advogado-transito/'
PHONE = '5534984248990'   # WhatsApp do Mário — (34) 98424-8990
MSG   = 'Olá! Vim pelo site e gostaria de falar com o advogado especialista em trânsito.'
# ==============================================

WA = 'https://wa.me/%s?text=%s' % (PHONE, urllib.parse.quote(MSG))

def phone_label(p):
    d = p[2:] if p.startswith('55') else p           # tira 55
    ddd, rest = d[:2], d[2:]
    if len(rest) == 9:
        return 'WhatsApp (%s) %s %s-%s' % (ddd, rest[0], rest[1:5], rest[5:])
    return 'WhatsApp (%s) %s-%s' % (ddd, rest[:4], rest[4:])
PHONE_LABEL = phone_label(PHONE)

WAI = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.7-.8-2-.9-.3-.1-.5-.1-.7.1-.2.3-.8.9-.9 1.1-.2.2-.3.2-.6.1-.3-.1-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.4-.5c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.1 4.9 4.3.7.3 1.2.5 1.6.6.7.2 1.3.2 1.8.1.6-.1 1.7-.7 1.9-1.4.2-.7.2-1.2.2-1.4-.1-.1-.3-.2-.6-.3M12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4C2.7 15.6 2.2 13.8 2.2 12 2.2 6.6 6.6 2.2 12 2.2S21.8 6.6 21.8 12 17.4 21.8 12 21.8M12 0C5.4 0 0 5.4 0 12c0 2.1.6 4.2 1.6 6L0 24l6.2-1.6C8 23.4 10 24 12 24c6.6 0 12-5.4 12-12S18.6 0 12 0"/></svg>'
CHECK = '<svg class="check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>'
SHIELD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2 4 6v6c0 5 3.5 8 8 10 4.5-2 8-5 8-10V6l-8-4z"/><path d="m9 12 2 2 4-4"/></svg>'
TRUST = '<div class="trust">%s<span><b>Atendimento direto pelo WhatsApp</b><br>Sigilo profissional · Resposta ágil</span></div>' % SHIELD

faq = [
 ("Como funciona o atendimento?", "Ao tocar em qualquer botão da página, você é direcionado para o WhatsApp do escritório. O advogado conversa com você, entende o seu problema e avalia o caso. Se for preciso, solicita os documentos para concluir a análise. Em seguida, apresenta a solução para o seu caso."),
 ("Preciso ir ao escritório?", "Não. O atendimento é 100% online, pelo WhatsApp, para motoristas de todo o Brasil."),
 ("Quanto vou gastar?", "Somente depois de conversar com você e entender o seu problema é possível formular uma proposta adequada à sua necessidade. Exponha seu caso para a nossa equipe."),
 ("Preciso de um advogado para resolver meu problema?", "Sim. O advogado é o profissional habilitado para assessorar você quando o problema é jurídico. Em questões de trânsito, contar com um advogado especialista é fundamental para apresentar a melhor defesa."),
]
FAQ = ''.join('<details%s><summary><span class="ic" aria-hidden="true">+</span>%s</summary><div class="ans">%s</div></details>'
             % (' open' if i == 0 else '', html.escape(q), html.escape(a)) for i, (q, a) in enumerate(faq))

schema = {"@context": "https://schema.org", "@graph": [
  {"@type": "LegalService", "@id": BASE + "#escritorio", "name": "Mário Júnior Advocacia",
   "description": "Advocacia especializada em Direito de Trânsito: suspensão e cassação de CNH, Lei Seca, recusa ao bafômetro e PPD.",
   "url": BASE, "image": BASE + "assets/img/og.jpg", "logo": BASE + "assets/img/logo-white.webp",
   "telephone": "+" + PHONE, "areaServed": {"@type": "Country", "name": "Brasil"},
   "founder": {"@type": "Person", "name": "Mário Júnior", "jobTitle": "Advogado especialista em Direito de Trânsito", "identifier": "OAB/MG 192.791"},
   "availableLanguage": "Portuguese"},
  {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}

t = open('template.html', encoding='utf-8').read()
rep = {'{{BASE}}': BASE, '{{SCHEMA}}': json.dumps(schema, ensure_ascii=False, separators=(',', ':')),
       '{{WA}}': html.escape(WA), '{{WAICON}}': WAI, '{{CHECK}}': CHECK, '{{TRUST}}': TRUST,
       '{{FAQ}}': FAQ, '{{PHONE_LABEL}}': PHONE_LABEL}
for k, v in rep.items():
    t = t.replace(k, v)
left = re.findall(r'\{\{[^}]+\}\}', t)
assert not left, left
open('index.html', 'w', encoding='utf-8').write(t)
print('ok', len(t), 'bytes | phone', PHONE_LABEL, '| transito' , 'trânsito' in t.lower())
