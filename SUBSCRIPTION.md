# 💳 Sistema de Planos e Assinatura

## 📊 Visão Geral

O Fight Analysis System possui um sistema de assinatura mensal com dois planos:

### 🎓 Plano Individual - R$ 40/mês
- 10 análises de vídeos por mês
- 50GB de armazenamento
- Detecção de movimentos e técnicas
- Identificação de erros técnicos
- Relatórios mensais
- Suporte via email

### 🏢 Plano Academia - R$ 80/mês
- 100 análises de vídeos por mês
- 500GB de armazenamento
- Detecção avançada de movimentos
- Identificação de erros técnicos
- Relatórios detalhados por atleta
- Análise comparativa entre alunos
- Acesso para múltiplos usuários
- Suporte prioritário via email e chat
- Exportação de relatórios em PDF

---

## 🔧 Como Usar

### Importar o gerenciador de assinaturas

```python
from src.subscription_manager import SubscriptionManager, PlanType

# Criar instância
manager = SubscriptionManager()
```

### Criar uma assinatura

```python
# Criar assinatura individual
subscription = manager.create_subscription(
    user_id="usuario_123",
    plan_type=PlanType.INDIVIDUAL,
    auto_renew=True
)

# Criar assinatura academia
subscription = manager.create_subscription(
    user_id="academia_456",
    plan_type=PlanType.ACADEMY,
    auto_renew=True
)
```

### Verificar assinatura ativa

```python
subscription = manager.get_subscription("usuario_123")

if subscription:
    print(f"Plano: {subscription.plan.name}")
    print(f"Preço: R$ {subscription.plan.price_monthly:.2f}/mês")
    print(f"Ativo: {subscription.is_active}")
else:
    print("Sem assinatura ativa")
```

### Usar análise de vídeo (decrementar limite)

```python
# Quando usuário analisa um vídeo
if manager.use_video_analysis("usuario_123"):
    print("✅ Vídeo analisado com sucesso")
else:
    print("❌ Limite de vídeos atingido este mês!")
```

### Ver estatísticas de uso

```python
stats = manager.get_usage_stats("usuario_123")

if stats:
    print(f"Plano: {stats['plan_name']}")
    print(f"Vídeos utilizados: {stats['videos_used']}/{stats['videos_limit']}")
    print(f"Vídeos restantes: {stats['videos_remaining']}")
    print(f"Armazenamento usado: {stats['storage_used_gb']}GB/{stats['storage_limit_gb']}GB")
    print(f"Dias até renovação: {stats['days_until_renewal']}")
```

### Upgrade de plano

```python
# Usuário individual quer virar academia
new_subscription = manager.upgrade_plan("usuario_123", PlanType.ACADEMY)

# Sistema calcula valor pro-rata e cobra a diferença
if new_subscription:
    print("✅ Plano atualizado com sucesso!")
```

### Cancelar assinatura

```python
if manager.cancel_subscription("usuario_123"):
    print("✅ Assinatura cancelada")
else:
    print("❌ Erro ao cancelar assinatura")
```

### Ver histórico de pagamentos

```python
payments = manager.get_payment_history("usuario_123")

for payment in payments:
    print(f"ID: {payment.payment_id}")
    print(f"Valor: R$ {payment.amount:.2f}")
    print(f"Data: {payment.payment_date}")
    print(f"Status: {payment.status.value}")
    print("---")
```

### Gerar fatura

```python
invoice = manager.generate_invoice("usuario_123", payment_id)

if invoice:
    print(f"Fatura: {invoice['invoice_id']}")
    print(f"Plano: {invoice['plan']}")
    print(f"Valor: R$ {invoice['amount']:.2f}")
    print(f"Data: {invoice['date']}")
```

### Ver todos os planos disponíveis

```python
all_plans = manager.get_all_plans()

for plan_key, plan_info in all_plans.items():
    print(f"\n{plan_info['name']}")
    print(f"Preço: R$ {plan_info['price_monthly']:.2f}/mês")
    print(f"Descrição: {plan_info['description']}")
    print(f"Vídeos/mês: {plan_info['max_videos_per_month']}")
    print(f"Armazenamento: {plan_info['max_storage_gb']}GB")
    print("Features:")
    for feature in plan_info['features']:
        print(f"  ✓ {feature}")
```

---

## 🔌 Integração com o analisador de vídeos

Para integrar com o `main.py` e verificar assinatura antes de analisar:

```python
from src.subscription_manager import SubscriptionManager, PlanType
from src.video_processor import FightAnalyzer

# Inicializar gerenciador
subscription_manager = SubscriptionManager()

# Verificar se usuário tem assinatura
user_id = "usuario_123"
subscription = subscription_manager.get_subscription(user_id)

if subscription is None:
    print("❌ Assinatura expirada! Renove agora para continuar.")
    exit()

# Tentar analisar vídeo
if not subscription_manager.use_video_analysis(user_id):
    print(f"❌ Limite de vídeos atingido!")
    stats = subscription_manager.get_usage_stats(user_id)
    print(f"Vídeos utilizados: {stats['videos_used']}/{stats['videos_limit']}")
    print(f"Próxima renovação: {stats['days_until_renewal']} dias")
    exit()

# Fazer análise do vídeo
analyzer = FightAnalyzer(
    video_path="data/videos/meu_video.mp4",
    fight_type="mma"
)
results = analyzer.analyze()

print(f"✅ Análise concluída!")
print(f"Score de performance: {results['performance_metrics']['overall_score']:.2f}/10.0")
```

---

## 💰 Estrutura de Dados

### Subscription

```python
{
    'user_id': str,           # ID único do usuário
    'plan': Plan,             # Objeto do plano
    'start_date': datetime,   # Data de início
    'end_date': datetime,     # Data de fim
    'is_active': bool,        # Se está ativa
    'auto_renew': bool,       # Renova automaticamente
    'videos_used_this_month': int,  # Vídeos usados
    'storage_used_gb': float        # Armazenamento usado
}
```

### Payment

```python
{
    'payment_id': str,        # ID único do pagamento
    'user_id': str,           # ID do usuário
    'amount': float,          # Valor do pagamento
    'payment_date': datetime, # Data do pagamento
    'status': PaymentStatus,  # Status (completed, pending, failed)
    'payment_method': str,    # Método (credit_card, paypal, etc)
    'description': str        # Descrição
}
```

---

## 🔔 Erros e Exceções

```python
# Usuário já tem assinatura
ValueError: "User usuario_123 already has an active subscription"

# Plano inválido
ValueError: "Invalid plan type: invalid_plan"

# Sem assinatura para o usuário
ValueError: "No subscription found for user usuario_123"

# Limite de preço negativo
ValueError: "Price cannot be negative"

# Limite de vídeos inválido
ValueError: "Max videos must be positive"
```

---

## 📋 Exemplo Completo

```python
from src.subscription_manager import SubscriptionManager, PlanType
from src.video_processor import FightAnalyzer

def main():
    # Inicializar
    subscription_manager = SubscriptionManager()
    
    # 1. Criar assinatura para academia
    print("1️⃣ Criando assinatura...")
    subscription = subscription_manager.create_subscription(
        user_id="academia_001",
        plan_type=PlanType.ACADEMY,
        auto_renew=True
    )
    print(f"✅ Assinatura criada: {subscription.plan.name}")
    
    # 2. Verificar planos disponíveis
    print("\n2️⃣ Planos disponíveis:")
    plans = subscription_manager.get_all_plans()
    for plan_key, plan_info in plans.items():
        print(f"  - {plan_info['name']}: R$ {plan_info['price_monthly']:.2f}/mês")
    
    # 3. Analisar vídeos
    print("\n3️⃣ Analisando vídeos...")
    for i in range(3):
        if subscription_manager.use_video_analysis("academia_001"):
            print(f"  ✅ Análise {i+1} realizada")
    
    # 4. Ver uso
    print("\n4️⃣ Estatísticas de uso:")
    stats = subscription_manager.get_usage_stats("academia_001")
    print(f"  Vídeos: {stats['videos_used']}/{stats['videos_limit']}")
    print(f"  Restantes: {stats['videos_remaining']}")
    
    # 5. Ver histórico de pagamentos
    print("\n5️⃣ Histórico de pagamentos:")
    payments = subscription_manager.get_payment_history("academia_001")
    for payment in payments:
        print(f"  R$ {payment.amount:.2f} - {payment.status.value}")

if __name__ == "__main__":
    main()
```

---

## 🚀 Próximas Features

- [ ] Integração com Stripe/PayPal
- [ ] Dashboard de administrador
- [ ] Relatórios de faturamento
- [ ] Cupons de desconto
- [ ] Trials gratuitos
- [ ] Plano empresarial customizado

