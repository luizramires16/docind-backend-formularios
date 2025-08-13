from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging
import socket
from datetime import datetime

formularios_bp = Blueprint("formularios", __name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def enviar_email(destinatario, assunto, corpo_html, corpo_texto=None):
    """
    Função para enviar emails via SMTP com timeout e tratamento robusto de erros
    """
    logger.info(f"Iniciando envio de email para: {destinatario}")
    
    try:
        # Configurações SMTP (usando variáveis de ambiente para segurança)
        smtp_server = os.environ.get("SMTP_SERVER", "smtp.hostinger.com")
        smtp_port = int(os.environ.get("SMTP_PORT", "465"))
        smtp_usuario = os.environ.get("SMTP_USUARIO")
        smtp_senha = os.environ.get("SMTP_SENHA")
        
        logger.info(f"Configurações SMTP - Server: {smtp_server}, Port: {smtp_port}, Usuario: {smtp_usuario is not None}")
        
        # Se não houver configurações SMTP, apenas loga (modo desenvolvimento)
        if not smtp_usuario or not smtp_senha:
            logger.warning("Configurações SMTP não encontradas - simulando envio")
            print(f"=== EMAIL SIMULADO (Configurações SMTP não encontradas) ===")
            print(f"Para: {destinatario}")
            print(f"Assunto: {assunto}")
            print(f"Corpo: {corpo_texto or corpo_html}")
            print(f"===================")
            return True
        
        # Configurar timeout para operações de socket
        socket.setdefaulttimeout(30)  # 30 segundos de timeout
        
        logger.info("Criando mensagem de email...")
        
        # Criar mensagem
        msg = MIMEMultipart("alternative")
        msg["Subject"] = assunto
        msg["From"] = smtp_usuario
        msg["To"] = destinatario
        
        # Adicionar corpo do email
        if corpo_texto:
            part1 = MIMEText(corpo_texto, "plain", "utf-8")
            msg.attach(part1)
        
        if corpo_html:
            part2 = MIMEText(corpo_html, "html", "utf-8")
            msg.attach(part2)
        
        logger.info(f"Conectando ao servidor SMTP: {smtp_server}:{smtp_port}")
        
        # Enviar email com timeout - usar SSL para porta 465
        if smtp_port == 465:
            # Conexão SSL direta (porta 465)
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=30)
        else:
            # Conexão STARTTLS (porta 587)
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
            server.starttls(timeout=30)
        
        logger.info("Fazendo login no servidor SMTP...")
        server.login(smtp_usuario, smtp_senha)
        
        logger.info("Enviando mensagem...")
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Email enviado com sucesso para {destinatario}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"Erro de autenticação SMTP: {e}")
        return False
    except smtplib.SMTPConnectError as e:
        logger.error(f"Erro de conexão SMTP: {e}")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"Erro SMTP: {e}")
        return False
    except socket.timeout as e:
        logger.error(f"Timeout na conexão SMTP: {e}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado ao enviar email: {e}")
        return False
    finally:
        # Restaurar timeout padrão
        socket.setdefaulttimeout(None)

@formularios_bp.route("/contato", methods=["POST", "OPTIONS"])
@cross_origin()
def processar_contato():
    if request.method == "OPTIONS":
        logger.info("Requisição OPTIONS recebida para /contato")
        return "", 200
    
    logger.info("Processando formulário de contato...")
    
    try:
        dados = request.get_json() if request.is_json else request.form.to_dict()
        logger.info(f"Dados recebidos: {list(dados.keys())}")  # Log apenas as chaves por segurança
        
        # Validação básica
        campos_obrigatorios = ["nome", "email", "assunto", "mensagem"]
        for campo in campos_obrigatorios:
            if not dados.get(campo):
                logger.warning(f"Campo obrigatório ausente: {campo}")
                return jsonify({"erro": f"Campo {campo} é obrigatório"}), 400
        
        logger.info("Validação dos campos concluída com sucesso")
        
        # Preparar email
        assunto_email = f"[DOC IND] Contato: {dados.get("assunto", "Sem assunto")}"
        
        corpo_email = f"""
        Nova mensagem de contato recebida:
        
        Nome: {dados.get("nome", "")}
        Empresa: {dados.get("empresa", "Não informado")}
        E-mail: {dados.get("email", "")}
        Telefone: {dados.get("telefone", "Não informado")}
        Assunto: {dados.get("assunto", "")}
        
        Mensagem:
        {dados.get("mensagem", "")}
        
        Newsletter: {"Sim" if dados.get("newsletter") else "Não"}
        Aceita política: {"Sim" if dados.get("privacidade") else "Não"}
        
        Data/Hora: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
        """
        
        logger.info("Iniciando envio de email...")
        
        # Enviar email
        email_enviado = enviar_email("docind@docind.com.br", assunto_email, corpo_email)
        
        if email_enviado:
            logger.info("Email de contato enviado com sucesso")
            return jsonify({"sucesso": True, "mensagem": "Mensagem enviada com sucesso!"}), 200
        else:
            logger.error("Falha no envio do email de contato")
            return jsonify({"erro": "Erro ao enviar mensagem. Tente novamente."}), 500
            
    except Exception as e:
        logger.error(f"Erro no processamento do contato: {e}", exc_info=True)
        return jsonify({"erro": "Erro interno do servidor"}), 500

@formularios_bp.route("/orcamento", methods=["POST", "OPTIONS"])
@cross_origin()
def processar_orcamento():
    if request.method == "OPTIONS":
        logger.info("Requisição OPTIONS recebida para /orcamento")
        return "", 200
    
    logger.info("Processando formulário de orçamento...")
    
    try:
        dados = request.get_json() if request.is_json else request.form.to_dict()
        logger.info(f"Dados recebidos: {list(dados.keys())}")  # Log apenas as chaves por segurança
        
        # Validação básica
        campos_obrigatorios = ["nome", "email", "empresa"]
        for campo in campos_obrigatorios:
            if not dados.get(campo):
                logger.warning(f"Campo obrigatório ausente: {campo}")
                return jsonify({"erro": f"Campo {campo} é obrigatório"}), 400
        
        logger.info("Validação dos campos concluída com sucesso")
        
        # Preparar email
        assunto_email = f"[DOC IND] Solicitação de Orçamento - {dados.get("nome", "")}"
        
        # Processar serviços selecionados
        servicos = []
        # Verifica se o valor é 'on' para adicionar o serviço
        if dados.get("servico_manuais") == "on": servicos.append("Manuais Técnicos Personalizados")
        if dados.get("servico_fmea") == "on": servicos.append("Análise de Falhas Estratégica (FMEA)")
        if dados.get("servico_manutencao") == "on": servicos.append("Gestão de Manutenção Inteligente")
        if dados.get("servico_qualidade") == "on": servicos.append("Documentação de Qualidade e Conformidade")
        if dados.get("servico_consultoria") == "on": servicos.append("Consultoria Estratégica em Documentação")
        if dados.get("servico_implantacao") == "on": servicos.append("Implantação de Sistemas e Treinamentos")
        
        corpo_email = f"""
        Nova solicitação de orçamento recebida:
        
        === INFORMAÇÕES DE CONTATO ===
        Nome: {dados.get("nome", "")}
        Empresa: {dados.get("empresa", "")}
        E-mail: {dados.get("email", "")}
        Telefone: {dados.get("telefone", "Não informado")}
        Cargo/Função: {dados.get("cargo", "Não informado")}
        Setor de Atuação: {dados.get("setor", "Não informado")}
        
        === SERVIÇOS DE INTERESSE ===
        {chr(10).join(["• " + servico for servico in servicos]) if servicos else "Nenhum serviço selecionado"}
        
        === DETALHES DO PROJETO ===
        Urgência: {dados.get("urgencia", "Não informado")}
        Orçamento Estimado: {dados.get("orcamento_estimado", "Não informado")}
        
        Equipamentos/Sistemas:
        {dados.get("equipamentos", "Não informado")}
        
        Descrição do Projeto:
        {dados.get("descricao_projeto", "Não informado")}
        
        === INFORMAÇÕES ADICIONAIS ===
        Possui documentação existente: {dados.get("documentacao_existente", "Não informado")}
        Normas específicas: {dados.get("normas", "Não informado")}
        Observações: {dados.get("observacoes", "Não informado")}
        
        === PREFERÊNCIAS DE CONTATO ===
        Melhor horário: {dados.get("horario_contato", "Não informado")}
        Meio preferido: {dados.get("meio_contato", "Não informado")}
        
        Data/Hora: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
        """
        
        logger.info("Iniciando envio de email...")
        
        # Enviar email
        email_enviado = enviar_email("docind@docind.com.br", assunto_email, corpo_email)
        
        if email_enviado:
            logger.info("Email de orçamento enviado com sucesso")
            return jsonify({"sucesso": True, "mensagem": "Solicitação de orçamento enviada com sucesso!"}), 200
        else:
            logger.error("Falha no envio do email de orçamento")
            return jsonify({"erro": "Erro ao enviar solicitação. Tente novamente."}), 500
            
    except Exception as e:
        logger.error(f"Erro no processamento do orçamento: {e}", exc_info=True)
        return jsonify({"erro": "Erro interno do servidor"}), 500

@formularios_bp.route("/status", methods=["GET"])
def status():
    """Endpoint para verificar se o serviço está funcionando"""
    return jsonify({"status": "ok", "servico": "Formulários DOC IND"}), 200



