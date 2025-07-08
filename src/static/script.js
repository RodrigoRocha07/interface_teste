// Função para mostrar/esconder tabs
function showTab(event, tabId) {
    // Remove "active" de todos conteúdos e abas
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));
    // Ativa aba e conteúdo clicado
    document.getElementById(tabId).classList.add('active');
    event.currentTarget.classList.add('active');
}

// Função para atualizar alerts
async function atualizarAlerts() {
    const btn = document.getElementById('refresh-alerts-btn');
    const alertsList = document.getElementById('alerts-list');
    
    // Mostra loading no botão
    btn.classList.add('loading');
    btn.textContent = 'Carregando...';
    btn.disabled = true;
    
    try {
        // Faz requisição para buscar novos alerts
        const response = await fetch('/alerts');
        const data = await response.json();
        
        if (data.success) {
            // Limpa a lista atual
            alertsList.innerHTML = '';
            
            // Adiciona os novos alerts
            if (data.alerts && data.alerts.length > 0) {
                data.alerts.forEach(alert => {
                    const alertItem = document.createElement('li');
                    alertItem.className = 'alert-item';
                    alertItem.innerHTML = `
                        <strong>${alert.alert}</strong>
                        <div class="alert-name">${alert.name || ''}</div>
                        <div class="alert-customer-id">${alert.customer_id}</div>
                        <div class="alert-customer-name">${alert.customer_name}</div>
                        <div class="alert-date">${alert.date}</div>
                    `;
                    alertsList.appendChild(alertItem);
                });
            } else {
                // Se não há alerts
                const emptyItem = document.createElement('li');
                emptyItem.className = 'alert-item empty';
                emptyItem.textContent = 'Nenhum alerta encontrado.';
                alertsList.appendChild(emptyItem);
            }
            
            console.log('✅ Alerts atualizados com sucesso!');
        } else {
            console.error('❌ Erro ao buscar alerts:', data.error);
            alert('Erro ao atualizar alerts: ' + data.error);
        }
    } catch (error) {
        console.error('❌ Erro na requisição:', error);
        alert('Erro ao conectar com o servidor');
    } finally {
        // Remove loading do botão
        btn.classList.remove('loading');
        btn.textContent = 'Atualizar';
        btn.disabled = false;
    }
}

// Função para toggle do input de depósito
function toggleDepositInput() {
    const checkbox = document.getElementById("valor-aleatorio-deposito");
    const input = document.getElementById("deposit-input");
    
    if (checkbox && input) {
        if (checkbox.checked) {
            input.value = "";
            input.disabled = true;
            input.placeholder = "Valor será gerado automaticamente";
        } else {
            input.disabled = false;
            input.placeholder = "";
        }
    }
}

// Função para toggle do input de saque
function toggleSaqueInput() {
    const checkbox = document.getElementById("valor-aleatorio-saque");
    const input = document.getElementById("saque-input");
    
    if (checkbox && input) {
        if (checkbox.checked) {
            input.value = "";
            input.disabled = true;
            input.placeholder = "Valor será gerado automaticamente";
        } else {
            input.disabled = false;
            input.placeholder = "";
        }
    }
}

// Função para toggle do input de game transaction (valor)
function toggleGameTransactionValueInput() {
    const checkbox = document.getElementById("valor-aleatorio-game-transaction");
    const input = document.getElementById("game-transaction-input");
    
    if (checkbox && input) {
        if (checkbox.checked) {
            input.value = "";
            input.disabled = true;
            input.placeholder = "Valor será gerado automaticamente";
        } else {
            input.disabled = false;
            input.placeholder = "";
        }
    }
}

// Função para toggle do input de game transaction (jogo)
function toggleGameTransactionGameInput() {
    const checkbox = document.getElementById("jogo-aleatorio-game-transaction");
    const input = document.getElementById("game-id-input");
    
    if (checkbox && input) {
        if (checkbox.checked) {
            input.value = "";
            input.disabled = true;
            input.placeholder = "ID será gerado automaticamente";
        } else {
            input.disabled = false;
            input.placeholder = "";
        }
    }
}

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 JavaScript carregado e inicializado!');
    
    // Configurar eventos para depósito
    const checkboxDeposito = document.getElementById("valor-aleatorio-deposito");
    if (checkboxDeposito) {
        toggleDepositInput(); // Estado inicial
        checkboxDeposito.addEventListener("change", toggleDepositInput);
    }
    
    // Configurar eventos para saque
    const checkboxSaque = document.getElementById("valor-aleatorio-saque");
    if (checkboxSaque) {
        toggleSaqueInput(); // Estado inicial
        checkboxSaque.addEventListener("change", toggleSaqueInput);
    }
    
    // Configurar eventos para game transaction (valor)
    const checkboxGameTransactionValue = document.getElementById("valor-aleatorio-game-transaction");
    if (checkboxGameTransactionValue) {
        toggleGameTransactionValueInput(); // Estado inicial
        checkboxGameTransactionValue.addEventListener("change", toggleGameTransactionValueInput);
    }
    
    // Configurar eventos para game transaction (jogo)
    const checkboxGameTransactionGame = document.getElementById("jogo-aleatorio-game-transaction");
    if (checkboxGameTransactionGame) {
        toggleGameTransactionGameInput(); // Estado inicial
        checkboxGameTransactionGame.addEventListener("change", toggleGameTransactionGameInput);
    }
});

// Opcional: Atualizar alerts automaticamente a cada 30 segundos
// setInterval(atualizarAlerts, 30000);

// Função utilitária para debug
function debugFormData(formId) {
    const form = document.getElementById(formId);
    if (form) {
        const formData = new FormData(form);
        console.log(`📋 Dados do formulário ${formId}:`);
        for (let [key, value] of formData.entries()) {
            console.log(`  ${key}: ${value}`);
        }
    }
}