# --- FAQ - NovaBank - Dados Homologados --> Respostas Rápidas e eficientes (Busca Semântica)
# Formato Aceito: Lista de Dicionários contendo 'pergunta' e 'resposta'.

novabank_faq = [
    # --- Seguranca e Acesso ---
    {
        "pergunta": "Como alterar a senha de acesso do aplicativo?",
        "resposta": "Para sua segurança, a alteração de senha deve ser feita logado no app. Vá em Perfil -> Segurança -> Alterar Senha de Acesso. Você precisará digitar a senha atual e definir uma nova. A nova senha deve ter entre 8 e 12 caracteres, conter pelo menos uma letra maiúscula, uma minúscula, um número e um símbolo (ex: @,#,$)."
    },
    {
        "pergunta": "Esqueci minha senha do app. O que devo fazer para recuperar?",
        "resposta": "Na tela inicial de login, clique no link 'Esqueceu a senha?'. Insira seu CPF ou e-mail cadastrado. Enviaremos um código de verificação para o seu e-mail ou SMS cadastrado. Siga as instruções na tela para criar uma nova senha de forma segura."
    },
    {
        "pergunta": "Como ativar a autenticação de dois fatores (2FA) para maior segurança?",
        "resposta": "A autenticação de dois fatores é essencial para proteger sua conta. Vá em Perfil -> Segurança -> Autenticação de Dois Fatores (2FA). Você pode escolher receber códigos via SMS/E-mail ou vincular a um aplicativo autenticador (como Google Authenticator). Recomendamos o uso de app autenticador para maior segurança contra golpes de SIM swap."
    },
    {
        "pergunta": "O que fazer se eu receber um SMS ou e-mail suspeito do NovaBank?",
        "resposta": "Fique alerta! O NovaBank nunca solicita senhas, tokens ou dados sensíveis via SMS ou e-mail, nem envia links para atualização cadastral com urgência. Se receber algo suspeito, NÃO clique em links. Denuncie imediatamente enviando um print para phishing@novabank.com.br e exclua a mensagem. Em caso de dúvida, entre em contato pelos nossos canais oficiais."
    },
    {
        "pergunta": "Qual o prazo de desbloqueio da conta após tentativas de senha incorreta?",
        "resposta": "Após 3 tentativas incorretas, seu acesso é bloqueado preventivamente por 30 minutos. Após este período, você receberá automaticamente um código de desbloqueio via SMS no celular cadastrado. Se o problema persistir, será necessário realizar a recuperação de senha."
    },

    # --- Cartões ---
    {
        "pergunta": "Meu cartão foi bloqueado. Como faço para desbloquear?",
        "resposta": "Se o bloqueio foi realizado por você preventivamente, acesse App -> aba Cartões -> Bloquear/Desbloquear e confirme com sua senha. Caso o bloqueio tenha sido realizado pelo banco por suspeita de fraude, você receberá uma notificação. Neste caso, é obrigatório entrar em contato com nossa Central de Segurança imediatamente para confirmação de transações."
    },
    {
        "pergunta": "Como faço para solicitar um cartão de crédito NovaBank?",
        "resposta": "A solicitação está sujeita à análise de crédito. No app, vá na aba Cartões e clique em 'Solicitar Cartão de Crédito'. Preencha os dados solicitados e anexe seu comprovante de renda atualizado (dos últimos 3 meses). A resposta da análise é enviada por e-mail em até 5 dias úteis."
    },
    {
        "pergunta": "Como solicitar a segunda via do meu cartão físico?",
        "resposta": "Vá na aba Cartões -> Configurações do Cartão -> Solicitar 2ª Via. Escolha o motivo (perda, roubo, dano). Confirme o endereço de entrega e a transação com sua senha. O novo cartão leva entre 7 e 10 dias úteis para chegar. O cartão virtual continua funcionando normalmente."
    },

    # --- Transações, Limites e Fraude ---
    {
        "pergunta": "Qual o limite diário padrão para transferências (TED/Pix)?",
        "resposta": "Para sua segurança, o limite diário padrão para transferências é de R$ 50.000,00 para dias úteis (entre 06h e 20h). Transações acima desse valor ou realizadas no período noturno/finais de semana podem exigir aprovação biométrica adicional no app ou aprovação prévia do seu gerente de conta, devido às normas do Banco Central."
    },
    {
        "pergunta": "Como registrar um boletim de ocorrência (BO) após sofrer uma fraude financeira?",
        "resposta": "Em casos de fraude, a rapidez é fundamental. 1º) Bloqueie seus cartões e conta no app. 2º) Registre o BO na Delegacia Eletrônica do seu estado, detalhando datas, valores e contas envolvidas. 3º) Após o registro, envie o PDF do BO e o número de protocolo para fraude@novabank.com.br para que nossa equipe jurídica possa iniciar o processo de contestação e cooperação com as autoridades."
    },
    {
        "pergunta": "Como configurar alertas e notificações de transações na minha conta?",
        "resposta": "Recomendamos ativar as notificações para monitorar sua conta em tempo real. Vá em Perfil -> Notificações -> Alertas de Transação. Ative as notificações push para compras no cartão, Pix enviados/recebidos e movimentações acima de um valor que você definir."
    },
    {
        "pergunta": "O que é o PIX e como posso começar a usar no NovaBank?",
        "resposta": "O PIX é o sistema de pagamentos instantâneos do Banco Central, gratuito para pessoas físicas, que funciona 24h por dia, todos os dias. No app NovaBank, vá em Transferências -> aba Pix. Lá você pode cadastrar suas chaves (CPF, Celular, E-mail ou Chave Aleatória), pagar via QR Code ou fazer transferências inserindo a chave do destinatário."
    },
    {
        "pergunta": "Como cancelar o agendamento de um pagamento ou transferência?",
        "resposta": "Vá na aba Pagamentos -> Agendados. Selecione o pagamento que deseja cancelar. O cancelamento só pode ser realizado até às 23:59h do dia útil anterior à data agendada para o débito. Pagamentos agendados para o próprio dia não podem ser cancelados."
    },

    # --- Serviços de Conta e Documentos ---
    {
        "pergunta": "Posso fazer depósito de cheque pelo celular?",
        "resposta": "Sim. Utilize a função 'Depósito de Cheque' no menu principal do app. Tire fotos nítidas da frente e do verso do cheque (que deve estar endossado). O valor é creditado em conta em até 2 dias úteis após a análise da imagem. Importante: guarde o cheque físico por 180 dias após o depósito."
    },
    {
        "pergunta": "Como faço para abrir uma conta conjunta no NovaBank?",
        "resposta": "Atualmente, o processo de abertura de conta conjunta é realizado exclusivamente pelo titular principal através do nosso site. Na área de abertura de conta, selecione a opção 'Conta Conjunta' e siga os passos para inserção dos dados de ambos os titulares. Ambos precisarão passar pela validação biométrica."
    },
    {
        "pergunta": "Quais os documentos necessários para solicitar um financiamento imobiliário?",
        "resposta": "Para a análise inicial de crédito habitacional, solicitamos: RG/CPF, Comprovante de Estado Civil, Comprovante de Residência (atualizado), Comprovante de Renda (Holerites ou Declaração IR Completa), Extratos Bancários dos últimos 3 meses e a Matrícula atualizada do imóvel. Recomendamos agendar uma conversa com um especialista em crédito imobiliário pelo chat."
    },
    {
        "pergunta": "Como solicitar um empréstimo pessoal no app?",
        "resposta": "Na aba 'Empréstimos', clique em 'Simular Solicitação'. Defina o valor desejado e o prazo de pagamento. A análise de risco de crédito é imediata. Se aprovado, as taxas pré-definidas serão apresentadas. A contratação é 100% digital e o dinheiro cai na conta na hora."
    },
    {
        "pergunta": "Onde posso consultar meu score de crédito no NovaBank?",
        "resposta": "Disponibilizamos essa informação gratuitamente. Vá em Perfil -> Serviços Adicionais -> Score de Crédito. Essa pontuação é fornecida por birôs de crédito parceiros (como Serasa/Boa Vista) e é atualizada mensalmente, influenciando diretamente as taxas e limites oferecidos pelo banco."
    },
    {
        "pergunta": "Como faço para atualizar meu endereço residencial cadastrado?",
        "resposta": "É essencial manter seus dados atualizados. Vá em Perfil -> Dados Pessoais -> Endereço residencial. Insira o novo CEP e o endereço completo. Será necessário anexar uma foto nítida de um comprovante de residência em seu nome (água, luz, telefone fixo) emitido nos últimos 90 dias."
    },
    {
        "pergunta": "Como entrar em contato com a Ouvidoria do NovaBank?",
        "resposta": "A Ouvidoria é a última instância de atendimento para casos não resolvidos satisfatoriamente pelos canais convencionais (SAC/Chat). Atendemos pelo telefone 0800 987 6543 (dias úteis, 09h às 18h) ou pelo e-mail ouvidoria@novabank.com.br. É obrigatório ter em mãos o protocolo do atendimento anterior."
    },

    # --- NOVAS Q&As ( value add de completude) ---
    {
        "pergunta": "Como fazer portabilidade de salário para o NovaBank?",
        "resposta": "É simples e gratuito. No app, vá em Perfil -> Portabilidade de Salário. Insira o CNPJ da empresa onde trabalha e o banco onde recebe atualmente. A solicitação leva até 10 dias úteis para ser processada pelos bancos. Você receberá uma notificação quando seu próximo salário cair direto no NovaBank."
    },
    {
        "pergunta": "O NovaBank oferece produtos de investimento? Quais?",
        "resposta": "Sim. Na aba 'Investimentos', oferecemos opções para diferentes perfis. Temos Renda Fixa (CDBs NovaBank com liquidez diária e rendimento acima da Poupança), Fundos de Investimento (Renda Fixa, Multimercado e Ações) e acesso direto à Bolsa de Valores para compra de Ações e FIIs. Você deve preencher seu questionário de Perfil de Investidor antes de começar."
    },
    {
        "pergunta": "Onde encontro meu Informe de Rendimentos para Declaração de Imposto de Renda?",
        "resposta": "O Informe de Rendimentos anual é disponibilizado até o último dia útil de fevereiro. No app, vá em Perfil -> Documentos -> Informe de Rendimentos. Você pode visualizar o PDF ou enviá-lo diretamente para seu e-mail."
    },
    {
        "pergunta": "Quais os horários de atendimento para falar com um humano?",
        "resposta": "Nosso chat no app funciona 24h para dúvidas gerais e suporte emergencial de cartões/fraude. O atendimento telefônico (SAC 0800) e Ouvidoria funcionam em dias úteis, das 09h às 18h. Para bloqueio de cartão por perda/roubo, nossa central telefônica de segurança também atende 24h."
    }
]