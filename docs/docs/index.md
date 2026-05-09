<div class="home-hero">
  <div class="container">
    <div class="text-center">
      <h1>Tech Challenge</h1>
      <h2>Grupo MLEKs</h2>
      <p class="lead">Documentação do projeto final da Fase 1 (MLET10).</p>
    </div>

    <hr class="home-divider" />

    <div class="row">
      <div class="col-md-10 col-md-offset-1">
        <p style="font-size: 18px; line-height: 1.55;">
          Esta documentacao centraliza o contexto do projeto (ML Canvas e dataset), a estrutura do repositorio,
          e como executar o ambiente localmente.
          Para entender o projeto, comece pelo <a href="ml-canvas/">ML Canvas</a> e pelo <a href="dataset/">Dataset</a>.
        </p>
      </div>
    </div>

    <div class="text-center home-actions">
      <a class="btn btn-primary btn-lg" href="getting-started/">Primeiros passos</a>
      <a class="btn btn-default btn-lg" href="comandos/">Comandos</a>
      <a class="btn btn-default btn-lg" href="ml-canvas/">ML Canvas</a>
      <a class="btn btn-default btn-lg" href="dataset/">Dataset</a>
    </div>
  </div>
</div>

<div class="home-section">
  <div class="container">
    <h2>Recursos</h2>

    <div class="row">
      <div class="col-md-6">
        <div class="home-card">
          <h3>Setup em um comando</h3>
          <p>
            O ambiente e as dependências são gerenciados com <code>uv</code>.
            Use <code>make setup</code> para criar a virtualenv e sincronizar o projeto.
          </p>
        </div>
      </div>

      <div class="col-md-6">
        <div class="home-card">
          <h3>Qualidade e testes</h3>
          <p>
            Padronize o codigo com <code>ruff</code> e rode testes com <code>pytest</code>.
            Targets: <code>make lint</code>, <code>make format</code>, <code>make test</code>.
          </p>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-md-6">
        <div class="home-card">
          <h3>Documentacao versionada</h3>
          <p>
            As paginas ficam em <code>docs/docs/</code> e o site gerado em <code>docs/site/</code>.
            Use <code>make docs</code> para visualizar localmente.
          </p>
        </div>
      </div>

      <div class="col-md-6">
        <div class="home-card">
          <h3>Estrutura do projeto</h3>
          <p>
            A pagina <a href="estrutura-do-projeto/">Estrutura do projeto</a> descreve as pastas do repositorio
            e onde colocar dados, notebooks e artefatos.
          </p>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-md-6">
        <div class="home-card">
          <h3>ML Canvas</h3>
          <p>
            A pagina <a href="ml-canvas/">ML Canvas</a> consolida a definicao do problema,
            metricas de sucesso, dados e riscos do projeto.
          </p>
        </div>
      </div>

      <div class="col-md-6">
        <div class="home-card">
          <h3>Dataset</h3>
          <p>
            A pagina <a href="dataset/">Dataset</a> descreve a fonte e o dicionario de dados
            do Telco Customer Churn (IBM).
          </p>
        </div>
      </div>
    </div>
  </div>
</div>
