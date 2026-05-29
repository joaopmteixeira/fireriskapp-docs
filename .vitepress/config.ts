import { defineConfig } from "vitepress";

export default defineConfig({
  lang: "pt-PT",
  title: "FireRiskApp Docs",
  description:
    "Documentação técnica do FireRiskApp e do método CHICHORRO de avaliação de risco de incêndio.",
  cleanUrls: true,
  lastUpdated: true,
  ignoreDeadLinks: [
    /^http:\/\/localhost:5173/,
    /SECURITY_PLAN$/,
    /AUTH_PLAN$/,
  ],
  themeConfig: {
    logo: undefined,
    siteTitle: "FireRiskApp Docs",
    search: {
      provider: "local",
    },
    socialLinks: [
      { icon: "github", link: "https://github.com/joaopmteixeira/fireriskapp-docs" },
    ],
    nav: [
      { text: "Início", link: "/" },
      { text: "Projeto", link: "/project/PROJECT_OVERVIEW" },
      { text: "Arquitetura", link: "/project/ARCHITECTURE" },
      { text: "Método", link: "/method/METODO_CALCULO" },
    ],
    sidebar: [
      {
        text: "Projeto",
        items: [
          { text: "Visão Geral", link: "/project/PROJECT_OVERVIEW" },
          { text: "Arquitetura Técnica", link: "/project/ARCHITECTURE" },
          { text: "PRD - Requisitos", link: "/project/PRD" },
          { text: "Método de Cálculo", link: "/method/METODO_CALCULO" },
        ],
      },
      {
        text: "Utilização",
        items: [
          { text: "Guia de Utilização", link: "/guides/USER_GUIDE" },
          {
            text: "Guidelines de Backend",
            link: "/guides/BACKEND_GUIDELINES",
          },
          {
            text: "Guidelines de Frontend",
            link: "/guides/FRONTEND_GUIDELINES",
          },
        ],
      },
      {
        text: "Infraestrutura",
        items: [
          { text: "Opções de Hosting", link: "/deploy/HOSTING_OPTIONS" },
          { text: "Serviços", link: "/project/SERVICES" },
        ],
      },
      {
        text: "Desenvolvimento",
        items: [
          { text: "Estado do Projeto", link: "/NEXT_STEPS" },
          { text: "Decisões Técnicas", link: "/changelog/DECISIONS_LOG" },
          { text: "Design", link: "/project/DESIGN" },
        ],
      },
      {
        text: "Planeamento",
        items: [
          {
            text: "Lista de Tarefas",
            link: "/TODO",
            items: [
              { text: "Por ID", link: "/TODO_LIST" },
              { text: "Por Prioridade", link: "/TODO_PRIORITIES" },
            ],
          },
        ],
      },
      {
        text: "Referência",
        items: [
          { text: "Changelog", link: "/changelog/CHANGELOG" },
        ],
      },
    ],
    outline: {
      label: "Nesta página",
      level: [2, 3],
    },
    docFooter: {
      prev: "Anterior",
      next: "Seguinte",
    },
    lastUpdated: {
      text: "Atualizado em",
      formatOptions: {
        dateStyle: "short",
        timeStyle: "short",
      },
    },
    darkModeSwitchLabel: "Tema",
    sidebarMenuLabel: "Menu",
    returnToTopLabel: "Voltar ao topo",
    langMenuLabel: "Alterar idioma",
  },
});
