// Script para integrar os formulários do site DOC IND com o backend Flask

// Configuração da API
const API_BASE_URL = window.location.origin + '/api/formularios';

// Função para mostrar mensagens de feedback
function mostrarMensagem(mensagem, tipo = 'success') {
    // Remove mensagem anterior se existir
    const mensagemAnterior = document.querySelector('.mensagem-feedback');
    if (mensagemAnterior) {
        mensagemAnterior.remove();
    }

    // Cria nova mensagem
    const div = document.createElement('div');
    div.className = `mensagem-feedback mensagem-${tipo}`;
    div.innerHTML = `
        <p>${mensagem}</p>
        <button onclick="this.parentElement.remove()">×</button>
    `;
    
    // Adiciona estilos inline
    div.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${tipo === 'success' ? '#4CAF50' : '#f44336'};
        color: white;
        padding: 15px 20px;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 10000;
        max-width: 400px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    `;
    
    div.querySelector('button').style.cssText = `
        background: none;
        border: none;
        color: white;
        font-size: 18px;
        cursor: pointer;
        margin-left: 10px;
    `;

    document.body.appendChild(div);

    // Remove automaticamente após 5 segundos
    setTimeout(() => {
        if (div.parentElement) {
            div.remove();
        }
    }, 5000);
}

// Função para desabilitar/habilitar botão de envio
function toggleBotaoEnvio(botao, desabilitar = true) {
    if (desabilitar) {
        botao.disabled = true;
        botao.textContent = 'Enviando...';
        botao.style.opacity = '0.6';
    } else {
        botao.disabled = false;
        botao.textContent = botao.getAttribute('data-texto-original') || 'Enviar';
        botao.style.opacity = '1';
    }
}

// Função para processar formulário de contato
async function processarFormularioContato(event) {
    event.preventDefault();
    
    const form = event.target;
    const botaoEnvio = form.querySelector('button[type="submit"]');
    
    // Salva texto original do botão
    if (!botaoEnvio.getAttribute('data-texto-original')) {
        botaoEnvio.setAttribute('data-texto-original', botaoEnvio.textContent);
    }
    
    toggleBotaoEnvio(botaoEnvio, true);

    try {
        // Coleta dados do formulário
        const formData = new FormData(form);
        const dados = {
            nome: formData.get('nome') || '',
            empresa: formData.get('empresa') || '',
            email: formData.get('email') || '',
            telefone: formData.get('telefone') || '',
            assunto: formData.get('assunto') || '',
            mensagem: formData.get('mensagem') || '',
            newsletter: formData.get('newsletter') === 'on',
            privacidade: formData.get('privacidade') === 'on'
        };

        // Validação básica
        if (!dados.nome || !dados.email || !dados.assunto || !dados.mensagem) {
            mostrarMensagem('Por favor, preencha todos os campos obrigatórios.', 'error');
            toggleBotaoEnvio(botaoEnvio, false);
            return;
        }

        if (!dados.privacidade) {
            mostrarMensagem('Você deve aceitar a política de privacidade para continuar.', 'error');
            toggleBotaoEnvio(botaoEnvio, false);
            return;
        }

        // Envia dados para o backend
        const response = await fetch(`${API_BASE_URL}/contato`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dados)
        });

        const resultado = await response.json();

        if (response.ok) {
            mostrarMensagem('Mensagem enviada com sucesso! Entraremos em contato em breve.', 'success');
            form.reset();
        } else {
            mostrarMensagem(resultado.erro || 'Erro ao enviar mensagem. Tente novamente.', 'error');
        }

    } catch (error) {
        console.error('Erro ao enviar formulário:', error);
        mostrarMensagem('Erro de conexão. Verifique sua internet e tente novamente.', 'error');
    } finally {
        toggleBotaoEnvio(botaoEnvio, false);
    }
}

// Função para processar formulário de orçamento
async function processarFormularioOrcamento(event) {
    event.preventDefault();
    
    const form = event.target;
    const botaoEnvio = form.querySelector('button[type="submit"]');
    
    // Salva texto original do botão
    if (!botaoEnvio.getAttribute('data-texto-original')) {
        botaoEnvio.setAttribute('data-texto-original', botaoEnvio.textContent);
    }
    
    toggleBotaoEnvio(botaoEnvio, true);

    try {
        // Coleta dados do formulário
        const formData = new FormData(form);
        const dados = {
            nome: formData.get('nome') || '',
            empresa: formData.get('empresa') || '',
            email: formData.get('email') || '',
            telefone: formData.get('telefone') || '',
            cargo: formData.get('cargo') || '',
            setor: formData.get('setor') || '',
            servico_manuais: formData.get('servico_manuais') === 'on',
            servico_fmea: formData.get('servico_fmea') === 'on',
            servico_manutencao: formData.get('servico_manutencao') === 'on',
            servico_qualidade: formData.get('servico_qualidade') === 'on',
            servico_consultoria: formData.get('servico_consultoria') === 'on',
            servico_implantacao: formData.get('servico_implantacao') === 'on',
            urgencia: formData.get('urgencia') || '',
            orcamento_estimado: formData.get('orcamento_estimado') || '',
            equipamentos: formData.get('equipamentos') || '',
            descricao_projeto: formData.get('descricao_projeto') || '',
            documentacao_existente: formData.get('documentacao_existente') || '',
            normas: formData.get('normas') || '',
            observacoes: formData.get('observacoes') || '',
            horario_contato: formData.get('horario_contato') || '',
            meio_contato: formData.get('meio_contato') || ''
        };

        // Validação básica
        if (!dados.nome || !dados.email || !dados.empresa) {
            mostrarMensagem('Por favor, preencha todos os campos obrigatórios.', 'error');
            toggleBotaoEnvio(botaoEnvio, false);
            return;
        }

        // Envia dados para o backend
        const response = await fetch(`${API_BASE_URL}/orcamento`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dados)
        });

        const resultado = await response.json();

        if (response.ok) {
            mostrarMensagem('Solicitação de orçamento enviada com sucesso! Entraremos em contato em até 24 horas.', 'success');
            form.reset();
        } else {
            mostrarMensagem(resultado.erro || 'Erro ao enviar solicitação. Tente novamente.', 'error');
        }

    } catch (error) {
        console.error('Erro ao enviar formulário:', error);
        mostrarMensagem('Erro de conexão. Verifique sua internet e tente novamente.', 'error');
    } finally {
        toggleBotaoEnvio(botaoEnvio, false);
    }
}

// Inicialização quando a página carrega
document.addEventListener('DOMContentLoaded', function() {
    // Identifica qual página estamos
    const isContatoPage = window.location.pathname.includes('contato') || document.querySelector('form[data-form="contato"]');
    const isOrcamentoPage = window.location.pathname.includes('orcamento') || document.querySelector('form[data-form="orcamento"]');

    // Configura o formulário de contato
    if (isContatoPage) {
        const formContato = document.querySelector('form');
        if (formContato) {
            formContato.addEventListener('submit', processarFormularioContato);
            console.log('Formulário de contato configurado');
        }
    }

    // Configura o formulário de orçamento
    if (isOrcamentoPage) {
        const formOrcamento = document.querySelector('form');
        if (formOrcamento) {
            formOrcamento.addEventListener('submit', processarFormularioOrcamento);
            console.log('Formulário de orçamento configurado');
        }
    }

    console.log('Sistema de formulários DOC IND carregado');
});

