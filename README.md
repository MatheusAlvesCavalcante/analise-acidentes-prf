# Análise de Acidentes da PRF no Ceará (2017–2025)

Este repositório contém a análise de dados abertos da Polícia Rodoviária Federal (PRF) referentes a acidentes em rodovias federais no estado do Ceará entre 2017 e 2025.  

## Ferramentas utilizadas
- Python (limpeza, integração das bases e análise preditiva)
- R (análises estatísticas)
- Scikit-Learn (Implementação de modelos de Machine Learning (Regressão Linear))
- Plotly (Visualizações dinâmicas e interativas)
- Power BI (dashboards e visualizações interativas)
- Streamlit (Desenvolvimento do dashboard interativo web)

##  Metodologia
1. **Coleta de dados**: download das bases abertas da PRF em formato CSV.  
2. **Pré-processamento**: padronização de colunas, correção de inconsistências (ex.: latitude/longitude).  
3. **Integração**: unificação de arquivos anuais em uma única base.  
4. **Análise exploratória**: estatísticas descritivas e estudo de padrões temporais e espaciais.  
5. **Visualização**: construção de dashboards interativos no Power BI.
6. **Análise Preditiva**: Implementação de modelos estatísticos para projeção de acidentes para os anos de 2025 e 2026, permitindo uma visão preventiva sobre a segurança nas rodovias.

## Funcionalidades do Web App
Filtros Inteligentes (Seleção por municípios, iniciais e rodovias específicas (BRs))
Predição On-the-fly (O usuário seleciona uma localidade e o app calcula automaticamente a tendência futura)
Interface Dark Premium (Design focado em experiência do usuário e alta densidade de informação)

##  Resultados
- Identificação de rodovias com maior índice de acidentes.  
- Relação entre horários, condições climáticas e tipos de ocorrência.  
- Picos de acidentes em períodos específicos do ano.  

##  Conclusões
A aplicação de técnicas de **Ciência de Dados** combinadas com ferramentas de visualização possibilitou a identificação de **pontos críticos de segurança viária**, fornecendo subsídios para políticas públicas e estratégias de prevenção.  

##  Estrutura do repositório
- `scripts/` → códigos em Python e R.  
- `dados/` → amostras de dados utilizados (ou links para download).  
- `dashboard/` → arquivo `.pbix` com o relatório do Power BI.  
- `relatorio/` → documento técnico com descrição completa da análise.  

---
