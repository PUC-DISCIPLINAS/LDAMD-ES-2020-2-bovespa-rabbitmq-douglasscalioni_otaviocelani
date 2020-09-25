# **Bovespa - RabbitMQ**

Disciplina: Laboratório de Desenvolvimento de Aplicações Móveis e Distribuídas 

Alunos:

- Douglas Scalioni Domingues
- Otávio Celani

### comentários

Hugo, não conseguimos terminar o trabalho.

O que falta:
- acessar e modificar o tópicos da corretora
- interface

O que está funcionando:
- Toda a comunicação está feita certinha do rabbitmq.
- compra, venda, transação

Da maneira como está, dá pra rodar da seguinte maneira:

python bovespa.py - não precisa de args

python broker.py "compra.PTRB" "quant:20,val:25.25,corretora:ABCD"

em outro broker:
python broker.py "venda.PTRB" "quant:20,val:25.25,corretora:ABCD"

resultado esperado:

 [x] Sent 'compra.PTRB':'compra.PTRB quant:20,val:25.25,corretora:ABCD'
 [x] 'venda.PTRB':b'quant:20,val:25.25,broker:ABCD'
 [x] 'transacao.PTRB':b'data-hora:2020-09-25 19:07:05.369857,corr_vd:ABCD,corr_cp:ABCD,quant:20,val:25.25'



