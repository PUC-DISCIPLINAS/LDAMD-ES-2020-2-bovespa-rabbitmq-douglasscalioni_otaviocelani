# **Bovespa - RabbitMQ**

Disciplina: Laboratório de Desenvolvimento de Aplicações Móveis e Distribuídas 

Data de entrega: 02/10/2020

Alunos:

- Douglas Scalioni Domingues
- Otávio Celani

Professor: Hugo de Paula

### Antes de mais nada:

O que falta:
- acessar e modificar o tópicos da corretora
- executar comandos durante execução do programa

O que está funcionando:
- Toda a comunicação do rabbitmq.
- compra, venda, transação



### Funcionamento

O diagrama descreve o fluxo de uma ordem de compra/venda, que tem início no *broker* (corretora).

![](C:\Users\dscal\git\github-classroom\bovespa-rabbitmq\notes\diagrama.jpg)

### Execução

Bolsa de valores:

   python bovespa.py server
			
argumentos: 

- server: URL RabbitMQ (opcional)

Corretora:

python broker.py nome --ordem tipo ativo quant val
			
argumentos:

-  nome(string): nome da corretora. Será automaticamente limitado em 4 caracteres, ex: ABCD
-  --ordem/-o: tipo(compra/venda) ativo(string) quant(int) val(float), 
-  --server/-s: URL RabbitMQ (opcional)
-  --help/-h

ex: ABCD -o compra PTRB 20 15.25
                

### Resultado esperado

roda a bolsa de valores:

python bovespa.py

`Bolsa de Valores de São Paulo.
2020-10-02 18:58:12.709045`

roda um broker:

python broker.py ABCD -o venda PTRB 20 32.25 

` [x] Sent 'venda.PTRB':'quant:20,val:32.25,corretora:ABCD'`

em outro broker:

python broker.py EFGH -o compra PTRB 20 32.25

 `[x] Sent 'compra.PTRB':'quant:20,val:32.25,corretora:EFGH'`

 `[x] 'compra.PTRB':b'quant:20,val:32.25,broker:EFGH'`

 `[x] 'transacao.PTRB':b'data-hora:2020-10-02 18:58:11.550258,corr_vd:ABCD,corr_cp:EFGH,quant:20,val:32.25'`



