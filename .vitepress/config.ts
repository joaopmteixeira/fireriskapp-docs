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
      { text: "Projeto", link: "/PROJECT_OVERVIEW" },
      { text: "Arquitetura", link: "/ARCHITECTURE" },
      { text: "Método", link: "/METODO_CALCULO" },
    ],
    sidebar: [
      {
        text: "Projeto",
        items: [
          { text: "Visão Geral", link: "/PROJECT_OVERVIEW" },
          { text: "Arquitetura Técnica", link: "/ARCHITECTURE" },
          { text: "PRD - Requisitos", link: "/PRD" },
          { text: "Método de Cálculo", link: "/METODO_CALCULO" },
        ],
      },
      {
        text: "Utilização",
        items: [
          { text: "Guia de Utilização", link: "/USER_GUIDE" },
          {
            text: "Guidelines de Backend",
            link: "/guidelines/BACKEND_GUIDELINES",
          },
          {
            text: "Guidelines de Frontend",
            link: "/guidelines/FRONTEND_GUIDELINES",
          },
        ],
      },
      {
        text: "Deploy e Infraestrutura",
        items: [
          { text: "Opções de Hosting", link: "/HOSTING_OPTIONS" },
          { text: "Serviços", link: "/SERVICES" },
          { text: "Deploy", link: "/deploy/DEPLOY" },
        ],
      },
      {
        text: "Desenvolvimento",
        items: [
          { text: "Estado do Projeto", link: "/NEXT_STEPS" },
          { text: "Decisões Técnicas", link: "/DECISIONS_LOG" },
          { text: "Design", link: "/DESIGN" },
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
          { text: "Changelog", link: "/CHANGELOG" },
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
